#!/usr/bin/env python3
"""example-gaps.py - worklist for the grounded-examples effort.

Every failure mode should carry three explicit examples, each one drawn from a
paper we actually read (tagged inline as [arXiv:id]) or clearly marked as an
illustrative scenario. Most modes already have a cited paper but no worked
examples. This script reports the gap and, crucially, ranks the cited papers by
how many example-less modes each one would serve, so a single read unlocks the
most examples.

Usage:
  experiments/example-gaps.py            # summary + top papers to read next
  experiments/example-gaps.py --modes    # list every mode missing >=3 examples
  experiments/example-gaps.py --paper ID # modes whose citation includes ID
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "experiments"
ONTOLOGY = ROOT / "ontology" / "ethical-ai.yaml"


def norm(pid):
    """Strip the trailing version (v1, v2) so 2510.06265v1 == 2510.06265."""
    pid = pid.strip()
    if "v" in pid:
        head = pid.split("v")[0]
        if head.replace(".", "").isdigit():
            return head
    return pid


def load():
    o = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    cat_papers = {int(k): v for k, v in
                  json.loads((EXP / "catalogue-papers.json").read_text()).items()}
    return o["modes"], cat_papers


def papers_for(mode, cat_papers):
    """Return [(id, title)] of papers cited for a mode, via its catalogue num."""
    num = mode.get("num")
    entry = cat_papers.get(num)
    if not entry:
        return []
    return [(norm(p["id"]), p.get("title", "")) for p in entry.get("papers", [])]


def example_count(mode):
    return len(mode.get("examples") or [])


def main():
    modes, cat_papers = load()
    missing = [m for m in modes if example_count(m) < 3]
    have = [m for m in modes if example_count(m) >= 3]

    arg = sys.argv[1] if len(sys.argv) > 1 else ""

    if arg == "--modes":
        for m in sorted(missing, key=lambda x: x["name"]):
            cites = ", ".join(pid for pid, _ in papers_for(m, cat_papers)) or "(no paper)"
            print(f"  [{example_count(m)}/3] {m['name']:38} {cites}")
        print(f"\n{len(missing)} modes missing >=3 examples")
        return

    if arg == "--paper":
        target = norm(sys.argv[2])
        hits = [m for m in missing if target in {p for p, _ in papers_for(m, cat_papers)}]
        for m in hits:
            print(f"  {m['name']}")
        print(f"\n{len(hits)} example-less modes cite {target}")
        return

    # default: summary + papers ranked by example-less modes served
    print(f"modes: {len(modes)}   with >=3 examples: {len(have)}   "
          f"missing: {len(missing)}")
    no_paper = [m for m in missing if not papers_for(m, cat_papers)]
    print(f"of the {len(missing)} missing, {len(missing) - len(no_paper)} already "
          f"cite a paper, {len(no_paper)} have none yet\n")

    served = defaultdict(list)
    title = {}
    for m in missing:
        for pid, t in papers_for(m, cat_papers):
            served[pid].append(m["name"])
            title.setdefault(pid, t)

    ranked = sorted(served.items(), key=lambda kv: -len(kv[1]))
    print("top papers to read next (unlock the most example-less modes):")
    for pid, names in ranked[:15]:
        t = (title[pid][:54] + "...") if len(title[pid]) > 57 else title[pid]
        print(f"  {len(names):2}x  arXiv:{pid:13} {t}")
        print(f"        -> {', '.join(names[:6])}{' ...' if len(names) > 6 else ''}")


if __name__ == "__main__":
    main()
