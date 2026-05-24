---
name: write-paper
description: Run the EthicalAI workshop paper council to draft or revise a paper section. Draft via paper-writer, dispatch paper-bias-judge and paper-ai-detector in parallel, check the draft against contracts/paper-writing-contract.md, synthesize paste-ready fixes, rewrite the section, iterate to consensus (max 3 rounds). Consensus = bias-judge no BLOCKERS, ai-detector ≤ 2/10, contract check PASS on every MUST clause. Invoke with the section name to draft, or with an existing draft + revision goal. Delivers the finished section text; the council report is an appendix.
---

# Write Paper

Council Lead for the EthicalAI workshop paper. Drafts and revises one section per
invocation, bound to `contracts/paper-writing-contract.md`. Returns a finished, contract-
compliant section, not a list of objections.

## When to invoke

- User types `/write-paper` with a section name (e.g. "Experiments", "Related Work",
  "Method") and optionally an existing draft + revision goal.
- User asks to "draft", "revise", "write the X section", or "iterate on this draft" of the
  EthicalAI / contract-grounded auditing paper described in `paper/proposal.md`.

Skip for: non-paper writing, the editorial / ONI council (that is the `editorialllm` repo's
`/write-editorial`), or any request to commit or push.

## Hard rule for every council member

A judge may not stop at "this is wrong". Every issue raised MUST come with a concrete,
paste-ready fix (the replacement sentence, the missing proof step, the citation to add,
the wording that drops the AI tell). A verdict without proposed fixes is incomplete and is
sent back to the source judge (`paper-writing-contract.md` PAP-QUA-03).

## File-access rule for every member, every round

Every council member MUST read its primary sources before judging. At minimum:

- `paper/proposal.md` (thesis, hybrid benchmark plan, vetted citations).
- `references/prior-art.md` (the three method families and the agentic-contract line).
- `experiments/seed-selective-evidence.md` (the headline numbers and the open calibration
  problem).
- `contracts/paper-writing-contract.md` (the binding standard).
- `contracts/ai-integrity-contract.md` (the system the paper describes; rubric source for
  every clause judge).

A member that reviews the draft without reading these files produced an incomplete review
and is re-dispatched.

## Process

1. **Draft.** Spawn `paper-writer` (via the Agent tool) with the section name, any existing
   draft, and any revision goal. The Writer returns paste-ready section text plus a
   `WRITER NOTES` block.

2. **Convene the council (parallel, one message).** Send the draft and the file list above
   concurrently to:
   - `paper-bias-judge` — runs the six relevant clause judges (overconfidence, selective-
     evidence, source-fabrication, confirmation-bias, anchoring, sycophancy) in parallel
     and aggregates with INT-* rule IDs.
   - `paper-ai-detector` — AI-writing-tell score (target ≤ 2/10) with flagged passages and
     paste-ready cuts.

3. **Contract check.** Lead reads `contracts/paper-writing-contract.md` and walks every MUST
   and MUST NOT clause against the draft, producing one PASS / REVISE / FAIL per clause and
   the exact fix when not PASS. The clauses to check on every section:
   - PAP-SCO-01..04 (scope, thesis, no-SOTA, novelty positioning vs trace-based assurance).
   - PAP-SRC-01..05 (groundedness, citations resolve, four unverified citations stay out,
     no invented numbers, [UNVERIFIED] tagging).
   - PAP-STR-01..04 (section in correct order; structure-specific rules for Related Work,
     Limitations, Experiments).
   - PAP-FMT-01..05 (plain language, no em/en-dashes, AI-tell score ≤ 2/10, model aliases,
     no meta apologetics).

4. **Synthesize.** Merge all paste-ready fixes from bias-judge, ai-detector, and the
   contract check into one ordered change list, deduplicated, by priority:
   `groundedness > contract-MUST > AI-tells > structure > prose`.
   Resolve conflicts by that priority. A style fix MUST NOT introduce an ungrounded claim
   or weaken a contract MUST.

5. **Revise. The Lead writes.** Apply the merged fixes and produce the improved section in
   full. This is the point of the council: it returns a better section each round, never a
   list of objections. The Writer agent MAY be re-spawned with the merged change list as
   the revision goal, OR the Lead may apply the fixes directly. Either way, the final text
   is the Lead's deliverable.

6. **Iterate.** Re-dispatch only the judges that did not PASS, on the revised section.
   **Max 3 rounds.** Consensus =
   - `paper-bias-judge` no BLOCKERS,
   - `paper-ai-detector` ≤ 2/10,
   - contract check PASS on every MUST / MUST NOT clause.

   If consensus is not reached within 3 rounds, deliver the best improved section anyway
   and list remaining dissent under "Unresolved" in the appendix.

## Deliver

The deliverable is the finished section text. The council report is the appendix.

````
## <Section name>

<the finished, council-improved section text>

---
## Council report (appendix)

| Member             | Final verdict |
|--------------------|---------------|
| paper-writer       | drafted (round n) |
| paper-bias-judge   | PASS / FLAG / BLOCK |
| paper-ai-detector  | <score>/10 |
| contract-check     | PASS / REVISE / FAIL |

Rounds: <n>
Consensus: <yes / no>
Unresolved: <none, or the list of remaining FLAG / BLOCK findings>
Rule IDs cited by paper-bias-judge: [INT-OVR-01, INT-SEL-01, ...]
PAP-* clauses verified: [PAP-SCO-01, PAP-STR-04, PAP-FMT-02, ...]
````

## Constraints

- Lead **writes**. The deliverable is the finished section, not a critique list.
- One section per invocation. To draft a different section, invoke again.
- Do not commit, do not push, do not modify any file other than the deliverable.
- Do not approve a section that fails any contract MUST clause. If unable to satisfy a
  MUST after 3 rounds, deliver the best version and surface the unresolved MUST in the
  appendix, do not silently ship.

## Failure modes to watch (Anti-Bias)

- **Critic loop.** Returning rounds of judge output without ever rewriting. The council
  exists to improve the section, not to argue about it. After every judging round, the
  Lead rewrites.
- **Soft-bragging in synthesis.** Recasting the seed result as a detection win. The
  honest framing is at-equal-recall **specificity** and **rule-ID traceability**, plus
  severity calibration as the named open problem.
- **Unverified citations slipping in.** AgentDojo, InjecAgent, RAGTruth, ImpossibleBench
  must stay out until `paper/proposal.md` moves them from "to verify" to "Confirmed".
- **Em-dashes re-introduced.** Every revision pass re-checks PAP-FMT-02.
