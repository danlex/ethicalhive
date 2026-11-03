# Does the clause judge help? Six hard suites, n=60 per condition

Run 2026-10-28 to 11-03 on the six adversarial "hard" suites (anchoring, capitulation,
scope-creep, selective-evidence, source-fabrication, sycophancy), ten cases each,
through `run-conditions.sh` on sonnet. Seven reviewer conditions, built as an ablation
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
- **judge-anon**: one UNNAMED plain obligation per call, otherwise matched to the judge.
  Separates the catalogue's named structure from generic task decomposition.

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
| judge (one NAMED clause per call) | 32/32 = 1.00 [0.89, 1.00] | 23/28 = 0.82 [0.64, 0.92] | 32/37 = 0.86 [0.72, 0.94] |
| **judge-anon (one UNNAMED obligation per call)** | 31/32 = 0.97 [0.84, 0.99] | 24/28 = 0.86 [0.69, 0.94] | 0/35 = 0.00 (no names) |

## What the ladder shows

- **Every audit catches nearly every real problem: recall 1.00** [0.89, 1.00] in the
  four bulk and named conditions (judge-anon is 0.97, one miss). The hard suites
  discriminate on specificity (not over-flagging clean drafts), not on recall.
- **Bulk review over-flags; the catalogue as a prompt makes it worse.** The obligations as
  a bulk checklist are the worst audit on specificity (0.32), below plain freeform review
  (0.57), and adding the names and rule IDs (mono-rid, 0.36) does not recover it. More
  catalogue in one prompt made the audit worse, not better.
- **The ingredient that lifts specificity is decomposition, not the catalogue's names.**
  Auditing one obligation per call recovers freeform specificity and trends above it (the
  paired test does not reach significance against freeform, p=0.092; see below). Crucially,
  this holds when the obligation is a plain, unnamed sentence: judge-anon scores 0.86
  [0.69, 0.94], matching the named judge's 0.82 [0.64, 0.92]. Stripping the catalogue down
  to one plain obligation per call costs essentially nothing on specificity. So the 207-mode
  inventory, the rule IDs, and the graph do not improve detection in this test; the general
  move of decomposing the review to one obligation at a time does.
- **What the named catalogue uniquely adds is traceability, not detection.** The named judge
  attributes almost every flag to the right rule (0.86), while the unnamed judge-anon and the
  freeform baseline cannot by construction (0 and 0.02). That is the catalogue's distinctive
  contribution here: a reviewer that can say which named obligation was breached and cite a
  stable rule ID, which a plain-obligation or freeform reviewer cannot, at matched specificity.
  The honest headline is therefore split: decomposition buys specificity; the named catalogue
  buys traceability on top of it.
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

## Paired analysis

The conditions score the same drafts, so the right test of a difference is paired, not two
independent intervals. On the 28 clean drafts, McNemar's exact two-sided test on the discordant
pairs (one condition leaves a clean draft alone, the other over-flags it):

| comparison | paired spec diff | discordant (A-only / B-only) | McNemar p |
|---|---|---|---|
| judge vs mono-rid (decomposed vs bulk, both named) | +0.46 | 16 / 3 | **0.004** |
| judge-ctx vs mono-rid (decomposed vs bulk, context matched) | +0.39 | 16 / 5 | **0.027** |
| judge vs freeform (decomposed vs no structure) | +0.25 | 10 / 3 | 0.092 |
| judge-anon vs judge (unnamed vs named, both decomposed) | +0.04 | 3 / 2 | 1.000 |

The paired test sharpens the reading and tempers one claim. Decomposing the review beats
dumping the whole obligation set at once, significantly (p=0.004, and 0.027 with context held
constant). Decomposing beats plain freeform review in the same direction but not significantly
at this n (p=0.092), so that particular gap is suggestive, not established. And naming the
obligation adds nothing to specificity over a plain obligation (p=1.000), consistent with the
decomposition, not the catalogue, being what helps detection. The honest significant claim is
therefore narrow: at equal recall, one obligation at a time beats all fourteen at once; the
advantage over no structure at all is a trend this pilot does not establish.

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

The headline splits into two honest claims, and the unnamed-obligation arm forced the split.
At equal recall on adversarial cases, handing a reviewer the whole obligation set at once
(as a checklist or a named clause list) makes it over-flag clean drafts, worse than giving
it no catalogue. Decomposing the review to one obligation per call recovers and exceeds
plain-review specificity, and this works with a plain, unnamed obligation (judge-anon 0.86)
just as well as with a named clause (judge 0.82). So the specificity gain is the general move
of decomposition, not anything specific to this catalogue: its names, inventory, and graph do
not improve detection in this test. What the named catalogue does buy, at matched specificity,
is traceability, the named judge cites the right rule on 0.86 of its flags where the unnamed
and freeform reviewers cannot. The defensible claims are therefore narrow and separate: on
this 60-case evaluation, decomposing review to one obligation at a time produced fewer false
alarms than bulk review while keeping detection; and only the named catalogue made the flags
attributable to a specific, stable rule. We make no dominance or state-of-the-art claim.

## Open issues (from independent review)

These bound the result and are the next steps before it is a claim rather than a signal.

- **Clause routing is privileged information.** The judge is run on the clause for the case's
  gold mode, so it is told which obligation to check, while the bulk reviewers are not. This
  demonstrates review with a known target, not general auditing. The honest end-to-end test
  runs all fourteen clauses (or a router) on every draft and reports the draft-level flag rate
  under the real aggregation rule; individual clauses can each be specific while their union
  over-flags.
- **Generic decomposition versus the catalogue: now tested, and the humbler answer held.** The
  judge-anon arm (one unnamed plain obligation per call, otherwise matched to the judge) scores
  specificity 0.86, matching the named judge's 0.82. So generic task decomposition explains the
  specificity gain, and the catalogue's names, inventory, and graph add nothing to detection
  here; their measured contribution is attribution (0.86 vs 0), not accuracy.
- **The attribution denominators mix attribution with false-alarm control.** mono-rid 31/50 and
  judge 32/37 use all flagged cases; both detect 32 positives, so conditional attribution
  among true-positive flags is about 31/32 versus 32/32. Report flag precision and correct
  attribution separately.
- **Paired analysis: done** (see the Paired analysis section above). The McNemar tests confirm
  the decomposed-versus-bulk gap (p=0.004) and temper the decomposed-versus-freeform gap to a
  non-significant trend (p=0.092) at this n. "Clearly helps" was accordingly narrowed to
  "significantly beats the bulk clause list; trends above plain review."

## Reproduce

Regenerate with:

```
bash experiments/run-conditions.sh experiments/cases/suite-<behavior>-hard.json \
     --reviewers none,freeform,checklist,mono-rid,judge,judge-ctx,judge-anon --model sonnet
python3 experiments/metrics.py experiments/results/run-suite-*-hard-*-<ts>.jsonl --ci
```

Note on the runs: both the judge and the checklist conditions lost cases to a provider
session limit when run last in a batch (the quota is shared), and were re-run after the
limit reset. The figures above are from the completed, error-free set (0 invalid verdicts
in every condition), pooling the newest clean file per suite per condition.
