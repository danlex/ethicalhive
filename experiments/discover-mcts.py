#!/usr/bin/env python3
"""discover-mcts.py - MCTS-style discovery of new AI failure modes.

An idea tree: root -> areas (branches) -> candidate behaviours (leaves). Each leaf
is scored by a reward that blends three signals:
  - grounding: does the AI literature actually study it (arXiv count, cs.AI/CL/LG)
  - novelty: is it absent from the current ontology (dedup by name)
  - (the human-parallel vs AI-native rule is applied by hand when accepting)
The per-AREA mean reward is the backpropagated value that says which branch to
expand next round (the selection step). The expansion step (generating child
candidates) is done by the model, not the script, so this is a model-in-the-loop
MCTS: the script runs selection, simulation (reward), and backprop; the policy is us.

Input: a TSV  area <TAB> term <TAB> arxiv-clause
Output: ranked novel candidates + per-area value, written to a results file.

Usage: discover-mcts.py [candidates.tsv]
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

from arxiv_citations import fetch  # reuses the grounded arXiv query

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ONTOLOGY = ROOT / "ontology" / "ethical-ai.yaml"


def slug(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def reward(count, novel):
    if not novel:
        return 0.0
    if count >= 20:
        return 3.0
    if count >= 5:
        return 2.0
    if count >= 1:
        return 1.0
    return 0.0


def main():
    cand_file = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "discover-candidates.tsv"
    onto = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    known = {slug(m["name"]) for m in onto["modes"]}
    # also known human_parallel phrases, to catch near-dups
    known_words = set()
    for m in onto["modes"]:
        known_words.update(slug(m["name"]).split())

    rows = []
    for line in cand_file.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line.count("\t") < 2:
            continue
        area, term, clause = [x.strip() for x in line.split("\t", 2)]
        total, papers = fetch(clause, 2)
        count = total or 0
        s = slug(term)
        novel = s not in known and not any(s == slug(m["name"]) for m in onto["modes"])
        r = reward(count, novel)
        top = papers[0][2] if papers else ""  # fetch returns (id, year, title) tuples
        rows.append({"area": area, "term": term, "count": count, "novel": novel,
                     "reward": r, "top": top})
        print(f"  {r:>3}  {term:<32} count={count:<5} novel={novel}  {top[:60]}",
              file=sys.stderr)

    rows.sort(key=lambda x: (-x["reward"], -x["count"]))
    area_val = defaultdict(list)
    for x in rows:
        area_val[x["area"]].append(x["reward"])
    areas = sorted(((a, sum(v) / len(v), len(v)) for a, v in area_val.items()),
                   key=lambda t: -t[1])

    out = [f"# MCTS discovery run: {len(rows)} candidates, {sum(r['novel'] for r in rows)} novel\n",
           "## Ranked candidates (reward = novelty x grounding)\n",
           "| Reward | Candidate | Area | arXiv | Novel | Top paper |",
           "|---|---|---|---|---|---|"]
    for x in rows:
        out.append(f"| {x['reward']:g} | {x['term']} | {x['area']} | {x['count']} | "
                   f"{'yes' if x['novel'] else 'no'} | {x['top'][:70]} |")
    out.append("\n## Branch value (where to expand next round)\n")
    out.append("| Area | mean reward | candidates |\n|---|---|---|")
    for a, mean, n in areas:
        out.append(f"| {a} | {mean:.2f} | {n} |")
    res = HERE / "discover-results.md"
    res.write_text("\n".join(out) + "\n", encoding="utf-8")
    import json
    (HERE / "discover-results.json").write_text(
        json.dumps({"candidates": rows,
                    "areas": [{"area": a, "mean": round(mn, 2), "n": n} for a, mn, n in areas]},
                   indent=2), encoding="utf-8")
    print(f"\nwrote {res} and discover-results.json", file=sys.stderr)


if __name__ == "__main__":
    main()
