#!/usr/bin/env python3
"""build-catalogue.py - regenerate the 100-mode catalogue grid on the EthicalAI
page from the neuroscience-parallels corpus, so every entry shows its definition
and nothing is hand-transcribed or invented.

Reads references/research-2026-05-23-neuroscience-parallels.md (the source of
truth for the 100 failure modes, their brain-system grouping, honesty tag, and
one-line definition) and emits the `<div class="cat-grid">...</div>` block.

Usage:
  experiments/build-catalogue.py            # print the grid HTML to stdout
  experiments/build-catalogue.py --write     # splice it into docs/index.html

The splice replaces the existing cat-grid in place (reversible via git).
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "references" / "research-2026-05-23-neuroscience-parallels.md"
PAGE = ROOT / "docs" / "index.html"
CITES = ROOT / "experiments" / "catalogue-citations.tsv"

ENTRY_RE = re.compile(r"^(\d+)\.\s+\*\*(.+?)\*\*\s+`(page|research|analogy)`\s+(.+)$")
SECTION_RE = re.compile(r"^##\s+\d+\.\s+(.+?)\s*$")


def load_cites():
    """num -> (count:int, arxivid, year, anchor). Empty if the file is absent."""
    cites = {}
    if not CITES.exists():
        return cites
    for line in CITES.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or "\t" not in line:
            continue
        parts = line.split("\t")
        num = int(parts[0])
        count = int(parts[1])
        arxivid = parts[2].strip()
        year = parts[3].strip() if len(parts) > 3 else ""
        anchor = parts[4].strip() if len(parts) > 4 else ""
        cites[num] = (count, arxivid, year, anchor)
    return cites


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def title_amp(title):
    # match the page's existing header style: " and " -> " & "
    return esc(title).replace(" and ", " &amp; ")


def parse():
    sections = []  # list of (title, [ (num, name, tag, definition), ... ])
    current = None
    for line in CORPUS.read_text(encoding="utf-8").splitlines():
        sm = SECTION_RE.match(line)
        if sm:
            current = (sm.group(1), [])
            sections.append(current)
            continue
        em = ENTRY_RE.match(line)
        if em and current is not None:
            num, name, tag, definition = em.groups()
            current[1].append((int(num), name.strip(), tag, definition.strip()))
    return sections


def render_numbered(sections, cites):
    out = ['    <div class="cat-grid">']
    for i, (title, entries) in enumerate(sections, 1):
        out.append(
            f'      <div class="cat-fam"><h3>{i}. {title_amp(title)}</h3>'
            f'<div class="cat-chips">'
        )
        for num, name, tag, definition in entries:
            n = f"{num:02d}"
            name_html = esc(name)
            cite = cites.get(num)
            if cite and cite[3]:  # link name to its detail block (examples)
                name_html = f'<a href="#{cite[3]}">{name_html}</a>'
            cite_html = ""
            if cite:
                count, arxivid, year, _ = cite
                yr = f" ({year})" if year else ""
                cite_html = (
                    f'<p class="cite"><b>{count:,}</b> arXiv papers · '
                    f'<a href="https://arxiv.org/abs/{arxivid}" target="_blank" '
                    f'rel="noopener">arXiv:{arxivid}{yr}</a></p>'
                )
            out.append(
                f'        <div class="cat-chip {tag}">'
                f'<span class="n">{n}</span>'
                f'<span class="nm">{name_html}</span>'
                f'<p class="dfn">{esc(definition)}</p>{cite_html}</div>'
            )
        out.append("      </div></div>")
    out.append("    </div>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="splice into docs/index.html")
    args = ap.parse_args()

    sections = parse()
    cites = load_cites()
    total = sum(len(e) for _, e in sections)
    if total != 100:
        print(f"WARNING: parsed {total} entries, expected 100", file=sys.stderr)
    grid = render_numbered(sections, cites)

    if not args.write:
        print(grid)
        return

    html = PAGE.read_text(encoding="utf-8")
    pattern = re.compile(
        r'    <div class="cat-grid">.*?</div>\s*(?=<details class="mm">)',
        re.DOTALL,
    )
    if not pattern.search(html):
        print("ERROR: could not locate cat-grid to replace", file=sys.stderr)
        sys.exit(1)
    html = pattern.sub(grid + "\n    ", html, count=1)

    # Remove the "Prompt to prevent it" section from every concept block.
    before = html.count("Prompt to prevent it")
    html = re.sub(
        r"\s*<h4>Prompt to prevent it</h4>.*?(?=<h4>Judge agent)",
        "\n      ",
        html,
        flags=re.DOTALL,
    )
    after = html.count("Prompt to prevent it")

    PAGE.write_text(html, encoding="utf-8")
    print(f"spliced {total} entries; removed {before - after} prevention-prompt blocks")


if __name__ == "__main__":
    main()
