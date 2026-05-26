#!/usr/bin/env bash
set -euo pipefail

# Run all benchmark reviewer conditions on one or more suites, then score.
#
# This is the reusable wrapper that replaces hand-bundled bash loops in
# Bash tool calls (per the Paper Writing Contract PAP-WORK-06: no vanilla
# multi-step bash; named, committed scripts only).
#
# Usage:
#   bash run-conditions.sh <suite.json> [<suite.json> ...] \
#       [--model sonnet|haiku|opus] [--reviewers none,freeform,contract,judge]
#
# Examples:
#   bash run-conditions.sh cases/suite-scope-creep.json
#   bash run-conditions.sh cases/suite-scope-creep.json cases/suite-scope-creep-hard.json
#   bash run-conditions.sh cases/suite-foo.json --model haiku --reviewers freeform,judge

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="$SCRIPT_DIR/run-suite.sh"
METRICS="$SCRIPT_DIR/metrics.py"

MODEL="sonnet"
REVIEWERS="none,freeform,contract,judge"
SUITES=()

# Parse positional suite paths until we hit a flag, then flags.
while [ $# -gt 0 ]; do
  case "$1" in
    --model)     MODEL="$2"; shift 2 ;;
    --reviewers) REVIEWERS="$2"; shift 2 ;;
    --*)         echo "Unknown flag: $1" >&2; exit 1 ;;
    *)           SUITES+=("$1"); shift ;;
  esac
done

if [ ${#SUITES[@]} -eq 0 ]; then
  echo "Usage: $0 <suite.json> [<suite.json> ...] [--model M] [--reviewers R1,R2,...]" >&2
  exit 1
fi

if [ ! -x "$RUNNER" ] && [ ! -f "$RUNNER" ]; then
  echo "Error: $RUNNER not found." >&2; exit 1
fi

# Split the comma-separated reviewers into an array.
IFS=',' read -r -a REV_ARR <<< "$REVIEWERS"

for SUITE in "${SUITES[@]}"; do
  if [ ! -f "$SUITE" ]; then
    echo "Error: suite file '$SUITE' not found." >&2; exit 1
  fi
  echo "================================================================"
  echo "Suite: $SUITE"
  echo "================================================================"
  for REV in "${REV_ARR[@]}"; do
    bash "$RUNNER" "$SUITE" --reviewer "$REV" --model "$MODEL"
  done

  # Score this suite's results: the latest jsonl per reviewer run above
  # (do not pull in historical runs).
  BASENAME="$(basename "$SUITE" .json)"
  LATEST_FILES=()
  for REV in "${REV_ARR[@]}"; do
    LATEST=$(ls -t "$SCRIPT_DIR/results/run-${BASENAME}-${REV}-"*.jsonl 2>/dev/null | head -1 || true)
    [ -n "$LATEST" ] && LATEST_FILES+=("$LATEST")
  done
  echo ""
  echo "---- metrics for $BASENAME (latest run per reviewer) ----"
  if [ ${#LATEST_FILES[@]} -gt 0 ]; then
    python3 "$METRICS" "${LATEST_FILES[@]}"
  else
    echo "  no result files found for $BASENAME"
  fi
done

