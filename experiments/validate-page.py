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
from catalogue_sources import selected_papers

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
    primary=onto['modes']
    n_modes = len(primary)
    n_shipped = sum(1 for m in primary if m.get("highlighted"))
    n_groups = len({m['category'] for m in primary})

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
    human = html.count('class="human-sources human-papers"')
    sections = html.count('class="research-papers"')
    expected_ai=sum(any(p['domain']=='ai' for p in selected_papers(m)) for m in primary)
    expected_human=sum(any(p['domain']=='human-related' for p in selected_papers(m)) for m in primary)
    groups = html.count('class="cat-group"')
    print(
        f"concept boxes: {concepts} (expect {n_modes}); highlighted: {shipped} "
        f"(expect {n_shipped}); groups: {groups} (expect {n_groups}); "
        f"research sections: {sections} (expect {n_modes}); "
        f"AI lists: {papers} (expect {expected_ai}); human/related lists: {human} (expect {expected_human})"
    )
    if concepts != n_modes or shipped != n_shipped or groups != n_groups \
            or sections!=n_modes or papers!=expected_ai or human!=expected_human:
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

