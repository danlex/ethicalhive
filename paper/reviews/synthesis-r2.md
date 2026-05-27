# Review synthesis: round 2 (after the explanatory rewrite)

**Gemini:** MINOR REVISION (was MAJOR). The rewrite resolved the "I don't
understand anything" problem. The novelty positioning, the limitations
section, and the severity-calibration framing are now strengths.
**Codex:** MAJOR REVISION (held). Editorial progress acknowledged; the
remaining concerns are structural: baseline fairness, n size, evidence-
authority policy, and reproducible method spec.

## Where they agree (apply now, editorial)

1. **§3 is still too thin.** Both want pseudocode or a compact formal
   interface (inputs, outputs, authority order, retry rule, aggregation
   rule, exact baseline access to CoVe / evidence / clause text).
   "Method or a better prompt with labels" is the reviewer reflex to
   pre-empt.
2. **Table 2 presentation.** Both: raw fractions (`8/10`) not bare
   decimals (`0.80`). Drop `none` rows or move to appendix. Footnote
   the `0.00` rule-ID cells: "by construction, baseline does not emit
   rule IDs."
3. **Title is a liability.** Gemini soft, codex direct: it directly
   contradicts §1.4's own honesty about not replacing sampling/probes.
   Option to keep with stronger §1.4 framing, or promote the subtitle.
4. **Cite cognitive-science primary literature.** Anchoring -> Tversky
   & Kahneman (1974). Confirmation bias -> Wason (1960). Automation
   bias -> Mosier & Skitka (1996). Sycophancy -> Sharma et al. (2023)
   on RLHF-induced agreement. At minimum: one primary reference per
   clause that uses cog-sci framing.
5. **SRC is a method-specification problem, not a sandbox bug.** Codex
   phrases it sharply: the audit pipeline needs an explicit
   evidence-authority model. Pin a one-paragraph policy: "judges treat
   `evidence[]` as ground truth; live-tool queries are advisory and
   surface inconsistencies between draft and `evidence[]`, never
   between draft and host filesystem."
6. **Tone "wins" down.** At n=5 clean per cell with Wilson CIs
   [0.57, 1.00], "wins" overclaims. Use "out-performs at pilot scale",
   "preliminary advantage", or "directional result".
7. **Citation fixes.** Codex caught two:
   - Semantic Energy: Ma et al. (2025), not Wang et al.
   - AgentVerify: full title is *AgentVerify: Compositional Formal
     Verification of AI Agent Safety Properties via LTL Model Checking*;
     preprints.org 202604.1029, posted 14 April 2026.
8. **Move epistemic-vs-functional distinction to §1.2.** Gemini: the
   deeper novelty currently surfaces only in §6. Lift it to §1.2 for
   novelty pop.

## Where they diverge (judgment calls)

- **Verdict gap.** Gemini accepted the brutally honest limitations as a
  successful pre-emption ("disarms the primary reason to reject");
  codex says the same paragraph reads as "the minimum has not been
  done" and would downgrade the paper to a pilot/design paper unless
  the independent annotation runs before submission.
- **Severity calibration.** Gemini says the framing is now strong and
  is exactly the kind of insight a workshop wants. Codex says it still
  reads defensive ("not an open problem in the field" is risky) and
  would replace with: "Severity calibration is the main contract-
  design failure exposed by the pilot. Rule identity and intervention
  severity must be specified separately." We will lean toward codex's
  wording: stronger, less defensive.

## What we cannot fix without new experiments (defer)

- **Rule-ID-capable monolithic baseline.** Both reviewers say this is
  needed. It is a fifth reviewer condition, requires authoring a new
  prompt for the monolithic agent that gives it the clause list, and
  running it across all six clauses x two suites x ten cases each.
  Estimated cost: ~6-8 hours of agent runtime, then re-figure and
  re-table.
- **n=20 per clean cell on hard suites.** Both reviewers say n=10 is
  borderline at workshop scale. Increase to n=20 clean + n=20 flagged
  per clause. This is benchmark-authoring time, not just runtime.
- **20-case independent-annotator IAA per clause.** Codex's strongest
  ask. Without it the paper is a pilot. With it, it can claim a
  preliminary evaluation result.
- **Per-clause severity ladder.** Codex's proposed fix for the REVISE/
  BLOCK ambiguity. Examples for SHIP/REVISE/BLOCK per clause, held out
  from test cases.

## Editorial punch list applied in this revision

A. Table 2: replace bare decimals with fractions (`8/10`); drop
   `none` rows; add the rule-ID-by-construction footnote.
B. §3: add pseudocode block for the audit pipeline; add a small table
   of judge I/O schema; pin evidence-authority policy explicitly.
C. §1.2: move the epistemic-vs-functional distinction up from §6.
D. Citations: Semantic Energy -> Ma et al. (2025); AgentVerify full
   title; add Tversky & Kahneman (1974), Wason (1960), Mosier &
   Skitka (1996).
E. Severity framing: replace defensive line with the codex wording.
F. SRC: reframe explicitly as a method-specification gap (evidence-
   authority policy missing), not a sandbox bug.
G. Throughout: "wins" -> "out-performs at pilot scale" or "directional".
H. §7: revise the IAA sentence so it does not read as "minimum has not
   been done." Either run it or downgrade explicitly to a pilot paper.

## Title

Two reviewers flagged "Contracts Is All You Need" as risky. Decision
point: keep the homage with §1.4 explicitly disarming it, or promote
the subtitle. Logged for the user.

## Verdict trajectory

Round 1: MAJOR / MAJOR.
Round 2: MAJOR / MINOR.
Gap closing. Next round target after editorial fixes + one new baseline
run: MINOR / MINOR. Submission-ready after the IAA pilot.
