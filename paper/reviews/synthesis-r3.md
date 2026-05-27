# Review synthesis: round 3 (after the human-agent reframing)

Three reviews this round: codex, gemini, and the AI-pattern audit via
`paper-ai-detector`.

## Verdicts

| Reviewer | R1 | R2 | R3 | Trajectory |
|---|---|---|---|---|
| codex (GPT-5.5) | MAJOR | MAJOR | MAJOR | held; empirical gaps remain the gate |
| gemini | MAJOR | MINOR | MINOR | held minor |
| AI-pattern audit | n/a | n/a | 3/10 | first run; PAP-FMT-03 target is <=2 |

The codex hold is not a regression; the diagnosis shifted from "writing
problem" to "empirical scope problem", which is the harder gate to clear.

## Highest-impact findings, applied in this revision

A. **Citation integrity (paper-ai-detector, HIGH).** The Trace-Based
   Assurance reference had no author list, and AgentVerify used a
   non-standard preprints.org handle without an author list. Both look
   like fabricated entries on a strict audit. Resolution: WebFetched
   authors for both. TBA is Paduraru, Bouruc, Stefanescu (March 2026);
   AgentVerify lead is Zhan, S. S. (April 2026). Both bibliography
   entries and the in-text cites updated.

B. **Contradiction (codex r3).** §1.2 said "Nothing is blocked, nothing
   is rewritten. The Principal keeps the final word" but §3.3 said "a
   single BLOCK in any clause is enough to halt delivery in interactive
   contexts." Rewrote §3.3 to surface BLOCK as "BLOCK-level advice"
   that is never executed as deletion or rewrite. Same wording adopted
   in §1.2 and §1.3.

C. **Terminology drift (codex r3).** Three verdict vocabularies were
   floating: PASS/ASK APPROVAL/REVISE/FAIL, PASS/REVISE/BLOCK,
   SHIP/REVISE/BLOCK. Picked one body ontology (PASS/REVISE/BLOCK) and
   noted in §2.3 that benchmark scoring collapses to SHIP/REVISE/BLOCK.

D. **Section-order bug (codex r3).** §5 referenced "§3.3 below" but
   §3.3 is above §5. Fixed.

E. **Six-clause vs five-check mismatch (gemini r3).** §5 baseline was
   described as "single five-check rubric reviewer" but the pilot
   audits six clauses. Rewrote the baseline description to clarify the
   monolithic rubric was extended to cover the six audited clauses.

F. **Orphan citations (gemini r3).** Wason (1960) and Mosier & Skitka
   (1996) were in References but never cited inline. Added inline
   cites in Table 1: anchoring -> Tversky and Kahneman 1974;
   confirmation bias -> Wason 1960; automation bias -> Mosier and
   Skitka 1996. Sharma et al. (2023) added inline for sycophancy.

G. **Figure 1 redundant (codex r3 + gemini r3).** Removed Figure 1
   from the body. Table 2 carries the specificity numbers; one
   sentence in §5 notes that at n=5 per clean cell, a bar chart
   over-dignifies the data.

H. **Abstract/conclusion paraphrase (paper-ai-detector, MEDIUM).**
   Both ended with a tripartite "The contribution is..." sentence
   recycling the same three themes in the same order. Jaccard above
   0.4 between the two. Rewrote the conclusion to point forward to
   what the architecture does not yet solve (severity calibration,
   evidence-authority, independent annotation) rather than restate
   the contribution.

I. **§1.2 overclaim (codex r3).** Removed "verdicts do not name what
   obligation was violated, because the rubric is internal to the
   prompt" (a prompted rubric can emit criterion labels). Replaced
   with the narrower claim: the obligation as a Principal-owned,
   versioned, amendable artefact with per-clause auditors and rule-ID
   attribution as a measured property is the absent piece.

J. **"Binding" language (codex r3).** Replaced "binding on the Agent
   per turn" with "normative for the Agent per turn".

K. **Filler hedge (paper-ai-detector).** Removed "We do not have a
   direct comparable in the published literature"; replaced with a
   scope-bounded claim.

L. **Marketing residue (paper-ai-detector).** "deeper novelty" had
   already been removed in an earlier pass; clean now.

M. **Rule-of-three lead-in (paper-ai-detector).** Rewrote §1.3 as
   continuous prose; removed the "Three concrete things change"
   bullet-list opener that triggered the AI-tell.

N. **Abstract opener (paper-ai-detector).** Replaced "We propose
   treating the relationship..." with a more distinctive lead: "When
   a human and an AI coding agent collaborate, the working
   relationship is implicit. We make it explicit as a written
   contract..."

O. **Method §3 prompt-design (codex + gemini).** Added a "Prompt
   design" subsection: prompts are templated, not few-shot; the
   clause text is referenced not paraphrased; the prompts were
   written before the suites; the suites were not iterated after
   judge mis-calls. Added G-Eval and MT-Bench inline as the
   methodological lineage and to References.

P. **Reproducibility (codex r3).** Pinned model tier (sonnet),
   deployment date window (2026-05-26..27), temperature (0), and
   stability check (5-case subset re-run, identical outputs).

Q. **Provenance promise (gemini r3).** The §4 promise of "results
   split by provenance" was never honoured because all current cases
   are `original`. Either we add the split or drop the promise; the
   honest path here is to fold provenance into the §4 benchmark text
   with the current count ("all 120 cases in the six audited modes
   are `original`; `recast` and `reused` cases are queued for the
   non-pilot clauses").  // Note: NOT YET APPLIED in this batch.
   Logged for follow-up.

## Still open after this revision

- **Rule-ID-capable monolithic baseline (codex; both rounds).** Not
  run. A monolithic agent given the clause list and asked to cite
  the best matching rule ID. This is the fifth condition the paper
  needs before the rule-ID column is a fair comparison rather than
  a property of the prompt.
- **n=20 per clean cell on hard suites (codex; both rounds).** Not
  done. Either we author 5-10 more clean cases per clause or we
  permanently brand §5 as a pilot.
- **20-case independent-annotator IAA per clause (codex; both
  rounds).** This is the gating step for the comparative
  evaluation claim. The conclusion now names it as the next step.
- **Provenance split in §4 / §5 (gemini r3).** Logged above as Q.
- **Severity confusion matrix (codex r3).** A REVISE-vs-BLOCK
  confusion matrix would do more for the severity-calibration
  argument than the per-condition exact column does. Logged.
- **G-Eval and MT-Bench cites added but not contextualised in §6.**
  Inline use in §3 is fine; §6 Related Work could grow a line on
  LLM-as-judge reliability.

## What the AI-pattern audit reports after this pass (estimated)

The Pattern Score before this batch was 3/10. The fixes hit five of
the six flagged items in the validation check (generic abstract
opener; cookie-cutter contribution; filler hedge; conclusion
paraphrases abstract; marketing residue). The "repetitive methodology
rhythm" in §6 Related Work is unchanged in this batch and is the most
likely remaining tell. Re-running the audit on the next iteration
should drop the score; the comparative result will show in the next
round.
