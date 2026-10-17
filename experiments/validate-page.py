#!/usr/bin/env python3
"""validate-page.py - structural sanity checks for docs/index.html.

Confirms the page parses and that key tags balance after a build. Run after
build-catalogue.py --write. Exit code 1 on any failure.

Usage: experiments/validate-page.py
"""

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

    catalogue = html.count('class="cat-chip ')
    papers = html.count('class="papers"')
    none = html.count("cite none")
    deep = html.count('class="concept"')
    print(
        f"catalogue: {catalogue} entries (expect 100); "
        f"deep blocks: {deep} (expect 14); "
        f"papers lists: {papers}, no-paper notes: {none} (expect sum 114)"
    )
    if catalogue != 100:
        ok = False
        print("  MISMATCH: expected 100 catalogue entries")
    if papers + none != 114:
        ok = False
        print("  MISMATCH: expected 114 papers/no-paper blocks (100 catalogue + 14 deep)")

    for stale in ("Prompt to prevent it", "<h4>Judge agent", "<h4>Contract clause"):
        n = html.count(stale)
        print(f"  {'OK ' if n == 0 else 'LEFTOVER'}  {stale!r}: {n}")
        if n:
            ok = False

    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
