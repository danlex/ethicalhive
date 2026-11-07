"""Apply reviewer source corrections to the candidate-behaviours markdown list.

Reads a review TSV (number, name, DEF, SRC, corrected source, AI, duplicate of, note) and,
for rows marked SRC WRONG with a corrected source, replaces the Source cell in the list.
Prints each change.

Usage: python apply-candidate-review.py <list.md> <review.tsv>
"""
import re
import sys

md, review = sys.argv[1], sys.argv[2]
fixes = {}
for line in open(review, encoding="utf-8"):
    f = line.rstrip("\n").split("\t")
    if len(f) == 8 and f[3] == "WRONG" and f[4].strip():
        fixes[f[0]] = f[4].strip().replace("|", "/")

out, changed = [], 0
for line in open(md, encoding="utf-8"):
    m = re.match(r"^\| (\d+) \|", line)
    if m and m.group(1) in fixes:
        cells = line.rstrip("\n").split(" | ")
        old = cells[2]
        cells[2] = fixes[m.group(1)]
        line = " | ".join(cells) + "\n"
        changed += 1
        print(f"{m.group(1)}: {old}  ->  {cells[2]}")
    out.append(line)
open(md, "w", encoding="utf-8").write("".join(out))
print(f"{changed} sources corrected")
