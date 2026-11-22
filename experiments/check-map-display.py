#!/usr/bin/env python3
"""Check that ontology-map labels and detail text remain readable in the host theme."""
import argparse
import functools
import hashlib
import http.server
from pathlib import Path
import re
import subprocess
import threading
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[1]
STYLE=re.compile(r'(<!-- MAP:START -->\s*<style>).*?(</style>)',re.S)
CONTRAST=r'''nodes=>{
  function rgba(value){return (value.match(/[\d.]+/g)||[]).map(Number)}
  function over(a,b){const alpha=a.length>3?a[3]:1;return a.slice(0,3).map((v,i)=>v*alpha+b[i]*(1-alpha))}
  function background(node){if(!node)return [255,255,255];return over(rgba(getComputedStyle(node).backgroundColor),background(node.parentElement))}
  function luminance(color){return color.map(v=>{v/=255;return v<=.04045?v/12.92:Math.pow((v+.055)/1.055,2.4)})
    .reduce((sum,v,i)=>sum+v*[.2126,.7152,.0722][i],0)}
  return nodes.filter(n=>n.getClientRects().length).map(n=>{
    const bg=background(n),fg=over(rgba(getComputedStyle(n).color),bg),a=luminance(bg),b=luminance(fg);
    return {text:(n.innerText||n.value||n.tagName).slice(0,70),ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)};
  }).filter(item=>item.ratio<4.5);
}'''


def check(baseline=None,live=None):
    from playwright.sync_api import sync_playwright
    if baseline:
        current=(ROOT/'docs/index.html').read_text()
        previous=subprocess.check_output(['git','show',baseline+':docs/index.html'],cwd=ROOT,text=True)
        assert STYLE.sub(r'\1\2',current)==STYLE.sub(r'\1\2',previous),'Content outside inline map styles changed'
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT/'docs')))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=live or 'http://127.0.0.1:'+str(server.server_port)+'/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            for width in (390,768,1440):
                page=browser.new_page(viewport={'width':width,'height':1000})
                errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
                page.goto(base,wait_until='domcontentloaded')
                page.add_style_tag(content='html{scroll-behavior:auto!important}')
                page.locator('.mm-expand').click()
                pills=page.locator('#mm .pill:visible')
                assert pills.count()>400
                page.locator('#mm li.ai>.row').scroll_into_view_if_needed()
                if width==390:page.screenshot(path='/tmp/ethicalai-map-labels-mobile.png')
                failures=pills.evaluate_all(CONTRAST)
                assert not failures,failures[:8]
                badges=page.locator('#mm .badge:visible').evaluate_all(CONTRAST)
                assert not badges,badges[:8]
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                assert page.locator('#mm .mm-stage').evaluate('(n)=>n.scrollWidth<=n.clientWidth+1')
                page.locator('.mm-q').fill('Alignment hallucination')
                node=page.locator('#mm [data-mid="alignment-hallucination"]')
                node.locator(':scope>.row>.pill').click()
                assert node.locator('.mm-detail').count()==1
                failures=page.locator('#mm .mm-detail p,#mm .mm-detail a,#mm .mm-detail .ptag,#mm .mm-q,#mm .mm-bar button').evaluate_all(CONTRAST)
                assert not failures,failures[:8]
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                if width==390:page.locator('#mm').screenshot(path='/tmp/ethicalai-map-detail-mobile.png')
                page.locator('.mm-collapse').click()
                assert page.locator('#mm .mm-detail').count()==0
                assert not errors,errors
                page.close()
            browser.close()
    finally:server.shutdown()
    if live:
        expected=(ROOT/'docs/index.html').read_bytes()
        digest=hashlib.sha256(expected).hexdigest()
        with urlopen(live.rstrip('/')+'/index.html?map='+digest[:16],timeout=45) as response:
            assert hashlib.sha256(response.read()).hexdigest()==digest
    print('PASS: map label/detail contrast, mobile wrapping, search, expand/collapse and no overflow at 390/768/1440px.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline');parser.add_argument('--live')
    args=parser.parse_args();check(args.baseline,args.live)
