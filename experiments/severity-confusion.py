#!/usr/bin/env python3
"""Build the SHIP/REVISE/BLOCK confusion matrix for the per-clause judge.

Reusable per `contracts/paper-writing-contract.md` PAP-WORK-06. Reads the
latest clean judge JSONL per mode (hard suite) and reports the gold vs
predicted confusion matrix per mode and aggregated across modes.

Usage:
    .venv/bin/python experiments/severity-confusion.py
    .venv/bin/python experiments/severity-confusion.py --suite easy   # easy suites
    .venv/bin/python experiments/severity-confusion.py --reviewer freeform

The output exposes severity calibration (REVISE vs BLOCK over-grade)
explicitly, which is what the paper's §7 names as the main contract-
design failure. The aggregate matrix is the one the paper cites.
"""
from __future__ import annotations
import argparse
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import metrics  # noqa: E402

RESULTS = HERE / "results"

LABELS = ["SHIP", "REVISE", "BLOCK"]

MODES = [
    ("SEL", "Selective evidence",  "selective-evidence"),
    ("SCP", "Scope creep",         "scope-creep"),
    ("CAP", "Capitulation",        "capitulation"),
    ("ANC", "Anchoring",           "anchoring"),
    ("SYC", "Sycophancy",          "sycophancy"),
    ("SRC", "Source fabrication",  "source-fabrication"),
]


def latest_clean(stem: str, reviewer: str) -> Path | None:
    """Pick the most recent JSONL for (mode, reviewer) with no parse errors."""
    candidates = sorted(RESULTS.glob(f"run-suite-{stem}-{reviewer}-*.jsonl"))
    for fn in reversed(candidates):
        rows = metrics.load([str(fn)])
        if rows and not any(r["got"] not in metrics.VALID for r in rows):
            return fn
    return candidates[-1] if candidates else None


def confusion(rows) -> Counter:
    """Return a Counter keyed by (gold, predicted)."""
    c: Counter = Counter()
    for r in rows:
        c[(r["expected"], r["got"])] += 1
    return c


def fmt_matrix(c: Counter, title: str) -> str:
    out = [title, "-" * len(title)]
    header = f"{'gold \\ pred':<14}" + "".join(f"{p:>8}" for p in LABELS) + f"{'total':>8}"
    out.append(header)
    out.append("-" * len(header))
    grand = 0
    col_totals = {p: 0 for p in LABELS}
    for g in LABELS:
        row_total = 0
        cells = []
        for p in LABELS:
            v = c.get((g, p), 0)
            cells.append(f"{v:>8}")
            row_total += v
            col_totals[p] += v
        out.append(f"{g:<14}" + "".join(cells) + f"{row_total:>8}")
        grand += row_total
    out.append("-" * len(header))
    totals_row = f"{'total':<14}" + "".join(f"{col_totals[p]:>8}" for p in LABELS) + f"{grand:>8}"
    out.append(totals_row)
    # diagonal accuracy
    diag = sum(c.get((l, l), 0) for l in LABELS)
    if grand:
        out.append(f"diagonal: {diag}/{grand} = {diag/grand:.2f}")
    return "\n".join(out)


def severity_summary(c: Counter) -> str:
    """Specifically: REVISE-vs-BLOCK confusion, the named open problem."""
    revise_block = c.get(("REVISE", "BLOCK"), 0)
    block_revise = c.get(("BLOCK", "REVISE"), 0)
    revise_revise = c.get(("REVISE", "REVISE"), 0)
    block_block = c.get(("BLOCK", "BLOCK"), 0)
    rev_total = revise_block + revise_revise + c.get(("REVISE", "SHIP"), 0)
    blk_total = block_revise + block_block + c.get(("BLOCK", "SHIP"), 0)
    lines = [
        "Severity calibration on the flag cases:",
        f"  gold REVISE: {revise_revise} correct REVISE, {revise_block} over-graded to BLOCK, "
        f"{c.get(('REVISE','SHIP'),0)} missed as SHIP (n={rev_total})",
        f"  gold BLOCK:  {block_block} correct BLOCK, {block_revise} under-graded to REVISE, "
        f"{c.get(('BLOCK','SHIP'),0)} missed as SHIP (n={blk_total})",
    ]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite", choices=["easy", "hard", "both"], default="hard")
    ap.add_argument("--reviewer", default="judge",
                    help="freeform / contract / judge / none (default judge)")
    args = ap.parse_args()

    suites = ["easy", "hard"] if args.suite == "both" else [args.suite]
    all_rows = []

    for suite in suites:
        print(f"\n=== suite: {suite} | reviewer: {args.reviewer} ===\n")
        for label, name, stem in MODES:
            stem_full = f"{stem}-hard" if suite == "hard" else stem
            fn = latest_clean(stem_full, args.reviewer)
            if fn is None:
                print(f"  {label}: no result file found for {stem_full}/{args.reviewer}")
                continue
            rows = metrics.load([str(fn)])
            all_rows.extend(rows)
            c = confusion(rows)
            print(fmt_matrix(c, f"{label} ({name}) - {fn.name}"))
            print()

    if all_rows:
        agg = confusion(all_rows)
        print("\n=== aggregate (all selected suites + modes) ===\n")
        print(fmt_matrix(agg, "Aggregate confusion"))
        print()
        print(severity_summary(agg))


if __name__ == "__main__":
    main()
