#!/usr/bin/env python3
"""build-ontology-map.py - an interactive node-link tree for the ontology.

Reads ontology/ethical-ai.yaml (and experiments/discover-results.json if present)
and writes docs/ontology-map.html: a collapsible horizontal tree you can pan, zoom,
expand branch by branch, and click a leaf to read it. Three top branches:
Human-paralleled (ten brain systems), AI-native behaviours, and Proposed (the
MCTS discovery run). Self-contained, no external libraries.

Usage: experiments/build-ontology-map.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY = ROOT / "ontology" / "ethical-ai.yaml"
DISCOVER = ROOT / "experiments" / "discover-results.json"
OUT = ROOT / "docs" / "ontology-map.html"


def build_tree():
    import yaml
    o = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    pn = {p["id"]: p["name"] for p in o["principles"]}
    hn = {h["id"]: h["name"] for h in o["harm_types"]}
    modes = o["modes"]

    def leaf(m):
        return {"n": m["name"], "k": "mode", "m": {
            "def": m.get("definition", ""),
            "pr": pn.get((m.get("violates") or ["?"])[0], "?"),
            "hm": hn.get((m.get("causes") or ["?"])[0], "?"),
            "hp": "" if m.get("ai_native") else m.get("human_parallel", ""),
            "pc": (m.get("arxiv") or {}).get("count") or 0,
            "hi": bool(m.get("highlighted")), "ai": bool(m.get("ai_native"))}}

    # human-paralleled groups in first-appearance order
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

    if DISCOVER.exists():
        d = json.loads(DISCOVER.read_text())
        by_area = {}
        for c in d["candidates"]:
            if c["novel"] and c["reward"] > 0:
                by_area.setdefault(c["area"], []).append(c)
        prop = []
        for area, cs in by_area.items():
            cs.sort(key=lambda x: -x["reward"])
            prop.append({"n": area, "k": "parea", "c": [
                {"n": c["term"], "k": "cand", "m": {
                    "def": f"{c['count']} arXiv papers. Top: {c.get('top','')}",
                    "pc": c["count"], "reward": c["reward"]}} for c in cs]})
        total = sum(len(v) for v in by_area.values())
        root["c"].append({"n": f"Proposed, MCTS search ({total})", "k": "proposed", "c": prop})
    return root


def main():
    tree = build_tree()
    page = TEMPLATE.replace("/*DATA*/", json.dumps(tree))
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT}")


TEMPLATE = r"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ontology tree · EthicalAI</title>
<link rel="icon" type="image/png" href="favicon.png">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Manrope:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{--accent:#FF4931;--accent-d:#c2341a;--ink:#141414;--muted:#64646a;--line:#eae8e6;--panel:#f6f5f4;--human:#2f6df6;--humansoft:#eaf1ff}
*{box-sizing:border-box}
html,body{margin:0;height:100%;font-family:Manrope,system-ui,sans-serif;color:var(--ink);background:#fff}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:10px 16px;border-bottom:1px solid var(--line);position:sticky;top:0;background:#fff;z-index:3}
.bar h1{font-family:'Space Grotesk',sans-serif;font-size:17px;margin:0 10px 0 0}
.bar .btn{font-size:12.5px;padding:6px 11px;border:1px solid var(--line);border-radius:999px;background:#fff;cursor:pointer;font-family:inherit}
.bar .hint{font-size:12px;color:var(--muted);margin-left:auto}
.bar a{font-size:12.5px;color:var(--accent-d);font-weight:600;text-decoration:none}
#stage{position:absolute;inset:52px 0 0 0;overflow:hidden;cursor:grab;background:radial-gradient(circle at 20% 20%,#fafafa,#fff)}
#stage.grab{cursor:grabbing}
svg{width:100%;height:100%;display:block}
.link{fill:none;stroke:var(--line);stroke-width:1.5}
.node text{font-size:12.5px;fill:var(--ink);dominant-baseline:middle;pointer-events:none;font-family:Manrope,sans-serif}
.node rect{cursor:pointer}
.node.root rect{fill:var(--ink)} .node.root text{fill:#fff;font-weight:700;font-family:'Space Grotesk'}
.node.tier rect{fill:var(--humansoft);stroke:var(--human)} .node.tier text{fill:#1b3e8c;font-weight:600}
.node.ai rect{fill:rgba(255,73,49,.1);stroke:var(--accent)} .node.ai text{fill:var(--accent-d);font-weight:600}
.node.proposed rect{fill:#fff6e6;stroke:#d99a00} .node.proposed text{fill:#8a5a00;font-weight:600}
.node.group rect{fill:var(--panel);stroke:var(--line)} .node.group text{font-weight:600}
.node.parea rect{fill:#fffaf0;stroke:#e0b000} .node.parea text{fill:#8a5a00;font-weight:600}
.node.mode rect{fill:#fff;stroke:var(--line)}
.node.mode.hum rect{stroke:var(--human)}
.node.mode.ain rect{fill:rgba(255,73,49,.06);stroke:var(--accent)}
.node.mode.flag rect{fill:#fdecf0;stroke:var(--accent)}
.node.cand rect{fill:#fff;stroke:#d99a00;stroke-dasharray:3 3}
.node .toggle{font-weight:700;fill:var(--muted)}
.node:hover rect{filter:brightness(.97)}
#panel{position:absolute;right:14px;top:66px;width:min(320px,80vw);background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:0 10px 40px rgba(0,0,0,.12);padding:16px 18px;display:none;z-index:4}
#panel h3{font-family:'Space Grotesk';margin:0 0 6px;font-size:16px}
#panel .tag{display:inline-block;font-size:11px;padding:1px 8px;border-radius:999px;background:var(--panel);color:var(--muted);margin:0 4px 6px 0}
#panel p{font-size:13px;margin:8px 0}
#panel .k{color:var(--muted);font-weight:600}
#panel .x{position:absolute;right:10px;top:8px;cursor:pointer;color:var(--muted);border:none;background:none;font-size:18px}
</style></head>
<body>
<div class="bar">
  <h1>Ontology tree</h1>
  <button class="btn" id="expand">Expand all</button>
  <button class="btn" id="collapse">Collapse</button>
  <button class="btn" id="reset">Reset view</button>
  <span class="hint">drag to pan · scroll to zoom · click a node to open · click a leaf to read</span>
  <a href="index.html">← catalogue</a>
</div>
<div id="stage"><svg id="svg"><g id="view"></g></svg></div>
<div id="panel"><button class="x" id="px">×</button><div id="pbody"></div></div>
<script>
const DATA = /*DATA*/;
let uid=0;
(function tag(n,d){ n._id=uid++; n._d=d; n._open=(d===0); (n.c||[]).forEach(c=>tag(c,d+1)); })(DATA,0);
const RX=10, XGAP=230, YGAP=26, NW=200, NH=22;
const view=document.getElementById('view'), svg=document.getElementById('svg'), stage=document.getElementById('stage');
let tx=40, ty=0, scale=1;

function esc(s){return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function layout(){
  let y=0;
  function walk(n,depth){
    n._x=depth*XGAP;
    const kids=(n._open&&n.c)?n.c:[];
    if(!kids.length){ n._y=y; y+=YGAP; }
    else { kids.forEach(k=>walk(k,depth+1)); n._y=(kids[0]._y+kids[kids.length-1]._y)/2; }
  }
  walk(DATA,0);
}
function visible(n,arr){ arr.push(n); if(n._open&&n.c) n.c.forEach(c=>visible(c,arr)); return arr; }
function trunc(s,m){ s=String(s); return s.length>m?s.slice(0,m-1)+'…':s; }
function render(){
  layout();
  const nodes=visible(DATA,[]);
  let h='';
  // links
  for(const n of nodes){ if(n._open&&n.c) for(const c of n.c){
    const x1=n._x+NW, y1=n._y, x2=c._x, y2=c._y, mx=(x1+x2)/2;
    h+=`<path class="link" d="M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}"/>`;
  }}
  // nodes
  for(const n of nodes){
    const hasKids=n.c&&n.c.length;
    let cls='node '+n.k;
    if(n.k==='mode'){ cls+=n.m.ai?' ain':' hum'; if(n.m.hi) cls+=' flag'; }
    const label=trunc(n.n,28);
    const tog=hasKids?`<text class="toggle" x="${NW-13}" y="${NH/2}">${n._open?'−':'+'}</text>`:'';
    h+=`<g class="${cls}" data-id="${n._id}" transform="translate(${n._x},${n._y-NH/2})">`
      +`<rect width="${NW}" height="${NH}" rx="8" ry="8"></rect>`
      +`<text x="12" y="${NH/2}">${esc(label)}</text>${tog}</g>`;
  }
  view.innerHTML=h;
  view.setAttribute('transform',`translate(${tx},${ty}) scale(${scale})`);
}
const byId={}; (function idx(n){byId[n._id]=n;(n.c||[]).forEach(idx);})(DATA);
svg.addEventListener('click',e=>{
  const g=e.target.closest('.node'); if(!g) return;
  const n=byId[g.dataset.id];
  if(n.c&&n.c.length){ n._open=!n._open; render(); }
  else if(n.m){ showPanel(n); }
});
function showPanel(n){
  const p=document.getElementById('panel'), b=document.getElementById('pbody');
  let t='';
  if(n.k==='cand'){ t=`<h3>${esc(n.n)}</h3><span class="tag">proposed</span><span class="tag">${n.m.pc} papers</span><p>${esc(n.m.def)}</p><p class="k">Candidate from the MCTS discovery run; not yet in the ontology.</p>`; }
  else { t=`<h3>${esc(n.n)}</h3>`
    +`<span class="tag">${n.m.ai?'AI-native':esc(n.m.pr)}</span><span class="tag">${esc(n.m.hm)}</span>`+(n.m.pc?`<span class="tag">${n.m.pc.toLocaleString()} papers</span>`:'')
    +`<p>${esc(n.m.def)}</p>`
    +(n.m.hp?`<p><span class="k">Human parallel:</span> ${esc(n.m.hp)}</p>`:`<p class="k">AI-native (no human parallel)</p>`); }
  b.innerHTML=t; p.style.display='block';
}
document.getElementById('px').onclick=()=>document.getElementById('panel').style.display='none';
document.getElementById('expand').onclick=()=>{(function o(n){n._open=true;(n.c||[]).forEach(o);})(DATA);render();};
document.getElementById('collapse').onclick=()=>{(function o(n,d){n._open=(d===0);(n.c||[]).forEach(c=>o(c,d+1));})(DATA,0);render();};
document.getElementById('reset').onclick=()=>{tx=40;ty=stage.clientHeight/2;scale=1;render();};
// pan
let drag=false,sx,sy;
stage.addEventListener('mousedown',e=>{drag=true;sx=e.clientX-tx;sy=e.clientY-ty;stage.classList.add('grab');});
window.addEventListener('mousemove',e=>{if(!drag)return;tx=e.clientX-sx;ty=e.clientY-sy;view.setAttribute('transform',`translate(${tx},${ty}) scale(${scale})`);});
window.addEventListener('mouseup',()=>{drag=false;stage.classList.remove('grab');});
// zoom
stage.addEventListener('wheel',e=>{e.preventDefault();const f=e.deltaY<0?1.1:0.9;const r=stage.getBoundingClientRect();const mx=e.clientX-r.left,my=e.clientY-r.top;tx=mx-(mx-tx)*f;ty=my-(my-ty)*f;scale*=f;view.setAttribute('transform',`translate(${tx},${ty}) scale(${scale})`);},{passive:false});
ty=stage.clientHeight/2; render();
</script>
</body></html>
"""


if __name__ == "__main__":
    main()
