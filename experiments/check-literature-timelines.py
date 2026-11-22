#!/usr/bin/env python3
"""Exercise annual-search completeness and inspect the actual catalogue widgets."""
import argparse
from collections import Counter
import csv
import functools
import hashlib
import http.server
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('timelines', ROOT/'experiments/literature-timelines.py')
collector = importlib.util.module_from_spec(spec); spec.loader.exec_module(collector)


def atom(total, rows=()):
    entries = ''.join('<entry><id>http://arxiv.org/abs/'+identity+'</id><published>'+date+
                      '</published><updated>2026-11-22T00:00:00Z</updated></entry>' for identity,date in rows)
    return ('<feed xmlns="http://www.w3.org/2005/Atom" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">'
            '<opensearch:totalResults>'+str(total)+'</opensearch:totalResults>'+entries+'</feed>').encode()


class Client:
    def __init__(self, responses): self.responses=iter(responses)
    def get(self, url):
        result=next(self.responses)
        if isinstance(result, Exception): raise result
        return result


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.mode={'id':'example','num':1,'name':'Example','literature_search':{
            'url':'https://export.arxiv.org/api/query?search_query=all%3Atest+AND+%28cat%3Acs.AI+OR+cat%3Acs.CL+OR+cat%3Acs.LG%29'}}
        self.directory=tempfile.TemporaryDirectory();self.addCleanup(self.directory.cleanup)
        self.cache=Path(self.directory.name)
    def collect(self, feeds, page_size=1000):
        return collector.collect(self.mode, Client(feeds), self.cache, 2026, page_size)
    def test_zero_is_a_complete_series(self):
        result=self.collect([atom(0)])
        self.assertEqual(result['status'],'complete');self.assertEqual(result['total'],0)
        self.assertEqual(sum(p['count'] for p in result['years']),0)
    def test_first_submission_year_not_revision_year(self):
        result=self.collect([atom(1,[('2001.00001v4','2020-01-01T00:00:00Z')])])
        years={p['year']:p['count'] for p in result['years']}
        self.assertEqual(years[2020],1);self.assertEqual(years[2026],0)
    def test_all_pages_are_required(self):
        result=self.collect([atom(3,[('2001.00001v1','2020-01-01T00:00:00Z'),('2401.00001v1','2024-01-01T00:00:00Z')]),
                             atom(3,[('2601.00001v1','2026-01-01T00:00:00Z')])],2)
        self.assertEqual(result['status'],'complete');self.assertEqual(len(result['pages']),2)
        self.assertEqual(sum(p['count'] for p in result['years']),3)
    def test_early_empty_page_is_not_zero(self):
        result=self.collect([atom(2,[('2001.00001v1','2020-01-01T00:00:00Z')]),atom(2)],1)
        self.assertEqual(result['status'],'partial');self.assertIsNone(result['years']);self.assertIsNone(result['total'])
    def test_duplicate_versions_are_not_double_counted(self):
        result=self.collect([atom(2,[('2001.00001v1','2020-01-01T00:00:00Z'),('2001.00001v2','2020-01-01T00:00:00Z')])])
        self.assertEqual(result['status'],'partial');self.assertIsNone(result['years'])
    def test_changing_total_is_not_presented_as_complete(self):
        result=self.collect([atom(2,[('2001.00001v1','2020-01-01T00:00:00Z')]),atom(3,[('2401.00001v1','2024-01-01T00:00:00Z')])],1)
        self.assertEqual(result['status'],'partial');self.assertIsNone(result['years'])
    def test_provider_failure_is_not_zero(self):
        result=self.collect([ValueError('Provider response missing')])
        self.assertEqual(result['status'],'unavailable');self.assertIsNone(result['total']);self.assertIsNone(result['years'])
    def test_missing_total_is_rejected(self):
        with self.assertRaises(ValueError): collector.parse_feed(b'<feed/>')
    def test_missing_publication_date_is_rejected(self):
        with self.assertRaises(ValueError): collector.parse_feed(atom(1,[('2001.00001v1','')]))
    def test_large_query_uses_reconciled_annual_totals(self):
        feeds=[atom(15000,[('2601.00001v1','2026-01-01T00:00:00Z')])]
        feeds += [atom(15000 if year==2026 else 0) for year in range(1991,2027)]
        result=self.collect(feeds)
        self.assertEqual(result['status'],'complete');self.assertEqual(result['years'][-1]['count'],15000)
        self.assertEqual(len(result['pages']),37)
    def test_annual_aggregate_mismatch_is_rejected(self):
        result=self.collect([atom(15000)]+[atom(0) for _ in range(36)])
        self.assertNotEqual(result['status'],'complete');self.assertIsNone(result['years'])
    def test_query_scope_is_required(self):
        self.mode['literature_search']['url']='https://export.arxiv.org/api/query?search_query=all%3Atest'
        with self.assertRaises(ValueError): collector.search_query(self.mode)
    def test_historical_zero_keeps_its_date_and_stops_at_that_year(self):
        self.mode['literature_search'].update(database='arXiv',status='available',count=0,queried_at='2025-10-03T12:00:00+00:00')
        result=collector.collect(self.mode,Client([]),self.cache,2026,reuse_zero=True)
        self.assertTrue(result['historical_zero_snapshot']);self.assertEqual(result['end_year'],2025)
        self.assertEqual(result['queried_at'],'2025-10-03T12:00:00+00:00')
        self.assertNotIn(2026,[p['year'] for p in result['years']])
    def test_nonzero_total_never_supplies_an_invented_distribution(self):
        self.mode['literature_search'].update(database='arXiv',status='available',count=3,queried_at='2025-10-03T12:00:00+00:00')
        self.assertIsNone(collector.historical_zero(self.mode,collector.search_query(self.mode)))
    def test_retry_after_is_respected_as_seconds_or_http_date(self):
        self.assertEqual(collector.retry_seconds('720',now=0),720)
        self.assertEqual(collector.retry_seconds('Thu, 01 Jan 1970 00:12:00 GMT',now=0),720)


def check_snapshot(require_complete=False):
    data=json.loads((ROOT/'docs/literature-timelines.json').read_text())
    modes=yaml.safe_load((ROOT/'ontology/ethical-ai.yaml').read_text())['modes']
    by_id={m['id']:m for m in modes}
    assert len(data['records'])==len(by_id)
    assert {r['id'] for r in data['records']}==set(by_id)
    for record in data['records']:
        assert record['query_hash']==collector.fingerprint(collector.search_query(by_id[record['id']]))
        if record['status']=='complete':
            assert [p['year'] for p in record['years']]==list(range(record['start_year'],record['end_year']+1))
            assert all(type(p['count']) is int and p['count']>=0 for p in record['years'])
            assert sum(p['count'] for p in record['years'])==record['total']
        else: assert record['years'] is None and record['total'] is None
    rows=list(csv.DictReader((ROOT/'docs/literature-timelines.csv').open()))
    for record in data['records']:
        subset=[r for r in rows if r['id']==record['id']]
        if record['status']=='complete': assert sum(int(r['matching_publications']) for r in subset)==record['total']
        else: assert len(subset)==1 and subset[0]['matching_publications']==''
    states=Counter(r['status'] for r in data['records'])
    if require_complete: assert states.get('complete')==len(modes),states
    print('PASS: stable IDs, exact queries, continuous annual series, totals and CSV reconcile;',dict(states))
    return data


def check_browser(data):
    from playwright.sync_api import sync_playwright
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args): pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT/'docs')))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base='http://127.0.0.1:'+str(server.server_port)+'/'
    positive=next(r for r in data['records'] if r['status']=='complete' and r['total']>1)
    zero=next(r for r in data['records'] if r['status']=='complete' and r['total']==0)
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            for width in (390,768,1440):
                page=browser.new_page(viewport={'width':width,'height':1000})
                page.route('https://**/*',lambda route:route.abort())
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                requests=[];page.on('request',lambda request:requests.append(request.url))
                page.goto(base,wait_until='domcontentloaded')
                assert not any('literature-timelines.json' in u for u in requests)
                widget=page.locator('[data-timeline-term="'+positive['id']+'"]')
                page.locator('details#'+positive['id']).evaluate('(node)=>node.open=true')
                widget.scroll_into_view_if_needed()
                page.wait_for_function('(id)=>document.querySelector("[data-timeline-term=\\""+id+"\\"]").dataset.timelineState==="ready"',arg=positive['id'])
                assert widget.locator('.timeline-bar').count()==len(positive['years'])
                assert widget.locator('.timeline-year-label').evaluate_all('''nodes=>nodes.every((node,i)=>
                    i===0 || nodes[i-1].getBoundingClientRect().right<node.getBoundingClientRect().left)''')
                widget.locator('.timeline-period').select_option('recent')
                assert widget.locator('.timeline-bar').count()==10
                widget.locator('.timeline-scale').select_option('log')
                widget.locator('.timeline-plot').focus();page.keyboard.press('End')
                assert str(positive['end_year']) in widget.locator('output').inner_text()
                assert 'partial year' in widget.locator('output').inner_text()
                widget.locator('.timeline-data summary').click()
                assert widget.locator('tbody tr').count()==10
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                if width==390:
                    widget.locator('.timeline-plot').evaluate('''node=>{
                        const bottom=Math.max(...['.topnav','.cat-controls','#jumpNav'].map(s=>document.querySelector(s).getBoundingClientRect().bottom));
                        window.scrollBy(0,node.getBoundingClientRect().top-bottom-70);
                    }''')
                    page.screenshot(path='/tmp/ethicalai-yearly-timeline-mobile.png')
                zero_widget=page.locator('[data-timeline-term="'+zero['id']+'"]')
                page.locator('details#'+zero['id']).evaluate('(node)=>node.open=true')
                zero_widget.scroll_into_view_if_needed()
                page.wait_for_function('(id)=>document.querySelector("[data-timeline-term=\\""+id+"\\"]").dataset.timelineState==="ready"',arg=zero['id'])
                assert 'No publications matched' in zero_widget.inner_text()
                assert len([u for u in requests if 'literature-timelines.json' in u])==1
                assert not errors,errors
                page.close()
            page=browser.new_page(viewport={'width':390,'height':900},java_script_enabled=False)
            page.goto(base,wait_until='domcontentloaded')
            assert page.locator('.concept').count()==len(data['records'])
            assert page.locator('.literature-timeline noscript').count()==len(data['records'])
            assert page.request.get(base+'literature-timelines.csv').ok
            page.close()
            # A failed data request is retryable and never creates zero-valued bars.
            page=browser.new_page(viewport={'width':390,'height':1000})
            page.route('**/literature-timelines.json',lambda route:route.fulfill(status=503,body='temporarily unavailable'))
            page.goto(base,wait_until='domcontentloaded')
            target=page.locator('[data-timeline-term="'+positive['id']+'"]')
            page.locator('details#'+positive['id']).evaluate('(node)=>node.open=true');target.scroll_into_view_if_needed()
            page.wait_for_function('(id)=>document.querySelector("[data-timeline-term=\\""+id+"\\"]").dataset.timelineState==="error"',arg=positive['id'])
            assert target.locator('.timeline-bar').count()==0
            page.unroute('**/literature-timelines.json')
            target.locator('.timeline-retry').focus();page.keyboard.press('Enter')
            page.wait_for_function('(id)=>document.querySelector("[data-timeline-term=\\""+id+"\\"]").dataset.timelineState==="ready"',arg=positive['id'])
            page.close()
            # Retrieved names and queries remain text, including hostile-looking data.
            payload=json.loads(json.dumps(data))
            item=next(r for r in payload['records'] if r['id']==positive['id'])
            item['name']='<img src=x onerror="window.timelineInjected=true">'
            item['query']='"><script>window.timelineInjected=true</script>'
            page=browser.new_page(viewport={'width':390,'height':1000})
            page.route('**/literature-timelines.json',lambda route:route.fulfill(content_type='application/json',body=json.dumps(payload)))
            page.goto(base,wait_until='domcontentloaded')
            target=page.locator('[data-timeline-term="'+positive['id']+'"]')
            page.locator('details#'+positive['id']).evaluate('(node)=>node.open=true');target.scroll_into_view_if_needed()
            page.wait_for_function('(id)=>document.querySelector("[data-timeline-term=\\""+id+"\\"]").dataset.timelineState==="ready"',arg=positive['id'])
            assert page.evaluate('window.timelineInjected===undefined')
            assert target.locator('img,script').count()==0
            page.close()
            # Partial coverage must not be rendered as a complete or zero series.
            item.update(status='partial',years=None,total=None)
            page=browser.new_page(viewport={'width':390,'height':1000})
            page.route('**/literature-timelines.json',lambda route:route.fulfill(content_type='application/json',body=json.dumps(payload)))
            page.goto(base,wait_until='domcontentloaded')
            target=page.locator('[data-timeline-term="'+positive['id']+'"]')
            page.locator('details#'+positive['id']).evaluate('(node)=>node.open=true');target.scroll_into_view_if_needed()
            page.wait_for_function('(id)=>document.querySelector("[data-timeline-term="+id+"]").dataset.timelineState==="unavailable"',arg=positive['id'])
            assert target.locator('.timeline-bar').count()==0
            assert 'Missing data is not shown as zero' in target.inner_text()
            page.close();browser.close()
    finally:server.shutdown()
    print('PASS: lazy single fetch, time/scale controls, keyboard values, partial-year marking, zero results, mobile/tablet/desktop and no-JS downloads.')


def check_live(base):
    for name in ('index.html','assets/literature-timelines.js','assets/literature-timelines.css','literature-timelines.json','literature-timelines.csv'):
        expected=(ROOT/'docs'/name).read_bytes()
        with urlopen(base.rstrip('/')+'/'+name+'?timeline='+hashlib.sha256(expected).hexdigest()[:16],timeout=45) as response:
            assert response.status==200
            assert hashlib.sha256(response.read()).digest()==hashlib.sha256(expected).digest(),name
    print('PASS: live HTML, chart assets and annual data match the tested files exactly over HTTPS.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser',action='store_true');parser.add_argument('--require-complete',action='store_true')
    parser.add_argument('--live')
    args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(CollectionTests))
    if not result.wasSuccessful():raise SystemExit(1)
    snapshot=check_snapshot(args.require_complete)
    if args.browser:check_browser(snapshot)
    if args.live:
        assert args.live.startswith('https://')
        check_live(args.live)
