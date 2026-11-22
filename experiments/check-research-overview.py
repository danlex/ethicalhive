#!/usr/bin/env python3
"""Check combined timeline arithmetic, comparisons and missing-data behaviour in the browser."""
import argparse
import functools
import http.server
import json
from pathlib import Path
import subprocess
import threading

from literature_timeline_ui import overview_placeholder

ROOT=Path(__file__).resolve().parents[1]


def check(baseline=None):
    from playwright.sync_api import sync_playwright
    data=json.loads((ROOT/'docs/literature-timelines.json').read_text())
    complete=[r for r in data['records'] if r['status']=='complete']
    positive=next(r for r in complete if r['total']>1)
    zero=next(r for r in complete if r['total']==0)
    end=data['end_year']
    total=sum(p['count'] for r in complete for p in r['years'] if p['year']==end)
    home=(ROOT/'docs/index.html').read_text()
    if baseline:
        previous=subprocess.check_output(['git','show',baseline+':docs/index.html'],cwd=ROOT,text=True)
        assert home.replace('    '+overview_placeholder()+'\n','')==previous,'Unrelated homepage content changed'
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT/'docs')))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    url='http://127.0.0.1:'+str(server.server_port)+'/'
    def ready(page):
        page.locator('#research-timeline').scroll_into_view_if_needed()
        page.wait_for_function('document.getElementById("research-timeline").dataset.overviewState==="ready"')
        return page.locator('#research-timeline')
    def clear_and_add(widget,record):
        widget.locator('.overview-mode').select_option('compare')
        while widget.locator('.overview-chip').count():widget.locator('.overview-chip').first.click()
        widget.locator('.overview-search').fill(record['name'])
        widget.locator('.overview-available').select_option(record['id'])
        widget.locator('.overview-add').click()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            for width in (390,768,1440):
                page=browser.new_page(viewport={'width':width,'height':1100})
                page.route('https://**/*',lambda route:route.abort())
                errors=[];requests=[]
                page.on('pageerror',lambda error:errors.append(str(error)))
                page.on('request',lambda request:requests.append(request.url))
                page.goto(url,wait_until='domcontentloaded')
                assert not any('literature-timelines.json' in u for u in requests)
                widget=ready(page)
                assert 'paper matching several searches is counted in each' in widget.inner_text()
                assert widget.locator('.timeline-bar').count()==end-data['start_year']+1
                assert f'{total:,} paper–term matches' in widget.locator('.overview-readout').inner_text()
                assert widget.locator('.timeline-year-label').evaluate_all('''nodes=>nodes.every((n,i)=>
                    i===0 || nodes[i-1].getBoundingClientRect().right<n.getBoundingClientRect().left)''')
                widget.locator('.overview-period').select_option('recent')
                assert widget.locator('.timeline-bar').count()==10
                widget.locator('.overview-scale').select_option('log')
                widget.locator('.overview-plot').focus();page.keyboard.press('Home')
                assert str(end-9) in widget.locator('.overview-readout').inner_text()
                page.keyboard.press('End')
                assert 'partial year' in widget.locator('.overview-readout').inner_text()
                widget.locator('.overview-data summary').click()
                latest=widget.locator('tbody tr').first.locator('td').all_text_contents()
                assert latest==[str(end)+'*',f'{total:,}',str(len(complete))]
                if width==1440:
                    widget.screenshot(path='/tmp/ethicalai-research-overview-desktop.png')
                widget.locator('.overview-mode').select_option('compare')
                assert widget.locator('.overview-line').count()==5
                assert widget.locator('.overview-available option').count()+widget.locator('.overview-chip').count()==len(complete)
                widget.locator('.overview-add').click()
                assert widget.locator('.overview-chip').count()==6 and widget.locator('.overview-add').is_disabled()
                clear_and_add(widget,positive)
                assert widget.locator('.overview-line').count()==1
                assert widget.locator('tbody tr').first.locator('td').nth(1).inner_text()==f"{positive['years'][-1]['count']:,}"
                widget.locator('.overview-search').fill(zero['name'])
                widget.locator('.overview-available').select_option(zero['id']);widget.locator('.overview-add').click()
                assert widget.locator('.overview-line').count()==2
                assert widget.locator('tbody tr').first.locator('td').nth(2).inner_text()=='0'
                assert widget.locator('.overview-values a').first.get_attribute('target') is None
                widget.locator('.overview-search').fill('no such term abcxyz')
                assert widget.locator('.overview-add').is_disabled()
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),page.evaluate('''Array.from(document.querySelectorAll('*')).filter(n=>{
                    const r=n.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+1||r.left<-1);
                }).slice(0,12).map(n=>({tag:n.tagName,cls:n.className,width:n.getBoundingClientRect().width,right:n.getBoundingClientRect().right}))''')
                if width==390:
                    widget.locator('.overview-mode').select_option('combined')
                    page.add_style_tag(content='html{scroll-behavior:auto!important}')
                    widget.scroll_into_view_if_needed()
                    widget.screenshot(path='/tmp/ethicalai-research-overview-mobile.png')
                # The overview and an existing detail share one data request.
                page.locator('details#'+positive['id']).evaluate('(node)=>node.open=true')
                page.locator('[data-timeline-term="'+positive['id']+'"]').scroll_into_view_if_needed()
                page.wait_for_function('(id)=>document.querySelector("[data-timeline-term="+id+"]").dataset.timelineState==="ready"',arg=positive['id'])
                assert len([u for u in requests if 'literature-timelines.json' in u])==1
                assert not errors,errors
                page.close()
            # Older complete snapshots have unknown future years, not zeroes.
            payload=json.loads(json.dumps(data))
            item=next(r for r in payload['records'] if r['id']==positive['id'])
            item['end_year']=end-1;item['years']=item['years'][:-1]
            item['total']=sum(p['count'] for p in item['years']);item['queried_at']=str(end-1)+'-11-09T00:00:00Z'
            page=browser.new_page()
            page.route('**/literature-timelines.json',lambda route:route.fulfill(content_type='application/json',body=json.dumps(payload)))
            page.goto(url,wait_until='domcontentloaded');widget=ready(page)
            clear_and_add(widget,item);widget.locator('.overview-plot').focus();page.keyboard.press('End')
            assert 'unavailable' in widget.locator('.overview-values').inner_text()
            widget.locator('.overview-data summary').click()
            assert widget.locator('tbody tr').first.locator('td').nth(1).inner_text()=='unavailable'
            page.close()
            # A source failure can be retried; it never creates a zero chart.
            page=browser.new_page()
            page.route('**/literature-timelines.json',lambda route:route.fulfill(status=503,body='unavailable'))
            page.goto(url,wait_until='domcontentloaded');page.locator('#research-timeline').scroll_into_view_if_needed()
            page.wait_for_function('document.getElementById("research-timeline").dataset.overviewState==="error"')
            assert page.locator('#research-timeline .timeline-bar').count()==0
            page.unroute('**/literature-timelines.json');page.locator('#research-timeline .timeline-retry').click();ready(page)
            page.close()
            # No valid series: show unavailability, never an empty zero total.
            for record in payload['records']:record.update(status='partial',years=None,total=None)
            page=browser.new_page()
            page.route('**/literature-timelines.json',lambda route:route.fulfill(content_type='application/json',body=json.dumps(payload)))
            page.goto(url,wait_until='domcontentloaded');page.locator('#research-timeline').scroll_into_view_if_needed()
            page.wait_for_function('document.getElementById("research-timeline").dataset.overviewState==="unavailable"')
            assert page.locator('#research-timeline .timeline-bar').count()==0
            page.close();browser.close()
    finally:server.shutdown()
    print('PASS: combined arithmetic, all-term coverage, comparison/search/removal, year/log controls, zero versus missing, retry, shared lazy loading and responsive charts.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--baseline')
    check(parser.parse_args().baseline)
