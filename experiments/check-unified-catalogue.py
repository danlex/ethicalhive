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
assert len(export['modes'])==434 and export['meta']['mode_count']==434
assert export['meta']['source_record_count']==434
assert export['modes']==sorted(onto['modes'],key=lambda m:m['num'])
assert [m['num'] for m in export['modes']]==list(range(1,435))
rows=list(csv.DictReader((ROOT/'docs/behaviours.csv').open()))
assert len(rows)==434
assert [int(r['num']) for r in rows]==list(range(1,435))
assert {r['id']:r['grouped_under'] for r in rows if r['grouped_under']}==expected_groups
by_num={m['num']:m for m in onto['modes']}
category_order=list(dict.fromkeys(m['category'] for m in sorted(onto['modes'],key=lambda m:m['num'])))
expected_numbers=[str(m['num']) for c in category_order for m in sorted(onto['modes'],key=lambda m:m['num']) if m['category']==c]
for row in rows:
    mode=by_num[int(row['num'])]
    for field in ('synonyms','is_a','relates_to','related_terms','terminology_sources'):
        assert json.loads(row[field])==mode.get(field,[])
    assert row['concept_boundary']==mode.get('concept_boundary','')
# These concepts were wrongly treated as interchangeable in the old aliases.
for num,names in {65:['People-pleasing'],144:['Prospect theory','Risk aversion'],183:['Membership inference'],196:['Over-privileged tool use'],140:['Horn effect','Fluency bias'],145:['Diffusion of responsibility','Cognitive loafing'],420:['Pattern noise']}.items():
    assert not set(names)&set(by_num[num].get('synonyms',[]))
assert by_num[274]['synonyms']==['All-or-nothing thinking']
assert by_num[196]['id'] in by_num[204]['is_a']
assert by_num[69]['id'] in by_num[65]['is_a'] and by_num[69]['id'] in by_num[129]['is_a']
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
            assert page.locator('.concept-variant').count()==0
            # Research badges must not create another summary column from #208.
            assert page.locator('.concept > summary .research-status').count()==0
            assert page.locator('.concept > summary .pcount').count()==434
            assert page.locator('.concept[data-candidate="1"] > .body > .research-status').count()>=227
            layouts=page.locator('.concept > summary > .head').evaluate_all('''heads=>heads.map(h=>{
                const box=h.getBoundingClientRect(), cells=[...h.children];
                return {classes:cells.map(c=>c.matches('h2')?'name':c.className),
                    category:h.querySelector('.fam').getBoundingClientRect().left-box.left,
                    countEnd:h.querySelector('.pcount').getBoundingClientRect().right-box.left,
                    height:box.height};
            })''')
            assert all(row['classes'][:3]==['name','one','fam'] and row['classes'][3].startswith('pcount') and len(row['classes'])==4 for row in layouts)
            # Compare actual geometry across the old and added records, not only markup.
            baseline=layouts[expected_numbers.index('170')]
            for num in (208,209,315,434):
                row=layouts[expected_numbers.index(str(num))]
                assert abs(row['countEnd']-baseline['countEnd'])<1,(width,num,row,baseline)
                assert abs(row['height']-baseline['height'])<1,(width,num,row,baseline)
                if width>640:
                    assert abs(row['category']-baseline['category'])<1,(width,num,row,baseline)
            assert page.locator('.concept > summary .num').count()==0
            assert page.locator('.concept').evaluate_all('(els)=>els.map(e=>e.dataset.num)')==expected_numbers
            assert page.locator('.cat-group').count()==len(category_order)==11
            assert page.locator('.cat-group[data-range]').count()==0
            assert page.locator('.cat-group').evaluate_all('(els)=>els.map(e=>e.dataset.category)')==category_order
            groups=page.locator('.cat-grid').evaluate('''grid=>{
                const result=[];let group;
                for(const el of grid.children){
                    if(el.matches('.cat-group')){group={category:el.dataset.category,id:el.id,numbers:[]};result.push(group);}
                    if(el.matches('.concept'))group.numbers.push(Number(el.dataset.num));
                }return result;
            }''')
            for group in groups:
                assert group['numbers']==sorted(m['num'] for m in onto['modes'] if m['category']==group['category'])
            assert page.locator('#jumpNav a').all_text_contents()==[f'{category} ({len(group["numbers"])})' for category,group in zip(category_order,groups)]
            assert page.locator('#jumpNav').get_attribute('aria-label')=='Jump to ontology category'
            ids=page.locator('.concept').evaluate_all('(els)=>els.map(e=>e.id)')
            assert len(ids)==len(set(ids))==434
            assert page.locator('#principles .card').count()==6
            assert page.locator('#self-eval-language-discrepancy').count()==1
            assert page.locator('#mm .li.mode').count()==434
            # Category navigation is a real anchor and keeps the stable IDs.
            page.locator('#jumpNav a').last.click()
            assert page.url.endswith('#grp-ai-native-behaviours')
            for num in (144,183):
                mode=by_num[num]
                entry=page.locator('#'+mode['id'])
                entry.locator('summary').click()
                assert 'Related terms · not synonyms' in entry.inner_text()
                if num==144:
                    assert 'Also known as' not in entry.inner_text()
                assert entry.locator('.body a[href="'+mode['terminology_sources'][0]['url']+'"]').count()==1
            tool=page.locator('#tool-selection-error')
            tool.locator('summary').click()
            assert tool.locator('.body a[href="#tool-over-privilege"]').count()>=1
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
            assert page.locator('#upload-009').get_attribute('data-overlap')=='overpromise-underdeliver'
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
            page.locator('#mm .mm-q').fill('Loss aversion')
            page.locator('#mm [data-mid="loss-aversion"] > .row .pill').click()
            term_panel=page.locator('#mm .mm-detail').inner_text()
            assert 'related terms · not synonyms' in term_panel.lower() and 'Prospect theory' in term_panel,term_panel
            assert 'also known as' not in term_panel.lower()
            page.locator('#mm .mm-q').fill('')
            page.locator('#mm .mm-q').fill('Omnipotent control')
            page.locator('#mm [data-mid="overpromise-underdeliver"] > .row .pill').click()
            assert 'linked overlap descriptions' in page.locator('#mm .mm-detail').inner_text().lower()
            assert page.locator('#mm .mm-detail a[href="./#upload-009"]').count()==1
            assert page.locator('#mm [data-mid="upload-009"]').count()==1
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
            page.locator('#upload-009 .body a[href="#overpromise-underdeliver"]').first.click()
            assert page.locator('#overpromise-underdeliver').get_attribute('open') is not None
            assert not errors,errors
            page.close()
        page=browser.new_page(java_script_enabled=False,viewport={'width':390,'height':900})
        page.route('https://**/*',lambda r:r.abort())
        page.goto(base,wait_until='domcontentloaded')
        assert page.locator('.concept').count()==434
        assert page.locator('.concept > summary .num').count()==0
        assert page.locator('.cat-group').count()==11
        page.locator('#upload-003 summary').click()
        assert page.locator('#upload-003 .human-sources').is_visible()
        page.locator('#upload-009 > summary').click()
        assert page.locator('#upload-009 .human-sources').is_visible()
        browser.close()
    print('PASS: 434 stable references in 11 ontology categories, corrected terminology and subtypes, ordered JSON/CSV, overlap links, map, filters, mobile and no-JS reading')
finally:server.shutdown()
