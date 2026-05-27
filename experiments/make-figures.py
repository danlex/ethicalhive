#!/usr/bin/env python3
"""Generate the workshop paper's headline figures from result JSONLs.

Reusable per `contracts/paper-writing-contract.md` PAP-WORK-06: figure
generation is one of the operations the contract names. Run via the project
venv:

    bash experiments/setup-venv.sh
    source .venv/bin/activate
    python experiments/make-figures.py

Outputs to paper/figures/:
    spec-by-mode-hard.pdf   bar chart of specificity, hard suites, by reviewer
    ruleid-by-mode-hard.pdf bar chart of rule-ID attribution, hard suites
    exact-by-mode-hard.pdf  bar chart of exact-verdict accuracy, hard suites

Numbers are computed by `metrics.score()` directly from the latest
`run-suite-<mode>-hard-<reviewer>-*.jsonl` per (mode, reviewer). Single source
of truth: the JSONL files. No transcription, no manual table. To regenerate
after a new mode is run, drop new result files into `experiments/results/`
and add the mode to MODES.
"""
from __future__ import annotations
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Make experiments/metrics.py importable.
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import metrics  # noqa: E402

RESULTS = HERE / "results"
OUT_DIR = HERE.parent / "paper" / "figures"

MODES = [
    # (short label, full name, suite stem used in result filenames)
    ("SEL", "Selective evidence",  "selective-evidence-hard"),
    ("SCP", "Scope creep",         "scope-creep-hard"),
    ("CAP", "Capitulation",        "capitulation-hard"),
    ("ANC", "Anchoring",           "anchoring-hard"),
    ("SYC", "Sycophancy",          "sycophancy-hard"),
    ("SRC", "Source fabrication",  "source-fabrication-hard"),
]

REVIEWERS = ["none", "freeform", "contract", "judge"]
DISPLAY   = ["none", "freeform", "contract (v5)", "judge (clauses)"]
COLORS    = ["#bbbbbb", "#4c9be8", "#f0a04b", "#3a8a4b"]


def latest_clean_result(stem: str, reviewer: str) -> Path | None:
    """Pick the most recent `.jsonl` for this (mode, reviewer) that has no
    parse errors. A session-limit hit produces PARSE_ERROR rows; we want the
    re-run, not the failed first attempt."""
    candidates = sorted(RESULTS.glob(f"run-suite-{stem}-{reviewer}-*.jsonl"))
    for fn in reversed(candidates):
        rows = metrics.load([str(fn)])
        if rows and not any(r["got"] not in metrics.VALID for r in rows):
            return fn
    return candidates[-1] if candidates else None


def collect() -> dict[str, dict[str, dict[str, float]]]:
    """Return {mode_label: {reviewer: {exact, recall, spec, ruleid}}}."""
    out: dict[str, dict[str, dict[str, float]]] = {}
    for label, _name, stem in MODES:
        out[label] = {}
        for rev in REVIEWERS:
            fn = latest_clean_result(stem, rev)
            if fn is None:
                out[label][rev] = dict(exact=float("nan"), spec=float("nan"),
                                        ruleid=float("nan"))
                continue
            rows = metrics.load([str(fn)])
            s = metrics.score(rows)
            out[label][rev] = dict(exact=s["exact_acc"], spec=s["specificity"],
                                    ruleid=s["ruleid"], source=fn.name)
    return out


def grouped_bars(data: dict, metric_key: str, ylabel: str, title: str,
                 outfile: str, ymax: float = 1.05) -> None:
    labels = [row[0] for row in MODES]
    n_groups = len(labels)
    n_bars   = len(REVIEWERS)
    width    = 0.18
    x = np.arange(n_groups)

    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    for j, rev in enumerate(REVIEWERS):
        ys = []
        nan_ix = []
        for i in range(n_groups):
            v = data[labels[i]][rev][metric_key]
            if v != v:  # NaN
                ys.append(0)
                nan_ix.append(i)
            else:
                ys.append(v)
        bars = ax.bar(x + (j - (n_bars - 1) / 2) * width, ys, width,
                      label=DISPLAY[j], color=COLORS[j],
                      edgecolor="black", linewidth=0.4)
        for i in nan_ix:
            ax.text(bars[i].get_x() + bars[i].get_width() / 2, 0.02, "n/a",
                    ha="center", va="bottom", fontsize=7, color="#666")

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, ymax)
    ax.set_title(title, fontsize=11)
    ax.legend(loc="lower right", fontsize=8, frameon=False, ncol=2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle=":", linewidth=0.5, alpha=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(OUT_DIR / outfile, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {OUT_DIR / outfile}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = collect()

    # Echo the numbers we used, with file provenance, so the figure inputs are auditable.
    print("Hard-suite metrics (computed from JSONL):\n")
    header = f"{'mode':<5}{'reviewer':<12}{'exact':>7}{'spec':>7}{'ruleID':>8}  source"
    print(header)
    print("-" * len(header))
    for label, _name, _stem in MODES:
        for rev in REVIEWERS:
            d = data[label][rev]
            src = d.get("source", "n/a")
            print(f"{label:<5}{rev:<12}{d['exact']:>7.2f}{d['spec']:>7.2f}"
                  f"{d['ruleid']:>8.2f}  {src}")
        print()

    grouped_bars(data, "spec", "Specificity",
                 "Specificity on hard suites by reviewer condition",
                 "spec-by-mode-hard.pdf")
    grouped_bars(data, "ruleid", "Rule-ID attribution",
                 "Rule-ID attribution on hard suites by reviewer condition",
                 "ruleid-by-mode-hard.pdf")
    grouped_bars(data, "exact", "Exact-verdict accuracy",
                 "Exact-verdict accuracy on hard suites by reviewer condition",
                 "exact-by-mode-hard.pdf")


if __name__ == "__main__":
    main()
