#!/usr/bin/env python3
"""Print Table 2 (per-mode per-reviewer fractions) for the workshop paper.

Reusable per `contracts/paper-writing-contract.md` PAP-WORK-06. Reads the
latest clean JSONL per (mode, reviewer), computes exact / recall / spec /
ruleID as raw fractions with their actual denominators, and emits a
Markdown table ready to paste into paper/draft.md §5.

Fixes the Table 2 denominator bug caught by codex r4: hard-suite gold
splits are not all 5/0/5; SEL and SCP are 4 SHIP / 2 REVISE / 4 BLOCK,
the rest are 5 / 1 / 4.
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import metrics  # noqa: E402

RESULTS = HERE / "results"

MODES = [
    ("SEL", "selective-evidence"),
    ("SCP", "scope-creep"),
    ("CAP", "capitulation"),
    ("ANC", "anchoring"),
    ("SYC", "sycophancy"),
    ("SRC", "source-fabrication"),
]
REVIEWERS = ["freeform", "contract", "mono-rid", "judge"]
DISPLAY = {
    "freeform": "freeform",
    "contract": "monolithic prose",
    "mono-rid": "monolithic + clauses",
    "judge":    "per-clause judge",
}

FLAG = {"REVISE", "BLOCK"}


def latest_clean(suite_stem: str, reviewer: str) -> Path | None:
    cands = sorted(RESULTS.glob(f"run-suite-{suite_stem}-{reviewer}-*.jsonl"))
    for fn in reversed(cands):
        rows = metrics.load([str(fn)])
        if rows and not any(r["got"] not in metrics.VALID for r in rows):
            return fn
    return cands[-1] if cands else None


def fractions(rows):
    n = len(rows)
    exact = sum(1 for r in rows if r["got"] == r["expected"])
    gold_flag = sum(1 for r in rows if r["expected"] in FLAG)
    gold_ship = sum(1 for r in rows if r["expected"] == "SHIP")
    tp = sum(1 for r in rows if r["expected"] in FLAG and r["got"] in FLAG)
    tn = sum(1 for r in rows if r["expected"] == "SHIP" and r["got"] == "SHIP")
    flagged = sum(1 for r in rows if r["got"] in FLAG)
    attrib = 0
    for r in rows:
        if r["got"] not in FLAG:
            continue
        rids = {x.split("-")[1] for x in r.get("rule_ids", []) if x.startswith("INT-")}
        gold = {x.split("-")[1] for x in r.get("gold_clauses", []) if x.startswith("INT-")}
        if rids & gold:
            attrib += 1
    return {
        "exact":    (exact, n),
        "recall":   (tp, gold_flag),
        "spec":     (tn, gold_ship),
        "rule_id":  (attrib, flagged),
    }


def fmt(num: int, den: int, na_if_zero: bool = False) -> str:
    if den == 0:
        return "n/a" if na_if_zero else "0/0"
    return f"{num}/{den}"


def main() -> None:
    rows_md = []
    for label, stem in MODES:
        hard_stem = f"{stem}-hard"
        per_reviewer = {}
        for rev in REVIEWERS:
            fn = latest_clean(hard_stem, rev)
            if fn is None:
                per_reviewer[rev] = None
                continue
            rows = metrics.load([str(fn)])
            per_reviewer[rev] = fractions(rows)
        for rev in REVIEWERS:
            d = per_reviewer[rev]
            if d is None:
                rows_md.append(f"| {label} | {DISPLAY[rev]} | n/a | n/a | n/a | n/a |")
                continue
            ex   = fmt(*d["exact"])
            rec  = fmt(*d["recall"])
            sp   = fmt(*d["spec"])
            rid  = fmt(*d["rule_id"], na_if_zero=True) if rev == "judge" else "0/n*"
            if rev == "mono-rid":
                rid = fmt(*d["rule_id"])
            rows_md.append(f"| {label} | {DISPLAY[rev]} | {ex} | {rec} | {sp} | {rid} |")

    print("| Mode | Reviewer | Exact | Recall | Spec | Rule-ID |")
    print("|---|---|---|---|---|---|")
    for line in rows_md:
        print(line)


if __name__ == "__main__":
    main()
