"""Merge agent-produced candidate TSV files into a new batch of the markdown list.

Each TSV line: group, name, source, human definition, in an AI, nearest existing, evidence.
Drops rows whose name already appears in the markdown list (case-insensitive, ignoring
punctuation) or earlier in the merge, numbers the rest from the next free number, and prints
a markdown section to stdout.

Usage: python merge-candidate-tsv.py <list.md> <batch-number> <first-letter-code> <a.tsv> [b.tsv ...]
"""
import re
import unicodedata
import sys


def key(name):
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", name.lower())


md, batch, code = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(md, encoding="utf-8").read()
taken = {key(m) for m in re.findall(r"^\| \d+ \| ([^|]+?) \|", text, flags=re.M)}
last = max(int(n) for n in re.findall(r"^\| (\d+) \|", text, flags=re.M))

groups, dropped = {}, []
for path in sys.argv[4:]:
    for line in open(path, encoding="utf-8"):
        f = [x.strip().replace("|", "/") for x in line.rstrip("\n").split("\t")]
        if len(f) != 7 or not f[1]:
            continue
        k = key(f[1])
        if k in taken:
            dropped.append(f[1])
            continue
        taken.add(k)
        groups.setdefault(f[0], []).append(f)

codes = []
c = code
for g in groups:
    codes.append(c)
    c = c[:-1] + chr(ord(c[-1]) + 1)

n = last
out = []
total = sum(len(v) for v in groups.values())
out.append(f"\n---\n\n# Batch {batch}: {total} more, checked through web search\n")
out.append("Date: 2026-11-06. Status: **candidates, search-checked** (same method and limits as "
           "batch 2). Found by four parallel search passes; definitions and evidence links come "
           "from search results, and the AI column is a hypothesis.\n")
for (g, rows), gc in zip(groups.items(), codes):
    out.append(f"## {gc}. {g} ({len(rows)})\n")
    out.append("| # | Behaviour | Source | Human definition | In an AI | Nearest existing | Evidence |")
    out.append("|---|---|---|---|---|---|---|")
    for f in rows:
        n += 1
        out.append(f"| {n} | {f[1]} | {f[2]} | {f[3]} | {f[4]} | {f[5]} | {f[6]} |")
    out.append("")
print("\n".join(out))
print(f"merged {total}, numbered {last + 1} to {n}; dropped duplicates: {', '.join(dropped) or 'none'}",
      file=sys.stderr)
