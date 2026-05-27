#!/usr/bin/env bash
set -euo pipefail

# Render paper/draft.md to paper/draft.pdf via pandoc + tectonic.
#
# Reusable per `contracts/paper-writing-contract.md` PAP-WORK-06: PDF build
# is a multi-step shell operation, so it lives in a committed script.
#
# Usage:
#   bash paper/build-pdf.sh                # build draft.md -> draft.pdf
#   bash paper/build-pdf.sh other.md       # build other.md -> other.pdf (in paper/)
#
# Prerequisites: pandoc, tectonic. Figures must already exist in
# paper/figures/ (run experiments/make-figures.py first).

PAPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="${1:-draft.md}"
SRC_PATH="$PAPER_DIR/$SRC"
OUT_PATH="$PAPER_DIR/${SRC%.md}.pdf"

if [ ! -f "$SRC_PATH" ]; then
  echo "Error: $SRC_PATH not found." >&2
  exit 1
fi

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc not installed." >&2; exit 1
fi
if ! command -v tectonic >/dev/null 2>&1; then
  echo "Error: tectonic not installed." >&2; exit 1
fi

cd "$PAPER_DIR"
pandoc "$SRC" \
  --pdf-engine=tectonic \
  --variable geometry:margin=1in \
  --variable fontsize=11pt \
  --variable colorlinks=true \
  --variable linkcolor=blue \
  --variable urlcolor=blue \
  --variable mainfont="" \
  --resource-path=".:figures" \
  --toc --toc-depth=2 \
  -o "$OUT_PATH"

echo "wrote $OUT_PATH"
ls -lh "$OUT_PATH"
