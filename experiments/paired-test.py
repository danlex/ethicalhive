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

Conditions use the same explicit run manifest as tables and figures. Exact case
IDs and gold verdicts must agree before a paired comparison is made.
"""
import math
from pathlib import Path
import argparse
from research_runs import DEFAULT_MANIFEST, load_condition, ResearchDataError

SUITES = ["anchoring", "capitulation", "scope-creep", "selective-evidence",
          "source-fabrication", "sycophancy"]
FLAG = {"REVISE", "BLOCK"}


def load(cond, suites, manifest=DEFAULT_MANIFEST):
    """case_id -> (prediction, gold), from verified manifest records."""
    _,rows=load_condition(cond,modes=suites,manifest=manifest)
    return {r['case_id']:(r['got'],r['expected']) for r in rows}


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
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('condition_a');parser.add_argument('condition_b')
    parser.add_argument('--manifest',type=Path,default=DEFAULT_MANIFEST)
    parser.add_argument('--suites',default=','.join(SUITES))
    args=parser.parse_args();condA,condB=args.condition_a,args.condition_b
    suites=[s.strip() for s in args.suites.split(',') if s.strip()]
    A, B = load(condA,suites,args.manifest),load(condB,suites,args.manifest)
    if A.keys()!=B.keys() or any(A[i][1]!=B[i][1] for i in A):
        raise ResearchDataError('Paired conditions must contain identical case IDs and gold verdicts')
    ids = list(A)
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
