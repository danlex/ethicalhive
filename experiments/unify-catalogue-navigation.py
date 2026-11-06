#!/usr/bin/env python3
"""Move research navigation into the existing list; preserve old links as redirects."""
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'docs/index.html';s=p.read_text()
s=re.sub(r'  <section class="framework" id="psychology-research">.*?</section>\s*','',s,count=1,flags=re.S)
s=re.sub(r'(<header class="hero"[^>]*>.*?<h1>).*?(</h1>)',r'\1Recognise AI behaviour. <span class="accent">Understand the risk. Check the evidence.</span>\2',s,count=1,flags=re.S)
s=re.sub(r'(<header class="hero"[^>]*>.*?<p class="lede">).*?(</p>)',r'\1A searchable directory of AI failures and proposed parallels with human behaviour. Find a pattern, read its definition and example, inspect its sources and limits, then decide what to check.\2',s,count=1,flags=re.S)
intro='''<span id="psychology-research"></span><h2>The catalogue</h2>
    <p>One list of <strong>434 behaviours and patterns</strong>: the previous 207 entries and 227 newly integrated human-behaviour analogies. Definitions, examples, sources and review status appear in the same expandable rows. The research supplied 228 records; one was already indexed as an alias and enriches its existing entry.</p>
    <p>New entries are labelled <strong>proposed analogy</strong>, with definition-source review stated individually. A named human behaviour does not establish a shared mechanism in AI. Some entries refine broader existing patterns or describe adaptive processes. No AI experiments were run for these additions.</p>
    <p><a href="behaviours.csv">Download the full list · CSV</a> &middot; <a href="behaviours.json">JSON</a> &middot; <a href="experiments/paper-index.html">Paper ↔ behaviour index</a></p>
    '''
s=re.sub(r'(<section class="framework catalogue" id="catalogue">\s*).*?(?=<div class="cat-legend">)',lambda m:m[1]+intro,s,count=1,flags=re.S)
if 'data-filter="new"' not in s:
 s=s.replace('<button data-filter="analogy">Analogy</button>','<button data-filter="analogy">Analogy</button>\n        <button data-filter="new">Added analogies</button>\n        <button data-filter="pending">Sources to check</button>')
 s=s.replace("if(activeFilter === 'all') return true;","if(activeFilter === 'all') return true;\n    if(activeFilter === 'new') return b.dataset.candidate === '1';\n    if(activeFilter === 'pending') return b.dataset.sourceStatus === 'pending-definition-source-check';")
s=s.replace("visible = (b.dataset.key + ' ' + b.textContent).toLowerCase().indexOf(q) !== -1;","visible = matchesChip(b) && (b.dataset.key + ' ' + b.textContent).toLowerCase().indexOf(q) !== -1;")
s=s.replace('aria-label="Search failure modes"','aria-label="Search behaviours and patterns"')
if 'id="research-entry-style"' not in s:
 s=s.replace('</head>','''<style id="research-entry-style">
.research-status{display:block;font-size:11px;color:var(--muted);margin-top:8px;line-height:1.5}.research-note{border-left:3px solid var(--accent);padding-left:12px}.human-sources li{margin-bottom:12px;overflow-wrap:anywhere}.concept .head{min-width:0}.concept .body{overflow-wrap:anywhere}.cat-controls{flex-wrap:wrap}.chips{flex-wrap:wrap}.cat-controls input{min-width:0;max-width:100%}.jump-nav{max-width:100%;overflow-x:auto}.meta dd{min-width:0;overflow-wrap:anywhere}
</style></head>''')
baseline='<p class="research-baseline-note"><strong>Research baseline:</strong> the paper and reported experiments below describe the original 207-entry catalogue. The newly integrated analogies were not included in those measurements.</p>'
if 'class="research-baseline-note"' not in s:
 s=s.replace('<section class="framework" id="paper">','<section class="framework" id="paper">\n    '+baseline)
s=s.replace('"dateModified": "2026-05-23"','"dateModified": "2026-11-06"')
s=s.replace('202 ways AI output goes wrong, each with a definition, an example, and the research behind it; most paralleled to human psychology, some AI-native.','434 behaviours and patterns, including explicitly labelled proposed human-behaviour analogies, with definitions, examples, sources and review status.')
p.write_text(s)

redirect='''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Behaviours are now in the main catalogue</title><link rel="canonical" href="https://ethicalai.alexandrudan.com/#catalogue"><meta name="robots" content="noindex"><script>const aliases={"candidate-018":"automation-complacency"};const h=location.hash.slice(1);location.replace('/#'+encodeURIComponent(aliases[h]||h||'catalogue'));</script><meta http-equiv="refresh" content="0;url=/#catalogue"></head><body><p>The research entries are now part of <a href="/#catalogue">the main catalogue</a>.</p></body></html>'''
for name in ['100-behaviours.html','behaviour-candidates.html']:(ROOT/'docs/research'/name).write_text(redirect+'\n')
sm=ROOT/'docs/sitemap.xml';t=sm.read_text()
t=re.sub(r'\s*<url>\s*<loc>https://ethicalai\.alexandrudan\.com/research/(?:100-behaviours|behaviour-candidates)\.html</loc>.*?</url>','',t,flags=re.S)
t=t.replace('<lastmod>2026-05-23</lastmod>','<lastmod>2026-11-06</lastmod>');sm.write_text(t)
print('One catalogue; old research URLs redirect to it; historical paper results remain scoped.')
