# Does the clause judge help? Six hard suites, n=60 per condition

Run 2026-10-28 to 11-01 on the six adversarial "hard" suites (anchoring, capitulation,
scope-creep, selective-evidence, source-fabrication, sycophancy), ten cases each,
through `run-conditions.sh` on sonnet. Five reviewer conditions, built as an ablation
ladder that adds one ingredient at a time, so we can see which ingredient carries any
benefit:

- **none**: no audit; every draft treated as shipped. The base rate.
- **freeform**: plain "review this draft for problems", no obligations, no clauses.
- **checklist**: the same integrity obligations in plain language, but with no named
  modes and no rule IDs. Tests whether having the obligations is what helps.
- **mono-rid**: one monolithic reviewer handed the full 14 named clauses with rule IDs.
  Tests whether naming the obligations is what helps. The fair baseline for attribution.
- **judge**: the per-clause judge, one clause per call (`judges/<mode>-judge.md`).
  Tests whether per-clause decomposition is what helps. The method under test.

Scored with `metrics.py --ci`. Flag = REVISE or BLOCK; recall is catching the gold
flag, specificity is leaving gold-SHIP drafts alone, rule-ID attribution is whether a
flag cited the right `INT-*` clause. Proportions are reported as counts with Wilson
95% intervals, per the small-sample rule (n is 60 pooled, 10 per suite per cell).

## Pooled result (n=60 per condition)

Ordered as the ladder (each row adds one ingredient):

| condition | recall | specificity | rule-ID attribution |
|---|---|---|---|
| none | 0/32 = 0.00 [0.00, 0.11] | 28/28 = 1.00 [0.88, 1.00] | n/a |
| freeform (no structure) | 32/32 = 1.00 [0.89, 1.00] | 16/28 = 0.57 [0.39, 0.73] | 1/44 = 0.02 [0.00, 0.12] |
| checklist (obligations, no names) | 32/32 = 1.00 [0.89, 1.00] | 9/28 = 0.32 [0.18, 0.51] | 0/51 = 0.00 [0.00, 0.07] |
| mono-rid (named clause list) | 32/32 = 1.00 [0.89, 1.00] | 10/28 = 0.36 [0.21, 0.54] | 31/50 = 0.62 [0.48, 0.74] |
| **judge (one clause per call)** | 32/32 = 1.00 [0.89, 1.00] | 23/28 = 0.82 [0.64, 0.92] | 32/37 = 0.86 [0.72, 0.94] |

## What the ladder shows

- **Every audit catches every real problem: recall 1.00** [0.89, 1.00] in all four
  audited conditions. The hard suites discriminate on specificity (not over-flagging
  clean drafts), not on recall.
- **The benefit is not the catalogue content, and it is not the names.** Giving a
  reviewer the obligations as a bulk checklist is the worst audit of all on specificity
  (0.32), below plain freeform review (0.57). Adding the names and rule IDs on top
  (mono-rid, 0.36) does not recover it. Both bulk-catalogue conditions over-flag clean
  drafts worse than a reviewer given no catalogue at all. More catalogue in the prompt
  made the audit worse, not better.
- **The one ingredient that helps is per-clause decomposition.** Only the judge, which
  sees one clause per call, beats plain review on specificity (0.82 [0.64, 0.92] vs
  0.57 [0.39, 0.73]) while also attributing almost every flag to the right rule (0.86 vs
  0.02 for freeform and 0 for the checklist, which has no names by construction). The
  judge-versus-mono-rid specificity gap does not overlap (0.82 [0.64, 0.92] vs 0.36
  [0.21, 0.54]); the judge-versus-freeform specificity gap is suggestive but its
  intervals touch.
- **A confound we cannot rule out at this design.** The judge sees one short clause; the
  checklist and mono-rid conditions see all fourteen obligations at once. So part of the
  judge's edge may be focus or context length, not the clause abstraction itself. What
  the ladder does establish is narrower and still useful: a reviewer handed the whole
  obligation set at once over-flags, and decomposing the review to one obligation at a
  time is what recovers and then exceeds plain-review specificity.

## What does not hold (the honest caveat)

The pooled specificity edge is **not uniform across suites**. Per suite, judge
specificity is a perfect 1.00 on four of the six (anchoring, capitulation,
scope-creep, selective-evidence), and it is carried by those:

| suite | freeform | checklist | mono-rid | judge |
|---|---|---|---|---|
| anchoring | 4/5 | 2/5 | 1/5 | 5/5 |
| capitulation | 4/5 | 2/5 | 2/5 | 5/5 |
| scope-creep | 1/4 | 0/4 | 0/4 | 4/4 |
| selective-evidence | 1/4 | 1/4 | 1/4 | 4/4 |
| source-fabrication | 3/5 | 3/5 | **4/5** | 3/5 |
| sycophancy | **3/5** | 1/5 | 2/5 | 2/5 |

The judge reaches perfect specificity on four of the six (anchoring, capitulation,
scope-creep, selective-evidence) and the pooled edge is carried by those. On
**source-fabrication** mono-rid beats the judge (4/5 vs 3/5), and on **sycophancy**
freeform beats it (3/5 vs 2/5). So the result is not "the clause judge dominates": it is
"the clause judge clearly helps on four of these six hard behaviours and does not win on
the other two." The checklist column makes the bulk-catalogue penalty visible per suite:
it matches or trails freeform on every suite. Each suite is ten cases, so a single
over-flagged draft moves specificity by 0.1 to 0.2; read the per-suite numbers as
direction, not as separated estimates.

## Reading

The headline is sharper than "the catalogue helps," and more useful. At equal recall on
adversarial cases, handing a reviewer the whole obligation set at once (as a checklist or
a named clause list) makes it over-flag clean drafts, worse than giving it no catalogue.
The gain comes from decomposing the review to one obligation per call, which is what the
per-clause judge does. That isolates the load-bearing design choice and reframes the
contribution: it is not the catalogue as a prompt ingredient, it is the catalogue as a set
of separately auditable units. The claim is bounded, not a dominance or state-of-the-art
claim: the judge wins on four of six behaviours, ties or loses on two, the
judge-versus-freeform specificity interval still touches, and a context-length confound
remains (one clause versus fourteen). The honest next steps are a context-matched judge
variant (one clause per call but with the other thirteen also in context) to remove that
confound, repeats to tighten the intervals, and understanding the source-fabrication and
sycophancy failures.

## Reproduce

Regenerate with:

```
bash experiments/run-conditions.sh experiments/cases/suite-<behavior>-hard.json \
     --reviewers none,freeform,checklist,mono-rid,judge --model sonnet
python3 experiments/metrics.py experiments/results/run-suite-*-hard-*-<ts>.jsonl --ci
```

Note on the runs: both the judge and the checklist conditions lost cases to a provider
session limit when run last in a batch (the quota is shared), and were re-run after the
limit reset. The figures above are from the completed, error-free set (0 invalid verdicts
in every condition), pooling the newest clean file per suite per condition.
