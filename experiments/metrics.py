#!/usr/bin/env python3
"""Score one or more run-suite.sh result files (.jsonl).

Treats REVISE and BLOCK as a positive "flag" and SHIP as negative, so a single-mode
suite is scored as binary detection plus exact-verdict accuracy.

Usage:
    python3 metrics.py results/run-foo-*.jsonl [more.jsonl ...] [--inspect [N]]

Flags:
    --inspect [N]   After the summary, print per-case detail: reviewer, got verdict,
                    gold_clauses, rule_ids cited, and the first N characters (default 600)
                    of the reviewer output. Useful for confirming rule-ID emission and
                    sanity-checking judge behavior without piping ad-hoc heredocs.
"""
import json, sys, glob, math
from collections import defaultdict

FLAG = {"REVISE", "BLOCK"}          # predicted/gold "needs attention"
VALID = {"SHIP", "REVISE", "BLOCK"}


def load(paths):
    """Read result files. Handles both true JSONL and pretty-printed jq output
    (concatenated JSON objects) by streaming with raw_decode."""
    rows = []
    dec = json.JSONDecoder()
    for pat in paths:
        for fn in glob.glob(pat):
            text = open(fn).read()
            idx, n = 0, len(text)
            while idx < n:
                while idx < n and text[idx].isspace():
                    idx += 1
                if idx >= n:
                    break
                obj, end = dec.raw_decode(text, idx)
                rows.append(obj)
                idx = end
    return rows


def score(rows):
    n = len(rows)
    exact = sum(1 for r in rows if r["got"] == r["expected"])
    errors = sum(1 for r in rows if r["got"] not in VALID)
    def clause(x):  # INT-SEL-01 -> SEL ; INT-SEL -> SEL
        p = x.split("-")
        return p[1] if len(p) > 1 and p[0] == "INT" else None

    tp = fp = tn = fn = 0
    flagged = attributed = 0
    for r in rows:
        gold_pos = r["expected"] in FLAG
        pred_pos = r["got"] in FLAG          # parse errors count as "no flag"
        if gold_pos and pred_pos: tp += 1
        elif gold_pos and not pred_pos: fn += 1
        elif not gold_pos and pred_pos: fp += 1
        else: tn += 1
        if pred_pos:                          # rule-ID attribution: did a flag cite the right clause?
            flagged += 1
            rids = {clause(x) for x in r.get("rule_ids", [])} - {None}
            gcls = {clause(x) for x in r.get("gold_clauses", [])} - {None}
            if rids & gcls:
                attributed += 1
    ruleid = attributed / flagged if flagged else float("nan")
    recall = tp / (tp + fn) if (tp + fn) else float("nan")        # caught real problems
    specificity = tn / (tn + fp) if (tn + fp) else float("nan")   # left clean drafts alone
    precision = tp / (tp + fp) if (tp + fp) else float("nan")
    f1 = (2 * precision * recall / (precision + recall)
          if precision == precision and recall == recall and (precision + recall) else float("nan"))
    return dict(n=n, exact=exact, exact_acc=exact / n if n else float("nan"),
                errors=errors, tp=tp, fp=fp, tn=tn, fn=fn,
                recall=recall, specificity=specificity, precision=precision, f1=f1,
                ruleid=ruleid)


def fmt(x):
    return f"{x:.2f}" if isinstance(x, float) and x == x else (str(x) if x == x else "n/a")


def wilson(k, n, z=1.96):
    """Wilson score 95% interval for a proportion k/n. Returns (lo, hi) or None if n==0.

    Preferred over the normal approximation at the small per-cell n (<=60 here) the
    small-sample reporting rule calls for: it stays inside [0,1] and does not collapse
    to a zero-width interval at k==0 or k==n."""
    if n == 0:
        return None
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, center - margin), min(1.0, center + margin))


def ci_line(label, k, n):
    """One 'metric  k/n = 0.83  [0.61, 0.94]' line, counts first per the small-n rule."""
    iv = wilson(k, n)
    if iv is None:
        return f"  {label:<22} {'n/a':>9}  (n=0)"
    return f"  {label:<22} {k:>3}/{n:<3} = {k/n:.2f}  [{iv[0]:.2f}, {iv[1]:.2f}]"


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(1)

    inspect = False
    want_ci = False
    inspect_chars = 600
    paths = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--inspect":
            inspect = True
            if i + 1 < len(args) and args[i + 1].isdigit():
                inspect_chars = int(args[i + 1]); i += 1
        elif a == "--ci":
            want_ci = True
        else:
            paths.append(a)
        i += 1

    rows = load(paths)
    if not rows:
        print("No rows found."); sys.exit(1)

    by_rev = defaultdict(list)
    for r in rows:
        by_rev[r.get("reviewer", "?")].append(r)

    cols = ["reviewer", "n", "exact_acc", "recall", "specificity", "precision", "f1", "errors"]
    print(f"{'reviewer':<10}{'n':>4}{'exact':>8}{'recall':>8}{'spec':>7}{'prec':>7}{'f1':>7}{'ruleID':>8}{'err':>5}")
    print("-" * 64)
    for rev in sorted(by_rev):
        s = score(by_rev[rev])
        print(f"{rev:<10}{s['n']:>4}{fmt(s['exact_acc']):>8}{fmt(s['recall']):>8}"
              f"{fmt(s['specificity']):>7}{fmt(s['precision']):>7}{fmt(s['f1']):>7}{fmt(s['ruleid']):>8}{s['errors']:>5}")

    # counts + Wilson 95% CIs for the headline proportions, per the small-n rule
    if want_ci:
        print("\nCounts and Wilson 95% CIs (counts first; proportions are small-n):")
        for rev in sorted(by_rev):
            s = score(by_rev[rev])
            print(f"\n[{rev}]  n={s['n']}  errors={s['errors']}")
            print(ci_line("recall (tp/tp+fn)", s["tp"], s["tp"] + s["fn"]))
            print(ci_line("specificity (tn/tn+fp)", s["tn"], s["tn"] + s["fp"]))
            print(ci_line("precision (tp/tp+fp)", s["tp"], s["tp"] + s["fp"]))
            flagged = s["tp"] + s["fp"]
            attributed = round(s["ruleid"] * flagged) if flagged and s["ruleid"] == s["ruleid"] else 0
            print(ci_line("rule-ID attribution", attributed, flagged))

    # per-case disagreement detail across reviewers, if more than one reviewer present
    if len(by_rev) > 1:
        print("\nPer-case verdicts:")
        by_case = defaultdict(dict)
        gold = {}
        for r in rows:
            by_case[r["case_id"]][r.get("reviewer", "?")] = r["got"]
            gold[r["case_id"]] = r["expected"]
        revs = sorted(by_rev)
        head = f"{'case':<34}{'gold':>6}  " + "  ".join(f"{rv:>8}" for rv in revs)
        print(head); print("-" * len(head))
        for cid in sorted(by_case):
            cells = "  ".join(f"{by_case[cid].get(rv,'-'):>8}" for rv in revs)
            print(f"{cid:<34}{gold[cid]:>6}  {cells}")

    if inspect:
        print("\nPer-case detail:")
        for r in rows:
            print(f"\n  case        {r['case_id']}")
            print(f"  reviewer    {r.get('reviewer','?')}")
            print(f"  expected    {r['expected']}")
            print(f"  got         {r['got']}")
            print(f"  gold_clauses {r.get('gold_clauses', [])}")
            print(f"  rule_ids    {r.get('rule_ids', [])}")
            snippet = (r.get("output", "") or "").strip().replace("\r", "")
            if snippet:
                if len(snippet) > inspect_chars:
                    snippet = snippet[:inspect_chars] + "\n  ... [truncated]"
                indented = "\n".join("    " + ln for ln in snippet.splitlines())
                print(f"  output:\n{indented}")


if __name__ == "__main__":
    main()
