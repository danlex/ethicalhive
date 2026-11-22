#!/usr/bin/env bash
# build-paper-pdf.sh - produce the resource paper PDF, preserving its bar chart.
# The web figure is a raw <figure><svg>; LaTeX cannot use that, so we strip the raw HTML block
# and let pandoc insert a LaTeX figure from a committed standalone (paper/figure1.tex) instead.
set -euo pipefail
cd "$(dirname "$0")/.."

SRC="paper/ontology-paper.md"
OUT="docs/paper.pdf"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

compile_tex() {
  if ! command -v pdflatex >/dev/null 2>&1; then
    (cd "$TMP" && tectonic "$1")
  else
    (cd "$TMP" && pdflatex -interaction=nonstopmode -halt-on-error "$1" >compile.log 2>&1 &&
      pdflatex -interaction=nonstopmode -halt-on-error "$1" >>compile.log 2>&1) || {
      tail -n 40 "$TMP/compile.log"
      return 1
    }
  fi
}

# 1. Replace the raw-HTML <figure> block with a pandoc image include of the rendered figure.
python3 - "$SRC" "$TMP/paper.md" <<'PY'
import hashlib, re, sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding="utf-8").read()
# drop the single raw <figure>...</figure> HTML line and replace with a LaTeX figure include
fig = (r"\begin{figure}[h]\centering\includegraphics[width=.8\linewidth]{figure1.pdf}"
       r"\caption{The seven operational principles the 434 behaviours violate, by number of "
       r"records (one primary label per record, summing to 434). Dark is the historical 207 "
       r"records, light the 227 proposed analogies. These are catalogue assignments, not validated mechanisms.}"
       r"\label{fig:principles}\end{figure}")
repl = "```{=latex}\n" + fig + "\n```"
t = re.sub(r"<figure.*?</figure>", lambda _m: repl, t, flags=re.S, count=1)
t = t.replace('---\n', '---\nsubject: "Source SHA256: ' + hashlib.sha256(open(src, 'rb').read()).hexdigest() + '"\n', 1)
open(dst, "w", encoding="utf-8").write(t)
print("prepared latex-safe markdown")
PY

# 2. Render the figure standalone to figure1.pdf (a simple LaTeX bar chart, counts match the table).
cat > "$TMP/figure1.tex" <<'TEX'
\documentclass[border=4pt]{standalone}
\usepackage{xcolor}
\usepackage{tikz}
\definecolor{dom}{HTML}{C0392B}\definecolor{prop}{HTML}{E3A7A0}
\begin{document}
\begin{tikzpicture}[yscale=.6,xscale=.07]
  \foreach \y/\name/\g/\t in {7/Honesty/67/112, 6/Calibration/45/100,
      5/Nonmaleficence/31/52, 4/Transparency/25/51, 3/Scope Fidelity/15/50,
      2/Independence/14/43, 1/Corrigibility/10/26}{
    \node[anchor=east] at (0,\y) {\footnotesize \name};
    \fill[dom] (0.3,\y-.32) rectangle (0.3+\g,\y+.32);
    \fill[prop] (0.3+\g,\y-.32) rectangle (0.3+\t,\y+.32);
    \node[anchor=west] at (0.3+\t+2,\y) {\footnotesize \t};
  }
\end{tikzpicture}
\end{document}
TEX
compile_tex figure1.tex

# 3. pandoc -> PDF via tectonic.
# Two-step (proven to compile): pandoc -> standalone .tex, then tectonic on that .tex.
# The direct pandoc->PDF path dropped part of pandoc's own preamble; the standalone .tex keeps it.
# graphicx is added explicitly because the raw-latex \includegraphics is not detected by pandoc.
printf '\\usepackage{graphicx}\n\\usepackage{xurl}\n' > "$TMP/header.tex"
pandoc "$TMP/paper.md" -s -t latex \
  -V geometry:margin=1in -V fontsize=11pt -V colorlinks=true -V linkcolor=blue \
  -H "$TMP/header.tex" \
  -o "$TMP/paper.tex"
compile_tex paper.tex
cp "$TMP/paper.pdf" "$OUT"
cp "$TMP/paper.pdf" paper/ontology-paper.pdf
echo "wrote $OUT ($(du -h "$OUT" | cut -f1))"
