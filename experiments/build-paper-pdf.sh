#!/usr/bin/env bash
# build-paper-pdf.sh - produce the submission PDF for the resource paper via pandoc + tectonic.
# The web figure is a raw <figure><svg>; LaTeX cannot use that, so we strip the raw HTML block
# and let pandoc insert a LaTeX figure from a committed standalone (paper/figure1.tex) instead.
set -euo pipefail
cd "$(dirname "$0")/.."

SRC="paper/ontology-paper.md"
OUT="docs/paper.pdf"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# 1. Replace the raw-HTML <figure> block with a pandoc image include of the rendered figure.
python3 - "$SRC" "$TMP/paper.md" <<'PY'
import re, sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding="utf-8").read()
# drop the single raw <figure>...</figure> HTML line and replace with a LaTeX figure include
fig = (r"\begin{figure}[h]\centering\includegraphics[width=.8\linewidth]{figure1.pdf}"
       r"\caption{The seven operational principles the 434 behaviours violate, by number of "
       r"behaviours (a partition: each breaches exactly one, summing to 434). Dark is the 207 "
       r"grounded records, light the 227 proposed analogies.}\label{fig:principles}\end{figure}")
repl = "```{=latex}\n" + fig + "\n```"
t = re.sub(r"<figure.*?</figure>", lambda _m: repl, t, flags=re.S, count=1)
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
      5/Non-maleficence/31/52, 4/Transparency/25/51, 3/Scope-fidelity/15/50,
      2/Independence/14/43, 1/Corrigibility/10/26}{
    \node[anchor=east] at (0,\y) {\footnotesize \name};
    \fill[dom] (0.3,\y-.32) rectangle (0.3+\g,\y+.32);
    \fill[prop] (0.3+\g,\y-.32) rectangle (0.3+\t,\y+.32);
    \node[anchor=west] at (0.3+\t+2,\y) {\footnotesize \t};
  }
\end{tikzpicture}
\end{document}
TEX
( cd "$TMP" && tectonic figure1.tex >/dev/null 2>&1 ) && echo "rendered figure1.pdf" || { echo "figure render failed"; exit 1; }

# 3. pandoc -> PDF via tectonic.
# Two-step (proven to compile): pandoc -> standalone .tex, then tectonic on that .tex.
# The direct pandoc->PDF path dropped part of pandoc's own preamble; the standalone .tex keeps it.
# graphicx is added explicitly because the raw-latex \includegraphics is not detected by pandoc.
printf '\\usepackage{graphicx}\n' > "$TMP/header.tex"
pandoc "$TMP/paper.md" -s -t latex \
  -V geometry:margin=1in -V fontsize=11pt -V colorlinks=true -V linkcolor=blue \
  -H "$TMP/header.tex" \
  -o "$TMP/paper.tex"
( cd "$TMP" && tectonic paper.tex >/dev/null 2>&1 )
cp "$TMP/paper.pdf" "$OUT"
echo "wrote $OUT ($(du -h "$OUT" | cut -f1))"
