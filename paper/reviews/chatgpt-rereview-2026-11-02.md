# ChatGPT re-review (GPT-6.1 Sol), 2026-11-02

Same conversation as the first review, so it re-graded against its own five prior concerns.
Prior verdict: reject in current form. **Updated verdict: MAJOR REVISION.** "The gap has
moved substantially. You have moved from a catalogue with unproven usefulness to a catalogue
accompanied by a promising, narrowly tested auditing procedure. That justifies major revision.
It does not yet justify minor revision or acceptance at a top-tier venue."

## Re-assessment against the five prior concerns

1. Mixed ontology + human/native split: **Unresolved.** The exclusive split is unchanged;
   reward hacking and scope creep still say "no human analogue"; the experiment does not test
   the distinction or the ten cognitive categories.
2. Label recoverability presented as validation: **Overclaim corrected, validation still
   missing.** Dropping "floor" and acknowledging shared model assumptions fixes the
   interpretation; still a codebook check with no human annotation.
3. Provenance overstated: **Partially addressed.** Residual-error qualification and the six
   unsupported examples are materially better; exact denominators, checker details,
   adjudication, and an independent recheck of the corrected release still missing.
4. Unsupported causal graph claims: **Partially addressed, inconsistently.** Section 5 now
   says the incidents illustrate the graph, but Section 3.3 still asserts injection "causes"
   sycophantic capitulation which "causes" scope creep. Edge semantics remain untested.
5. Coverage too easy; usefulness unproven: **Utility partly addressed, coverage unresolved.**
   The ablation gives a real utility signal; twelve author-selected incidents still do not
   establish coverage, and six behaviours do not validate 207 modes.

## What the ablation genuinely adds (credited)

judge-ctx vs mono-rid (both see all 14 clauses): specificity 10/28 -> 21/28, a 39-point
observed gain, both detect 32/32 positives. "A substantial observed difference. It weakens
the explanation that the original benefit arose solely from omitting thirteen clauses." The
defensible bounded claim: "On this 60-case evaluation, clause-focused review produced fewer
false alarms than bulk review while retaining detection of all positive cases."

## What the ablation does NOT yet establish (new, sharp)

1. **Clause routing is the key missing detail.** How does the judge know which clause to
   evaluate? If the suite name / gold behaviour selects the clause, the judge gets privileged
   information the bulk reviewer lacks, so it demonstrates review *with a known target*, not
   general auditing. If all 14 judges run per draft, report the combined draft-level result
   under the real aggregation rule. If a router selects, include its errors and cost.
2. **Missing arm: one UNNAMED obligation per call**, otherwise matched to the judge. Without
   it, generic task decomposition may explain the gain; the 207-mode inventory, cognitive
   organisation, provenance links, and graph may contribute nothing to this result.
3. **Attribution metric mixes attribution with false-positive control.** Denominators use all
   flagged cases (mono-rid 31/50, judge 32/37). Report flag precision, correct attribution
   among true-positive flags, and wrong-clause flags separately. Comparing rule-ID against
   conditions deliberately denied IDs is not informative.
4. **"Context-length confound ruled out" is too strong.** judge-ctx addresses one alternative,
   not all; 0.75 vs 0.82 with 28 negatives is imprecise. Give exact prompts, token counts,
   clause ordering, output budgets, call counts.
5. **Needs paired statistics.** Same cases across conditions, so overlapping Wilson intervals
   are not the right test of the difference; publish case-level paired outcomes and a paired
   test. Also: "a single over-flagged draft moves specificity by 0.1 to 0.2" is wrong; with
   4-5 clean cases per suite it moves it by 0.20 to 0.25, so "clearly helps on four
   behaviours" should be "improved observed specificity on four suites."

## Manuscript contradictions requiring direct edits

- Section 2 says it grounds "every entry", although 21 entries are ungrounded.
- The abstract still presents "no human analogue" as established.
- Section 3.3 retains causal assertions that Section 5 says are untested.
- Section 5.1 "six discordances" is wrong: sonnet 3 + haiku 5 = eight rater-to-catalogue
  disagreements across five distinct modes, three missed by both.
- The ablation must be integrated into the paper's contribution and results, not only appended.

## Shortest credible route to acceptance

Resolve clause routing and report end-to-end draft-level performance; add the unnamed,
single-obligation control; release exact prompts, case-level outputs, scoring rules, and a
paired analysis; replace the exclusive human/native claim and qualify graph causality
consistently; add independent human annotation and an independent provenance recheck.
