#!/usr/bin/env python3
"""Check coverage truthfulness, citation traceability and the rendered paper filter."""
import csv
from datetime import date
import functools
import http.server
import json
import threading
from pathlib import Path

import yaml
from playwright.sync_api import sync_playwright
from catalogue_sources import definition_sources, research_papers, source_coverage

ROOT=Path(__file__).resolve().parents[1]
onto=yaml.safe_load((ROOT/'ontology/ethical-ai.yaml').read_text())
by_num={m['num']:m for m in onto['modes']}
coverage=json.loads((ROOT/'docs/source-coverage.json').read_text())
expected=[source_coverage(by_num[n]) for n in sorted(by_num)]
assert coverage['records']==expected and len(expected)==434
assert len({m['category'] for m in onto['modes']})==11
assert [r['num'] for r in expected]==list(range(1,435))
assert coverage['counts']['entries_with_ai_papers']==sum(bool(r['ai_paper_links']) for r in expected)
assert coverage['counts']['entries_with_human_related_papers']==sum(bool(r['human_related_paper_links']) for r in expected)
gaps=[r for r in expected if not r['ai_paper_links'] and not r['human_related_paper_links']]
assert coverage['counts']['entries_without_research_papers']==len(gaps)
assert all(r['coverage_status'] in ('reference-sources-only','supplied-attributions-only','no-linked-source') for r in gaps)
for row in csv.DictReader((ROOT/'docs/behaviours.csv').open()):
    assert json.loads(row['research_papers'])==research_papers(by_num[int(row['num'])])
rows=list(csv.DictReader((ROOT/'docs/source-coverage.csv').open()))
assert len(rows)==434
for row,record in zip(rows,expected):
    for key in ('ai_paper_links','human_related_paper_links','reference_source_links'):
        assert int(row[key])==record[key]
    assert row['coverage_status']==record['coverage_status']
for mode in onto['modes']:
    for source in research_papers(mode):
        p=source['publication']
        assert p['authors'] and 1800<int(p['year'])<=2026 and p['venue']
        assert source['url'].startswith('https://') and p['verification_url'].startswith('https://')
        assert p['evidence_scope'] and source['consulted']
        assert date.fromisoformat(p['verified_date'])<=date.fromisoformat(onto['meta']['updated'])
    if mode.get('research_candidate'):
        assert mode['ai_evidence_status']=='Proposed analogy; not tested in this research'

# DOI presence alone must never turn a book chapter or reference page into a paper.
book={'id':'book','num':1,'name':'Book test','definition_sources':[
    {'id':'book-source','url':'https://doi.org/10.example/book','title':'A chapter','consulted':'Metadata only',
     'publication':{'type':'book-chapter'}}]}
assert research_papers(book)==[] and source_coverage(book)['coverage_status']=='reference-sources-only'
assert not any(s.get('publication') for s in by_num[238]['definition_sources'] if s['id']=='zero')
assert any(s.get('publication',{}).get('doi')=='10.1027/2151-2604/a000284' for s in by_num[238]['definition_sources'])
assert not any(s.get('publication') for s in by_num[256]['definition_sources'] if s['id']=='reciprocity')
# Preserve contrary evidence and limitations, rather than just counting citations.
assert any('2026.102886' in s['publication'].get('doi','') for s in research_papers(by_num[260]))
assert any('challenges' in s['publication']['evidence_scope'] for s in research_papers(by_num[251]))
assert all('2026.102886' not in s['publication'].get('doi','') or 'Contrary' in s['publication']['evidence_scope']
           for s in research_papers(by_num[260]))

reviews=[]
review_path=onto['meta']['paper_source_review']['record']
visited=set()
while review_path:
    assert review_path.startswith('references/') and '..' not in Path(review_path).parts
    assert review_path not in visited, 'Source-review history must not cycle'
    visited.add(review_path)
    review=json.loads((ROOT/review_path).read_text())
    reviews.append(review)
    review_path=review.get('previous_review')
assert len(reviews)==2
assert onto['meta']['paper_source_review']['previous_record']=='references/paper-source-review-2026-11-08.json'
# The latest reviewed version wins if a later pass revises a source.
sources={}
for review in reversed(reviews):
    for r in review['records']:
        source=r['current_source']
        sources[(r['num'],source['id'],source['url'])]=source
for (num,source_id,url),source in sources.items():
    matches=[s for s in definition_sources(by_num[num]) if s['id']==source_id and s['url']==url]
    assert matches==[source],(num,source_id)
assert set(sources)=={(m['num'],s['id'],s['url']) for m in onto['modes'] for s in research_papers(m)}
audit=reviews[-1]  # The earlier publication remains traceable and unchanged.
for repair in audit['ai_paper_repairs']:
    assert by_num[repair['num']]['arxiv']['papers']==repair['papers']
    assert by_num[repair['num']]['arxiv']['count'] is None
assert {r['num'] for r in audit['ai_paper_repairs']}=={4,22,67,70,75,86,103}
followup=reviews[0]
assert len(followup['decisions'])==64
assert {r['num'] for r in followup['decisions']}==set(followup['baseline']['paper_gap_numbers'])
assert {r['num'] for r in followup['decisions'] if r['decision']=='paper-gap-retained'}=={r['num'] for r in gaps}
assert followup['result']['entries_without_paper_links']==len(gaps)
assert followup['result']['entries_with_paper_links']==434-len(gaps)
for r in followup['reference_source_additions']:
    assert r['current_source'] in by_num[r['num']]['definition_sources']
    assert not r['current_source'].get('publication')
for r in followup['ai_paper_additions']:
    assert by_num[r['num']]['arxiv']['papers']==r['papers']
    assert by_num[r['num']]['arxiv']['count'] is None
    assert r['taxonomy_label'] and r['passage_locator']
    assert all(p['id']=='2311.07954' and 'recognition' in p['relevance'] for p in r['papers'])
assert {r['num'] for r in followup['ai_paper_additions']}=={346,363,374,375,377,378,413,421}
for r in followup['source_check_changes']:
    assert r['previous_status']=='pending-definition-source-check'
    assert by_num[r['num']]['source_check']==r['current_status']=='definition-source-consulted'
    assert r['passage_locator'] and r['reason']
    assert any(s['id']==r['source_id'] and s['consulted'] for s in by_num[r['num']]['definition_sources'])
# Theoretical and historical papers must preserve their limitations/contrary evidence.
assert 'Critical review' in research_papers(by_num[403])[-1]['publication']['evidence_scope']
assert 'challenging' in research_papers(by_num[362])[-1]['publication']['evidence_scope']
assert by_num[392]['source_check']=='pending-definition-source-check'
assert all(not research_papers(by_num[n]) for n in (411,415,416,417,425,426))
assert by_num[375]['ai_evidence_status']=='Proposed analogy; not tested in this research'

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
            assert page.locator('.source-scope').count()==1
            rendered={r['id']:r for r in page.locator('.concept').evaluate_all('''entries=>entries.map(e=>({
                id:e.id,paperCount:e.querySelectorAll('.human-papers > li').length,paperFlag:e.dataset.papers,
                displayedCount:e.querySelector('summary .pcount').textContent
            }))''')}
            for mode in onto['modes']:
                entry=rendered[mode['id']]
                sources=research_papers(mode)
                assert entry['paperCount']==len(sources)
                assert entry['paperFlag']==('1' if sources or (mode.get('arxiv') or {}).get('papers') else '0')
                cited=len(sources)+len((mode.get('arxiv') or {}).get('papers') or [])
                assert entry['displayedCount']==(str(cited) if cited else '—')
            page.locator('[data-filter="paper"]').click()
            assert page.locator('.concept:visible').count()==434-len(gaps)
            assert not page.locator('#'+by_num[415]['id']).is_visible()  # A consulted book chapter alone is not a paper.
            assert page.locator('#'+by_num[238]['id']).is_visible()  # A separate genuine journal paper is now linked.
            assert page.locator('#'+by_num[373]['id']).is_visible()  # A philosophical journal article is a paper.
            page.locator('[data-filter="no-paper"]').click()
            assert page.locator('.concept:visible').count()==len(gaps)
            assert page.locator('#'+by_num[415]['id']).is_visible()
            assert not page.locator('#'+by_num[238]['id']).is_visible()
            assert not page.locator('#'+by_num[373]['id']).is_visible()
            page.locator('[data-filter="all"]').click()
            page.locator('#search').fill('Inattentional blindness')
            entry=page.locator('#b022-inattentional-blindness')
            if entry.get_attribute('open') is None:
                entry.locator('summary').click()
            assert entry.locator('.papers a').count()==1 and entry.locator('.human-papers a').count()==1
            text=entry.inner_text().lower()
            assert 'mixrea' in text and 'gorillas in our midst' in text
            assert entry.locator('summary .num').count()==0
            page.locator('#search').fill('Kettle logic')
            entry=page.locator('#'+by_num[346]['id'])
            if entry.get_attribute('open') is None:
                entry.locator('summary').click()
            assert entry.locator('.papers a').count()==1 and entry.locator('.human-papers a').count()==1
            assert 'recognition/self-verification' in entry.inner_text()
            assert entry.locator('summary .pcount').inner_text()=='2'
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            if width==390:page.screenshot(path='/tmp/ethicalai-paper-coverage-mobile.png')
            page.locator('#search').fill('')
            page.locator('#mm .mm-q').fill('Encoding specificity')
            page.locator('#mm [data-mid="candidate-001"] > .row .pill').click()
            panel=page.locator('#mm .mm-detail')
            assert 'human and related research' in panel.inner_text().lower()
            assert panel.locator('a[href="https://doi.org/10.1037/h0020071"]').count()==1
            page.goto(base+'experiments/paper-index.html',wait_until='domcontentloaded')
            assert 'Human/related' in page.locator('body').inner_text()
            assert 'does not by itself establish co-occurrence' in page.locator('body').inner_text()
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            assert not errors,errors
            page.close()
        page=browser.new_page(java_script_enabled=False,viewport={'width':390,'height':900})
        page.route('https://**/*',lambda r:r.abort())
        page.goto(base,wait_until='domcontentloaded')
        entry=page.locator('#candidate-001')
        entry.locator('summary').click()
        assert entry.locator('.human-papers a').is_visible()
        assert 'Encoding specificity and retrieval processes' in entry.inner_text()
        browser.close()
    print(f'PASS: 434 coverage records; {434-len(gaps)} entries with paper links; {len(gaps)} explicit gaps; typed sources, audit trace, filters, map-ready metadata, index, CSV and no-JS reading.')
finally:
    server.shutdown()
