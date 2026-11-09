#!/usr/bin/env bash
set -euo pipefail
# The canonical Markdown supplies the title, date, abstract and body.
# Usage: bash paper/build-latex.sh [--anon]
# Default outputs paper/latex/main.tex and main.pdf plus the public methods PDF.
# --anon outputs only paper/latex/anonymous.pdf.
PAPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "${1:-}" = "--anon" ]; then
  exec python3 "$PAPER_DIR/../experiments/build-research-papers.py" --source draft.md --anonymous
fi
exec python3 "$PAPER_DIR/../experiments/build-research-papers.py" --source draft.md
