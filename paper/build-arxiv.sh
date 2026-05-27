#!/usr/bin/env bash
set -euo pipefail

# Build the arXiv submission package.
#
# Reusable per `contracts/paper-writing-contract.md` PAP-WORK-06.
#
# Steps:
#   1. Regenerate paper/arxiv/body.tex from paper/draft.md via pandoc.
#   2. Strip the duplicated title block so body starts at §1 Introduction.
#   3. Local test compile with tectonic (catches issues before arXiv does).
#   4. Tar up paper/arxiv/{main.tex,body.tex} as the upload package.
#
# Usage:
#   bash paper/build-arxiv.sh
#
# Output:
#   paper/arxiv/main.pdf           - local-compiled PDF for sanity check
#   paper/arxiv/submission.tar.gz  - the tarball to upload to arXiv
#
# arXiv accepts: PDF-only OR LaTeX source. We submit source so arXiv
# re-compiles and the .tex stays the version of record. The PDF in this
# script is for the user's local sanity check, not the submission.

PAPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$PAPER_DIR/draft.md"
ARXIV_DIR="$PAPER_DIR/arxiv"

if [ ! -f "$SRC" ]; then
  echo "Error: $SRC not found." >&2; exit 1
fi
if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc not installed." >&2; exit 1
fi
if ! command -v tectonic >/dev/null 2>&1; then
  echo "Error: tectonic not installed." >&2; exit 1
fi
if [ ! -f "$ARXIV_DIR/main.tex" ]; then
  echo "Error: $ARXIV_DIR/main.tex not found. Did you set up the arXiv directory?" >&2
  exit 1
fi

echo "Step 1: pandoc paper/draft.md -> body.tex"
pandoc "$SRC" --to latex --top-level-division=section -o "$ARXIV_DIR/body.tex"

echo "Step 2: strip duplicated front matter"
python3 - <<'PY'
from pathlib import Path
body = Path("paper/arxiv/body.tex").read_text()
marker = "\\section{1. Introduction}"
i = body.find(marker)
if i >= 0:
    Path("paper/arxiv/body.tex").write_text(body[i:])
    print("    stripped before " + marker)
else:
    print("    no front-matter marker found, leaving body intact")
PY

echo "Step 3: local tectonic test compile"
cd "$ARXIV_DIR"
tectonic main.tex 2>&1 | tail -5
if [ ! -f "$ARXIV_DIR/main.pdf" ]; then
  echo "ERROR: tectonic build failed; do not upload to arXiv until this passes." >&2
  exit 1
fi
echo "    PDF built: $(ls -lh main.pdf | awk '{print $5}')"

echo "Step 4: tar the submission package"
cd "$ARXIV_DIR"
TAR="$ARXIV_DIR/submission.tar.gz"
rm -f "$TAR"
tar -czf "$TAR" main.tex body.tex
echo "    Wrote $TAR ($(ls -lh "$TAR" | awk '{print $5}'))"

echo
echo "Ready. Upload $TAR to arXiv at https://arxiv.org/submit"
echo "Local sanity-check PDF: $ARXIV_DIR/main.pdf"
