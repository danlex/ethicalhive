#!/usr/bin/env python3
"""validate-page.py - structural sanity checks for docs/index.html.

Confirms the page parses and that key tags balance after a build. Run after
build-catalogue.py --write. Exit code 1 on any failure.

Usage: experiments/validate-page.py
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "docs" / "index.html"


def main():
    html = PAGE.read_text(encoding="utf-8")
    HTMLParser().feed(html)  # raises on malformed markup

    ok = True

    def pair(open_tag, close_tag):
        nonlocal ok
        o, c = html.count(open_tag), html.count(close_tag)
        flag = "OK " if o == c else "MISMATCH"
        if o != c:
            ok = False
        print(f"  {flag}  {open_tag} {o} / {close_tag} {c}")

    print("balance:")
    pair("<details", "</details>")
    pair("<ul", "</ul>")
    pair("<a ", "</a>")

    concepts = len(re.findall(r'class="concept ', html))
    shipped = html.count('class="concept shipped"')
    papers = html.count('class="papers"')
    none = html.count("cite none")
    groups = html.count('class="cat-group"')
    print(
        f"concept boxes: {concepts} (expect 129); highlighted: {shipped} (expect 25); "
        f"groups: {groups} (expect 12); "
        f"papers lists: {papers}, no-paper notes: {none} (expect sum 129)"
    )
    if concepts != 129 or shipped != 25 or groups != 12 or papers + none != 129:
        ok = False
        print("  MISMATCH: expected 129 boxes (25 highlighted) in 12 groups")

    stale_markers = (
        "Prompt to prevent it",
        "<h4>Judge agent",
        "<h4>Contract clause",
        '<main id="list"',
        'id="contract"',
        'href="#list"',
        'href="#framework"',
        'href="#contract"',
    )
    for stale in stale_markers:
        n = html.count(stale)
        print(f"  {'OK ' if n == 0 else 'LEFTOVER'}  {stale!r}: {n}")
        if n:
            ok = False

    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
