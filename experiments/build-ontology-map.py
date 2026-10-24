#!/usr/bin/env python3
"""build-ontology-map.py - an interactive HTML tree for the ontology.

Reads ontology/ethical-ai.yaml (and the RISE discovery results if present) and
writes docs/ontology-map.html: a collapsible indented mindmap built from real
HTML/CSS nodes (pill divs, CSS connectors), not SVG. Three top branches:
Human-paralleled (ten brain systems), AI-native behaviours, and Proposed (the
discovery run). Click a branch to expand, a mode to read it, or search. Scrolls
instead of pan/zoom. Self-contained, no external libraries.

Usage: experiments/build-ontology-map.py
"""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY = ROOT / "ontology" / "ethical-ai.yaml"
RISE = ROOT / "experiments" / "discover-rise-results.json"
DISCOVER = ROOT / "experiments" / "discover-results.json"
OUT = ROOT / "docs" / "ontology-map.html"

# principle dot colours (a touch stronger than the pastel fills, for the dots)
PRINC = {"honesty": "#6f9bf0", "calibration": "#4fb985", "non-maleficence": "#e07a6c",
         "scope-fidelity": "#d99a3f", "independence": "#9b78d6", "transparency": "#48b4ca",
         "corrigibility": "#d873b0"}


def build_tree():
    import yaml
    o = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    pn = {p["id"]: p["name"] for p in o["principles"]}
    hn = {h["id"]: h["name"] for h in o["harm_types"]}
    modes = o["modes"]

    id2name = {m["id"]: m["name"] for m in modes}

    def leaf(m):
        return {"n": m["name"], "k": "mode", "m": {
            "def": m.get("definition", ""),
            "ex": m.get("example", ""),
            "grp": m.get("group_label", ""),
            "syn": m.get("synonyms") or [],
            "rel": [id2name.get(r, r) for r in (m.get("relates_to") or [])],
            "pr": pn.get((m.get("violates") or ["?"])[0], "?"),
            "hm": hn.get((m.get("causes") or ["?"])[0], "?"),
            "hp": "" if m.get("ai_native") else m.get("human_parallel", ""),
            "pc": (m.get("arxiv") or {}).get("count") or 0,
            "hi": bool(m.get("highlighted")), "ai": bool(m.get("ai_native"))}}

    human = [m for m in modes if not m.get("ai_native")]
    order, idx = [], {}
    for m in human:
        g = m["group_label"]
        if g not in idx:
            idx[g] = len(order); order.append([g, []])
        order[idx[g]][1].append(m)
    human_children = [{"n": g, "k": "group", "c": [leaf(m) for m in ms]} for g, ms in order]

    ai = [leaf(m) for m in modes if m.get("ai_native")]

    root = {"n": "Ethical AI ontology", "k": "root", "c": [
        {"n": f"Human-paralleled ({len(human)})", "k": "tier", "c": human_children},
        {"n": f"AI-native behaviours ({len(ai)})", "k": "ai", "c": ai},
    ]}

    import re as _re
    onto_slugs = {_re.sub(r"[^a-z0-9]+", " ", m["name"].lower()).strip() for m in modes}
    src, label = (RISE, "RISE search") if RISE.exists() else (DISCOVER, "MCTS search")
    if src.exists():
        d = json.loads(src.read_text())
        by_area = {}
        for c in d["candidates"]:
            cslug = _re.sub(r"[^a-z0-9]+", " ", c["term"].lower()).strip()
            if c["novel"] and c["reward"] > 0 and cslug not in onto_slugs:
                by_area.setdefault(c["area"], []).append(c)
        prop = []
        for area, cs in by_area.items():
            cs.sort(key=lambda x: -x["reward"])
            prop.append({"n": area, "k": "parea", "c": [
                {"n": c["term"], "k": "cand", "m": {
                    "def": f"{c['count']} arXiv papers. Top: {c.get('top','')}",
                    "pc": c["count"], "reward": c["reward"]}} for c in cs]})
        total = sum(len(v) for v in by_area.values())
        root["c"].append({"n": f"Proposed, {label} ({total})", "k": "proposed", "c": prop})
    return root


def leaf_count(node):
    kids = node.get("c")
    return sum(leaf_count(c) for c in kids) if kids else 1


def render_li(node, meta, ctr):
    ctr[0] += 1
    nid = ctr[0]
    kids = node.get("c") or []
    k = node["k"]
    m = node.get("m")
    classes = ["li", k]
    search = node["n"].lower()
    dot = ""
    if k == "mode":
        classes.append("ain" if m["ai"] else "hum")
        if m.get("hi"):
            classes.append("flag")
        col = PRINC.get((m.get("pr") or "").lower(), "#cfcfcf")
        dot = f'<span class="dot" style="background:{col}"></span>'
        search += " " + (m.get("def") or "").lower() + " " + " ".join(m.get("syn") or []).lower()
    if m is not None:
        meta[nid] = {**m, "n": node["n"]}
    if kids:
        classes.append("branch")
        if k != "root":
            classes.append("collapsed")
    caret = '<span class="caret"></span>' if kids else '<span class="caret empty"></span>'
    badge = f'<span class="badge">{leaf_count(node)}</span>' if kids else ""
    pill = f'<span class="pill">{dot}{html.escape(node["n"])}{badge}</span>'
    row = f'<div class="row">{caret}{pill}</div>'
    child = f'<ul>{"".join(render_li(c, meta, ctr) for c in kids)}</ul>' if kids else ""
    return (f'<li class="{" ".join(classes)}" data-id="{nid}" '
            f'data-s="{html.escape(search, quote=True)}">{row}{child}</li>')


def main():
    tree = build_tree()
    meta, ctr = {}, [0]
    tree_html = f'<ul class="tree" id="tree">{render_li(tree, meta, ctr)}</ul>'
    page = (TEMPLATE
            .replace("/*META*/", json.dumps(meta))
            .replace("<!--TREE-->", tree_html))
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT} ({len(meta)} nodes with detail)")


TEMPLATE = r"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ontology tree · EthicalAI</title>
<link rel="icon" type="image/png" href="favicon.png">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Manrope:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{--accent:#FF4931;--accent-d:#c2341a;--ink:#141414;--muted:#6d6c71;--line:#e7e5e2;--panel:#f6f5f4;--human:#2f6df6;--humansoft:#eef3fb}
*{box-sizing:border-box}
html,body{margin:0;height:100%;font-family:Manrope,system-ui,sans-serif;color:var(--ink);background:#fff}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:10px 16px;border-bottom:1px solid var(--line);position:sticky;top:0;background:#fff;z-index:3}
.bar h1{font-family:'Space Grotesk',sans-serif;font-size:17px;margin:0 10px 0 0}
.bar .btn{font-size:12.5px;padding:6px 11px;border:1px solid var(--line);border-radius:999px;background:#fff;cursor:pointer;font-family:inherit}
.bar .btn:hover{background:var(--panel)}
.bar #q{font-family:inherit;font-size:13px;padding:6px 12px;border:1px solid var(--line);border-radius:999px;width:230px;outline:none}
.bar #q:focus{border-color:var(--accent)}
.bar .hint{font-size:12px;color:var(--muted);margin-left:auto}
.bar a{font-size:12.5px;color:var(--accent-d);font-weight:600;text-decoration:none}
#stage{position:absolute;inset:52px 0 0 0;overflow:auto;padding:18px 22px 60px}
.embed .bar{display:none}
.embed #stage{inset:0}
.embed .legend{display:none}
/* indented tree */
.tree,.tree ul{list-style:none;margin:0;padding:0}
.tree{font-size:13.5px;width:max-content;min-width:100%}
.tree ul{margin-left:15px;position:relative}
.tree li{position:relative;padding-left:18px}
.tree li::before{content:"";position:absolute;left:0;top:0;height:100%;border-left:1px solid var(--line)}
.tree li:last-child::before{height:17px}
.tree li::after{content:"";position:absolute;left:0;top:17px;width:12px;border-top:1px solid var(--line)}
.tree>li{padding-left:0}
.tree>li::before,.tree>li::after{display:none}
.tree>li>ul{margin-left:7px}
.li.collapsed>ul{display:none}
.li.hide{display:none}
.row{display:flex;align-items:center;gap:3px;padding:2px 0}
.caret{width:15px;height:20px;flex:none;cursor:pointer;display:inline-flex;align-items:center;justify-content:center}
.caret::before{content:"\25be";font-size:10px;color:var(--muted);transition:transform .12s}
.li.collapsed>.row .caret::before{transform:rotate(-90deg)}
.caret.empty{visibility:hidden}
.pill{display:inline-flex;align-items:center;gap:6px;padding:3px 11px;border:1px solid var(--line);border-radius:8px;background:#fff;cursor:pointer;white-space:nowrap}
.pill:hover{filter:brightness(.975)}
.dot{width:8px;height:8px;border-radius:50%;flex:none}
.badge{font-size:10.5px;color:#a7a5a2;margin-left:3px}
.root>.row>.pill{background:var(--ink);color:#fff;border-color:var(--ink);font-weight:700;font-family:'Space Grotesk'}
.tier>.row>.pill{background:#f3f6fb;border-color:#c4d0e4;color:#3b4a63;font-weight:600}
.ai>.row>.pill{background:#faf2f0;border-color:#e3c3bb;color:#8a5243;font-weight:600}
.proposed>.row>.pill{background:#fdf7ea;border-color:#e3c98f;color:#8a6a1f;font-weight:600}
.group>.row>.pill,.parea>.row>.pill{background:var(--panel);font-weight:600}
.mode.hum>.row>.pill{border-color:#bcc8dc}
.mode.ain>.row>.pill{border-color:#ddc3ba}
.mode.flag>.row>.pill{border-color:#d98b7a;border-width:1.6px}
.cand>.row>.pill{border-style:dashed;border-color:#dcc08a}
.hit>.row>.pill{outline:2px solid var(--accent);outline-offset:1px}
.legend{position:fixed;right:14px;bottom:14px;background:rgba(255,255,255,.95);border:1px solid var(--line);border-radius:12px;padding:11px 13px;font-size:11.5px;z-index:4;max-width:230px;box-shadow:0 8px 24px rgba(0,0,0,.08)}
.legend b{font-family:'Space Grotesk';font-size:11px;letter-spacing:.3px;text-transform:uppercase;color:var(--muted);display:block;margin:0 0 6px}
.legend .row{display:flex;align-items:center;gap:7px;margin:3px 0;padding:0;color:#3a3a3a}
.legend .dt{width:10px;height:10px;border-radius:50%;flex:none}
.legend hr{border:none;border-top:1px solid var(--line);margin:8px 0}
#panel{position:fixed;right:14px;top:66px;width:min(366px,86vw);max-height:calc(100% - 84px);overflow:auto;background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:0 14px 48px rgba(0,0,0,.16);padding:16px 18px 18px;display:none;z-index:5}
#panel .ptag{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;padding:3px 9px;border-radius:999px;margin-bottom:9px}
#panel h3{font-family:'Space Grotesk';margin:0 0 9px;font-size:18px;line-height:1.2;padding-right:18px}
#panel .chips{margin:0 0 2px}
#panel .tag{display:inline-block;font-size:11px;padding:2px 9px;border-radius:999px;background:var(--panel);color:#444;margin:0 4px 6px 0}
#panel .tag .sw{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:middle}
#panel p{font-size:13.5px;margin:9px 0 0;line-height:1.55}
#panel .sec{margin:12px 0 0;padding-top:11px;border-top:1px solid var(--line)}
#panel .sec .k{display:block;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;margin-bottom:2px;color:var(--muted);font-weight:600}
#panel .sec p{margin:0}
#panel .note{font-size:12px;color:var(--muted);font-style:italic;margin-top:11px}
#panel .x{position:absolute;right:10px;top:8px;cursor:pointer;color:var(--muted);border:none;background:none;font-size:20px;line-height:1}
</style></head>
<body>
<div class="bar">
  <h1>Ontology tree</h1>
  <input id="q" type="search" placeholder="Search modes…" autocomplete="off">
  <button class="btn" id="expand">Expand all</button>
  <button class="btn" id="collapse">Collapse</button>
  <span class="hint">click a branch to open, a mode to read it</span>
  <a href="index.html">← catalogue</a>
</div>
<div id="stage"><!--TREE--></div>
<div class="legend" id="legend"></div>
<div id="panel"><button class="x" id="px">×</button><div id="pbody"></div></div>
<script>
const META=/*META*/;
const PRIN={honesty:'#6f9bf0',calibration:'#4fb985','non-maleficence':'#e07a6c','scope-fidelity':'#d99a3f',independence:'#9b78d6',transparency:'#48b4ca',corrigibility:'#d873b0'};
function pcol(n){return PRIN[(n||'').toLowerCase()]||'#cfcfcf';}
function esc(s){return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
const EMBED=location.search.includes('embed');
if(EMBED)document.body.classList.add('embed');
const tree=document.getElementById('tree'), stage=document.getElementById('stage');
const panel=document.getElementById('panel'), pbody=document.getElementById('pbody');

function defaultView(){
  tree.querySelectorAll('li.branch').forEach(li=>li.classList.add('collapsed'));
  tree.querySelectorAll(':scope>li').forEach(li=>li.classList.remove('collapsed'));
  if(EMBED) document.querySelectorAll('#tree>li>ul>li.branch').forEach(li=>li.classList.remove('collapsed'));
}
defaultView();

tree.addEventListener('click',e=>{
  const li=e.target.closest('li'); if(!li) return;
  if(e.target.closest('.caret')){ li.classList.toggle('collapsed'); return; }
  if(e.target.closest('.pill')){
    if(li.classList.contains('branch')) li.classList.toggle('collapsed');
    else showPanel(li.dataset.id);
  }
});
function showPanel(id){
  const m=META[id]; if(!m) return;
  let t='';
  if(!('pr' in m)){
    t=`<div class="ptag" style="color:#8a5a00;background:#fff6e6">Proposed · RISE discovery</div>`
     +`<h3>${esc(m.n)}</h3>`
     +`<div class="chips"><span class="tag">${(m.pc||0).toLocaleString()} arXiv papers</span>${m.reward!=null?`<span class="tag">reward ${m.reward}</span>`:''}</div>`
     +`<p>${esc(m.def)}</p><p class="note">Surfaced by the discovery loop; not yet in the ontology.</p>`;
  } else {
    const tier=m.ai?'AI-native':'Human-paralleled';
    t=`<div class="ptag" style="color:${m.ai?'var(--accent-d)':'#1b3e8c'};background:${m.ai?'rgba(255,73,49,.1)':'var(--humansoft)'}">${tier}${m.grp?' · '+esc(m.grp):''}</div>`
     +`<h3>${esc(m.n)}</h3>`
     +`<div class="chips"><span class="tag"><span class="sw" style="background:${pcol(m.pr)}"></span>violates ${esc(m.pr)}</span><span class="tag">causes ${esc(m.hm)}</span>${m.pc?`<span class="tag">${m.pc.toLocaleString()} papers</span>`:''}</div>`
     +`<p>${esc(m.def)}</p>`
     +(m.syn&&m.syn.length?`<div class="sec"><span class="k">Also known as</span><p>${m.syn.map(esc).join(', ')}</p></div>`:'')
     +(m.ex?`<div class="sec"><span class="k">Example</span><p>${esc(m.ex)}</p></div>`:'')
     +(m.hp?`<div class="sec"><span class="k">Human parallel</span><p>${esc(m.hp)}</p></div>`:`<p class="note">AI-native: no human analogue.</p>`)
     +(m.rel&&m.rel.length?`<div class="sec"><span class="k">Related</span><p>${m.rel.map(esc).join(' · ')}</p></div>`:'');
  }
  pbody.innerHTML=t; panel.style.display='block';
}
document.getElementById('px').onclick=()=>panel.style.display='none';
window.addEventListener('keydown',e=>{if(e.key==='Escape')panel.style.display='none';});
document.getElementById('expand').onclick=()=>tree.querySelectorAll('li.branch').forEach(li=>li.classList.remove('collapsed'));
document.getElementById('collapse').onclick=defaultView;
// search: reveal matches and their ancestors, highlight, scroll to first
const q=document.getElementById('q');
q.addEventListener('input',()=>{
  const s=q.value.trim().toLowerCase();
  const lis=[...tree.querySelectorAll('li')];
  lis.forEach(li=>li.classList.remove('hit','hide'));
  if(!s){ defaultView(); return; }
  lis.forEach(li=>li.classList.add('hide'));
  let first=null;
  for(const li of lis){
    if((li.dataset.s||'').includes(s)){
      li.classList.remove('hide'); li.classList.add('hit'); if(!first) first=li;
      let p=li.parentElement;
      while(p && p.id!=='tree'){ if(p.tagName==='LI'){ p.classList.remove('hide','collapsed'); } p=p.parentElement; }
    }
  }
  if(first) first.scrollIntoView({block:'center'});
});
// legend
document.getElementById('legend').innerHTML=
  '<b>Violated principle</b>'+Object.entries(PRIN).map(([k,v])=>
    `<div class="row"><span class="dt" style="background:${v}"></span>${k.replace('-',' ')}</div>`).join('')
  +'<hr><b>Tier (pill border)</b>'
  +'<div class="row"><span class="dt" style="background:#bcc8dc"></span>human-paralleled</div>'
  +'<div class="row"><span class="dt" style="background:#ddc3ba"></span>AI-native</div>'
  +'<div class="row"><span class="dt" style="background:#dcc08a"></span>proposed (RISE)</div>';
</script>
</body></html>
"""


if __name__ == "__main__":
    main()
