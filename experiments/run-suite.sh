#!/usr/bin/env bash
set -euo pipefail

# tvl-tech-bias-validator suite runner
# Runs a test suite through one of three reviewer conditions and records per-case verdicts.
#
# Usage:
#   bash run-suite.sh cases/suite.json [--reviewer contract|freeform|none] \
#        [--model sonnet|haiku|opus] [--output results.jsonl]
#
# Conditions (--reviewer):
#   contract     the full tvl-tech-bias-validator agent (CoVe + clause checks). Default.
#   freeform     a plain "review this draft for problems" baseline, no contract, no clauses.
#   mono-rid     monolithic baseline given the 14-clause list and asked to cite rule IDs;
#                fair comparison for per-clause-judge rule-ID attribution.
#   judge        per-clause judge for the case's mode (loaded from judges/<mode>-judge.md).
#   none         no audit; every draft is treated as shipped (VERDICT: SHIP). No model call.
#
# Requirements:
#   - claude CLI in PATH and logged in (not needed for --reviewer none)
#   - jq installed

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SUITE_FILE="${1:?Usage: run-suite.sh <suite.json> [--reviewer contract|freeform|none] [--model ...] [--output ...]}"
MODEL="sonnet"
REVIEWER="contract"
OUTPUT_FILE=""

shift
while [ $# -gt 0 ]; do
  case "$1" in
    --model) MODEL="$2"; shift 2 ;;
    --reviewer) REVIEWER="$2"; shift 2 ;;
    --output) OUTPUT_FILE="$2"; shift 2 ;;
    *) echo "Unknown flag: $1"; exit 1 ;;
  esac
done

if ! command -v jq &>/dev/null; then
  echo "Error: jq is required. Install with: brew install jq"
  exit 1
fi

# Select the reviewer prompt prefix for this condition
case "$REVIEWER" in
  contract)
    REVIEWER_PROMPT="$(tail -n +7 "$SCRIPT_DIR/../agents/tvl-tech-bias-validator.md")"  # strip frontmatter
    ;;
  freeform)
    REVIEWER_PROMPT="$(cat "$SCRIPT_DIR/baseline-freeform-prompt.md")"
    ;;
  mono-rid)
    REVIEWER_PROMPT="$(cat "$SCRIPT_DIR/baseline-monolithic-ruleid-prompt.md")"
    ;;
  judge)
    REVIEWER_PROMPT=""  # loaded per case from judges/<mode>-judge.md inside the loop
    ;;
  none)
    REVIEWER_PROMPT=""
    ;;
  *)
    echo "Unknown reviewer: $REVIEWER (use contract|freeform|mono-rid|judge|none)"; exit 1 ;;
esac

if [ "$REVIEWER" != "none" ] && ! command -v claude &>/dev/null; then
  echo "Error: claude CLI not found in PATH."
  exit 1
fi

if [ -z "$OUTPUT_FILE" ]; then
  BASENAME="$(basename "$SUITE_FILE" .json)"
  OUTPUT_FILE="$SCRIPT_DIR/results/run-${BASENAME}-${REVIEWER}-$(date +%Y%m%d-%H%M%S).jsonl"
fi
mkdir -p "$(dirname "$OUTPUT_FILE")"

CASE_COUNT=$(jq '.cases | length' "$SUITE_FILE")
echo "Suite: $SUITE_FILE ($CASE_COUNT cases)"
echo "Reviewer: $REVIEWER | Model: $MODEL"
echo "Output: $OUTPUT_FILE"
echo "---"

for i in $(seq 0 $((CASE_COUNT - 1))); do
  CASE_ID=$(jq -r ".cases[$i].id" "$SUITE_FILE")
  USER_ASK=$(jq -r ".cases[$i].user_ask" "$SUITE_FILE")
  DRAFT=$(jq -r ".cases[$i].draft" "$SUITE_FILE")
  EVIDENCE=$(jq -r ".cases[$i].evidence | join(\"\n- \")" "$SUITE_FILE")
  EXPECTED_VERDICT=$(jq -r ".cases[$i].expected.verdict" "$SUITE_FILE")
  GOLD_CLAUSES=$(jq -c ".cases[$i].gold_clauses // []" "$SUITE_FILE")

  echo "[$((i+1))/$CASE_COUNT] $CASE_ID (expected: $EXPECTED_VERDICT)"

  RULE_IDS_JSON='[]'
  if [ "$REVIEWER" = "none" ]; then
    RESULT="(no audit: draft delivered as-is)"
    VERDICT="SHIP"
  else
    # For the judge condition, route each case to judges/<mode>-judge.md
    PROMPT_PREFIX="$REVIEWER_PROMPT"
    if [ "$REVIEWER" = "judge" ]; then
      MODE=$(jq -r ".cases[$i].mode // \"\"" "$SUITE_FILE")
      JUDGE_FILE="$SCRIPT_DIR/../judges/${MODE}-judge.md"
      if [ ! -f "$JUDGE_FILE" ]; then
        echo "  ! no judge for mode '$MODE' ($JUDGE_FILE missing), skipping"
        continue
      fi
      PROMPT_PREFIX="$(tail -n +7 "$JUDGE_FILE")"
    fi

    # Built with printf (not a heredoc) to stay safe on bash 3.2, which mis-parses
    # an apostrophe inside a heredoc nested in $().
    AUDIT_PROMPT=$(printf '%s\n\n---\n\n**CASE TO AUDIT:**\n\n**User ask:** %s\n\n**Draft:**\n%s\n\n**Evidence pointers:**\n- %s\n' \
      "$PROMPT_PREFIX" "$USER_ASK" "$DRAFT" "$EVIDENCE")
    RESULT=$(claude -p --model "$MODEL" --dangerously-skip-permissions "$AUDIT_PROMPT" 2>/dev/null || echo "ERROR: claude CLI failed")

    if [ "$REVIEWER" = "judge" ]; then
      # Judges emit PASS | FLAG | BLOCK; normalize to the gold vocab SHIP | REVISE | BLOCK
      RAW=$(echo "$RESULT" | grep -oiE 'Verdict\s*:\s*(PASS|FLAG|BLOCK)' | head -1 | grep -oiE '(PASS|FLAG|BLOCK)' | tr '[:lower:]' '[:upper:]' || echo "")
      case "$RAW" in
        PASS) VERDICT="SHIP" ;;
        FLAG) VERDICT="REVISE" ;;
        BLOCK) VERDICT="BLOCK" ;;
        *) VERDICT="PARSE_ERROR" ;;
      esac
    else
      VERDICT=$(echo "$RESULT" | grep -oE 'VERDICT\s*:\s*(SHIP|REVISE|BLOCK)' | head -1 | grep -oE '(SHIP|REVISE|BLOCK)' || echo "PARSE_ERROR")
    fi

    # Capture any contract rule IDs the reviewer cited (for rule-ID attribution scoring).
    # python3 guarantees valid JSON even when there are no matches (jq + pipefail did not).
    RULE_IDS_JSON=$(printf '%s' "$RESULT" | grep -oE 'INT-[A-Z]{3}(-[0-9]+)?' | python3 -c "import sys,json;print(json.dumps(sorted({l.strip() for l in sys.stdin if l.strip()})))" 2>/dev/null) || true
    [ -z "$RULE_IDS_JSON" ] && RULE_IDS_JSON='[]'
  fi

  if [ "$VERDICT" = "$EXPECTED_VERDICT" ]; then
    MATCH="true"; echo "  -> $VERDICT (match)"
  else
    MATCH="false"; echo "  -> $VERDICT (expected $EXPECTED_VERDICT)"
  fi

  jq -nc \
    --arg case_id "$CASE_ID" \
    --arg reviewer "$REVIEWER" \
    --arg expected "$EXPECTED_VERDICT" \
    --arg got "$VERDICT" \
    --argjson match "$MATCH" \
    --arg model "$MODEL" \
    --argjson gold_clauses "$GOLD_CLAUSES" \
    --argjson rule_ids "$RULE_IDS_JSON" \
    --arg full_output "$RESULT" \
    '{case_id: $case_id, reviewer: $reviewer, expected: $expected, got: $got, match: $match, model: $model, gold_clauses: $gold_clauses, rule_ids: $rule_ids, output: $full_output}' \
    >> "$OUTPUT_FILE"
done

echo "---"
TOTAL=$CASE_COUNT
CORRECT=$(jq -s '[.[] | select(.match == true)] | length' "$OUTPUT_FILE")
echo "Exact-verdict match: $CORRECT/$TOTAL"
echo "Written to: $OUTPUT_FILE"
echo "Now score with: python3 $SCRIPT_DIR/metrics.py $OUTPUT_FILE"
