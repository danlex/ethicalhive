#!/usr/bin/env bash
set -euo pipefail

# Build the LaTeX version of the paper via pandoc + tectonic.
#
# Reusable per `contracts/paper-writing-contract.md` PAP-WORK-06.
#
# Usage:
#   bash paper/build-latex.sh          # build paper/latex/main.pdf
#   bash paper/build-latex.sh --anon   # build the anonymous version
#
# Output: paper/latex/main.pdf
#
# The skeleton in paper/latex/main.tex uses a generic article class so it
# compiles anywhere tectonic / pdflatex is available. To retarget to a
# specific venue (NeurIPS 2026 workshop, ICLR 2026 workshop, ACL 2026
# workshop), drop the venue .sty into paper/latex/ and swap the
# \documentclass line in main.tex.

PAPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LATEX_DIR="$PAPER_DIR/latex"
SRC="$PAPER_DIR/draft.md"

ANON=0
if [ "${1:-}" = "--anon" ]; then
  ANON=1
fi

if [ ! -f "$SRC" ]; then
  echo "Error: $SRC not found." >&2
  exit 1
fi

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc not installed." >&2; exit 1
fi
if ! command -v tectonic >/dev/null 2>&1; then
  echo "Error: tectonic not installed." >&2; exit 1
fi

# 1. Pandoc-convert the body to LaTeX (no preamble).
pandoc "$SRC" --to latex --top-level-division=section \
  -o "$LATEX_DIR/body.tex"

# 2. Strip the abstract (it is already in main.tex) and the
#    front-matter title block from the body so we do not duplicate.
#    We keep everything from \section{1. Introduction} onward.
python3 - <<'PY'
from pathlib import Path
src = Path("paper/latex/body.tex").read_text()
marker = "\\section{1. Introduction}"
i = src.find(marker)
if i < 0:
    Path("paper/latex/body-stripped.tex").write_text(src)
else:
    Path("paper/latex/body-stripped.tex").write_text(src[i:])
PY

# 3. Optional: anonymous version (toggle the author block).
if [ "$ANON" = "1" ]; then
  cp "$LATEX_DIR/main.tex" "$LATEX_DIR/main.tex.bak"
  python3 - <<'PY'
from pathlib import Path
p = Path("paper/latex/main.tex")
s = p.read_text()
s = s.replace("\\author{\n  Alexandru Dan \\\\\n  Triumvirate Labs \\\\\n  \\texttt{alexandru.dan@triumviratelabs.ro}\n}",
              "% \\author{Alexandru Dan ...}")
s = s.replace("% \\author{Anonymous Authors}",
              "\\author{Anonymous Authors}")
p.write_text(s)
PY
fi

# 4. Build with tectonic.
cd "$LATEX_DIR"
tectonic main.tex 2>&1 | tail -10

# 5. Restore non-anon main.tex if we touched it.
if [ "$ANON" = "1" ] && [ -f "$LATEX_DIR/main.tex.bak" ]; then
  mv "$LATEX_DIR/main.tex.bak" "$LATEX_DIR/main.tex"
fi

if [ -f "$LATEX_DIR/main.pdf" ]; then
  ls -lh "$LATEX_DIR/main.pdf"
  echo "Wrote $LATEX_DIR/main.pdf"
else
  echo "ERROR: main.pdf not produced." >&2
  exit 1
fi
