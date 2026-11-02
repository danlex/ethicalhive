# Does the clause judge help? Six hard suites, n=60 per condition

Run 2026-10-28 to 11-02 on the six adversarial "hard" suites (anchoring, capitulation,
scope-creep, selective-evidence, source-fabrication, sycophancy), ten cases each,
through `run-conditions.sh` on sonnet. Six reviewer conditions, built as an ablation
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
- **judge-ctx**: the per-clause judge's decomposed task (verdict on one clause) but with
  all fourteen clauses in context, matched to mono-rid's context length. Separates the
  decomposition from the context-length confound.

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
| mono-rid (named clause list, bulk task) | 32/32 = 1.00 [0.89, 1.00] | 10/28 = 0.36 [0.21, 0.54] | 31/50 = 0.62 [0.48, 0.74] |
| judge-ctx (all 14 in context, decide one) | 32/32 = 1.00 [0.89, 1.00] | 21/28 = 0.75 [0.57, 0.87] | 32/39 = 0.82 [0.67, 0.91] |
| **judge (one clause per call)** | 32/32 = 1.00 [0.89, 1.00] | 23/28 = 0.82 [0.64, 0.92] | 32/37 = 0.86 [0.72, 0.94] |

## What the ladder shows

- **Every audit catches every real problem: recall 1.00** [0.89, 1.00] in all five
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
- **The context-length confound, the main alternative tested and weakened.** The plain judge
  sees one short clause while mono-rid sees all fourteen, so its edge could have been focus or
  context length rather than the clause decomposition itself. The judge-ctx condition
  separates the two: it carries all fourteen clauses in context (matched to mono-rid) but
  renders its verdict on one clause (the judge's decomposed task). Holding context fixed at
  fourteen, the decomposed task scores 0.75 [0.57, 0.87] against the bulk task's 0.36
  [0.21, 0.54]. This weakens the explanation that the benefit came only from a shorter prompt;
  it does not prove decomposition is the sole cause. Holding the task fixed at one clause,
  shortening the context lifts specificity only from 0.75 to 0.82, a difference that with 28
  clean cases is imprecisely estimated. So the ladder points to decomposition as the main
  ingredient rather than context length, with that one alternative addressed, not every one.

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
over-flagged draft moves specificity by 0.20 to 0.25 (four or five clean cases per suite); read the per-suite numbers as
direction, not as separated estimates.

## Reading

The headline is sharper than "the catalogue helps," and more useful. At equal recall on
adversarial cases, handing a reviewer the whole obligation set at once (as a checklist or
a named clause list) makes it over-flag clean drafts, worse than giving it no catalogue.
The gain comes from decomposing the review to one obligation per call, which is what the
per-clause judge does. That isolates the load-bearing design choice and reframes the
contribution: it is not the catalogue as a prompt ingredient, it is the catalogue as a set
of separately auditable units. The claim is bounded, not a dominance or state-of-the-art
claim: the judge wins on four of six behaviours, ties or loses on two, and the
judge-versus-freeform specificity interval still touches. The context-length confound that
earlier qualified this has now been tested with the judge-ctx condition and weakened: the
benefit largely survives when context is held constant, so the main ingredient is the
decomposition, not a shorter prompt. The defensible claim is narrow: on this 60-case
evaluation, clause-focused review produced fewer false alarms than bulk review while
retaining detection of all positive cases.

## Open issues (from independent review)

These bound the result and are the next steps before it is a claim rather than a signal.

- **Clause routing is privileged information.** The judge is run on the clause for the case's
  gold mode, so it is told which obligation to check, while the bulk reviewers are not. This
  demonstrates review with a known target, not general auditing. The honest end-to-end test
  runs all fourteen clauses (or a router) on every draft and reports the draft-level flag rate
  under the real aggregation rule; individual clauses can each be specific while their union
  over-flags.
- **A missing arm isolates the catalogue from generic decomposition.** We have not run "one
  unnamed obligation per call, otherwise matched to the judge." Without it, generic task
  decomposition may explain the gain, and the catalogue's names, inventory, and graph may add
  nothing to this particular result.
- **The attribution denominators mix attribution with false-alarm control.** mono-rid 31/50 and
  judge 32/37 use all flagged cases; both detect 32 positives, so conditional attribution
  among true-positive flags is about 31/32 versus 32/32. Report flag precision and correct
  attribution separately.
- **The analysis should be paired.** The conditions score the same cases, so overlapping Wilson
  intervals are not the right test of the difference; case-level paired outcomes and a paired
  test are needed, and "clearly helps on four behaviours" should read "improved observed
  specificity on four suites."

## Reproduce

Regenerate with:

```
bash experiments/run-conditions.sh experiments/cases/suite-<behavior>-hard.json \
     --reviewers none,freeform,checklist,mono-rid,judge,judge-ctx --model sonnet
python3 experiments/metrics.py experiments/results/run-suite-*-hard-*-<ts>.jsonl --ci
```

Note on the runs: both the judge and the checklist conditions lost cases to a provider
session limit when run last in a batch (the quota is shared), and were re-run after the
limit reset. The figures above are from the completed, error-free set (0 invalid verdicts
in every condition), pooling the newest clean file per suite per condition.
