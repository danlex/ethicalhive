#!/usr/bin/env bash
set -euo pipefail

# Run one LLM rater over a taxonomy-agreement prompt set and record its category
# assignments. Reusable named script (no inline heredocs), mirrors run-suite.sh.
#
# Usage:
#   bash run-taxonomy-raters.sh <prompts.jsonl> --model sonnet|haiku|opus [--output out.jsonl]
#
# Input:  one {"id","prompt"} per line (from `taxonomy-agreement.py prompts`).
# Output: one {"id","assigned"} per line, the category the rater chose (validated against
#         the eleven category names; unparseable replies recorded as "UNPARSED").

PROMPTS="${1:?Usage: run-taxonomy-raters.sh <prompts.jsonl> --model M [--output out.jsonl]}"
shift
MODEL="sonnet"
OUT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --model)  MODEL="$2"; shift 2 ;;
    --output) OUT="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[ -z "$OUT" ] && OUT="$SCRIPT_DIR/results/taxonomy-raters-${MODEL}-$(date +%Y%m%d-%H%M%S).jsonl"
mkdir -p "$(dirname "$OUT")"

CATS="Perception|Memory|Attention|Heuristics|Reasoning|Metacognition|Language|Social|Moral|Self & agency|AI-native"

: > "$OUT"
N=$(grep -c . "$PROMPTS")
i=0
while IFS= read -r line; do
  [ -z "$line" ] && continue
  i=$((i+1))
  ID=$(printf '%s' "$line" | jq -r '.id')
  PROMPT=$(printf '%s' "$line" | jq -r '.prompt')
  RAW=$(claude -p --model "$MODEL" --dangerously-skip-permissions "$PROMPT" 2>/dev/null || echo "ERROR")
  # match the reply against a known category name (longest match first for "Self & agency")
  ASSIGNED=$(printf '%s' "$RAW" | grep -oiE "Self & agency|AI-native|Perception|Memory|Attention|Heuristics|Reasoning|Metacognition|Language|Social|Moral" | head -1 || true)
  [ -z "$ASSIGNED" ] && ASSIGNED="UNPARSED"
  printf '%s\n' "$(jq -cn --arg id "$ID" --arg a "$ASSIGNED" '{id:$id, assigned:$a}')" >> "$OUT"
  echo "[$i/$N] $ID -> $ASSIGNED"
done < "$PROMPTS"
echo "Wrote $OUT"
