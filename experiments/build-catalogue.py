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
import copy
import csv
import html as html_lib
import io
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY = ROOT / "ontology" / "ethical-ai.yaml"
PAGE = ROOT / "docs" / "index.html"


def esc(text):
    return html_lib.escape(str(text), quote=True)


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
MODE_NUM = {}
MIT_NAME = {}   # mitigation id -> name, for detected_by
GROUPED = {}    # primary id -> retained overlapping records


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
    n = str(num) if isinstance(num, int) else ""
    cls = "concept shipped" if hl else f'concept {mode.get("tag", "")}'.strip()
    datafam = "page" if hl else mode.get("tag", "")
    tag = mode.get("tag", "")
    key = esc(mode["name"].lower())
    arx = mode.get("arxiv") or {}
    variants = GROUPED.get(mode['id'], [])
    has_papers = "1" if arx.get("papers") else "0"
    cnt = arx.get("count")
    pcount_html = (
        f'<span class="pcount" title="arXiv papers on this concept">{cnt:,}</span>'
        if isinstance(cnt, int) else ""
    )
    cat = esc(mode.get("category", ""))
    proposed = bool(mode.get('research_candidate'))
    review = mode.get('source_check', '')
    candidate = proposed
    has_analogy = mode.get('tag') == 'analogy'
    badge = ('<span class="research-status">Proposed analogy · '+
             ('definition source consulted' if review=='definition-source-consulted' else 'source check pending')+'</span>') if proposed else ''
    related=mode.get('grouped_under')
    if related:
        badge += f'<span class="research-status">Linked overlap with #{MODE_NUM[related]} · {esc(MODE_NAME[related])}</span>'
    # examples: prefer a list of several; fall back to the single legacy field
    exs = mode.get("examples") or ([mode["example"]] if mode.get("example") else [])
    ex_html = ""
    if exs:
        lis = "".join(f"<li>{esc(e)}</li>" for e in exs)
        ex_html = f'<h4>Example{"s" if len(exs) > 1 else ""}</h4><ul class="examples">{lis}</ul>'
    if proposed:
        ex_html = '<h4>Proposed AI manifestation / test · untested</h4><p>'+esc(mode['proposed_ai_manifestation'])+'</p>'
    return (
        f'      <details id="{mode["id"]}" class="{cls}" data-fam="{datafam}" '
        f'data-num="{num}" data-overlap="{esc(related or "")}" data-tag="{tag}" data-papers="{has_papers}" data-candidate="{1 if candidate else 0}" data-has-analogy="{1 if has_analogy else 0}" data-source-status="{review}" data-key="{key}">'
        f'<summary><span class="num">{n}</span>'
        f'<div class="head"><h2>{esc(mode["name"])}</h2>'
        f'<p class="one">{esc(mode["definition"])}</p>{badge}'
        f'<span class="fam">{cat}</span>'
        f'{pcount_html}</div>'
        f'<span class="chev">▸</span></summary>'
        f'<div class="body"><h4>Definition</h4><p class="def">{esc(mode["definition"])}</p>'
        f'{ex_html}'
        f'<h4>Research papers</h4>{render_papers(arx)}'
        f'{research_block(mode)}{experiment_block(mode)}{meta_block(mode)}'
        f'{overlap_block(mode)}</div></details>'
    )


def overlap_block(mode):
    out=[]
    target=mode.get('grouped_under')
    if target:
        out.append('<h4>Related operational description</h4><p><a href="#'+esc(target)+'">#'+str(MODE_NUM[target])+' · '+esc(MODE_NAME[target])+'</a></p><p>'+esc(mode['grouping_reason'])+'</p>')
    variants=GROUPED.get(mode['id'],[])
    if variants:
        out.append('<h4>Linked overlap descriptions</h4><ul>'+''.join('<li><a href="#'+esc(v['id'])+'">#'+str(v['num'])+' · '+esc(v['name'])+'</a></li>' for v in variants)+'</ul>')
    return ''.join(out)


def research_block(mode):
    notes = mode.get('research_notes', [])
    if not mode.get('research_candidate') and not notes:
        return ''
    out=[]
    records=[mode] if mode.get('research_candidate') else notes
    for record in records:
        out.append('<h4>Human-behaviour research</h4>')
        if not mode.get('research_candidate'):
            out.append('<p><b>'+esc(record['name'])+'.</b> '+esc(record['definition'])+'</p><p>'+esc(record['catalogue_boundary'])+'</p>')
        out.append('<p class="research-note">Human definitions and AI proposals are separate. The analogy has not been tested in this research; clinical terms do not diagnose AI or establish feelings, unconscious motives or intent. Some conditioning evidence also comes from nonhuman animals.</p>')
        boundary=record.get('research_boundary',record.get('distinction_and_limits',''))
        if boundary:out.append('<p><b>Boundary and limits.</b> '+esc(boundary)+'</p>')
        sources=record.get('definition_sources',[])
        if sources:
            out.append('<ul class="human-sources">'+''.join('<li><a href="'+esc(s['url'])+'">'+esc(s['title'])+'</a><br><small>Access: '+esc(s['consulted'])+'</small></li>' for s in sources)+'</ul>')
        else:
            out.append('<p><b>Source check pending.</b> The supplied attribution is a research lead, not a verified definition-source passage.</p>')
        provenance=record.get('research_provenance',record)
        contrib=provenance.get('contributions',[])
        if contrib:
            out.append('<h4>Supplied source attributions</h4><ul>'+''.join('<li>Upload row '+str(c['upload_row'])+': '+esc(c['supplied_name'])+' — '+esc(c['supplied_source'])+'. Historical attribution not independently confirmed by import.</li>' for c in contrib)+'</ul>')
    return ''.join(out)


def export_catalogue(onto):
    public=copy.deepcopy(onto)
    public['modes']=sorted(public['modes'],key=lambda m:m['num'])
    public['meta']['source_record_count']=len(onto['modes'])
    public['meta']['mode_count']=len(public['modes'])
    (ROOT/'docs/behaviours.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n')
    buffer=io.StringIO(newline='')
    fields=['id','num','name','definition','category','tag','research_candidate','source_check','ai_evidence_status','proposed_ai_manifestation','definition_sources','source_access','grouped_under','grouping_reason']
    writer=csv.DictWriter(buffer,fieldnames=fields,lineterminator='\n');writer.writeheader()
    for mode in sorted(onto['modes'],key=lambda m:m['num']):
        row={k:mode.get(k,'') for k in fields}
        row['definition_sources']=' ; '.join(s['url'] for s in mode.get('definition_sources',[]))
        row['source_access']=' ; '.join(s['consulted'] for s in mode.get('definition_sources',[]))
        writer.writerow(row)
    (ROOT/'docs/behaviours.csv').write_text(buffer.getvalue())
    # Existing download URLs remain aliases of the same catalogue, not parallel lists.
    for suffix in ('json','csv'):
        content=(ROOT/f'docs/behaviours.{suffix}').read_bytes()
        for stem in ('100-behaviours','behaviour-candidates'):
            (ROOT/f'docs/research/{stem}.{suffix}').write_bytes(content)


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
    modes=sorted(modes,key=lambda m:m['num'])
    n = len(modes)
    ai = sum(1 for m in modes if m.get("ai_native"))
    grounded = sum(1 for m in modes if (m.get("arxiv") or {}).get("count"))
    detected = sum(1 for m in modes if m.get("detected_by"))
    shipped = sum(1 for m in modes if m.get("highlighted"))
    proposed=sum(bool(m.get('research_candidate')) for m in modes)
    stats = (f'<div class="cat-stats"><b>{n}</b> numbered entries · {ai} AI-native · {grounded} with AI paper links'
             f' · {shipped} highlighted · {detected} with detection links</div>')
    out = [f'    {stats}', '    <div class="cat-grid">']
    seen_groups=set()
    for i,m in enumerate(modes):
        if i%50==0:
            end=min(i+50,n)
            out.append(f'<h3 class="cat-group" data-range="1" id="range-{i+1}">{i+1}–{end}</h3>')
        if m['group_label'] not in seen_groups:
            seen_groups.add(m['group_label'])
            out.append(f'<span class="legacy-group-anchor" id="grp-{slug(m["group_label"])}"></span>')
        out.append(box(m))
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
    MODE_NUM.update({m['id']:m['num'] for m in onto['modes']})
    GROUPED.clear()
    for m in onto['modes']:
        if m.get('grouped_under'):GROUPED.setdefault(m['grouped_under'],[]).append(m)
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
    export_catalogue(onto)

    hl = sum(1 for m in modes if m.get("highlighted"))
    print(f"rendered {len(modes)} numbered entries in ascending reference order ({hl} highlighted)")


if __name__ == "__main__":
    main()

