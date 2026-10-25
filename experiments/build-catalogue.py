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
MODE_NAME = {}  # id -> name, for relates_to links
MIT_NAME = {}   # mitigation id -> name, for detected_by


def meta_block(mode):
    """Surface the ontology metadata in the expanded body."""
    rows = []
    if mode.get("is_a"):
        links = ", ".join(f'<a href="#{r}">{esc(MODE_NAME.get(r, r))}</a>' for r in mode["is_a"])
        rows.append(("Type of", links))
    if mode.get("human_parallel"):
        rows.append(("Human parallel", esc(mode["human_parallel"])))
    elif mode.get("ai_native"):
        rows.append(("Human parallel", "None (AI-native behaviour)"))
    if mode.get("synonyms"):
        rows.append(("Also known as", esc(", ".join(mode["synonyms"]))))
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
    if mode.get("relates_to"):
        links = ", ".join(f'<a href="#{r}">{esc(MODE_NAME.get(r, r))}</a>'
                          for r in mode["relates_to"])
        rows.append(("Related", links))
    if mode.get("opposite_of"):
        links = ", ".join(f'<a href="#{r}">{esc(MODE_NAME.get(r, r))}</a>'
                          for r in mode["opposite_of"])
        rows.append(("Opposite of", links))
    if mode.get("root_of"):
        links = ", ".join(f'<a href="#{r}">{esc(MODE_NAME.get(r, r))}</a>'
                          for r in mode["root_of"])
        rows.append(("Root of", links))
    if mode.get("detected_by"):
        rows.append(("Detected by", esc(", ".join(MIT_NAME.get(d, d) for d in mode["detected_by"]))))
    if mode.get("mitigated_by"):
        rows.append(("Mitigated by", esc(", ".join(MIT_NAME.get(d, d) for d in mode["mitigated_by"]))))
    if mode.get("maps_to"):
        rows.append(("Maps to", esc("; ".join(mode["maps_to"]))))
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
    # examples: prefer a list of several; fall back to the single legacy field
    exs = mode.get("examples") or ([mode["example"]] if mode.get("example") else [])
    ex_html = ""
    if exs:
        lis = "".join(f"<li>{esc(e)}</li>" for e in exs)
        ex_html = f'<h4>Example{"s" if len(exs) > 1 else ""}</h4><ul class="examples">{lis}</ul>'
    return (
        f'      <details id="{mode["id"]}" class="{cls}" data-fam="{datafam}" '
        f'data-tag="{tag}" data-papers="{has_papers}" data-key="{key}">'
        f'<summary><span class="num">{n}</span>'
        f'<div class="head"><h2>{esc(mode["name"])}</h2>'
        f'<p class="one">{esc(mode["definition"])}</p>'
        f'<span class="fam">{cat}</span>'
        f'<span class="pcount" title="arXiv papers on this concept">{pcount}</span></div>'
        f'<span class="chev">▸</span></summary>'
        f'<div class="body"><h4>Definition</h4><p class="def">{esc(mode["definition"])}</p>'
        f'{ex_html}'
        f'<h4>Research papers</h4>{render_papers(arx)}'
        f'{experiment_block(mode)}{meta_block(mode)}</div></details>'
    )


def experiment_block(mode):
    exp = mode.get("experiment")
    if not exp:
        return ""
    out = ["<h4>Experiment</h4>"]
    if exp.get("result"):
        out.append(f'<p class="exp"><b>Result.</b> {esc(exp["result"])}</p>')
    if exp.get("takeaway"):
        out.append(f'<p class="exp"><b>Takeaway.</b> {esc(exp["takeaway"])}</p>')
    if not exp.get("result") and not exp.get("takeaway"):
        out.append(f'<p class="exp">{esc(exp.get("summary", ""))}</p>')
    if exp.get("url"):
        out.append(f'<p class="exp"><a href="{esc(exp["url"])}">'
                   f'See the full experiment &rarr;</a></p>')
    return "".join(out)


CONCLUSION = (
    "Several probes so far. Three run on six cheap models over OpenRouter, the rest run "
    "in-session or blind on the Claude tiers (Opus, Sonnet, Haiku). The pattern that matters: no "
    "single model is safe across behaviours, and doing well on one failure mode does not "
    "predict another. deepseek-chat-v3.1 resisted authority and a noble excuse but still "
    "fabricated under re-sampling; mistral-small held firm on facts yet bent to a "
    "for-their-own-good justification; and all three Claude tiers refused to fabricate on "
    "clearly-fictional prompts, a floor that a harder probe will need to break.")


def experiments_section(modes):
    exps = [(m["name"], m["experiment"]) for m in modes if m.get("experiment")]
    if not exps:
        return ""
    cards = []
    for name, exp in exps:
        link = (f' <a href="{esc(exp["url"])}">Read the full experiment &rarr;</a>'
                if exp.get("url") else "")
        cards.append(f'<div class="exp-card"><h3>{esc(name)}</h3>'
                     f'<p>{esc(exp.get("summary", ""))}{link}</p></div>')
    return (f'<h2>Model probes</h2>\n    <p class="exp-intro">{esc(CONCLUSION)} '
            f'<a href="experiments/research-note.html">Read the position note &rarr;</a></p>\n'
            f'    <div class="exp-grid">{"".join(cards)}</div>')


def render(modes):
    """Group by group_label in first-appearance order. The Highlighted group is
    rendered where it falls in that order (last), not pinned to the top."""
    n = len(modes)
    ai = sum(1 for m in modes if m.get("ai_native"))
    grounded = sum(1 for m in modes if (m.get("arxiv") or {}).get("count"))
    detected = sum(1 for m in modes if m.get("detected_by"))
    shipped = sum(1 for m in modes if m.get("highlighted"))
    stats = (f'<div class="cat-stats"><b>{n}</b> failure modes · {n - ai} human-paralleled'
             f' · {ai} AI-native · {grounded} paper-grounded · {shipped} shipped checks'
             f' · {detected} auto-detected</div>')
    out = [f'    {stats}', '    <div class="cat-grid">']
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
    MODE_NAME.update({m["id"]: m["name"] for m in onto["modes"]})
    MIT_NAME.update({m["id"]: m["name"] for m in onto.get("mitigations", [])})
    modes = onto["modes"]
    grid = render(modes)

    if not args.write:
        print(grid)
        return

    html = PAGE.read_text(encoding="utf-8")
    pattern = re.compile(
        r'(?:    <div class="cat-stats">.*?</div>\s*)*'
        r'    <div class="cat-grid">.*?</div>\s*(?=<details class="mm">|</section>)',
        re.DOTALL,
    )
    if not pattern.search(html):
        print("ERROR: could not locate cat-grid to replace", file=sys.stderr)
        sys.exit(1)
    html = pattern.sub(grid + "\n    ", html, count=1)

    # fill the Model probes section from the modes that carry an experiment
    sec = experiments_section(modes)
    html = re.sub(
        r"(<!-- EXPERIMENTS:START -->).*?(<!-- EXPERIMENTS:END -->)",
        lambda m: f"{m.group(1)}\n    {sec}\n    {m.group(2)}",
        html, count=1, flags=re.DOTALL)

    PAGE.write_text(html, encoding="utf-8")

    hl = sum(1 for m in modes if m.get("highlighted"))
    print(f"rendered {len(modes)} boxes ({hl} highlighted) from {ONTOLOGY.name}")


if __name__ == "__main__":
    main()
