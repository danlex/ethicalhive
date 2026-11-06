#!/usr/bin/env python3
"""Check reconciliation, exports, controls, internal links and accessible static rendering."""
import csv
import functools
import http.server
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright
import yaml

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'docs/research/behaviour-candidates.json').read_text())
entries=data['entries']
counts=data['counts']
rows=list(csv.DictReader((ROOT/'docs/research/behaviour-candidates.csv').open()))
assert len(rows)==len(entries)==228
assert [r['id'] for r in rows]==[e['id'] for e in entries]
assert len(data['merged_overlaps'])==17
assert sorted(c['upload_row'] for e in entries for c in e['contributions'])==list(range(1,146))
assert sum('attachment' in e['origins'] for e in entries)==145
assert sum('earlier-research' in e['origins'] for e in entries)==100
assert counts['definition_source_consulted']+counts['pending_definition_source_check']==228
ontology=yaml.safe_load((ROOT/'ontology/ethical-ai.yaml').read_text())
mode_ids={m['id'] for m in ontology['modes']}
assert len(mode_ids)==207
assert all(m['id'] in mode_ids for e in entries for m in e['related_modes'])
assert all(e['ai_status']=='PROPOSED ANALOGY; NOT TESTED IN THIS RESEARCH' for e in entries)
assert next(e for e in entries if e['id']=='upload-003')['name']=='Displacement'
assert 'feigning' not in next(e for e in entries if e['id']=='upload-139')['definition']
assert next(e for e in entries if e['id']=='upload-056')['source_check']=='pending-definition-source-check'
assert next(e for e in entries if e['id']=='upload-061')['source_check']=='pending-definition-source-check'

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):
        pass

server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT/'docs')))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/research/behaviour-candidates.html'
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        for width in (320,390,768,1440):
            page=browser.new_page(viewport={'width':width,'height':1000})
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            assert page.goto(url).status==200
            assert page.locator('article').count()==228
            assert page.locator('h1').count()==1
            ids=page.locator('[id]').evaluate_all('(es)=>es.map(e=>e.id)')
            assert len(ids)==len(set(ids))
            for href in page.locator('a[href^="#"]').evaluate_all('(es)=>es.map(e=>e.getAttribute("href"))'):
                assert href[1:] in ids,href
            page.locator('#origin').select_option('attachment')
            assert page.locator('article:visible').count()==145
            page.locator('#origin').select_option('earlier-research')
            assert page.locator('article:visible').count()==100
            page.locator('#reset').click()
            page.locator('#review').select_option('pending-definition-source-check')
            assert page.locator('article:visible').count()==counts['pending_definition_source_check']
            page.locator('#reset').click()
            page.locator('#q').fill('all-or-nothing')
            assert page.locator('#candidate-068').is_visible()
            page.locator('#reset').click()
            page.locator('#q').fill('not-a-matching-behaviour-zzzz')
            assert page.locator('article:visible').count()==0
            assert page.locator('#empty').is_visible()
            page.locator('#reset').click()
            page.locator('#q').fill('normalization of deviance')
            page.locator('#upload-054 summary').click()
            assert page.locator('#upload-054 details').get_attribute('open') is not None
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
            page.locator('#reset').click()
            page.locator('#field').select_option('Transactional analysis games')
            assert page.locator('article:visible').count()==6
            assert not errors,errors
            page.locator('#reset').click()
            page.evaluate('scrollTo(0,0)')
            for theme in ('light','dark'):
                page.emulate_media(color_scheme=theme)
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,theme)
                page.screenshot(path=f'/tmp/candidates-{width}-{theme}.png')
            page.close()
        context=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':900})
        page=context.new_page()
        page.goto(url)
        assert page.locator('article:visible').count()==228
        page.locator('#upload-003 summary').click()
        assert page.locator('#upload-003 details').get_attribute('open') is not None
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        browser.close()
    print('PASS: 228 entries; 145 contributions; 17 merges; valid catalogue relations; consistent exports; four viewport sizes; light/dark, filters, aliases, details and no-JS reading')
finally:
    server.shutdown()
