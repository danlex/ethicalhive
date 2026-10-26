#!/usr/bin/env python3
"""add-citation.py - attach a paper citation for a mode in
experiments/catalogue-papers.json, keyed by the mode's catalogue number.

Used while grounding modes that had no citation: once a genuine supporting paper
has been read, record it so the catalogue "Papers" section matches the inline
[arXiv:id] tags on the mode's examples.

Appends a compact single-line entry (or replaces one if NUM already exists)
without reformatting the rest of the file, so diffs stay small. Validates that
the result still parses as JSON.

Usage:
  experiments/add-citation.py NUM ARXIV_ID YEAR "Title"
  experiments/add-citation.py 158 2307.03172 2023 "Lost in the Middle: How Language Models Use Long Contexts"
"""

import json
import re
import sys
from pathlib import Path

CAT = Path(__file__).resolve().parent / "catalogue-papers.json"


def main():
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(2)
    num, pid, year, title = sys.argv[1:5]
    text = CAT.read_text(encoding="utf-8")
    d = json.loads(text)  # parse to validate and to check existence

    entry = (f'  "{num}": {{"count": 1, "papers": [{{"id": "{pid}", '
             f'"year": "{year}", "title": {json.dumps(title, ensure_ascii=False)}}}]}}')

    if num in d:
        # replace the existing block for this num (compact or multi-line)
        pat = re.compile(r'[ \t]*"' + re.escape(num) + r'": \{.*?\n?\s*\}(?=,\n|\n\})',
                         re.DOTALL)
        if not pat.search(text):
            print(f"could not locate existing block for num {num}", file=sys.stderr)
            sys.exit(1)
        text = pat.sub(entry.rstrip(), text, count=1)
    else:
        # insert before the final closing brace
        idx = text.rstrip().rfind("}")
        head = text[:idx].rstrip()
        if not head.endswith(","):
            head += ","
        text = head + "\n" + entry + "\n}\n"

    json.loads(text)  # re-validate
    CAT.write_text(text, encoding="utf-8")
    print(f"set num {num} -> arXiv:{pid} ({year}) {title}")


if __name__ == "__main__":
    main()
