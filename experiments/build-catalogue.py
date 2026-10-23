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


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


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


MEAS = {
    "draft": "a single draft",
    "multi-turn": "behaviour across turns",
    "undetectable": "not from a single draft",
}
ORIGIN = {
    "cognitive-neuroscience": "Cognitive neuroscience",
    "software-engineering": "Software engineering",
    "alignment": "AI alignment",
    "mixed": "Mixed",
}
TAGL = {
    "shipped": "Shipped check", "research": "Paper-backed",
    "page": "Brain-map parallel", "analogy": "Analogy only",
}
PRIN_NAME = {}  # populated from the ontology in main()
HARM_NAME = {}


def meta_block(mode):
    """Surface the ontology metadata in the expanded body."""
    rows = []
    viol = [PRIN_NAME.get(p, p) for p in mode.get("violates", [])]
    if viol:
        rows.append(("Violates", esc(", ".join(viol))))
    harm = [HARM_NAME.get(h, h) for h in mode.get("causes", [])]
    if harm:
        rows.append(("Causes", esc(", ".join(harm))))
    if mode.get("category"):
        rows.append(("Category", esc(mode["category"])))
    if mode.get("origin"):
        rows.append(("Origin", esc(ORIGIN.get(mode["origin"], mode["origin"]))))
    if mode.get("measurability"):
        rows.append(("Measurable from", esc(MEAS.get(mode["measurability"], mode["measurability"]))))
    if mode.get("tag"):
        rows.append(("Type", esc(TAGL.get(mode["tag"], mode["tag"]))))
    if mode.get("contract_clause"):
        rows.append(("Contract clause", esc(mode["contract_clause"])))
    if mode.get("same_as"):
        sa = mode["same_as"]
        label = re.sub(r"^b\d+-", "", sa).replace("-", " ")
        rows.append(("Also in the brain map", f'<a href="#{sa}">{esc(label)}</a>'))
    if not rows:
        return ""
    items = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)
    return f'<h4>Details</h4><dl class="meta">{items}</dl>'


def box(mode):
    """Render one failure mode as an expandable spreadsheet row."""
    hl = mode.get("highlighted")
    num = mode.get("num")
    n = f"{num:02d}" if isinstance(num, int) else "—"
    cls = "concept shipped" if hl else f'concept {mode.get("tag", "")}'.strip()
    datafam = "page" if hl else mode.get("tag", "")
    tag = mode.get("tag", "")
    key = esc(mode["name"].lower())
    arx = mode.get("arxiv") or {}
    has_papers = "1" if arx.get("papers") else "0"
    cnt = arx.get("count")
    pcount = f"{cnt:,}" if isinstance(cnt, int) else "—"
    cat = esc(mode.get("category", ""))
    ex = mode.get("example") or ""
    ex_html = (
        f'<h4>Example</h4><ul class="examples"><li>{esc(ex)}</li></ul>' if ex else ""
    )
    return (
        f'      <details id="{mode["id"]}" class="{cls}" data-fam="{datafam}" '
        f'data-tag="{tag}" data-papers="{has_papers}" data-key="{key}">'
        f'<summary><span class="num">{n}</span>'
        f'<div class="head"><h2>{esc(mode["name"])}</h2>'
        f'<p class="one">{esc(mode["definition"])}</p>'
        f'<span class="fam">{cat}</span>'
        f'<span class="pcount" title="arXiv papers on this concept">{pcount}</span></div>'
        f'<span class="chev">▸</span></summary>'
        f'<div class="body">{ex_html}'
        f'<h4>Research papers</h4>{render_papers(arx)}'
        f'{experiment_block(mode)}{meta_block(mode)}</div></details>'
    )


def experiment_block(mode):
    exp = mode.get("experiment")
    if not exp:
        return ""
    link = ""
    if exp.get("url"):
        link = (f' <a href="{esc(exp["url"])}">See the full experiment &rarr;</a>')
    return f'<h4>Experiment</h4><p class="exp">{esc(exp.get("summary", ""))}{link}</p>'


def render(modes):
    """Group by group_label in first-appearance order. The Highlighted group is
    rendered where it falls in that order (last), not pinned to the top."""
    out = ['    <div class="cat-grid">']
    groups = []
    index = {}
    for m in modes:
        g = m["group_label"]
        if g not in index:
            index[g] = len(groups)
            groups.append((g, []))
        groups[index[g]][1].append(m)
    for i, (g, members) in enumerate(groups, 1):
        out.append(f'      <h3 class="cat-group" id="grp-{slug(g)}">{i}. {title_amp(g)}</h3>')
        out += [box(m) for m in members]
    out.append("    </div>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="splice into docs/index.html")
    args = ap.parse_args()

    onto = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    PRIN_NAME.update({p["id"]: p["name"] for p in onto.get("principles", [])})
    HARM_NAME.update({h["id"]: h["name"] for h in onto.get("harm_types", [])})
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
