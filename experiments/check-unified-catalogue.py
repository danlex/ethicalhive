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
added=[m for m in onto['modes'] if m.get('research_candidate')]
assert len(added)==227
assert sum(m['source_check']=='pending-definition-source-check' for m in added)==99
assert sum(m['source_check']=='definition-source-consulted' for m in added)==128
assert all(m['tag']=='analogy' and not m['violates'] and not m['causes'] for m in added)
manifest=json.loads((ROOT/'references/catalogue-integration-2026-11-06.json').read_text())
assert len(manifest['decisions'])==228
assert len({m['num'] for m in onto['modes']})==434
export=json.loads((ROOT/'docs/behaviours.json').read_text())
assert export==onto
assert len(list(csv.DictReader((ROOT/'docs/behaviours.csv').open())))==434
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
            assert page.locator('.concept').count()==434
            assert page.locator('#principles .card').count()==6
            assert page.locator('#self-eval-language-discrepancy').count()==1
            assert page.locator('#mm .li.mode').count()==434
            page.locator('[data-filter="new"]').click()
            assert page.locator('.concept:visible').count()==227
            page.locator('[data-filter="pending"]').click()
            assert page.locator('.concept:visible').count()==99
            page.locator('#search').fill('encoding specificity')
            assert page.locator('.concept:visible').count()==0
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
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),page.evaluate('''() => [...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(0,8).map(e=>({tag:e.tagName,id:e.id,cls:e.className,right:e.getBoundingClientRect().right}))''')
            page.screenshot(path=f'/tmp/unified-catalogue-{width}.png')
            page.goto(base+'research/behaviour-candidates.html#upload-003',wait_until='domcontentloaded')
            page.wait_for_url('**/#upload-003')
            assert page.locator('#upload-003').get_attribute('open') is not None
            assert page.locator('#upload-003 .research-status').is_visible()
            assert not errors,errors
            page.close()
        page=browser.new_page(java_script_enabled=False,viewport={'width':390,'height':900})
        page.route('https://**/*',lambda r:r.abort())
        page.goto(base,wait_until='domcontentloaded')
        assert page.locator('.concept').count()==434
        page.locator('#upload-003 summary').click()
        assert page.locator('#upload-003 .human-sources').is_visible()
        browser.close()
    print('PASS: one 434-entry list; 227 added analogies; 99 pending sources; 228 research records reconciled; same exports; map, six principles, self-evaluation, mobile layout, filters, aliases, legacy redirects and no-JS reading')
finally:server.shutdown()
