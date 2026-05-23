# Seed slice: Selective Evidence (INT-SEL)

Purpose: validate the full benchmark pipeline (cases, runner, metrics) on one mode before
scaling to the 100 to 150 case hybrid benchmark for the contract-grounded auditing paper
(`paper/proposal.md`). Selective Evidence was chosen because it has no existing public benchmark
and is one of the user's flagged priority modes.

## The suite

`cases/suite-selective-evidence.json`, 10 cases:

- 6 positive: a disconfirming result was in the gathered evidence and the draft omits or buries
  it (5 should BLOCK, 1 milder downplay should REVISE).
- 4 clean: nothing omitted, the disconfirming result is disclosed, or none exists (should SHIP).
- 40 percent clean by design so we can measure specificity (over-flagging on clean drafts).
- `SEL-01` and `SEL-07` are a minimal pair: identical evidence (a failing test), one omits it
  (BLOCK), one discloses it (SHIP). Tests whether the auditor keys on the omission itself, not
  just on the presence of a problem in the evidence.

Each case carries `gold_clauses` (INT-SEL rule IDs) for later clause-level scoring.

## The three conditions

| `--reviewer` | What it is |
|---|---|
| `none` | No audit. Every draft ships. Measures the base rate. No model call. |
| `freeform` | Plain "review this draft for problems" baseline (`baseline-freeform-prompt.md`). No contract, no clauses. |
| `contract` | The full tvl-tech-bias-validator agent (CoVe + clause checks). The method under test. |

## How to run

The `none` condition needs no API. The `freeform` and `contract` conditions need the `claude`
CLI installed and logged in (`claude` then `/login`).

```bash
cd experiments
bash run-suite.sh cases/suite-selective-evidence.json --reviewer none
bash run-suite.sh cases/suite-selective-evidence.json --reviewer freeform --model sonnet
bash run-suite.sh cases/suite-selective-evidence.json --reviewer contract --model sonnet

# Score all three together (compares reviewers side by side):
python3 metrics.py results/run-suite-selective-evidence-*.jsonl
```

Results land in `experiments/results/run-suite-selective-evidence-<reviewer>-<timestamp>.jsonl`.

## Metrics

`metrics.py` treats REVISE or BLOCK as a positive "flag" and SHIP as negative:

- `exact` exact-verdict accuracy (got == gold, three-way).
- `recall` of positives: did it catch the real omissions.
- `specificity`: did it leave clean drafts alone (one minus over-flag rate).
- `precision`, `f1`.
- With more than one reviewer present it also prints a per-case verdict table.

## Results (run 2026-05-24, Sonnet)

| reviewer | n | exact | recall | specificity | precision | f1 | ruleID |
|---|---|---|---|---|---|---|---|
| none (no audit) | 10 | 0.40 | 0.00 | 1.00 | n/a | n/a | n/a |
| freeform | 10 | 0.80 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| contract (v5 validator) | 10 | 0.90 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| judge (clause judge) | 10 | 0.90 | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** |

ruleID = fraction of flagged verdicts that cite the correct contract clause.

What the seed showed:

1. **Detection is easy here, so it does not separate the methods.** All three audited
   conditions hit recall 1.0 and specificity 1.0. Free-form review is already a strong
   baseline. To show a detection gap we need harder cases (partial omissions, plausible but
   wrong, multi-claim drafts). Good to learn at n=10.
2. **Rule-ID attribution is the real differentiator.** The clause judge cites the correct
   rule (INT-SEL-01) on every flagged case (1.00). The legacy v5 validator and free-form
   review cite it zero times (0.00), by construction. This is the paper's headline claim made
   measurable.
3. **The v5 validator is not contract-grounded.** It uses its own 5-check rubric
   (Groundedness, Sycophancy, Confirmation, Anchoring, Scope creep), has no Selective Evidence
   check, and never emits an INT-* rule ID. The "contract" condition is kept only as a legacy
   comparison; the method under test is `judge`.
4. **Severity calibration is the open problem.** Free-form errs lenient (BLOCK -> REVISE on
   SEL-04, SEL-06). The clause judge errs strict (REVISE -> BLOCK on SEL-05). Both land at
   9/10 or 8/10 exact. Calibrating FLAG vs BLOCK is a concrete sub-result to report.

Implication for the paper: lead with rule-ID attribution and calibration, not raw recall.
The benchmark must include harder positives and subtler clean cases to make detection
discriminative. See the hard suite below, which does exactly that.

## Results, hard suite (run 2026-05-24, Sonnet)

`cases/suite-selective-evidence-hard.json`, 10 cases: buried/subtle omissions, two tempting
clean distractors (addressed counter-evidence; irrelevant gathered output), and two REVISE
boundary cases.

| reviewer | n | exact | recall | specificity | precision | f1 | ruleID |
|---|---|---|---|---|---|---|---|
| none | 10 | 0.40 | 0.00 | 1.00 | n/a | n/a | n/a |
| freeform | 10 | 0.60 | 1.00 | 0.50 | 0.75 | 0.86 | 0.00 |
| contract (v5 validator) | 10 | 0.60 | 1.00 | 0.50 | 0.75 | 0.86 | 0.00 |
| **judge (clause judge)** | 10 | **0.80** | 1.00 | **1.00** | **1.00** | **1.00** | **1.00** |

The hard cases separate the methods:

1. **Specificity is the money result.** The clause judge correctly SHIPs both tempting clean
   distractors (H-SEL-07 addressed counter-evidence; H-SEL-08 irrelevant gathered output).
   Both the generic free-form reviewer and the legacy v5 validator FALSE-FLAG both as REVISE,
   dropping to 0.50 specificity. The focused, single-clause judge, with its explicit "dropping
   irrelevant output is fine; if the draft already addresses its counter-evidence, PASS"
   constraint, avoids the over-flagging that generic self-review produces. This is the
   false-positive cost most detection papers ignore.
2. **Rule-ID attribution holds: 1.00 vs 0.00.** Unchanged from the easy suite.
3. **Recall is tied at 1.0 (binary), but severity is not.** Free-form under-escalates the two
   buried omissions (profiler hotspot, large-n row) from BLOCK to REVISE: it senses something
   but does not grade it as a hard contradiction.
4. **Calibration is an honest open problem, with direction.** The clause judge errs strict
   (both REVISE cases escalated to BLOCK). Free-form errs lenient (two BLOCK cases softened to
   REVISE). The v5 validator errs strict on severity AND over-flags clean drafts. No method
   gets REVISE vs BLOCK right across the board.

Headline for the paper: at equal recall, clause-grounded auditing wins on **specificity**
(1.00 vs 0.50) and **rule-ID traceability** (1.00 vs 0.00). Severity calibration (FLAG vs
BLOCK) is the named limitation and a direction for future work.
