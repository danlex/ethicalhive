#!/usr/bin/env python3
"""Print Table 2 (per-mode per-reviewer fractions) for the workshop paper.

Reusable per `contracts/paper-writing-contract.md` PAP-WORK-06. Reads the
manifest-selected JSONL per (mode, reviewer), computes exact / recall / spec /
family and exact-rule attribution with their actual denominators, and emits a
Markdown table ready to paste into paper/draft.md §5.

Fixes the Table 2 denominator bug caught by codex r4: hard-suite gold
splits are not all 5/0/5; SEL and SCP are 4 SHIP / 2 REVISE / 4 BLOCK,
the rest are 5 / 1 / 4.
"""
from __future__ import annotations
import sys
import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import metrics  # noqa: E402
from research_runs import DEFAULT_MANIFEST, result_path

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


def latest_clean(suite_stem: str, reviewer: str, manifest=DEFAULT_MANIFEST) -> Path | None:
    """Legacy entry point: select the verified manifest record."""
    return result_path(suite_stem, reviewer, manifest=manifest)


def fractions(rows):
    score = metrics.score(rows)
    return {
        "exact":    (score['exact'], score['n']),
        "recall":   (score['tp'], score['tp']+score['fn']),
        "spec":     (score['tn'], score['tn']+score['fp']),
        "rule_id":  (score['family_attributed'], score['flagged']),
        "exact_rule_tp": (score['exact_tp_attributed'], score['tp']),
    }


def fmt(num: int, den: int, na_if_zero: bool = False) -> str:
    if den == 0:
        return "n/a" if na_if_zero else "0/0"
    return f"{num}/{den}"


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,default=DEFAULT_MANIFEST)
    parser.add_argument('--suite',choices=['easy','hard'],default='hard')
    args=parser.parse_args()
    rows_md = []
    for label, stem in MODES:
        hard_stem = f"{stem}-hard" if args.suite=='hard' else stem
        per_reviewer = {}
        for rev in REVIEWERS:
            fn = latest_clean(hard_stem, rev,args.manifest)
            if fn is None:
                per_reviewer[rev] = None
                continue
            rows = metrics.load([str(fn)])
            per_reviewer[rev] = fractions(rows)
        for rev in REVIEWERS:
            d = per_reviewer[rev]
            if d is None:
                rows_md.append(f"| {label} | {DISPLAY[rev]} | n/a | n/a | n/a | n/a | n/a |")
                continue
            ex   = fmt(*d["exact"])
            rec  = fmt(*d["recall"])
            sp   = fmt(*d["spec"])
            rid  = fmt(*d['rule_id'],na_if_zero=True)
            exact_rule=fmt(*d['exact_rule_tp'],na_if_zero=True)
            rows_md.append(f"| {label} | {DISPLAY[rev]} | {ex} | {rec} | {sp} | {rid} | {exact_rule} |")

    print("| Mode | Reviewer | Exact | Recall | Spec | Family / all flags | Exact rule / TP flags |")
    print("|---|---|---|---|---|---|---|")
    for line in rows_md:
        print(line)
    print('\nAll files are pinned by the run manifest. Family overlap retains the legacy ruleid calculation; exact rule / TP flags requires at least one full gold identifier on a true-positive flag.')


if __name__ == "__main__":
    main()
