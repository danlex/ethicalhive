#!/usr/bin/env python3
"""Validate count, export consistency, filtering, mobile layout and no-JS reading."""
import csv
import functools
import http.server
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT/'references/behaviour-candidates-100-2026-11-06.json').read_text())
rows = list(csv.DictReader((ROOT/'docs/research/100-behaviours.csv').open()))
assert len(rows) == len(data['entries']) == 100
assert [r['name'] for r in rows] == [r['name'] for r in data['entries']]
assert len({r['id'] for r in rows}) == 100
assert json.loads((ROOT/'docs/research/100-behaviours.json').read_text()) == data
assert all(r['definition'] and r['sources'] and r['distinction_and_limits'] for r in rows)

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT/'docs')))
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}/research/100-behaviours.html'
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        for width in (390, 768, 1440):
            page = browser.new_page(viewport={'width':width, 'height':900})
            errors=[]
            page.on('pageerror', lambda e: errors.append(str(e)))
            assert page.goto(url).status == 200
            assert page.locator('article').count() == 100
            assert page.locator('h2').count() == 10
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            page.locator('#search').fill('Ovsiankina')
            assert page.locator('article:visible').count() == 1
            page.locator('article:visible summary').click()
            assert page.locator('article:visible details').get_attribute('open') is not None
            page.locator('#search').fill('zzzzzz-no-match')
            assert page.locator('article:visible').count() == 0
            page.locator('#search').fill('')
            assert page.locator('article:visible').count() == 100
            assert not errors, errors
            page.screenshot(path=f'/tmp/behaviours-100-{width}.png')
            page.close()
        ctx=browser.new_context(java_script_enabled=False, viewport={'width':390,'height':844})
        page=ctx.new_page()
        page.goto(url)
        assert page.locator('article').count()==100
        page.locator('article summary').first.click()
        assert page.locator('article details').first.get_attribute('open') is not None
        browser.close()
    print('PASS: 100 consistent JSON/CSV records; three viewport sizes; filter, details and no-JS reading')
finally:
    server.shutdown()
