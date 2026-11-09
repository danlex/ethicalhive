#!/usr/bin/env python3
"""Verify manuscript tables, derived PDFs/LaTeX and the public paper page."""
import argparse
from collections import Counter
import functools
import hashlib
from html.parser import HTMLParser
import http.server
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import threading
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, urlopen

import yaml

from research_runs import ROOT


def manuscript(path):
    text=path.read_text()
    assert text.startswith('---\n'),path
    _,header,body=text.split('---\n',2)
    return yaml.safe_load(header),body


def tables(body):
    groups=[];current=[]
    for line in body.splitlines()+['']:
        if line.startswith('|'):
            row=[c.strip().replace('`','') for c in line.strip('|').split('|')]
            if not all(re.fullmatch(r'[:\- ]*',c) for c in row):current.append(row)
        elif current:groups.append(current);current=[]
    return groups


def fraction(a,b):return f'{a}/{b}' if b else 'n/a'


class PageLinks(HTMLParser):
    def __init__(self,path):
        super().__init__();self.ids=[];self.links=[];self.feed(path.read_text())

    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        self.links.extend(attrs[k] for k in ('href','src') if attrs.get(k))


def check_links():
    root=ROOT/'docs';assets=set()
    for name in ('index.html','paper.html','ontology-map.html','404.html'):
        path=root/name;page=PageLinks(path);assets.add(path)
        assert not [key for key,n in Counter(page.ids).items() if n>1],name
        for link in page.links:
            u=urlsplit(link)
            if u.scheme or u.netloc:continue
            target=(root/unquote(u.path).lstrip('/')) if u.path.startswith('/') else (path.parent/unquote(u.path) if u.path else path)
            if target.is_dir():target=target/'index.html'
            target=target.resolve();target.relative_to(root)
            assert target.is_file(),(name,link)
            assets.add(target)
            if u.fragment and target.suffix=='.html':
                ids=page.ids if target==path else PageLinks(target).ids
                assert unquote(u.fragment) in ids,(name,link)
    print(f'PASS: {len(assets)} internal page/asset targets and local fragments resolve without duplicate HTML IDs.')
    return assets


def check_live(base,assets):
    assert urlsplit(base).scheme=='https','Live verification requires HTTPS'
    revision=hashlib.sha256((ROOT/'docs/index.html').read_bytes()).hexdigest()[:16]
    for path in sorted(assets):
        name=path.relative_to(ROOT/'docs').as_posix()
        url=urljoin(base.rstrip('/')+'/',name)+'?paper-revision='+revision
        request=Request(url,headers={'User-Agent':'EthicalAI-paper-verification/1.0','Cache-Control':'no-cache'})
        with urlopen(request,timeout=45) as response:
            assert response.status==200,(name,response.status)
            assert hashlib.sha256(response.read()).digest()==hashlib.sha256(path.read_bytes()).digest(),name
    print(f'PASS: all {len(assets)} live HTTPS page/asset bodies match the tested publication files exactly.')


def check_sources():
    source=ROOT/'paper/draft.md';data,body=manuscript(source)
    resource,rbody=manuscript(ROOT/'paper/ethicalai-benchmark.md')
    results=json.loads((ROOT/'experiments/research-results-2026-11-09.json').read_text())
    parsed=tables(body)
    detection=next(t for t in parsed if t[0]==['Condition','Exact verdict','Recall','Specificity','Flag precision'])
    expected=['none','freeform','checklist','mono-rid','judge-ctx','judge','judge-anon']
    assert [r[0] for r in detection[1:]]==expected
    for row in detection[1:]:
        s=results['suites']['hard'][row[0]]['score']
        assert row[1:]==[fraction(s['exact'],s['n']),fraction(s['tp'],s['tp']+s['fn']),
                        fraction(s['tn'],s['tn']+s['fp']),fraction(s['tp'],s['tp']+s['fp'])],row
    confusion=next(t for t in parsed if t[0]==['Gold verdict','Predicted SHIP','Predicted REVISE','Predicted BLOCK'])
    for row in confusion[1:]:
        assert list(map(int,row[1:]))==[results['suites']['hard']['judge']['confusion'][row[0]][p] for p in ('SHIP','REVISE','BLOCK')]
    attribution=next(t for t in parsed if t[0][0]=='Reviewer' and 'Exact gold rule' in t[0][2])
    for row in attribution[1:]:
        s=results['suites']['hard'][row[0]]['score']
        assert row[1:]==[fraction(s['family_tp_attributed'],s['tp']),fraction(s['exact_tp_attributed'],s['tp']),fraction(s['tp'],s['tp']+s['fp'])]
    supplement=next(t for t in parsed if t[0][:2]==['Suite','Reviewer'])
    assert len(supplement)==9
    for row in supplement[1:]:
        reviewer=row[1].split(',')[0]
        s=results['suites'][row[0].lower()][reviewer]['score']
        assert row[2:]==[fraction(s['exact'],s['n']),fraction(s['tp'],s['tp']+s['fn']),
                        fraction(s['tn'],s['tn']+s['fp']),fraction(s['exact_tp_attributed'],s['tp'])],row
    named=results['suites']['hard']['judge']['score']
    assert (named['exact_rule_set_hits_tp'],named['exact_rule_set_predictions_tp'],named['exact_rule_set_gold_tp'])==(37,84,37)
    assert '37/84' in body and '37/37' in body
    for path,meta,content in [(source,data,body),(ROOT/'paper/ethicalai-benchmark.md',resource,rbody)]:
        assert all(meta.get(k) for k in ('title','author','date','abstract'))
        assert not any(c in path.read_text() for c in ('—','–'))
        assert '[UNVERIFIED]' not in path.read_text()
    assert '8798134341ea386da80fb5602bc7dd06ef81cf24' in rbody
    assert '3b9b50021ef5eefb15a28d4edb7a5264f2fb626f' in rbody
    assert (ROOT/'paper/latex/main.tex').read_bytes()==(ROOT/'paper/arxiv/main.tex').read_bytes()
    for path,meta in [(source,data),(ROOT/'paper/ethicalai-benchmark.md',resource)]:
        pdf=path.with_suffix('.pdf')
        info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
        pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M)[1])
        assert 4<=pages<=8,(path,pages)
        assert meta['title'] in info
        assert hashlib.sha256(path.read_bytes()).hexdigest() in info,'PDF does not match the complete canonical manuscript'
        text=subprocess.check_output(['pdftotext',str(pdf),'-'],text=True)
        flatten=lambda s:re.sub(r'\s+',' ',s).strip()
        assert flatten(meta['abstract'][:100]) in flatten(text)
        target='methods-paper.pdf' if path==source else 'paper.pdf'
        assert pdf.read_bytes()==(ROOT/'docs'/target).read_bytes()
    print('PASS: manuscript tables match frozen raw results; canonical metadata, PDFs, LaTeX and six-page paper copies agree.')


def check_browser():
    from playwright.sync_api import sync_playwright
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT/'docs')))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}/'
    title=manuscript(ROOT/'paper/ethicalai-benchmark.md')[0]['title']
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            for width in (390,768,1440):
                page=browser.new_page(viewport={'width':width,'height':1000},java_script_enabled=False)
                page.route('https://**/*',lambda r:r.abort())
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                response=page.goto(base+'paper.html',wait_until='domcontentloaded')
                assert response.status==200
                assert page.locator('h1').all_text_contents()==[title]
                assert 'arXiv metadata-query matches' in page.locator('body').inner_text()
                assert page.locator('a[href="methods-paper.pdf"]').count()==1
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                for filename in ('paper.pdf','methods-paper.pdf'):
                    result=page.request.get(base+filename)
                    assert result.ok and result.body().startswith(b'%PDF-')
                    assert hashlib.sha256(result.body()).digest()==hashlib.sha256((ROOT/'docs'/filename).read_bytes()).digest()
                if width==390:page.screenshot(path='/tmp/ethicalai-revised-paper-mobile.png')
                page.goto(base+'#paper',wait_until='domcontentloaded')
                assert page.locator('#paper article').count()==2
                assert page.locator('.concept').count()==434
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                assert not errors,errors
                page.close()
            browser.close()
        print('PASS: public paper page and homepage summaries, PDF downloads, no-JS reading and no overflow at 390/768/1440 px.')
    finally:server.shutdown()


def check_rebuild():
    paths=[ROOT/p for p in ('paper/draft.pdf','paper/ethicalai-benchmark.pdf','paper/latex/main.tex','paper/arxiv/main.tex','docs/index.html','docs/paper.html','docs/paper.pdf','docs/methods-paper.pdf')]
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    before={str(p):digest(p) for p in paths}
    subprocess.run(['python3',str(ROOT/'experiments/build-research-papers.py')],cwd=ROOT,check=True)
    subprocess.run(['python3',str(ROOT/'experiments/build-paper-page.py')],cwd=ROOT,check=True)
    assert before=={str(p):digest(p) for p in paths},'Rebuilding changed generated paper artifacts'
    print('PASS: repeated Markdown-to-PDF/LaTeX/HTML build is byte-identical.')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--browser',action='store_true');ap.add_argument('--rebuild',action='store_true')
    ap.add_argument('--live',metavar='HTTPS_URL',help='Compare the deployed site and linked assets with the tested docs files')
    args=ap.parse_args();check_sources();assets=check_links()
    if args.rebuild:check_rebuild()
    if args.browser:check_browser()
    if args.live:check_live(args.live,assets)


if __name__=='__main__':main()
