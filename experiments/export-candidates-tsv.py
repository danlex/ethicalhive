"""Export the candidate-behaviours markdown list to TSV chunks for independent review.

Each output line: number, name, source, human definition, in an AI, nearest existing, evidence.

Usage: python export-candidates-tsv.py <list.md> <out-dir> <chunks>
"""
import os
import re
import sys

md, out_dir, chunks = sys.argv[1], sys.argv[2], int(sys.argv[3])
rows = []
for line in open(md, encoding="utf-8"):
    m = re.match(r"^\| (\d+) \|(.*)\|\s*$", line)
    if m:
        c = [x.strip().replace("*", "") for x in m.group(2).split("|")]
        c += [""] * (6 - len(c))
        rows.append([m.group(1)] + c[:6])
os.makedirs(out_dir, exist_ok=True)
size = -(-len(rows) // chunks)
for i in range(chunks):
    part = rows[i * size:(i + 1) * size]
    with open(os.path.join(out_dir, f"chunk{i + 1}.tsv"), "w", encoding="utf-8") as f:
        for r in part:
            f.write("\t".join(r) + "\n")
    print(f"chunk{i + 1}.tsv: {part[0][0]} to {part[-1][0]} ({len(part)})")
