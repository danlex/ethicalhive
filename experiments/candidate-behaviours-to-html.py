"""Render the candidate-behaviours markdown list as a browsable HTML page.

Usage: python candidate-behaviours-to-html.py <input.md> <output.html>
"""
import html
import json
import os
import re
import sys
from pathlib import Path

src, out = sys.argv[1], sys.argv[2]
only_new = "--only-new" in sys.argv[3:]
rows, groups, group, letter = [], [], None, None
for line in open(src, encoding="utf-8"):
    m = re.match(r"^## ([A-Z]{1,2})\. (.+?) \(\d+\)", line)
    if m:
        letter, group = m.group(1), m.group(2)
        groups.append({"key": letter, "name": group})
        continue
    m = re.match(r"^\| (\d+) \|(.*)\|\s*$", line)
    if m and group:
        c = [x.strip().replace("*", "") for x in m.group(2).split("|")]
        rows.append({"n": int(m.group(1)), "g": letter, "name": c[0],
                     "src": c[1], "human": c[2], "ai": c[3], "near": c[4],
                     "ev": c[5] if len(c) > 5 else "",
                     "b": 8 if int(m.group(1)) > 422 else 7 if int(m.group(1)) > 305 else 6 if int(m.group(1)) > 190 else 5 if int(m.group(1)) > 180 else 4 if int(m.group(1)) > 169 else 3 if int(m.group(1)) > 145 else 2 if int(m.group(1)) > 100 else 1})
assert len(rows) == 541, len(rows)
review_path = os.path.join(os.path.dirname(src), "candidate-review-2026-11-06.tsv")
review = {}
if os.path.exists(review_path):
    for line in open(review_path, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) == 8:
            review[int(f[0])] = f
for r in rows:
    v = review.get(r["n"])
    if not v:
        r["rv"], r["rvn"] = "", ""
        continue
    flags = []
    if v[2] != "OK":
        flags.append("Definition questioned")
    if v[3] == "WRONG":
        flags.append("Source corrected")
    elif v[3] != "OK":
        flags.append("Source unconfirmed")
    if v[5] != "OK":
        flags.append("Weak AI parallel")
    if v[6].strip() and not r["near"]:
        r["near"] = v[6].strip()
        flags.append("Duplicate found in review")
    r["rv"] = "; ".join(flags) or "No unresolved flags in the supplied review scope"
    r["rvn"] = v[7]
orig_path = os.path.join(os.path.dirname(src), "candidate-original-check-2026-11-07.tsv")
orig = {}
if os.path.exists(orig_path):
    for line in open(orig_path, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) == 8:
            orig[int(f[0])] = f
for r in rows:
    o = orig.get(r["n"])
    m = re.match(r"[A-Za-z0-9_.\-]+", o[3].strip()) if o else None
    r["oc"], r["od"] = (o[4], o[5]) if o else ("", "")
    r["oid"] = m.group(0) if m and o[4] == "FOUND" else ""
    r["oq"], r["on"] = (o[6], o[7]) if o else ("", "")
    r["ow"] = o[2] if o else ""
correction_path = Path(src).resolve().parents[1] / "references/source-corrections-review-2026-11-07.json"
corrections = {}
if correction_path.exists():
    corrections = {r["bundle_candidate_id"]: r for r in json.loads(correction_path.read_text())["records"]}
for r in rows:
    c = corrections.get(r["n"])
    if c:
        r["cr"] = {k: c[k] for k in ("bibliographic_review", "definition_review", "qualification")}
if only_new:
    rows = [r for r in rows if not r["near"]]
    groups = [g for g in groups if any(r["g"] == g["key"] for r in rows)]
flagged = sum(1 for r in rows if r["rv"] and r["rv"] != "No unresolved flags in the supplied review scope")
confirmed = sum(1 for r in rows if r["oc"] == "FOUND")
near = sum(1 for r in rows if r["near"])
b2 = sum(1 for r in rows if r["b"] > 1)

data = json.dumps({"groups": groups, "rows": rows}, ensure_ascii=False)
data = data.replace("</", "<\\/")

page = r"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research Bundle: Candidate Behaviours</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
/* Layout: dark masthead with the three counts, then a sticky filter bar over a
   grouped two-column ledger (human definition | in an AI) per behaviour. */
:root{
  --bg:#ffffff; --panel:#f6f5f4; --line:#eae8e6; --ink:#141414; --muted:#64646a;
  --accent:#FF4931; --accent-ink:#c92f1a; --accent-soft:rgba(255,73,49,.10);
  --hero:#0c0c0e; --hero-ink:#f4f3f2; --hero-muted:#a9a8ad; --hero-line:rgba(255,255,255,.14);
  --warn-bg:#fff6e5; --warn-ink:#7a4b00; --warn-line:#f1d9a6;
  --sans:'Manrope',system-ui,-apple-system,"Segoe UI",sans-serif;
  --head:'Space Grotesk','Manrope',system-ui,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#111113; --panel:#1a1a1d; --line:#2a2a2e; --ink:#ecebea; --muted:#9d9ca3;
  --accent:#ff6a55; --accent-ink:#ff8a78; --accent-soft:rgba(255,106,85,.14);
  --hero:#060607; --hero-ink:#f4f3f2; --hero-muted:#a9a8ad; --hero-line:rgba(255,255,255,.12);
  --warn-bg:#2a2112; --warn-ink:#f0c879; --warn-line:#4a3a1c; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#111113; --panel:#1a1a1d; --line:#2a2a2e; --ink:#ecebea; --muted:#9d9ca3;
  --accent:#ff6a55; --accent-ink:#ff8a78; --accent-soft:rgba(255,106,85,.14);
  --hero:#060607; --hero-ink:#f4f3f2; --hero-muted:#a9a8ad; --hero-line:rgba(255,255,255,.12);
  --warn-bg:#2a2112; --warn-ink:#f0c879; --warn-line:#4a3a1c; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font:16px/1.6 var(--sans);-webkit-font-smoothing:antialiased}
.gut{max-width:1180px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
a{color:var(--accent-ink)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

.mast{background:var(--hero);color:var(--hero-ink)}
.mast .gut{padding-block:44px 36px;display:grid;gap:22px}
.eyebrow{font:600 12px/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--hero-muted)}
.eyebrow b{color:var(--accent);font-weight:700}
h1{font:700 clamp(30px,5vw,50px)/1.05 var(--head);margin:0;letter-spacing:-.02em;text-wrap:balance;max-width:20ch}
.lede{margin:0;color:var(--hero-muted);max-width:64ch;font-size:17px}
.stats{display:flex;flex-wrap:wrap;gap:0;border-top:1px solid var(--hero-line);padding-top:18px}
.stat{padding-right:32px;margin-right:32px;border-right:1px solid var(--hero-line)}
.stat:last-child{border-right:0}
.stat .v{font:700 34px/1 var(--head);font-variant-numeric:tabular-nums}
.stat .v.acc{color:var(--accent)}
.stat .k{font-size:13px;color:var(--hero-muted);margin-top:6px}

.note{margin-top:22px;background:var(--warn-bg);color:var(--warn-ink);border:1px solid var(--warn-line);border-radius:12px;padding:12px 16px;font-size:14.5px;max-width:86ch}
.note b{font-weight:700}

.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--line);margin-top:18px}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
.bar .gut{padding-block:12px;display:grid;gap:10px}
.row1{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.search{flex:1 1 260px;min-width:0;font:inherit;font-size:15px;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:9px 16px}
.toggle{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--muted);cursor:pointer;user-select:none}
.toggle input{accent-color:var(--accent);width:16px;height:16px}
.count{font-size:14px;color:var(--muted);font-variant-numeric:tabular-nums;margin-left:auto}
.chips{display:flex;gap:6px;overflow-x:auto;padding-bottom:2px;scrollbar-width:thin}
.chip{flex:0 0 auto;font:600 13px/1 var(--sans);color:var(--ink);background:transparent;border:1px solid var(--line);border-radius:999px;padding:8px 12px;cursor:pointer;white-space:nowrap}
.chip .c{color:var(--muted);font-weight:500;margin-left:4px;font-variant-numeric:tabular-nums}
.chip[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.chip[aria-pressed="true"] .c{color:var(--bg);opacity:.7}

.seg{display:flex;border:1px solid var(--line);border-radius:999px;padding:3px;background:var(--panel);flex-wrap:wrap}
.seg button{font:600 13px/1 var(--sans);color:var(--muted);background:transparent;border:0;border-radius:999px;padding:8px 12px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--accent);color:#fff}
main .gut{padding-block:8px 64px}
.part{margin-top:40px}
.part-head{display:grid;gap:6px;padding:22px 24px;border-radius:14px;background:var(--panel);border:1px solid var(--line)}
.part-new .part-head{background:var(--accent-soft);border-color:var(--accent)}
.ptag{font:600 12px/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.part-new .ptag{color:var(--accent-ink)}
.ptitle{display:flex;align-items:baseline;gap:12px;font:700 clamp(24px,3.4vw,32px)/1.1 var(--head);margin:0;letter-spacing:-.015em}
.pn{font:700 clamp(24px,3.4vw,32px)/1 var(--head);color:var(--accent-ink);font-variant-numeric:tabular-nums}
.part-near .pn{color:var(--muted)}
.part-new .near{display:none}
.meta{display:flex;flex-wrap:wrap;align-items:center;gap:8px 18px;margin-top:10px}
.meta .near{margin-top:0}
.ev{font-size:13px;color:var(--muted);display:flex;align-items:center;gap:8px;flex-wrap:wrap;min-width:0}
.ev a{word-break:break-all}
.bt{font:700 11px/1 var(--sans);letter-spacing:.06em;text-transform:uppercase;border-radius:999px;padding:4px 8px;border:1px solid var(--line);color:var(--muted)}
.bt.b2{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.bt.rok{border-color:var(--line);color:var(--muted)}
.bt.rbad{border-color:var(--warn-line);background:var(--warn-bg);color:var(--warn-ink)}
.ev.rv{flex-basis:100%}
.rvn{flex-basis:100%;font-size:12.5px;color:var(--muted);padding-left:2px}
.bt.ook{background:var(--accent-soft);border-color:var(--accent);color:var(--accent-ink)}
.part-head p{margin:0;color:var(--muted);max-width:70ch;font-size:15px}
.grp{margin-top:30px}
.grp .gh{display:flex;align-items:baseline;gap:12px;font:700 22px/1.2 var(--head);margin:0 0 4px;letter-spacing:-.01em}
.grp .gh .L{font:600 13px/1 var(--mono);color:var(--accent-ink);background:var(--accent-soft);border-radius:6px;padding:5px 7px}
.grp .gh .n{font:500 14px/1 var(--sans);color:var(--muted)}
.grp .srcs{margin:0 0 10px;color:var(--muted);font-size:14px;max-width:90ch}

.item{display:grid;grid-template-columns:56px minmax(0,1fr);gap:4px 16px;padding:18px 0;border-top:1px solid var(--line)}
.num{font:600 14px/1.9 var(--mono);color:var(--muted);font-variant-numeric:tabular-nums}
.head{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 12px}
.name{font:700 19px/1.3 var(--head);margin:0}
.src{font-size:13px;color:var(--muted)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:8px}
.cols > div{min-width:0}
.lab{font:600 11px/1 var(--sans);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:5px}
.lab.ai{color:var(--accent-ink)}
.cols p{margin:0;font-size:15px;max-width:62ch}
.near{margin-top:10px;font-size:13px;color:var(--muted)}
.near span{display:inline-block;background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:2px 10px;color:var(--ink);margin-left:4px}
.new{display:inline-block;font:700 11px/1 var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--accent-ink);border:1px solid var(--accent);border-radius:999px;padding:4px 8px}
mark{background:var(--accent-soft);color:inherit;border-radius:3px}
.empty{padding:48px 0;color:var(--muted);text-align:center}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:13.5px}
footer .gut{padding-block:22px 40px}

@media (max-width:720px){
  .cols{grid-template-columns:1fr;gap:12px}
  .item{grid-template-columns:1fr}
  .num{line-height:1}
  .stats{display:grid;grid-template-columns:1fr 1fr;gap:16px 0}
  .stat{border-right:0;margin-right:0;padding-right:12px}
  .count{margin-left:0}
}
@media (prefers-reduced-motion:no-preference){.item{transition:background .15s}}
</style>

<header class="mast">
  <div class="gut">
    <div class="eyebrow"><b>EthicalAI</b> &nbsp;·&nbsp; catalogue candidates &nbsp;·&nbsp; 6 November 2026</div>
    <h1>__TOTAL__ human behaviours to look for in AI</h1>
    <p class="lede">Behaviours named in psychology, psychotherapy, group dynamics, medicine, aviation, research practice, software engineering, statistics, design and rhetoric, each with its source, its human definition, and a proposed AI example. Many names already occur in the 434-record catalogue. Supplied overlap labels are historical review leads, not evidence of novelty or distinct mechanisms.</p>
    <div class="stats">
      <div class="stat"><div class="v">__TOTAL__</div><div class="k">behaviours</div></div>
      <div class="stat"><div class="v">__FIELDS__</div><div class="k">source fields</div></div>
      <div class="stat"><div class="v acc">__NEW__</div><div class="k">no overlap recorded in bundle</div></div>
      <div class="stat"><div class="v">__NEAR__</div><div class="k">close to an existing mode</div></div>
      <div class="stat"><div class="v">__B2__</div><div class="k">checked through search</div></div>
      <div class="stat"><div class="v">__FLAGGED__</div><div class="k">flagged in review</div></div>
      <div class="stat"><div class="v acc">__CONFIRMED__</div><div class="k">historical reported term hits</div></div>
    </div>
  </div>
</header>

<div class="gut">
  <p class="note"><b>Research bundle, not an additional catalogue.</b> Local research IDs differ from website Reference IDs. The supplied bundle reports general-knowledge drafting, search checks and text searches; these reports do not establish full-book reading or an independent audit. The 18 reviewed corrections (2026-11-07) separate bibliographic support, definition support and untested AI examples; their before/after text and evidence are in <code>references/source-corrections-review-2026-11-07.json</code>. Prior text-search results refer to the named work/edition, which may differ from the corrected citation. Failed searches do not prove absence. The remaining records have not been re-audited. An empty overlap field does not establish novelty.</p>
</div>

<div class="bar">
  <div class="gut">
    <div class="row1">
      <input id="q" class="search" type="search" placeholder="Search names, definitions, sources" aria-label="Search behaviours">
      <div class="seg" id="seg" role="group" aria-label="Show">
        <button type="button" data-v="all" aria-pressed="true">Both parts</button>
        <button type="button" data-v="new" aria-pressed="false">Overlap not recorded</button>
        <button type="button" data-v="near" aria-pressed="false">Close to existing</button>
      </div>
      <div class="seg" id="bseg" role="group" aria-label="Batch">
        <button type="button" data-b="0" aria-pressed="true">All batches</button>
        <button type="button" data-b="1" aria-pressed="false">Batch 1</button>
        <button type="button" data-b="2" aria-pressed="false">Batch 2</button>
        <button type="button" data-b="3" aria-pressed="false">Batch 3</button>
        <button type="button" data-b="4" aria-pressed="false">Batch 4</button>
        <button type="button" data-b="5" aria-pressed="false">Batch 5</button>
        <button type="button" data-b="6" aria-pressed="false">Batch 6</button>
        <button type="button" data-b="7" aria-pressed="false">Batch 7</button>
        <button type="button" data-b="8" aria-pressed="false">Batch 8</button>
      </div>
      <span class="count" id="count" aria-live="polite"></span>
    </div>
    <div class="chips" id="chips" role="group" aria-label="Filter by field"></div>
  </div>
</div>

<main><div class="gut" id="list"></div></main>

<footer><div class="gut">Source list: <code>experiments/candidate-behaviours-2026-11-06.md</code> in the EthicalHive repository, also available as an Excel workbook. "Close to" names the nearest existing catalogue mode, so a reviewer can decide whether the entry is a new mode or a synonym.</div></footer>

<script>
const DATA = __DATA__;
const SRCS = {
  A:"Anna Freud, The Ego and the Mechanisms of Defence (1936); Kernberg (1975); McWilliams, Psychoanalytic Diagnosis.",
  B:"Beck, Cognitive Therapy and the Emotional Disorders (1976); Burns, Feeling Good (1980).",
  C:"Motivational Interviewing, DBT, transactional analysis, family systems and medical ethics.",
  D:"Social psychology of groups and persuasion: Latané, Harvey, Brehm, Cialdini, Ross.",
  E:"Goffman on self-presentation and face; Sartre; Lutz on doublespeak.",
  F:"Organisational failure: Vaughan, Argyris and Schön, Merton, Parkinson, Feynman.",
  G:"Judgment and decision research: Kahneman, Tversky, Pronin, Ellsberg and others.",
  H:"Informal logic and argumentation.",
  I:"Moral psychology: Tenbrunsel and Messick, Haidt.",
  J:"Neuropsychology, human error research and couples-conflict research.",
  K:"Berne, Games People Play (1964).",
  L:"Janis, Victims of Groupthink (1972); Bion, Experiences in Groups (1961).",
  M:"Hirschman, The Rhetoric of Reaction (1991); Schopenhauer, The Art of Being Right (1831).",
  N:"Tetlock; Kahneman, Sibony and Sunstein, Noise (2021); Kahneman (2011); Taleb (2007); Fromm (1941).",
  O:"Reason, Human Error (1990); Dörner, The Logic of Failure (1989).",
  P:"Linehan, Ellis, Horney, Gottman, Watzlawick and Goffman.",
  Q:"Croskerry on cognitive errors in diagnosis (2002, 2003).",
  R:"Aviation human factors, FAA hazardous attitudes, military history, Lanir.",
  S:"Research-integrity literature: Kerr, Gelman and Loken, Simmons et al., Boutron et al.",
  T:"Software engineering lore: The Pragmatic Programmer, Chesterton, the Jargon File.",
  U:"Economics (Siebert, Lucas), journalism (Davies) and Seligman on explanatory style.",
  V:"Statistical reasoning: informal logic and Blyth on Simpson's paradox.",
  W:"Fricker, Epistemic Injustice (2007).",
  X:"Brignull on deceptive design (2010, 2023); Gray et al. (2018).",
  Y:"Aristotle, Nicomachean Ethics, Book VII.",
  Z:"Lifton, Thought Reform and the Psychology of Totalism (1961).",
  AA:"Institute for Propaganda Analysis (1937).",
  AB:"Thompson and Schumann (1987); Berkson (1946); Fisher and Ury, Getting to Yes (1981).",
  AC:"Informal logic and rhetoric.",
  AD:"Young's schema therapy, ACT, Bowen family systems, attachment theory, Rogers, Winnicott.",
  AE:"Safety science (Dekker, Snook, Reason, Weick), medicine, finance and software anti-patterns.",
  AF:"Sociology (Merton, Goffman, Hirschman), media studies and management.",
  AG:"Behavioural economics, game theory and public choice.",
  AH:"Research methods, science studies and epistemology.",
  AI:"Piaget, learning science, motivation research and human factors.",
  AJ:"Heuer on intelligence analysis, criminal justice, bioethics, Ryle and philosophy of mind.",
  AK:"Classical, religious and Chinese moral traditions; literary archetypes.",
  AL:"Pragmatics, conversation analysis, translation studies and usage.",
  AM:"Systems archetypes (Senge), Brooks, Conway, operations and security engineering.",
  AN:"Ethology, learning theory, neuropsychology and psychiatric phenomenology.",
  AO:"Sales and negotiation tactics, con artistry and intelligence tradecraft."
};
let active = null, show = "all", batch = 0;
const $ = s => document.querySelector(s);
const esc = s => s.replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const hl = (s, q) => {
  const e = esc(s);
  if (!q) return e;
  const re = new RegExp("(" + q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
  return e.replace(re, "<mark>$1</mark>");
};

function chips(){
  const all = [{key:null,name:"All fields"}].concat(DATA.groups);
  $("#chips").innerHTML = all.map(g => {
    const n = g.key ? DATA.rows.filter(r => r.g === g.key).length : DATA.rows.length;
    return `<button class="chip" type="button" data-k="${g.key||""}" aria-pressed="${g.key===active}">${esc(g.name)}<span class="c">${n}</span></button>`;
  }).join("");
}
function render(){
  const q = $("#q").value.trim();
  const ql = q.toLowerCase();
  const rows = DATA.rows.filter(r =>
    (!active || r.g === active) &&
    (show === "all" || (show === "new") === !r.near) &&
    (!batch || r.b === batch) &&
    (!ql || [r.name, r.src, r.human, r.ai, r.near].join(" ").toLowerCase().includes(ql)));
  $("#count").textContent = rows.length === 1 ? "1 behaviour" : rows.length + " behaviours";
  if (!rows.length){ $("#list").innerHTML = '<p class="empty">No behaviour matches. Clear the search or pick another field.</p>'; return; }
  const neu = rows.filter(r => !r.near), close = rows.filter(r => r.near);
  $("#list").innerHTML =
    part("new", "Part 1", "No overlap recorded in bundle", "The original bundle assigned no close mode. These records still require comparison with the current catalogue.", neu, q) +
    part("near", "Part 2", "Close to an existing mode", "Each sits near a mode the catalogue already has. Decide for each whether it is a new mode or a synonym of that mode.", close, q);
}
function rvBadge(r){
  if (!r.rv) return "";
  const ok = r.rv === "No unresolved flags in the supplied review scope";
  return `<div class="ev rv"><span class="bt ${ok ? "rok" : "rbad"}">Review</span>${esc(r.rv)}${r.rvn ? `<span class="rvn">${esc(r.rvn)}</span>` : ""}</div>`;
}
function ocBadge(r){
  if (!r.oc) return "";
  const label = {
    FOUND: r.od === "MATCHES" ? "Supplied search reports term and definition match" : "Supplied search reports term found; historical definition result: " + r.od,
    NOT_FOUND: "Supplied search did not find the term; this does not prove absence",
    NOT_AVAILABLE: "Work unavailable in the supplied search; not checked there",
    NO_SPECIFIC_WORK: "No specific work named in the prior search; not checked there"
  }[r.oc] || r.oc;
  const cls = r.oc === "FOUND" ? "ook" : r.oc === "NOT_FOUND" ? "rbad" : "rok";
  const link = r.oid ? ` <a href="https://archive.org/details/${encodeURIComponent(r.oid)}" target="_blank" rel="noopener">scan</a>` : "";
  const quote = r.oq ? `<span class="rvn">“${esc(r.oq)}”</span>` : "";
  const note = r.on ? `<span class="rvn">${esc(r.on)}</span>` : "";
  return `<div class="ev rv"><span class="bt ${cls}">Prior text search</span>${esc(label)}${link}<span class="rvn">Work searched: ${esc(r.ow)}</span>${quote}${note}</div>`;
}
function evid(r){
  const c = r.cr;
  const current = c ? `<div class="ev rv"><span class="bt rok">2026-11-07 correction</span>Bibliography: ${esc(c.bibliographic_review.status)}; definition: ${esc(c.definition_review.status)}<span class="rvn">Access: ${esc(c.bibliographic_review.access_depth)} ${esc(c.qualification)}</span>${c.bibliographic_review.evidence_urls.map(u=>`<a href="${esc(u)}" target="_blank" rel="noopener">evidence</a>`).join(" ")}</div>` : "";
  return evidBase(r) + current + ocBadge(r);
}
function evidBase(r){
  if (r.b === 1) return `<div class="ev"><span class="bt b1">Batch 1</span>Written from general knowledge</div>` + rvBadge(r);
  const e = r.ev || "";
  const body = /^https?:\/\//.test(e)
    ? `Checked via <a href="${esc(e)}" target="_blank" rel="noopener">${esc(e.replace(/^https?:\/\/(www\.)?/, "").split("/")[0])}</a>`
    : e === "Name only" ? "Name confirmed in search; definition from general knowledge"
    : "Checked via several secondary pages";
  return `<div class="ev"><span class="bt b2">Batch ${r.b}</span>${body}</div>` + rvBadge(r);
}
function part(id, tag, title, blurb, rows, q){
  if (!rows.length) return "";
  return `<section class="part part-${id}" id="part-${id}">
    <div class="part-head"><span class="ptag">${tag}</span><h2 class="ptitle">${title}<span class="pn">${rows.length}</span></h2><p>${blurb}</p></div>
    ${groupsHtml(rows, q)}</section>`;
}
function groupsHtml(rows, q){
  return DATA.groups.map(g => {
    const rs = rows.filter(r => r.g === g.key);
    if (!rs.length) return "";
    return `<section class="grp"><h3 class="gh"><span class="L">${g.key}</span>${esc(g.name)}<span class="n">${rs.length}</span></h3>
      <p class="srcs">${esc(SRCS[g.key]||"")}</p>
      ${rs.map(r => `<article class="item" id="b${r.n}">
        <div class="num">${String(r.n).padStart(3,"0")}</div>
        <div>
          <div class="head"><h4 class="name">${hl(r.name,q)}</h4><span class="src">${hl(r.src,q)}</span></div>
          <div class="cols">
            <div><div class="lab">Human definition</div><p>${hl(r.human,q)}</p></div>
            <div><div class="lab ai">In an AI</div><p>${hl(r.ai,q)}</p></div>
          </div>
          <div class="meta">
            <div class="near">${r.near ? `Close to<span>${hl(r.near,q)}</span>` : `<span class="new">Overlap not recorded</span>`}</div>
            ${evid(r)}
          </div>
        </div></article>`).join("")}
    </section>`;
  }).join("");
}
$("#chips").addEventListener("click", e => {
  const b = e.target.closest(".chip"); if (!b) return;
  active = b.dataset.k || null; chips(); render();
});
$("#seg").addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b) return;
  show = b.dataset.v;
  document.querySelectorAll("#seg button").forEach(x => x.setAttribute("aria-pressed", x === b));
  render();
});
$("#bseg").addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b) return;
  batch = Number(b.dataset.b);
  document.querySelectorAll("#bseg button").forEach(x => x.setAttribute("aria-pressed", x === b));
  render();
});
$("#q").addEventListener("input", render);
chips(); render();
</script>
</html>
"""
if only_new:
    page = page.replace("<title>Research Bundle: Candidate Behaviours</title>", "<title>Research Bundle: Historical Shortlist</title>")
    page = page.replace("__TOTAL__ human behaviours to look for in AI", "__TOTAL__ records in the historical shortlist")
    page = page.replace(".part-new .near{display:none}", ".part-new .near{display:none}\n#seg{display:none}")
page = (page.replace("__DATA__", data)
            .replace("__NEAR__", str(near))
            .replace("__TOTAL__", str(len(rows)))
            .replace("__FIELDS__", str(len(groups)))
            .replace("__B2__", str(b2))
            .replace("__FLAGGED__", str(flagged))
            .replace("__CONFIRMED__", str(confirmed))
            .replace("__NEW__", str(len(rows) - near)))
open(out, "w", encoding="utf-8").write(page)
print(f"wrote {len(rows)} behaviours ({near} close to existing) -> {out}")
