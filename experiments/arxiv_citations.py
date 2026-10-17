#!/usr/bin/env python3
"""arxiv_citations.py - per failure-mode term, fetch the AI-domain paper count
and the top-N most relevant arXiv papers (id, year, title).

One arXiv request per term returns BOTH the total match count and the top-N
entries, so this supersedes running the count and the sampler separately.

Scope and honesty notes (the point of this repo):
  - Counts arXiv preprints in cs.AI / cs.CL / cs.LG only. Not all AI literature,
    not conference-only or journal-only work. A proxy for term prevalence.
  - A keyword hit is not a topic hit. Read the returned titles before trusting a
    number: some terms are homonyms inside AI (e.g. "confirmation bias" also
    means pseudo-label self-reinforcement in semi-supervised learning).
  - Every citation printed is a real arXiv id returned by the API this run.
    Nothing here is generated from memory.

Usage:
  experiments/arxiv_citations.py <terms.tsv> [--top N] [--sleep SECONDS]

terms.tsv rows: <label><TAB><arxiv_clause>  (# comments and blank lines skipped)
The category filter (cs.AI OR cs.CL OR cs.LG) is appended to every clause.
"""

import argparse
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

API = "https://export.arxiv.org/api/query"
CATEGORY_FILTER = "(cat:cs.AI OR cat:cs.CL OR cat:cs.LG)"
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
}


def fetch(clause, top):
    """Return (total:int|None, [(arxiv_id, year, title), ...]) for one clause."""
    query = f"{clause} AND {CATEGORY_FILTER}"
    params = urllib.parse.urlencode(
        {
            "search_query": query,
            "sortBy": "relevance",
            "sortOrder": "descending",
            "max_results": str(top),
        }
    )
    req = urllib.request.Request(
        f"{API}?{params}", headers={"User-Agent": "ethicalhive-term-map/1.0"}
    )
    with urllib.request.urlopen(req, timeout=40) as resp:
        xml = resp.read().decode("utf-8")
    root = ET.fromstring(xml)

    total_el = root.find("opensearch:totalResults", NS)
    total = int(total_el.text) if total_el is not None and total_el.text else None

    papers = []
    for entry in root.findall("atom:entry", NS):
        raw_id = (entry.findtext("atom:id", default="", namespaces=NS) or "").strip()
        # error feed uses id https://arxiv.org/api/errors
        if "arxiv.org/api/errors" in raw_id:
            return None, []
        arxiv_id = raw_id.rsplit("/abs/", 1)[-1]
        published = entry.findtext("atom:published", default="", namespaces=NS) or ""
        year = published[:4]
        title = " ".join(
            (entry.findtext("atom:title", default="", namespaces=NS) or "").split()
        )
        papers.append((arxiv_id, year, title))
    return total, papers


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("terms", help="path to a terms TSV (label<TAB>clause)")
    ap.add_argument("--top", type=int, default=3, help="papers per term (default 3)")
    ap.add_argument("--sleep", type=float, default=3.0, help="seconds between requests")
    args = ap.parse_args()

    with open(args.terms, encoding="utf-8") as fh:
        rows = []
        for line in fh:
            line = line.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if "\t" not in line:
                continue
            label, clause = line.split("\t", 1)
            rows.append((label.strip(), clause.strip()))

    print(f"# Term literature map ({len(rows)} terms, arXiv cs.AI/CL/LG)\n")
    for i, (label, clause) in enumerate(rows):
        try:
            total, papers = fetch(clause, args.top)
        except Exception as exc:  # network / parse failure, keep going
            print(f"## {label}\n\n_query failed: {exc}_\n")
            continue
        count = "ERR" if total is None else str(total)
        print(f"## {label}  (count: {count})")
        print(f"\n`{clause}`\n")
        if papers:
            for arxiv_id, year, title in papers:
                print(f"- arXiv:{arxiv_id} ({year}) - {title}")
        else:
            print("- _no papers returned_")
        print()
        if i < len(rows) - 1:
            time.sleep(args.sleep)


if __name__ == "__main__":
    main()
