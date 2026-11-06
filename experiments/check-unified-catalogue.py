#!/usr/bin/env python3
"""Validate the expanded catalogue and legacy-link migration in the actual homepage."""
import csv
import functools
import http.server
import json
import threading
from pathlib import Path
import yaml
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
onto=yaml.safe_load((ROOT/'ontology/ethical-ai.yaml').read_text())
assert len(onto['modes'])==434
primary=[m for m in onto['modes'] if not m.get('grouped_under')]
grouped=[m for m in onto['modes'] if m.get('grouped_under')]
assert len(primary)==425 and len(grouped)==9
expected_groups={'social-desirability-bias':'b069-social-desirability-people-pleasing','clarification-avoidance':'x107-silent-assumption-gap','escalation-of-commitment':'b038-sunk-cost-fallacy','upload-009':'overpromise-underdeliver','upload-136':'b025-cognitive-tunneling','upload-137':'perseveration','upload-125':'b058-einstellung-mental-set','upload-124':'self-serving-bias','upload-140':'laziness'}
assert {m['id']:m['grouped_under'] for m in grouped}==expected_groups
added=[m for m in onto['modes'] if m.get('research_candidate')]
assert len(added)==227
assert sum(m['source_check']=='pending-definition-source-check' for m in added)==99
assert sum(m['source_check']=='definition-source-consulted' for m in added)==128
assert all(m['tag']=='analogy' and not m['violates'] and not m['causes'] for m in added)
manifest=json.loads((ROOT/'references/catalogue-integration-2026-11-06.json').read_text())
assert len(manifest['decisions'])==228
assert len({m['num'] for m in onto['modes']})==434
export=json.loads((ROOT/'docs/behaviours.json').read_text())
assert len(export['modes'])==425 and export['meta']['mode_count']==425
assert export['meta']['source_record_count']==434
assert {m['id'] for m in export['modes']}=={m['id'] for m in primary}
flat=[]
for m in export['modes']:
    item=dict(m);flat.extend(item.pop('grouped_variants'));flat.append(item)
assert {m['id']:m for m in flat}=={m['id']:m for m in onto['modes']}
rows=list(csv.DictReader((ROOT/'docs/behaviours.csv').open()))
assert len(rows)==425
assert sorted(v['id'] for r in rows for v in json.loads(r['grouped_variants_json'] or '[]'))==sorted(expected_groups)
for suffix in ('json','csv'):
    for stem in ('100-behaviours','behaviour-candidates'):
        assert (ROOT/f'docs/research/{stem}.{suffix}').read_bytes()==(ROOT/f'docs/behaviours.{suffix}').read_bytes()

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT/'docs')))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        for width in (390,768,1440):
            page=browser.new_page(viewport={'width':width,'height':1000})
            page.route('https://**/*',lambda r:r.abort())
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(base,wait_until='domcontentloaded')
            assert page.locator('.concept').count()==425
            assert page.locator('.concept-variant').count()==9
            assert page.locator('#principles .card').count()==6
            assert page.locator('#self-eval-language-discrepancy').count()==1
            assert page.locator('#mm .li.mode').count()==425
            page.locator('[data-filter="new"]').click()
            assert page.locator('.concept:visible').count()==227
            page.locator('[data-filter="pending"]').click()
            assert page.locator('.concept:visible').count()==99
            page.locator('#search').fill('encoding specificity')
            assert page.locator('.concept:visible').count()==0
            page.locator('[data-filter="all"]').click()
            page.locator('#search').fill('Omnipotent control')
            assert page.locator('#overpromise-underdeliver').is_visible()
            assert page.locator('#upload-009').is_visible()
            assert page.locator('#upload-009').get_attribute('open') is not None
            assert page.locator('#upload-009').evaluate('(e)=>e.closest(".concept").id')=='overpromise-underdeliver'
            page.locator('[data-filter="all"]').click()
            page.locator('#search').fill('all-or-nothing')
            assert page.locator('#candidate-068').is_visible()
            page.locator('[data-filter="all"]').click()
            page.locator('#search').fill('vigilance decrement')
            assert page.locator('#automation-complacency').is_visible()
            assert page.locator('#candidate-018').count()==0
            page.locator('[data-filter="all"]').click()
            page.locator('#mm .mm-q').fill('Displacement')
            page.locator('#mm [data-mid="upload-003"] > .row .pill').click()
            panel=page.locator('#mm .mm-detail').inner_text()
            assert 'Untested AI analogy' in panel
            assert 'violates ?' not in panel
            page.locator('#mm .mm-q').fill('')
            page.locator('#mm .mm-q').fill('Omnipotent control')
            page.locator('#mm [data-mid="overpromise-underdeliver"] > .row .pill').click()
            assert 'grouped overlap variants' in page.locator('#mm .mm-detail').inner_text().lower()
            assert page.locator('#mm .mm-detail a[href="./#upload-009"]').count()==1
            assert page.locator('#mm [data-mid="upload-009"]').count()==0
            page.locator('#mm .mm-q').fill('')
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),page.evaluate('''() => [...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(0,8).map(e=>({tag:e.tagName,id:e.id,cls:e.className,right:e.getBoundingClientRect().right}))''')
            page.screenshot(path=f'/tmp/unified-catalogue-{width}.png')
            page.goto(base+'research/behaviour-candidates.html#upload-003',wait_until='domcontentloaded')
            page.wait_for_url('**/#upload-003')
            assert page.locator('#upload-003').get_attribute('open') is not None
            assert page.locator('#upload-003 .research-status').is_visible()
            page.goto(base+'research/behaviour-candidates.html#upload-009',wait_until='domcontentloaded')
            page.wait_for_url('**/#upload-009')
            assert page.locator('#upload-009').get_attribute('open') is not None
            assert page.locator('#overpromise-underdeliver').get_attribute('open') is not None
            assert not errors,errors
            page.close()
        page=browser.new_page(java_script_enabled=False,viewport={'width':390,'height':900})
        page.route('https://**/*',lambda r:r.abort())
        page.goto(base,wait_until='domcontentloaded')
        assert page.locator('.concept').count()==425
        page.locator('#upload-003 summary').click()
        assert page.locator('#upload-003 .human-sources').is_visible()
        page.locator('#overpromise-underdeliver > summary').click()
        page.locator('#upload-009 > summary').click()
        assert page.locator('#upload-009 .human-sources').is_visible()
        browser.close()
    print('PASS: 425 primary entries, 9 nested overlaps, all 434 source records and anchors retained; grouped exports; distinct trigger variants preserved; map, filters, links and no-JS reading')
finally:server.shutdown()
