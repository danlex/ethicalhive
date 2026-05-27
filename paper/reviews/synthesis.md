# Review synthesis: codex (GPT-5.5) + gemini

Both reviewers returned **MAJOR REVISION**. Strong agreement on the structural
issues; each caught distinct concrete errors the other missed. The picture
below merges them into a punch list ordered by priority.

## Where they agree (high confidence, apply now)

1. **§3 Method is too thin.** Both: a reviewer cannot reproduce the pipeline
   from the current text. Needs the claim-decomposition mechanism, judge
   prompt schema, model/config/aggregation policy, and one worked example.
   Gemini: "Section 3 is currently a high-level architectural description,
   not a reproducible method." Codex: "Need the actual input schema, judge
   prompt template, model version, temperature, retry policy, context
   isolation, and aggregation rules."
2. **n=10 per cell is pilot-grade.** Specificity 1.00 is one wrong flag from
   0.80. Both want counts or CIs, not bare decimals. Codex: report counts
   (5/5 clean), bootstrap or binomial CIs, run >=3 stochastic repeats.
   Gemini: aggregate clean-sweep modes to n=40 per cell so 0.95 vs 0.65 is
   meaningful, not a two-prompt swing.
3. **Figures + Table 2 are redundant.** Drop two of the three bar charts;
   keep Table 2 (or its compact form) and one summary figure. Both said it.
4. **Severity calibration framing is excuse-flavored.** Codex: treat it as a
   measured failure mode with a SHIP/REVISE/BLOCK confusion matrix. Gemini:
   "It is not an open problem in the field; it is a fuzzy boundary in your
   specific contract definitions." Rename: "Calibration sensitivity", not
   "open problem".
5. **Author-built benchmark §Limitations is too short.** Both: brutally
   honest does not equal sufficient. Gemini: "submitting a paper saying 'we
   tested our own prompt on a dataset we wrote to prove our prompt works,
   validation coming later' will likely get you rejected." Both want at
   least a 20-case pilot IAA / Cohen kappa before submission.
6. **Citation hygiene is broken.** TBA, RFCAudit, AgentVerify all need full
   authors + venues. Cognitive bias citations are missing or appear as raw
   arXiv IDs in prose.

## What codex caught that gemini missed

7. **RFCAudit citation is plainly wrong.** Authors are
   **Zheng, Wang, Liu, Guo, Feng, Zhang** (network protocol bug detection),
   not "Cheng et al." That was a conflation with ELEPHANT.
8. **MiniCheck is misplaced.** It is a small fact-checking model, not a
   hidden-state probe. Move it out of "Hidden-state and logit probes."
9. **"none" specificity 1.00 is trivial.** It never flags anything;
   specificity is by construction perfect. Mark it as a base-rate
   comparator only.
10. **Rule-ID baseline is structurally unfair.** Free-form and v5 score 0.00
    on rule-ID *by construction*. Add a baseline where the monolithic
    reviewer is given the clause list and asked to cite the best matching
    rule ID. Without that the comparison is rigged.
11. **Author-built specifics.** Were cases written before or after the judge
    prompts? Were failed cases iterated into the suite? Were negative
    examples adversarially selected? Limitations must answer these.
12. **SRC counter-finding has a structural risk.** Codex: it shows the
    verification machinery can override benchmark evidence. Need explicit
    evidence-authority policy before running Hallucination and
    Confabulation, which inherit the same shape.

## What gemini caught that codex missed

13. **RFC 2119 itself is uncited.** The paper leans on RFC 2119 for the
    contract clauses and never cites Bradner 1997. A reviewer will spot
    this in five seconds.
14. **Raw arXiv IDs leak in prose.** `[2410.15413, 2509.22856, 2505.15392]`
    appear naked in §Related Work. Convert to proper author-year cites or
    drop.
15. **Zero cognitive-science citations.** The introduction frames the
    catalogue as parallel to the cognitive-science literature; the paper
    then cites no cognitive-science paper. Either drop the framing or
    ground it.
16. **Internal project jargon.** "tvl-tech-bias-validator" is internal-
    memo language. Rename to "monolithic prose baseline" everywhere. Same
    for any reference to plugin names a reader will not recognise.
17. **SRC counter-finding is "just a broken eval".** Gemini's reading is
    sharper than codex's: the case states the file resolves, but the agent
    is allowed to query the live filesystem where the file does not exist.
    That is a benchmark sandbox bug, not a structural finding. Frame it
    that way or fix the sandbox.

## Punch list (priority order, for the next revision)

A. **Citation surgery (mechanical, do first):**
   - RFCAudit: Zheng et al. (2025), arXiv:2506.00714. Title: *RFCAudit: An
     LLM Agent for Functional Bug Detection in Network Protocols*.
   - Add Bradner (1997) for RFC 2119.
   - Move MiniCheck out of the hidden-state probes paragraph.
   - Replace `[2410.15413, ...]` raw IDs with proper author-year cites or
     remove the parenthetical.
   - Add SycEval (arXiv:2502.08177) explicitly.
   - Add at least 2-3 cognitive-science references for the failure-mode
     catalogue (or drop the cognitive-science framing).

B. **Jargon and stance (sharper claim):**
   - Rename "contract (v5 validator)" to "monolithic prose baseline" in
     prose, table, and figures.
   - Rewrite the novelty paragraph to lead with **architectural
     decoupling of epistemic checks into independent, parallel, rule-ID-
     emitting advisory layers**, not just "breadth + traceability".
   - Soften the §1 line "None of them produce verdicts an external reader
     can trace to a specific obligation the agent was bound by"; TBA does
     traceability, just not of epistemic obligations.
   - Reframe severity as "Calibration sensitivity", not "open problem".

C. **Method §3 reproducibility (the largest structural fix):**
   - Add a pipeline figure: draft -> CoVe -> per-clause judges -> verdict
     aggregation.
   - Specify claim decomposition: how (LLM call, sentence split, hybrid),
     prompt, label set (verified / inferred / assumed / unsupported).
   - Publish one full worked example (one case end to end with the actual
     judge output).
   - Pin model alias, temperature, retry policy, context isolation,
     aggregation rule. (Model aliases only per PAP-FMT-04.)
   - Link to the judge prompt files in the repo as supplementary.

D. **Experiments rigor:**
   - Replace bare decimals with counts (e.g., "5/5 clean, 4/4 flagged").
   - Aggregate clean-sweep modes into one row (n=40) so the headline is
     statistically meaningful.
   - Add binomial CIs to the headline numbers (Wilson or Clopper-Pearson).
   - Add a rule-ID-capable monolithic baseline so the rule-ID comparison
     is not structurally rigged.
   - Drop "none" from the specificity figure or mark it explicitly as
     base-rate comparator.
   - Drop two of the three bar charts; keep the specificity one or fold
     all three into one multi-panel figure.

E. **Limitations expansion:**
   - Were cases written before or after the judge prompts?
   - Were failed cases iterated into the suite?
   - Were negative examples adversarially selected?
   - Run a 20-case pilot IAA with one independent annotator and report
     Cohen kappa before submission.

F. **SRC framing:**
   - Move the SRC counter-finding from "structural problem with
     verification-heavy judges" to "benchmark sandbox issue: the case
     states the file resolves but the host filesystem does not contain it.
     The audit's file-existence mandate dominates the case text." Fix the
     sandbox before running Hallucination / Confabulation.

## Verdict

Two independent reviewers, two MAJOR REVISIONs, convergent diagnosis. The
work is sound; the writing is not yet a paper at workshop bar.
