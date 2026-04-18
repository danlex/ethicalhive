#!/usr/bin/env bash
set -euo pipefail

# bias-validator suite runner
# Runs a test suite through the v5.1 subagent and records per-case verdicts.
#
# Usage:
#   bash run-suite.sh cases/suite-v1.json [--model sonnet|haiku] [--output results.jsonl]
#
# Requirements:
#   - claude CLI in PATH
#   - jq installed
#   - Working internet connection (API calls)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBAGENT_PROMPT="$(cat "$SCRIPT_DIR/../agents/bias-validator.md" | tail -n +7)"  # strip frontmatter

SUITE_FILE="${1:?Usage: run-suite.sh <suite.json> [--model sonnet|haiku] [--output results.jsonl]}"
MODEL="sonnet"
OUTPUT_FILE=""

# Parse optional flags
shift
while [ $# -gt 0 ]; do
  case "$1" in
    --model) MODEL="$2"; shift 2 ;;
    --output) OUTPUT_FILE="$2"; shift 2 ;;
    *) echo "Unknown flag: $1"; exit 1 ;;
  esac
done

if [ -z "$OUTPUT_FILE" ]; then
  BASENAME="$(basename "$SUITE_FILE" .json)"
  OUTPUT_FILE="$SCRIPT_DIR/results/run-${BASENAME}-$(date +%Y%m%d-%H%M%S).jsonl"
fi

if ! command -v jq &>/dev/null; then
  echo "Error: jq is required. Install with: brew install jq"
  exit 1
fi

if ! command -v claude &>/dev/null; then
  echo "Error: claude CLI not found in PATH."
  exit 1
fi

CASE_COUNT=$(jq '.cases | length' "$SUITE_FILE")
echo "Suite: $SUITE_FILE ($CASE_COUNT cases)"
echo "Model: $MODEL"
echo "Output: $OUTPUT_FILE"
echo "---"

for i in $(seq 0 $((CASE_COUNT - 1))); do
  CASE_ID=$(jq -r ".cases[$i].id" "$SUITE_FILE")
  USER_ASK=$(jq -r ".cases[$i].user_ask" "$SUITE_FILE")
  DRAFT=$(jq -r ".cases[$i].draft" "$SUITE_FILE")
  EVIDENCE=$(jq -r ".cases[$i].evidence | join(\"\n- \")" "$SUITE_FILE")
  EXPECTED_VERDICT=$(jq -r ".cases[$i].expected.verdict" "$SUITE_FILE")

  echo "[$((i+1))/$CASE_COUNT] $CASE_ID (expected: $EXPECTED_VERDICT)"

  # Build the audit prompt
  AUDIT_PROMPT="$(cat <<PROMPT_EOF
$SUBAGENT_PROMPT

---

**CASE TO AUDIT:**

**User's original ask:** $USER_ASK

**Draft:**
$DRAFT

**Evidence pointers:**
- $EVIDENCE
PROMPT_EOF
)"

  # Run through Claude CLI
  RESULT=$(claude -p --model "$MODEL" --bare --dangerously-skip-permissions "$AUDIT_PROMPT" 2>/dev/null || echo "ERROR: claude CLI failed")

  # Extract verdict from output
  VERDICT=$(echo "$RESULT" | grep -oE 'VERDICT\s*:\s*(SHIP|REVISE|BLOCK)' | head -1 | grep -oE '(SHIP|REVISE|BLOCK)' || echo "PARSE_ERROR")

  # Score
  if [ "$VERDICT" = "$EXPECTED_VERDICT" ]; then
    MATCH="true"
    echo "  -> $VERDICT ✓"
  else
    MATCH="false"
    echo "  -> $VERDICT ✗ (expected $EXPECTED_VERDICT)"
  fi

  # Write result
  jq -n \
    --arg case_id "$CASE_ID" \
    --arg expected "$EXPECTED_VERDICT" \
    --arg got "$VERDICT" \
    --argjson match "$MATCH" \
    --arg model "$MODEL" \
    --arg full_output "$RESULT" \
    '{case_id: $case_id, expected: $expected, got: $got, match: $match, model: $model, output: $full_output}' \
    >> "$OUTPUT_FILE"
done

echo "---"

# Summary
TOTAL=$CASE_COUNT
CORRECT=$(jq -s '[.[] | select(.match == true)] | length' "$OUTPUT_FILE")
echo "Results: $CORRECT/$TOTAL = $(echo "scale=0; $CORRECT * 100 / $TOTAL" | bc)%"
echo "Written to: $OUTPUT_FILE"
