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

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "docs" / "index.html"
ONTOLOGY = ROOT / "ontology" / "ethical-ai.yaml"


def main():
    html = PAGE.read_text(encoding="utf-8")
    HTMLParser().feed(html)  # raises on malformed markup

    # Expected counts are derived from the ontology, not hard-coded, so adding a
    # mode does not require editing this file.
    import yaml
    onto = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    n_modes = len(onto["modes"])
    n_shipped = sum(1 for m in onto["modes"] if m.get("highlighted"))
    n_groups = len({m["group_label"] for m in onto["modes"]})

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
        f"concept boxes: {concepts} (expect {n_modes}); highlighted: {shipped} "
        f"(expect {n_shipped}); groups: {groups} (expect {n_groups}); "
        f"papers lists: {papers}, no-paper notes: {none} (expect sum {n_modes})"
    )
    if concepts != n_modes or shipped != n_shipped or groups != n_groups \
            or papers + none != n_modes:
        ok = False
        print(f"  MISMATCH: expected {n_modes} boxes ({n_shipped} highlighted) "
              f"in {n_groups} groups")

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
