#!/usr/bin/env bash
set -euo pipefail

# Run a non-interactive Gemini review of a paper payload file.
#
# Reusable per `contracts/paper-writing-contract.md` PAP-WORK-06: env loading
# plus model invocation is multi-step shell, so it lives in a committed
# script. Inline `source .env && gemini -p ...` chains in Bash tool calls
# are Breaches.
#
# Usage:
#   bash experiments/run-gemini-review.sh                # uses /tmp/paper-review-payload.txt
#   bash experiments/run-gemini-review.sh <payload-file> # override input
#
# Output goes to paper/reviews/gemini.txt (and stdout). The payload file
# itself is not committed; .env is gitignored.
#
# Requires GEMINI_API_KEY in .env (or in the shell env already). Auth is
# checked before the full review runs; a missing key fails fast.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$REPO_ROOT/.env"
PAYLOAD="${1:-/tmp/paper-review-payload.txt}"
OUT_DIR="$REPO_ROOT/paper/reviews"
OUT_FILE="$OUT_DIR/gemini.txt"

if [ -f "$ENV_FILE" ]; then
  set -a
  # shellcheck disable=SC1090
  . "$ENV_FILE"
  set +a
fi

if [ -z "${GEMINI_API_KEY:-}" ]; then
  echo "Error: GEMINI_API_KEY is not set. Edit $ENV_FILE and add the value." >&2
  exit 1
fi

if [ ! -f "$PAYLOAD" ]; then
  echo "Error: payload file '$PAYLOAD' not found." >&2
  exit 1
fi

if ! command -v gemini >/dev/null 2>&1; then
  echo "Error: gemini CLI not installed. brew/npm install it first." >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

echo "Running Gemini review on $PAYLOAD"
echo "Output: $OUT_FILE"
echo "Payload size: $(wc -c < "$PAYLOAD") bytes"
echo

gemini -p "$(cat "$PAYLOAD")" --approval-mode plan 2>&1 | tee "$OUT_FILE"

echo
echo "Review saved to $OUT_FILE"
