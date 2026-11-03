#!/usr/bin/env python3
"""paired-test.py - paired comparison of two reviewer conditions on the same cases.

The ablation conditions all score the same drafts, so the right test of a difference is
paired, not two independent Wilson intervals. For the clean (gold-SHIP) cases, this reports
the discordant pairs (where one condition leaves a clean draft alone and the other
over-flags it), McNemar's exact two-sided p on those discordant pairs, and the paired
difference in specificity. Uses the committed result files; no model calls.

Usage:
  paired-test.py <condA> <condB> [--suites s1,s2,...]
  e.g. paired-test.py judge mono-rid

For condition names, a glob of '<cond>-20*' is used, so 'judge' excludes 'judge-ctx' and
'judge-anon' (which are '<cond>-ctx-20*' etc.).
"""
import glob
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "experiments" / "results"
SUITES = ["anchoring", "capitulation", "scope-creep", "selective-evidence",
          "source-fabrication", "sycophancy"]
FLAG = {"REVISE", "BLOCK"}


def load(cond, suites):
    """case_id -> got, from the newest file per suite for this condition."""
    out = {}
    for s in suites:
        files = sorted(glob.glob(str(RESULTS / f"run-suite-{s}-hard-{cond}-20*.jsonl")))
        if not files:
            continue
        for line in open(files[-1]):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            out[r["case_id"]] = (r["got"], r["expected"])
    return out


def mcnemar_exact_p(b, c):
    """Two-sided exact binomial p on the smaller discordant count (n=b+c, p=0.5)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    # two-sided: 2 * sum_{i=0..k} C(n,i) 0.5^n, capped at 1
    s = sum(math.comb(n, i) for i in range(k + 1)) * (0.5 ** n)
    return min(1.0, 2 * s)


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    condA, condB = sys.argv[1], sys.argv[2]
    suites = SUITES
    for i, a in enumerate(sys.argv):
        if a == "--suites" and i + 1 < len(sys.argv):
            suites = [x.strip() for x in sys.argv[i + 1].split(",") if x.strip()]
    A, B = load(condA, suites), load(condB, suites)
    ids = [i for i in A if i in B]
    clean = [i for i in ids if A[i][1] == "SHIP"]

    # On clean cases: "correct" = left alone (SHIP); "wrong" = over-flagged.
    both_ok = a_only = b_only = both_flag = 0
    for i in clean:
        ga = A[i][0] == "SHIP"
        gb = B[i][0] == "SHIP"
        if ga and gb: both_ok += 1
        elif ga and not gb: a_only += 1   # A leaves clean, B over-flags
        elif gb and not ga: b_only += 1   # B leaves clean, A over-flags
        else: both_flag += 1
    n = len(clean)
    specA = (both_ok + a_only) / n if n else float("nan")
    specB = (both_ok + b_only) / n if n else float("nan")
    # discordant: b = A-correct-B-wrong (favours A), c = B-correct-A-wrong (favours B)
    p = mcnemar_exact_p(a_only, b_only)

    print(f"Paired specificity: {condA} vs {condB}  (clean gold-SHIP cases, n={n})")
    print(f"  {condA} specificity : {both_ok + a_only}/{n} = {specA:.2f}")
    print(f"  {condB} specificity : {both_ok + b_only}/{n} = {specB:.2f}")
    print(f"  paired difference  : {specA - specB:+.2f}")
    print(f"  discordant pairs   : {condA}-only-correct = {a_only}, {condB}-only-correct = {b_only}")
    print(f"  McNemar exact p    : {p:.3f}  ({'significant' if p < 0.05 else 'not significant'} at .05)")


if __name__ == "__main__":
    main()
