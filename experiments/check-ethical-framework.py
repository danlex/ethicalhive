#!/usr/bin/env python3
"""Check the supplied ethical wording across the paper, website and data exports."""
import argparse
import functools
import hashlib
from html import unescape
import http.server
import json
from pathlib import Path
import re
import subprocess
import threading
from urllib.request import Request, urlopen

import yaml
from ethical_framework import ROOT, framework

PUBLIC = ['index.html', 'paper/ontology-paper.html', 'paper.pdf', 'behaviours.json',
          'research/100-behaviours.json', 'research/behaviour-candidates.json']


def plain(text):
    return ' '.join(unescape(re.sub(r'<[^>]+>', ' ', text)).split())


def check_content():
    ethical, categories = framework()
    assert [p['count'] for p in categories] == [112, 100, 52, 51, 50, 43, 26]
    md = (ROOT/'paper/ontology-paper.md').read_text()
    home = plain((ROOT/'docs/index.html').read_text())
    article = plain((ROOT/'docs/paper/ontology-paper.html').read_text())
    raw = subprocess.check_output(['pdftotext', str(ROOT/'docs/paper.pdf'), '-'], text=True)
    pdf = ' '.join(re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', raw).split())
    for p in ethical + categories:
        assert p['statement'] in ' '.join(md.split()), p['name']
        for label, text in [('homepage', home), ('article', article), ('PDF', pdf)]:
            assert p['statement'] in text, (label, p['name'])
    for p in categories:
        assert f"{p['name']} ({p['count']})" in home
        assert f"{p['name']} ({p['count']})" in article
    for path in ('behaviours.json', 'research/100-behaviours.json', 'research/behaviour-candidates.json'):
        data = json.loads((ROOT/'docs'/path).read_text())
        assert data['principles'] == [{k:p[k] for k in ('id','name','statement')} for p in categories]
        assert len(data['modes']) == 434 and len({m['category'] for m in data['modes']}) == 11
    info = subprocess.check_output(['pdfinfo', str(ROOT/'docs/paper.pdf')], text=True)
    assert hashlib.sha256(md.encode()).hexdigest() in info
    assert (ROOT/'docs/paper.pdf').read_bytes() == (ROOT/'paper/ontology-paper.pdf').read_bytes()
    assert 'historical 207' in pdf
    print('PASS: all 13 supplied statements, seven counts, 434 records/11 browsing categories and PDF source hash agree.')


def check_browser():
    from playwright.sync_api import sync_playwright
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args): pass
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Handler, directory=str(ROOT/'docs')))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
            for width in (390, 768, 1440):
                page = browser.new_page(viewport={'width':width,'height':1000}, java_script_enabled=False)
                page.route('https://**/*', lambda r:r.abort())
                page.goto(f'http://127.0.0.1:{server.server_port}/', wait_until='domcontentloaded')
                assert page.locator('#principles .cx-card').count() == 6
                assert page.locator('#evaluation-categories .cx-card').count() == 7
                assert page.locator('.concept').count() == 434
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                if width == 390:
                    page.locator('#evaluation-categories').scroll_into_view_if_needed()
                    page.screenshot(path='/tmp/ethical-framework-mobile.png')
                page.goto(f'http://127.0.0.1:{server.server_port}/paper/ontology-paper.html', wait_until='domcontentloaded')
                assert page.locator('h1').count() == 1
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                assert page.request.get(f'http://127.0.0.1:{server.server_port}/paper.pdf').body().startswith(b'%PDF-')
                page.close()
            browser.close()
    finally:
        server.shutdown()
    print('PASS: six principle cards, seven evaluation cards, no-JS reading and no overflow at 390/768/1440px.')


def check_live(base):
    for name in PUBLIC:
        local = (ROOT/'docs'/name).read_bytes()
        digest = hashlib.sha256(local).hexdigest()
        request = Request(base.rstrip('/')+'/'+name+'?framework='+digest[:16], headers={'Cache-Control':'no-cache'})
        with urlopen(request, timeout=45) as response:
            assert response.status == 200
            assert hashlib.sha256(response.read()).hexdigest() == digest, name
    print('PASS: all six live publication files match the checked local files over HTTPS.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser', action='store_true')
    parser.add_argument('--live', metavar='HTTPS_URL')
    args = parser.parse_args()
    check_content()
    if args.browser: check_browser()
    if args.live:
        assert args.live.startswith('https://')
        check_live(args.live)
