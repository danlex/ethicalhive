#!/usr/bin/env bash
set -euo pipefail
# Build and locally compile the source package. This does not submit to arXiv.
# Outputs paper/arxiv/main.tex, main.pdf and submission.tar.gz.
PAPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$PAPER_DIR/../experiments/build-research-papers.py" --source draft.md --arxiv-package
