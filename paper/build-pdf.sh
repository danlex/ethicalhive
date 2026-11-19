#!/usr/bin/env bash
set -euo pipefail
# Build a canonical manuscript with installed pandoc and pdflatex.
# Usage: bash paper/build-pdf.sh [benchmark-paper.md|ontology-paper.md]
PAPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$PAPER_DIR/../experiments/build-research-papers.py" --source "${1:-benchmark-paper.md}"
