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
RISE = ROOT / "experiments" / "discover-rise-results.json"
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
            "ex": m.get("example", ""),
            "grp": m.get("group_label", ""),
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

    # prefer the RISE run if present, else the single-round MCTS scorer
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
.bar .btn:hover{background:var(--panel)}
.bar #q{font-family:inherit;font-size:13px;padding:6px 12px;border:1px solid var(--line);border-radius:999px;width:230px;outline:none}
.bar #q:focus{border-color:var(--accent)}
.bar .hint{font-size:12px;color:var(--muted);margin-left:auto}
.bar a{font-size:12.5px;color:var(--accent-d);font-weight:600;text-decoration:none}
#crumb{position:absolute;top:52px;left:0;right:0;height:34px;display:flex;align-items:center;gap:1px;padding:0 16px;background:#fff;border-bottom:1px solid var(--line);font-size:12.5px;overflow-x:auto;white-space:nowrap;z-index:2}
#crumb .cr{cursor:pointer;color:var(--accent-d);font-weight:600;padding:3px 7px;border-radius:6px}
#crumb .cr:hover{background:var(--panel)}
#crumb .cr:last-child{color:var(--ink);cursor:default}
#crumb .sep{color:var(--muted);margin:0 1px}
.embed #crumb{display:none}
#stage{position:absolute;inset:86px 0 0 0;overflow:hidden;cursor:grab;background:radial-gradient(circle at 20% 15%,#fafafa,#fff)}
#stage.grab{cursor:grabbing}
svg{width:100%;height:100%;display:block}
.link{fill:none;stroke:var(--line);stroke-width:1.5;transition:opacity .12s,stroke .12s}
.node{transition:opacity .12s}
.node text{font-size:12.5px;fill:var(--ink);dominant-baseline:middle;pointer-events:none;font-family:Manrope,sans-serif}
.node rect{cursor:pointer}
.node.root rect{fill:var(--ink)} .node.root text{fill:#fff;font-weight:700;font-family:'Space Grotesk'}
.node.tier rect{fill:#f3f6fb;stroke:#c4d0e4} .node.tier text{fill:#3b4a63;font-weight:600}
.node.ai rect{fill:#faf2f0;stroke:#e3c3bb} .node.ai text{fill:#8a5243;font-weight:600}
.node.proposed rect{fill:#fdf7ea;stroke:#e3c98f} .node.proposed text{fill:#8a6a1f;font-weight:600}
.node.group rect{fill:var(--panel);stroke:var(--line)} .node.group text{font-weight:600}
.node.parea rect{fill:#fdfaf1;stroke:#e3c98f} .node.parea text{fill:#8a6a1f;font-weight:600}
.node.mode rect{fill:#fff;stroke:var(--line)}
.node.mode.hum rect{stroke:#bcc8dc}
.node.mode.ain rect{stroke:#ddc3ba}
.node.mode.flag rect{stroke:#d98b7a;stroke-width:1.8}
.node.cand rect{fill:#fff;stroke:#dcc08a;stroke-dasharray:3 3}
.node .toggle{font-weight:700;fill:var(--muted)}
.node .badge{font-size:10px;fill:#b2b0ad;text-anchor:end}
.node:hover rect{filter:brightness(.97)}
/* hover lineage: one warm accent on the path, the rest softly dimmed */
.hovering .node:not(.lit){opacity:.4}
.hovering .link:not(.lit){opacity:.18}
.link.lit{stroke:var(--accent);stroke-width:2.2}
.node.lit rect{stroke:var(--accent);stroke-width:1.8}
/* search */
.searching .node.off{opacity:.2}
.node.hit rect{stroke:var(--accent);stroke-width:2.4}
.embed .bar{display:none}
.embed #stage{inset:0}
.embed .legend{display:none}
.legend{position:absolute;left:14px;bottom:14px;background:rgba(255,255,255,.94);border:1px solid var(--line);border-radius:12px;padding:11px 13px;font-size:11.5px;z-index:4;max-width:230px;box-shadow:0 8px 24px rgba(0,0,0,.08)}
.legend b{font-family:'Space Grotesk';font-size:11px;letter-spacing:.3px;text-transform:uppercase;color:var(--muted);display:block;margin:0 0 6px}
.legend .row{display:flex;align-items:center;gap:7px;margin:3px 0;color:#3a3a3a}
.legend .sw{width:13px;height:13px;border-radius:4px;border:1px solid var(--line);flex:none}
.legend .bd{width:13px;height:13px;border-radius:4px;background:#fff;flex:none}
.legend hr{border:none;border-top:1px solid var(--line);margin:8px 0}
#panel{position:absolute;right:14px;top:66px;width:min(366px,86vw);max-height:calc(100% - 84px);overflow:auto;background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:0 14px 48px rgba(0,0,0,.16);padding:16px 18px 18px;display:none;z-index:5}
#panel .ptag{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;padding:3px 9px;border-radius:999px;margin-bottom:9px}
#panel h3{font-family:'Space Grotesk';margin:0 0 9px;font-size:18px;line-height:1.2;padding-right:18px}
#panel .chips{margin:0 0 2px}
#panel .tag{display:inline-block;font-size:11px;padding:2px 9px;border-radius:999px;background:var(--panel);color:#444;margin:0 4px 6px 0}
#panel .tag .sw{display:inline-block;width:9px;height:9px;border-radius:3px;margin-right:5px;vertical-align:middle;border:1px solid rgba(0,0,0,.08)}
#panel p{font-size:13.5px;margin:9px 0 0;line-height:1.55}
#panel .sec{margin:12px 0 0;padding-top:11px;border-top:1px solid var(--line)}
#panel .sec .k{display:block;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;margin-bottom:2px}
#panel .sec p{margin:0}
#panel .k{color:var(--muted);font-weight:600}
#panel .note{font-size:12px;color:var(--muted);font-style:italic;margin-top:11px}
#panel .x{position:absolute;right:10px;top:8px;cursor:pointer;color:var(--muted);border:none;background:none;font-size:20px;line-height:1}
</style></head>
<body>
<div class="bar">
  <h1>Ontology tree</h1>
  <input id="q" type="search" placeholder="Search modes…" autocomplete="off">
  <button class="btn" id="expand">Expand all</button>
  <button class="btn" id="collapse">Collapse</button>
  <button class="btn" id="reset">Fit view</button>
  <span class="hint">click a branch to drill in, the view auto-fits · click a mode to read</span>
  <a href="index.html">← catalogue</a>
</div>
<nav id="crumb"></nav>
<div id="stage"><svg id="svg"><g id="view"></g></svg></div>
<div class="legend" id="legend"></div>
<div id="panel"><button class="x" id="px">×</button><div id="pbody"></div></div>
<script>
const DATA = /*DATA*/;
const PRIN={honesty:'#e8f0ff',calibration:'#e7f6ee','non-maleficence':'#fdeceb','scope-fidelity':'#fff3e0',independence:'#efeafb',transparency:'#e6f6fb',corrigibility:'#fdeef8'};
function pcol(name){return PRIN[(name||'').toLowerCase()]||'#ffffff';}
let uid=0;
(function tag(n,d){ n._id=uid++; n._d=d; n._open=(d===0); (n.c||[]).forEach(c=>tag(c,d+1)); })(DATA,0);
(function leaves(n){ n._leaves=(n.c&&n.c.length)?n.c.reduce((s,c)=>s+leaves(c),0):1; return n._leaves; })(DATA);
const EMBED=location.search.includes('embed');
if(EMBED){ document.body.classList.add('embed'); (DATA.c||[]).forEach(b=>b._open=true); }
const XGAP=230, YGAP=26, NW=200, NH=22;
const view=document.getElementById('view'), svg=document.getElementById('svg'), stage=document.getElementById('stage');
let tx=40, ty=0, scale=1, searchActive=false;

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
  for(const n of nodes){ if(n._open&&n.c) for(const c of n.c){
    const x1=n._x+NW, y1=n._y, x2=c._x, y2=c._y, mx=(x1+x2)/2;
    h+=`<path class="link" data-c="${c._id}" d="M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}"/>`;
  }}
  for(const n of nodes){
    const hasKids=n.c&&n.c.length;
    let cls='node '+n.k, style='';
    if(n.k==='mode'){ cls+=n.m.ai?' ain':' hum'; if(n.m.hi) cls+=' flag'; style=`style="fill:${pcol(n.m.pr)}"`; }
    if(searchActive){ cls+=n._rel?' rel':' off'; if(n._hit) cls+=' hit'; }
    const label=trunc(n.n,28);
    const tog=hasKids?`<text class="toggle" x="${NW-13}" y="${NH/2}">${n._open?'−':'+'}</text>`:'';
    const badge=(hasKids&&!n._open)?`<text class="badge" x="${NW-25}" y="${NH/2}">${n._leaves}</text>`:'';
    h+=`<g class="${cls}" data-id="${n._id}" transform="translate(${n._x},${n._y-NH/2})">`
      +`<rect width="${NW}" height="${NH}" rx="8" ry="8" ${style}></rect>`
      +`<text x="12" y="${NH/2}">${esc(label)}</text>${badge}${tog}</g>`;
  }
  view.innerHTML=h;
  view.classList.toggle('searching',searchActive);
  view.setAttribute('transform',`translate(${tx},${ty}) scale(${scale})`);
  renderCrumb();
}
const byId={}; (function idx(n,p){n._parent=p||null;byId[n._id]=n;(n.c||[]).forEach(c=>idx(c,n));})(DATA,null);
svg.addEventListener('click',e=>{
  const g=e.target.closest('.node'); if(!g) return;
  const n=byId[g.dataset.id];
  if(n.c&&n.c.length){
    if(n._open){ n._open=false; }
    else { if(n._parent) n._parent.c.forEach(s=>{ if(s!==n) s._open=false; }); n._open=true; }  // accordion: one branch per level
    fitVisible();
  } else if(n.m){ showPanel(n); }
});
// hover lineage
svg.addEventListener('mouseover',e=>{
  const g=e.target.closest('.node'); if(!g) return;
  const line=new Set(); let p=byId[g.dataset.id]; while(p){line.add(p._id);p=p._parent;}
  view.classList.add('hovering');
  view.querySelectorAll('.node').forEach(el=>el.classList.toggle('lit',line.has(+el.dataset.id)));
  view.querySelectorAll('.link').forEach(el=>el.classList.toggle('lit',line.has(+el.dataset.c)));
});
stage.addEventListener('mouseleave',()=>{ view.classList.remove('hovering');
  view.querySelectorAll('.lit').forEach(el=>el.classList.remove('lit')); });
function showPanel(n){
  const p=document.getElementById('panel'), b=document.getElementById('pbody');
  let t='';
  if(n.k==='cand'){
    t=`<div class="ptag" style="color:#8a5a00;background:#fff6e6">Proposed · RISE discovery</div>`
     +`<h3>${esc(n.n)}</h3>`
     +`<div class="chips"><span class="tag">${(n.m.pc||0).toLocaleString()} arXiv papers</span>${n.m.reward!=null?`<span class="tag">reward ${n.m.reward}</span>`:''}</div>`
     +`<p>${esc(n.m.def)}</p>`
     +`<p class="note">Surfaced by the discovery loop; not yet in the ontology.</p>`;
  } else {
    const tier=n.m.ai?'AI-native':'Human-paralleled';
    t=`<div class="ptag" style="color:${n.m.ai?'var(--accent-d)':'#1b3e8c'};background:${n.m.ai?'rgba(255,73,49,.1)':'var(--humansoft)'}">${tier}${n.m.grp?' · '+esc(n.m.grp):''}</div>`
     +`<h3>${esc(n.n)}</h3>`
     +`<div class="chips"><span class="tag"><span class="sw" style="background:${pcol(n.m.pr)}"></span>violates ${esc(n.m.pr)}</span><span class="tag">causes ${esc(n.m.hm)}</span>${n.m.pc?`<span class="tag">${n.m.pc.toLocaleString()} papers</span>`:''}</div>`
     +`<p>${esc(n.m.def)}</p>`
     +(n.m.ex?`<div class="sec"><span class="k">Example</span><p>${esc(n.m.ex)}</p></div>`:'')
     +(n.m.hp?`<div class="sec"><span class="k">Human parallel</span><p>${esc(n.m.hp)}</p></div>`:`<p class="note">AI-native: no human analogue.</p>`);
  }
  b.innerHTML=t; p.style.display='block';
}
document.getElementById('px').onclick=()=>document.getElementById('panel').style.display='none';
window.addEventListener('keydown',e=>{if(e.key==='Escape')document.getElementById('panel').style.display='none';});
document.getElementById('expand').onclick=()=>{(function o(n){n._open=true;(n.c||[]).forEach(o);})(DATA);fitVisible();};
document.getElementById('collapse').onclick=()=>{(function o(n,d){n._open=(d===0);(n.c||[]).forEach(c=>o(c,d+1));})(DATA,0);fitVisible();};
// fit everything currently visible into the viewport, so nothing is ever off-screen
function fitVisible(){
  layout();
  const ns=visible(DATA,[]);
  let a=1e9,b=-1e9,c=1e9,d=-1e9;
  for(const n of ns){ a=Math.min(a,n._x); b=Math.max(b,n._x+NW); c=Math.min(c,n._y-NH/2); d=Math.max(d,n._y+NH/2); }
  const W=stage.clientWidth,H=stage.clientHeight,pad=44,cw=Math.max(1,b-a),ch=Math.max(1,d-c);
  scale=Math.max(0.3,Math.min((W-2*pad)/cw,(H-2*pad)/ch,1.15));
  tx=pad - a*scale; ty=(H-ch*scale)/2 - c*scale;
  render();
}
function fit(){ (function o(n,dep){ n._open = EMBED ? (dep<=1) : (dep===0); (n.c||[]).forEach(k=>o(k,dep+1)); })(DATA,0); fitVisible(); }
document.getElementById('reset').onclick=fit;
function centerOn(n){ const s=Math.max(scale,0.8); scale=s; tx=stage.clientWidth*0.3 - n._x*s; ty=stage.clientHeight/2 - n._y*s; view.setAttribute('transform',`translate(${tx},${ty}) scale(${s})`); }
// breadcrumb of the currently open path
function openPath(){ const p=[DATA]; let n=DATA; while(n._open&&n.c){ const o=n.c.find(x=>x._open); if(!o) break; p.push(o); n=o; } return p; }
function renderCrumb(){ const el=document.getElementById('crumb'); if(!el) return;
  el.innerHTML=openPath().map(n=>`<span class="cr" data-id="${n._id}">${esc(trunc(n.n,24))}</span>`).join('<span class="sep">›</span>'); }
const crumbEl=document.getElementById('crumb');
if(crumbEl) crumbEl.addEventListener('click',e=>{ const c=e.target.closest('.cr'); if(!c) return;
  const n=byId[c.dataset.id]; (n.c||[]).forEach(function cl(x){ x._open=false; (x.c||[]).forEach(cl); }); n._open=true; fitVisible(); });
// search: highlight matches and auto-open their ancestors
const q=document.getElementById('q');
q.addEventListener('input',()=>{
  const s=q.value.trim().toLowerCase();
  (function clear(n){n._hit=false;n._rel=false;(n.c||[]).forEach(clear);})(DATA);
  searchActive=!!s;
  const hits=[];
  if(s){ (function walk(n){
      let hit=(n.n||'').toLowerCase().includes(s) || (n.m&&(n.m.def||'').toLowerCase().includes(s));
      let sub=false; (n.c||[]).forEach(c=>{ if(walk(c)) sub=true; });
      if(hit){ n._hit=true; hits.push(n); }
      n._rel=hit||sub;
      if(sub&&n.c) n._open=true;
      return n._rel;
    })(DATA); }
  render();
  if(hits.length) centerOn(hits[0]);  // bring the first match into view
});
// pan
let drag=false,sx,sy;
stage.addEventListener('mousedown',e=>{drag=true;sx=e.clientX-tx;sy=e.clientY-ty;stage.classList.add('grab');});
window.addEventListener('mousemove',e=>{if(!drag)return;tx=e.clientX-sx;ty=e.clientY-sy;view.setAttribute('transform',`translate(${tx},${ty}) scale(${scale})`);});
window.addEventListener('mouseup',()=>{drag=false;stage.classList.remove('grab');});
// zoom
stage.addEventListener('wheel',e=>{e.preventDefault();const f=e.deltaY<0?1.06:0.945;const r=stage.getBoundingClientRect();const mx=e.clientX-r.left,my=e.clientY-r.top;const ns=Math.min(2.2,Math.max(0.3,scale*f)),k=ns/scale;tx=mx-(mx-tx)*k;ty=my-(my-ty)*k;scale=ns;view.setAttribute('transform',`translate(${tx},${ty}) scale(${scale})`);},{passive:false});
// legend
document.getElementById('legend').innerHTML=
  '<b>Violated principle</b>'+Object.entries(PRIN).map(([k,v])=>
    `<div class="row"><span class="sw" style="background:${v}"></span>${k.replace('-',' ')}</div>`).join('')
  +'<hr><b>Tier</b>'
  +'<div class="row"><span class="bd" style="border:1.5px solid #bcc8dc"></span>human-paralleled</div>'
  +'<div class="row"><span class="bd" style="border:1.5px solid #ddc3ba"></span>AI-native</div>'
  +'<div class="row"><span class="bd" style="border:1.5px dashed #dcc08a"></span>proposed (RISE)</div>';
fit();
</script>
</body></html>
"""


if __name__ == "__main__":
    main()
