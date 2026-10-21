#!/usr/bin/env python3
"""build-catalogue.py - render the EthicalAI catalogue from the ontology.

Reads ontology/ethical-ai.yaml (the single source of truth) and splices the
catalogue grid into docs/index.html: a red-bordered Highlighted group first, then
the family groups (the ten brain systems plus the agentic/engineering group).
Every box is an expandable .concept with definition, example, and research papers.

Usage:
  experiments/build-catalogue.py            # print the grid HTML to stdout
  experiments/build-catalogue.py --write     # splice it into docs/index.html

The ontology is produced once by build-ontology.py and then maintained by hand;
this script is the only thing that turns it into the page, and the splice is
idempotent.
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY = ROOT / "ontology" / "ethical-ai.yaml"
PAGE = ROOT / "docs" / "index.html"


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def title_amp(text):
    return esc(text).replace(" and ", " &amp; ")


def render_papers(arxiv):
    """count + top-3 papers, or an honest 'no paper' note."""
    if not arxiv or not arxiv.get("papers"):
        return '<p class="cite none">No direct AI paper found yet.</p>'
    count = arxiv.get("count")
    cnt = f"{count:,}" if isinstance(count, int) else "?"
    items = []
    for p in arxiv["papers"][:3]:
        pid = re.sub(r"v\d+$", "", p.get("id", ""))
        yr = f' ({p["year"]})' if p.get("year") else ""
        items.append(
            f'<li><a href="https://arxiv.org/abs/{pid}" target="_blank" '
            f'rel="noopener">arXiv:{pid}</a>{yr} {esc(p.get("title", ""))}</li>'
        )
    return (
        f'<p class="cite"><b>{cnt}</b> arXiv papers (cs.AI/CL/LG)</p>'
        f'<ul class="papers">{"".join(items)}</ul>'
    )


def box(mode):
    """Render one failure mode as an expandable .concept box."""
    hl = mode.get("highlighted")
    num = mode.get("highlight_order") if hl else mode.get("num")
    n = f"{num:02d}"
    cls = "concept shipped" if hl else f'concept {mode.get("tag", "")}'.strip()
    fam = "Highlighted check" if hl else title_amp(mode["group_label"])
    datafam = "page" if hl else mode.get("tag", "")
    key = esc(mode["name"].lower())
    ex = mode.get("example") or ""
    ex_html = (
        f'<h4>Example</h4><ul class="examples"><li>{esc(ex)}</li></ul>' if ex else ""
    )
    return (
        f'      <details class="{cls}" data-fam="{datafam}" data-key="{key}">'
        f'<summary><span class="num">{n}</span>'
        f'<div class="head"><h2>{esc(mode["name"])}</h2>'
        f'<p class="one">{esc(mode["definition"])}</p>'
        f'<span class="fam">{fam}</span></div>'
        f'<span class="chev">▸</span></summary>'
        f'<div class="body">{ex_html}'
        f'<h4>Research papers</h4>{render_papers(mode.get("arxiv"))}</div></details>'
    )


def render(modes):
    out = ['    <div class="cat-grid">']
    highlighted = sorted(
        (m for m in modes if m.get("highlighted")), key=lambda m: m["highlight_order"]
    )
    if highlighted:
        out.append('      <h3 class="cat-group">Highlighted checks</h3>')
        out += [box(m) for m in highlighted]
    # family groups, in first-appearance order
    groups = []
    index = {}
    for m in modes:
        if m.get("highlighted"):
            continue
        g = m["group_label"]
        if g not in index:
            index[g] = len(groups)
            groups.append((g, []))
        groups[index[g]][1].append(m)
    for i, (g, members) in enumerate(groups, 1):
        out.append(f'      <h3 class="cat-group">{i}. {title_amp(g)}</h3>')
        out += [box(m) for m in members]
    out.append("    </div>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="splice into docs/index.html")
    args = ap.parse_args()

    onto = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    modes = onto["modes"]
    grid = render(modes)

    if not args.write:
        print(grid)
        return

    html = PAGE.read_text(encoding="utf-8")
    pattern = re.compile(
        r'    <div class="cat-grid">.*?</div>\s*(?=<details class="mm">|</section>)',
        re.DOTALL,
    )
    if not pattern.search(html):
        print("ERROR: could not locate cat-grid to replace", file=sys.stderr)
        sys.exit(1)
    html = pattern.sub(grid + "\n    ", html, count=1)
    PAGE.write_text(html, encoding="utf-8")

    hl = sum(1 for m in modes if m.get("highlighted"))
    print(f"rendered {len(modes)} boxes ({hl} highlighted) from {ONTOLOGY.name}")


if __name__ == "__main__":
    main()
