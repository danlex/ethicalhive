# EthicalAI experiment harness

The benchmark + runner + writeups behind the EthicalAI workshop paper. Direction and citations
in [`../paper/proposal.md`](../paper/proposal.md); binding writing standard in
[`../contracts/paper-writing-contract.md`](../contracts/paper-writing-contract.md).

## What lives here

```
experiments/
├── run-suite.sh              # per-(suite, reviewer) runner; the four reviewer conditions
├── run-conditions.sh         # reusable wrapper: all reviewers x all suites + score (PAP-WORK-06)
├── metrics.py                # exact, recall, specificity, precision, F1, rule-ID attribution
├── baseline-freeform-prompt.md   # the free-form reviewer's prompt for the baseline condition
├── cases/                    # clause-labeled benchmark suites per mode
│   ├── suite-selective-evidence.json
│   ├── suite-selective-evidence-hard.json
│   ├── suite-scope-creep.json
│   ├── suite-scope-creep-hard.json
│   ├── suite-source-fabrication.json
│   ├── suite-source-fabrication-hard.json
│   ├── suite-capitulation.json
│   ├── suite-capitulation-hard.json
│   └── suite-scope-creep-smoke.json     # 1-case multi-mode validation
├── results/                  # JSONL audit-run records (one row per case-x-reviewer)
├── seed-selective-evidence.md   # mode writeup: 4-way comparison + analysis
├── seed-scope-creep.md
└── README.md                 # this file
```

## The four reviewer conditions

| `--reviewer` | What it is | Notes |
|---|---|---|
| `none` | No audit; every draft ships. Measures base rate. | No model call. Specificity 1.0 by construction, recall 0 by construction. |
| `freeform` | Plain "review this draft for problems" baseline. Same model, no contract, no clauses. | The honest baseline `references/prior-art.md` demands. |
| `contract` | The legacy v5 `tvl-tech-bias-validator` (CoVe + 5-check rubric). | Kept for comparison. Not contract-grounded; emits no `INT-*` rule IDs. |
| **`judge`** | Routes each case to `judges/<mode>-judge.md`. Emits `Clause: INT-XXX` + tags findings with the specific rule ID. | The method under test. |

## How to run

The reusable runner sweeps all four reviewers on each suite and scores per suite:

```bash
bash experiments/run-conditions.sh \
    experiments/cases/suite-selective-evidence.json \
    experiments/cases/suite-selective-evidence-hard.json
```

Optional flags: `--model sonnet|haiku|opus` (default `sonnet`), `--reviewers none,freeform,contract,judge` (default all four).

Single-condition runs (rarely needed) go through `run-suite.sh` directly:

```bash
bash experiments/run-suite.sh experiments/cases/suite-foo.json --reviewer judge --model sonnet
```

Score a result file (or a glob) with `metrics.py`:

```bash
python3 experiments/metrics.py experiments/results/run-suite-foo-*.jsonl
python3 experiments/metrics.py experiments/results/run-suite-foo-*.jsonl --inspect 600
```

The `--inspect [N]` flag prints per-case detail (reviewer, expected, got, gold_clauses,
rule_ids cited, and the first N characters of the reviewer's output). Useful for confirming
rule-ID emission without hand-bundled inspection scripts (PAP-WORK-06).

## How to add a new mode

The clause judges and the harness work over any suite that follows the schema. To add a new
mode (`<mode>`):

1. Pick a clause from `contracts/ai-integrity-contract.md` (e.g. `INT-ANC` for Anchoring).
2. Confirm the corresponding judge exists in `judges/<mode>-judge.md` and emits its
   `Clause: INT-XXX` + rule IDs (all 14 do as of commit `0c4c691`).
3. Author `experiments/cases/suite-<mode>.json` and `experiments/cases/suite-<mode>-hard.json`
   following the existing shape: `{id, mode, user_ask, draft, evidence[],
   expected{verdict, rationale}, gold_clauses[], provenance}`. Aim for ~40 percent clean
   cases to measure specificity, and include at least one minimal pair (same ask, omit vs
   disclose) to test that the judge keys on the omission itself.
4. Run via `run-conditions.sh`; write a `experiments/seed-<mode>.md` describing what the
   numbers showed, what they did not, and what they imply for the paper.

For modes that need conversational context (e.g. Capitulation), embed it in `user_ask`; no
schema or runner change is needed.

## Seed results so far

| Mode | Hard suite specificity (judge vs freeform vs v5) | ruleID (judge vs others) | Writeup |
|---|---|---|---|
| Selective Evidence (`INT-SEL`) | 1.00 vs 0.50 vs 0.50 | 1.00 vs 0.00 | [seed-selective-evidence.md](seed-selective-evidence.md) |
| Scope Creep (`INT-SCP`) | 1.00 vs 0.50 vs **0.00** | 1.00 vs 0.00 | [seed-scope-creep.md](seed-scope-creep.md) |
| Source Fabrication (`INT-SRC`) | pending (sweep) | pending | pending |
| Capitulation (`INT-CAP`) | pending (queued) | pending | pending |

Severity calibration (REVISE vs BLOCK) is the consistent open problem across modes: free-form
under-grades, the clause judge over-grades on REVISE boundary cases.
