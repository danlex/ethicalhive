#!/usr/bin/env python3
"""add-citation.py - attach a paper citation for a mode in
experiments/catalogue-papers.json, keyed by the mode's catalogue number.

Used while grounding modes: once a genuine supporting paper has been read, record
it so the catalogue "Papers" section matches the inline [arXiv:id] tags on the
mode's examples. Replaces any existing papers for that NUM with the single paper
given (these modes are grounded from one primary source).

Parses and re-dumps the JSON (2-space indent, matching the file's existing
format), so diffs stay to the single changed entry.

Usage:
  experiments/add-citation.py NUM ARXIV_ID YEAR "Title"
"""

import json
import sys
from pathlib import Path

CAT = Path(__file__).resolve().parent / "catalogue-papers.json"


def main():
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(2)
    num, pid, year, title = sys.argv[1:5]
    d = json.loads(CAT.read_text(encoding="utf-8"))
    d[num] = {"label": num, "count": 1,
              "papers": [{"id": pid, "year": year, "title": title}]}
    CAT.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"set num {num} -> arXiv:{pid} ({year}) {title}")


if __name__ == "__main__":
    main()
