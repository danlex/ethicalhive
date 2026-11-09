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

Numbers are computed by `metrics.score()` from the files in the pinned run
manifest, after hash, reviewer and case validation. New result files do not
change a released figure until a new manifest is explicitly selected. The
attribution chart uses exact full rule IDs on true-positive flags.
"""
from __future__ import annotations
import sys
import argparse
import os
import tempfile
from pathlib import Path

_cache=Path(tempfile.gettempdir())/'ethicalai-paper-cache'
_cache.mkdir(exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR',str(_cache/'matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(_cache))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Make experiments/metrics.py importable.
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import metrics  # noqa: E402
from research_runs import DEFAULT_MANIFEST, result_path

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


def latest_clean_result(stem: str, reviewer: str,manifest=DEFAULT_MANIFEST) -> Path | None:
    """Legacy entry point: return the pinned result after hash/row checks."""
    return result_path(stem,reviewer,manifest=manifest)


def collect(manifest=DEFAULT_MANIFEST) -> dict[str, dict[str, dict[str, float]]]:
    """Return {mode_label: {reviewer: {exact, recall, spec, ruleid}}}."""
    out: dict[str, dict[str, dict[str, float]]] = {}
    for label, _name, stem in MODES:
        out[label] = {}
        for rev in REVIEWERS:
            fn = latest_clean_result(stem, rev,manifest)
            if fn is None:
                out[label][rev] = dict(exact=float("nan"), spec=float("nan"),
                                        ruleid=float("nan"))
                continue
            rows = metrics.load([str(fn)])
            s = metrics.score(rows)
            out[label][rev] = dict(exact=s["exact_acc"], spec=s["specificity"],
                                    ruleid=s['exact_rule_tp_attribution'], source=fn.name)
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
    fig.savefig(OUT_DIR / outfile, bbox_inches="tight",
                metadata={'CreationDate':None,'ModDate':None})
    plt.close(fig)
    print(f"wrote {OUT_DIR / outfile}")


def main() -> None:
    global OUT_DIR
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,default=DEFAULT_MANIFEST)
    parser.add_argument('--output-dir',type=Path,default=OUT_DIR)
    args=parser.parse_args();OUT_DIR=args.output_dir
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = collect(args.manifest)

    # Echo the numbers we used, with file provenance, so the figure inputs are auditable.
    print("Hard-suite metrics (computed from JSONL):\n")
    header = f"{'mode':<5}{'reviewer':<12}{'exact':>7}{'spec':>7}{'exactRule/TP':>13}  source"
    print(header)
    print("-" * len(header))
    for label, _name, _stem in MODES:
        for rev in REVIEWERS:
            d = data[label][rev]
            src = d.get("source", "n/a")
            print(f"{label:<5}{rev:<12}{d['exact']:>7.2f}{d['spec']:>7.2f}"
                  f"{d['ruleid']:>13.2f}  {src}")
        print()

    grouped_bars(data, "spec", "Specificity",
                 "Specificity on hard suites by reviewer condition",
                 "spec-by-mode-hard.pdf")
    grouped_bars(data, "ruleid", "Exact rule match / true-positive flags",
                 "Exact-rule attribution on hard suites by reviewer condition",
                 "ruleid-by-mode-hard.pdf")
    grouped_bars(data, "exact", "Exact-verdict accuracy",
                 "Exact-verdict accuracy on hard suites by reviewer condition",
                 "exact-by-mode-hard.pdf")


if __name__ == "__main__":
    main()
