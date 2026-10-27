# Does the clause judge help? Six hard suites, n=60 per condition

Run 2026-10-28 on the six adversarial "hard" suites (anchoring, capitulation,
scope-creep, selective-evidence, source-fabrication, sycophancy), ten cases each,
through `run-conditions.sh` on sonnet. Four reviewer conditions:

- **none**: no audit; every draft treated as shipped. The base rate.
- **freeform**: plain "review this draft for problems", no contract, no clause list.
- **mono-rid**: one monolithic reviewer handed the 14-clause list and asked to cite
  rule IDs. The fair baseline for rule-ID attribution.
- **judge**: the per-clause judge for each case's mode (`judges/<mode>-judge.md`).
  The method under test.

Scored with `metrics.py --ci`. Flag = REVISE or BLOCK; recall is catching the gold
flag, specificity is leaving gold-SHIP drafts alone, rule-ID attribution is whether a
flag cited the right `INT-*` clause. Proportions are reported as counts with Wilson
95% intervals, per the small-sample rule (n is 60 pooled, 10 per suite per cell).

## Pooled result (n=60 per condition)

| condition | recall | specificity | precision | rule-ID attribution |
|---|---|---|---|---|
| none | 0/32 = 0.00 [0.00, 0.11] | 28/28 = 1.00 [0.88, 1.00] | n/a | n/a |
| freeform | 32/32 = 1.00 [0.89, 1.00] | 16/28 = 0.57 [0.39, 0.73] | 32/44 = 0.73 [0.58, 0.84] | 1/44 = 0.02 [0.00, 0.12] |
| mono-rid | 32/32 = 1.00 [0.89, 1.00] | 10/28 = 0.36 [0.21, 0.54] | 32/50 = 0.64 [0.50, 0.76] | 31/50 = 0.62 [0.48, 0.74] |
| **judge** | 32/32 = 1.00 [0.89, 1.00] | 23/28 = 0.82 [0.64, 0.92] | 32/37 = 0.86 [0.72, 0.94] | 32/37 = 0.86 [0.72, 0.94] |

## What holds

- **All three audits catch every real problem on these hard cases: recall 1.00**
  [0.89, 1.00] for freeform, mono-rid, and judge alike. The hard suites are hard on
  specificity (not over-flagging the clean drafts), not on recall.
- **At that equal, ceiling recall, the clause judge has the highest specificity and
  the highest rule-ID attribution.** Against mono-rid the specificity gap is the
  clearest signal in the run: 0.82 [0.64, 0.92] versus 0.36 [0.21, 0.54], intervals
  that do not overlap. Against freeform on rule-ID attribution the gap is also clean:
  0.86 [0.72, 0.94] versus 0.02 [0.00, 0.12] (freeform almost never cites a clause).
- The judge-versus-freeform **specificity** gap (0.82 vs 0.57) and the
  judge-versus-mono-rid **attribution** gap (0.86 vs 0.62) are suggestive but their
  intervals touch; they are not separated at this n.

## What does not hold (the honest caveat)

The pooled specificity edge is **not uniform across suites**. Per suite, judge
specificity is a perfect 1.00 on four of the six (anchoring, capitulation,
scope-creep, selective-evidence), and it is carried by those:

| suite | freeform spec | mono-rid spec | judge spec |
|---|---|---|---|
| anchoring | 0.80 | 0.20 | 1.00 |
| capitulation | 0.80 | 0.40 | 1.00 |
| scope-creep | 0.25 | 0.00 | 1.00 |
| selective-evidence | 0.25 | 0.25 | 1.00 |
| source-fabrication | 0.60 | **0.80** | 0.60 |
| sycophancy | **0.60** | 0.40 | 0.40 |

On **source-fabrication** mono-rid beats the judge (0.80 vs 0.60), and on
**sycophancy** freeform beats it (0.60 vs 0.40). So the result is not "the clause
judge dominates": it is "the clause judge clearly helps on four of these six hard
behaviors and does not win on the other two." Each suite is ten cases, so a single
over-flagged draft moves specificity by 0.1 to 0.2 and these per-suite numbers should
be read as direction, not as separated estimates.

## Reading

This points the way the seed runs suggested, with named exceptions: at equal recall
on adversarial cases, naming the specific clause a reviewer must check raises both how
often it leaves clean drafts alone and how often it attributes a flag to the right
rule, most strongly against the monolithic-clause-list baseline on specificity. It
does not establish dominance, and it is not state of the art. The honest next step for
a defensible claim is repeats (to tighten the per-suite intervals) and understanding
why the judge under-performs on source-fabrication and sycophancy specifically.

## Reproduce

File set pooled for this result is recorded in the commit; regenerate with:

```
bash experiments/run-conditions.sh experiments/cases/suite-<behavior>-hard.json \
     --reviewers none,freeform,mono-rid,judge --model sonnet
python3 experiments/metrics.py experiments/results/run-suite-*-hard-*-<ts>.jsonl --ci
```

Note on the run: the judge condition initially lost 18 of 60 cases to a provider
session limit (it runs last in each suite's sequence, so six parallel suites exhausted
the quota). Those were re-run after the limit reset; the figures above are from the
completed, error-free set (0 invalid verdicts in every condition).
