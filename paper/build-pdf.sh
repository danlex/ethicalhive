#!/usr/bin/env bash
set -euo pipefail
# Build a canonical manuscript with installed pandoc and pdflatex.
# Usage: bash paper/build-pdf.sh [draft.md|ethicalai-benchmark.md]
PAPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$PAPER_DIR/../experiments/build-research-papers.py" --source "${1:-draft.md}"
