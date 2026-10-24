#!/usr/bin/env python3
"""build-ontology-map.py - an interactive explorer for the ontology.

Reads ontology/ethical-ai.yaml and writes docs/ontology-map.html: a collapsible
tree you can re-group by group / principle / harm, search live, and expand. Also
computes coverage (modes per principle and per harm) and renders an expansion
panel pointing at the thin cells. Self-contained, no external libraries.

Usage: experiments/build-ontology-map.py
"""

import html
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY = ROOT / "ontology" / "ethical-ai.yaml"
OUT = ROOT / "docs" / "ontology-map.html"


def esc(s):
    return html.escape(str(s))


def main():
    import yaml
    o = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    modes = o["modes"]
    prin_name = {p["id"]: p["name"] for p in o["principles"]}
    harm_name = {h["id"]: h["name"] for h in o["harm_types"]}

    data = []
    for m in modes:
        data.append({
            "name": m["name"],
            "def": m.get("definition", ""),
            "group": m["group_label"],
            "principle": prin_name.get((m.get("violates") or ["?"])[0], "?"),
            "harm": harm_name.get((m.get("causes") or ["?"])[0], "?"),
            "tier": "AI-native" if m.get("ai_native") else "Human-paralleled",
            "hp": m.get("human_parallel", "") if not m.get("ai_native") else "",
            "papers": (m.get("arxiv") or {}).get("count") or 0,
            "hi": bool(m.get("highlighted")),
        })

    prin_counts = Counter(d["principle"] for d in data)
    harm_counts = Counter(d["harm"] for d in data)
    tier_counts = Counter(d["tier"] for d in data)

    def bar(counts, title):
        total = sum(counts.values())
        rows = "".join(
            f'<div class="cov-row"><span class="cov-k">{esc(k)}</span>'
            f'<span class="cov-bar"><span style="width:{(n/total*100):.0f}%"></span></span>'
            f'<span class="cov-n">{n}</span></div>'
            for k, n in counts.most_common())
        return f'<div class="cov"><h3>{esc(title)}</h3>{rows}</div>'

    # expansion proposals from the thinnest cells
    thin_p = ", ".join(f"{k} ({n})" for k, n in prin_counts.most_common()[-3:])
    thin_h = ", ".join(f"{k} ({n})" for k, n in harm_counts.most_common()[-3:])

    page = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ontology map &amp; expansion · EthicalAI</title>
<link rel="icon" type="image/png" href="favicon.png">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Manrope:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{{--accent:#FF4931;--accent-d:#c2341a;--ink:#141414;--muted:#64646a;--line:#eae8e6;--panel:#f6f5f4}}
*{{box-sizing:border-box}}
body{{font-family:Manrope,system-ui,sans-serif;color:var(--ink);margin:0;background:#fff;line-height:1.5}}
.wrap{{max-width:min(1100px,94vw);margin:0 auto;padding:0 20px 80px}}
h1,h2,h3{{font-family:'Space Grotesk',sans-serif;letter-spacing:-.4px}}
h1{{font-size:clamp(26px,4vw,38px);margin:32px 0 4px}}
.lede{{color:var(--muted);font-size:17px;max-width:70ch}}
a{{color:var(--accent-d)}}
.controls{{position:sticky;top:0;background:#fff;z-index:5;display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:12px 0;border-bottom:1px solid var(--line);margin-top:18px}}
.controls input{{flex:1 1 220px;min-width:180px;padding:8px 11px;border:1px solid var(--line);border-radius:9px;font-size:14px;font-family:inherit}}
.seg button,.btn{{font-size:12.5px;padding:6px 11px;border:1px solid var(--line);border-radius:999px;background:#fff;cursor:pointer;font-family:inherit;color:var(--ink)}}
.seg button.on{{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}}
.count{{font-size:12.5px;color:var(--muted);margin-left:auto;font-variant-numeric:tabular-nums}}
#tree{{margin-top:12px}}
.grp{{border:1px solid var(--line);border-radius:10px;margin:8px 0;overflow:hidden}}
.grp>summary{{cursor:pointer;list-style:none;padding:10px 14px;font-family:'Space Grotesk',sans-serif;font-weight:600;background:var(--panel)}}
.grp>summary::-webkit-details-marker{{display:none}}
.grp .gc{{color:var(--muted);font-weight:400;font-size:12.5px}}
.mode{{border-top:1px solid var(--line)}}
.mode>summary{{cursor:pointer;list-style:none;padding:7px 14px;display:flex;gap:10px;align-items:baseline;font-size:13.5px}}
.mode>summary::-webkit-details-marker{{display:none}}
.mode.hi>summary{{background:#fdecf0}}
.mode .nm{{font-weight:600;min-width:160px}}
.badge{{font-size:10.5px;padding:1px 7px;border-radius:999px;background:var(--panel);color:var(--muted);white-space:nowrap}}
.badge.ai{{background:rgba(255,73,49,.1);color:var(--accent-d)}}
.mode .body{{padding:4px 14px 12px 14px;font-size:13px;color:var(--ink)}}
.mode .body .k{{color:var(--muted);font-weight:600}}
.cov-wrap{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:18px 0}}
.cov h3{{font-size:14px;margin:0 0 8px}}
.cov-row{{display:grid;grid-template-columns:130px 1fr 32px;gap:8px;align-items:center;font-size:12.5px;margin:3px 0}}
.cov-bar{{background:var(--panel);border-radius:5px;height:10px;overflow:hidden}}
.cov-bar span{{display:block;height:100%;background:var(--accent)}}
.cov-n{{text-align:right;color:var(--muted);font-variant-numeric:tabular-nums}}
.panel{{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:10px;padding:16px 18px;margin:18px 0;font-size:14px}}
.back{{display:inline-block;margin:28px 0 0;font-family:'Space Grotesk',sans-serif;font-weight:600}}
@media(max-width:680px){{.cov-wrap{{grid-template-columns:1fr}}.mode .nm{{min-width:0}}}}
</style></head>
<body><div class="wrap">
<h1>Ontology map</h1>
<p class="lede">{len(data)} AI integrity failure modes. Re-group them by brain/engineering group, by the principle they violate, or by the harm they cause. Click a group to open it, a mode to read it, or search.</p>

<div class="controls">
  <input id="q" type="search" placeholder="Search modes, e.g. authority, reward, memory…" autocomplete="off">
  <div class="seg" id="lens">
    <button data-lens="group" class="on">By group</button>
    <button data-lens="principle">By principle</button>
    <button data-lens="harm">By harm</button>
    <button data-lens="tier">By tier</button>
  </div>
  <button class="btn" id="toggle">Expand all</button>
  <span class="count" id="count"></span>
</div>
<div id="tree"></div>

<h2>Coverage</h2>
<p class="lede">How the {len(data)} modes spread across principles and harms. Short bars are thin cells, where the map is under-developed.</p>
<div class="cov-wrap">{bar(prin_counts, "Principle violated")}{bar(harm_counts, "Harm caused")}</div>

<div class="panel">
<h3 style="margin-top:0">Proposed expansion</h3>
<p>The thinnest principle cells are <b>{esc(thin_p)}</b> and the thinnest harm cells are <b>{esc(thin_h)}</b>; those are where new modes add the most. Concrete candidates, each with a human parallel to keep the rule:</p>
<ul>
<li><b>Scope-fidelity</b> is sparse: add <i>mission creep</i> (human: organisational mission creep) and <i>feature gold-plating</i> (human: over-engineering beyond the brief).</li>
<li><b>Corrigibility</b> is sparse: add <i>defensiveness under correction</i> (human: ego defence / rationalising away feedback) and <i>shutdown avoidance</i> as a human-paralleled self-preservation drive.</li>
<li><b>Security-breach</b> harm is thin on the human side: add <i>social-engineering compliance</i> (human: susceptibility to pretexting) distinct from prompt injection.</li>
<li><b>Relations are sparse</b>: only a few modes carry relates_to and none carry opposite_of or root_of. Populating opposite_of (overconfidence vs performative hedging) and root_of (conformity is a root of sycophancy) would make the graph navigable.</li>
<li><b>The AI-native tier is small ({tier_counts.get('AI-native',0)})</b>: candidates with no human parallel include <i>tokenizer artefacts</i>, <i>context-window eviction</i>, and <i>retrieval poisoning</i>; each needs an arXiv check before adding.</li>
</ul>
<p><small>Discovery and inclusion are still single-annotator judgment; see the <a href="experiments/research-note.html">research note</a> on how terms are found and vetted.</small></p>
</div>

<a class="back" href="index.html">← Back to the catalogue</a>
</div>

<script>
const MODES = {json.dumps(data)};
const tree = document.getElementById('tree');
const q = document.getElementById('q');
const count = document.getElementById('count');
let lens = 'group';

function groupsBy(key){{
  const m = new Map();
  for(const d of MODES){{ const k = d[key]; if(!m.has(k)) m.set(k, []); m.get(k).push(d); }}
  return [...m.entries()].sort((a,b)=> b[1].length - a[1].length);
}}
function render(){{
  const term = q.value.trim().toLowerCase();
  const groups = groupsBy(lens);
  let shown = 0;
  tree.innerHTML = '';
  for(const [g, items] of groups){{
    const matched = items.filter(d => !term ||
      (d.name+' '+d.def+' '+d.hp+' '+d.group+' '+d.principle+' '+d.harm).toLowerCase().includes(term));
    if(!matched.length) continue;
    shown += matched.length;
    const det = document.createElement('details'); det.className='grp'; det.open = !!term;
    det.innerHTML = '<summary>'+esc(g)+' <span class="gc">('+matched.length+')</span></summary>';
    for(const d of matched){{
      const md = document.createElement('details'); md.className='mode'+(d.hi?' hi':'');
      const badges = '<span class="badge'+(d.tier==='AI-native'?' ai':'')+'">'+esc(d.tier==='AI-native'?'AI-native':d.principle)+'</span>'
                   + '<span class="badge">'+esc(d.harm)+'</span>'
                   + (d.papers?'<span class="badge">'+d.papers.toLocaleString()+' papers</span>':'');
      md.innerHTML = '<summary><span class="nm">'+esc(d.name)+'</span>'+badges+'</summary>'
        + '<div class="body"><p>'+esc(d.def)+'</p>'
        + (d.hp?'<p><span class="k">Human parallel:</span> '+esc(d.hp)+'</p>':'<p><span class="k">AI-native</span> (no human parallel)</p>')
        + '<p><span class="k">Violates</span> '+esc(d.principle)+' · <span class="k">Causes</span> '+esc(d.harm)+'</p></div>';
      det.appendChild(md);
    }}
    tree.appendChild(det);
  }}
  count.textContent = shown + ' of ' + MODES.length;
}}
function esc(s){{return String(s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));}}
document.getElementById('lens').addEventListener('click', e=>{{
  const b = e.target.closest('button'); if(!b) return;
  lens = b.dataset.lens;
  document.querySelectorAll('#lens button').forEach(x=>x.classList.toggle('on', x===b));
  render();
}});
q.addEventListener('input', render);
const toggle = document.getElementById('toggle');
toggle.addEventListener('click', ()=>{{
  const open = toggle.textContent.startsWith('Expand');
  document.querySelectorAll('#tree details.grp').forEach(d=>d.open=open);
  toggle.textContent = open ? 'Collapse all' : 'Expand all';
}});
render();
</script>
</body></html>
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT} ({len(data)} modes)")


if __name__ == "__main__":
    main()
