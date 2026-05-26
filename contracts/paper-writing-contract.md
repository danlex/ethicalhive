# Paper Writing Contract

**Version:** 1.1
**Effective date:** 2026-05-26 (was 1.0 on 2026-05-24)
**Document type:** Binding writing standard for the EthicalAI workshop paper.
**Auditors:** `paper-bias-judge`, `paper-ai-detector`, and the relevant EthicalAI clause
judges named below.
**Orchestrator:** `/write-paper` (Council Lead).
**Companion contract:** `contracts/ai-integrity-contract.md` (the system being described).

This is the contract every draft section of the paper must satisfy before publication. It is
the document the writer is bound by, and the council members are the Auditors that check each
clause. It is advisory in the same sense the AI Integrity Contract is: it gives the Principal
structured signal before delivery, and the Principal keeps the final word.

## 1. Parties and Roles

- **Principal** the human author. Sets the thesis, accepts or rejects, ships.
- **Writer** the `paper-writer` agent. Drafts and revises sections.
- **Council** the judges that audit each draft: `paper-bias-judge` (composes the relevant
  EthicalAI clause judges), `paper-ai-detector` (AI-writing tells), and the contract check the
  orchestrator runs against this document.
- **Lead** `/write-paper`. Drafts via Writer, dispatches the Council in parallel, synthesizes
  paste-ready fixes, **writes** the improved section, iterates to consensus.

## 2. Definitions

The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY follow
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and
[RFC 8174](https://www.rfc-editor.org/rfc/rfc8174), only when in ALL CAPS.

- **Section** a unit of the paper: Abstract, Introduction, The AI Integrity Contract, Method,
  Benchmark, Experiments, Related Work, Limitations, Conclusion.
- **Grounded** every load-bearing claim resolves to a named source in `paper/proposal.md`,
  `references/prior-art.md`, `experiments/seed-selective-evidence.md`, a committed result
  JSONL, or an external citation that exists and says what is claimed.
- **Tagged** marked `[UNVERIFIED]` in the draft if a claim cannot be grounded yet.

## 3. Scope (PAP-SCO)

- **PAP-SCO-01** (MUST). The paper's thesis is **clause-grounded advisory auditing of AI
  integrity**, as locked in `paper/proposal.md`. Drift to a different thesis is a BLOCK.
- **PAP-SCO-02** (MUST). The target is a **workshop / short paper**, 4 to 8 pages. Drafts MUST
  fit that budget.
- **PAP-SCO-03** (MUST NOT). The paper MUST NOT claim state of the art on hallucination
  detection or any other Family 2 / Family 3 metric. The honest placement (Family 1
  prose-rubric, strictly weaker on raw factuality) is fixed in `references/prior-art.md`.
- **PAP-SCO-04** (MUST). The novelty positioning MUST cite and distinguish:
  Trace-Based Assurance Framework for Agentic AI (arXiv 2603.18096), RFCAudit (arXiv
  2506.00714), AgentVerify (preprints 202604.1029). Functional/safety/orchestration vs
  epistemic-integrity output, formal/LTL/trace vs RFC 2119 natural-language clauses, runtime
  block-or-rewrite vs advisory + human-in-the-loop.

## 4. Source policy and integrity (PAP-SRC)

- **PAP-SRC-01** (MUST). Every load-bearing claim is grounded (see §2). Hand-waved claims are a
  BLOCK.
- **PAP-SRC-02** (MUST). Citations resolve. A cited arXiv ID, venue, author, or URL MUST point
  to what the draft says it does. The `source-fabrication-judge` enforces this.
- **PAP-SRC-03** (MUST NOT). No citation in the "References to verify before citing (do not
  cite unchecked)" list of `paper/proposal.md` appears in any final draft section until it
  has been moved to the confirmed list with arXiv ID and authors. (As of v1.1 on 2026-05-26,
  AgentDojo arXiv 2406.13352, InjecAgent arXiv 2403.02691, RAGTruth arXiv 2401.00396, and
  ImpossibleBench arXiv 2510.20270 have been verified and are now citable; the to-verify
  list is empty.)
- **PAP-SRC-04** (MUST NOT). Do not invent experimental numbers, authors, venues, arXiv IDs,
  or any quantitative result. Experimental numbers come from `experiments/results/*.jsonl` and
  the tables in `experiments/seed-selective-evidence.md`.
- **PAP-SRC-05** (MUST). Use `[UNVERIFIED]` tags for any claim that cannot yet be grounded.
  Tags are tracked outside the editorial body in the orchestrator's change list and removed
  before publish.

## 5. Required structure (PAP-STR)

- **PAP-STR-01** (MUST). Sections in this order: Abstract → Introduction → The AI Integrity
  Contract → Method (clause-grounded audit) → Benchmark (hybrid, agentic coding) →
  Experiments (no-audit / freeform / contract / judge) → Related Work → Limitations →
  Conclusion. Optional Acknowledgments and References as needed by venue.
- **PAP-STR-02** (MUST). The Related Work section MUST distinguish three method families
  (prose-rubric self-review, sampling-based uncertainty, hidden-state / logit probes) and the
  agentic-contract / assurance line. The distinctions are in `references/prior-art.md`.
- **PAP-STR-03** (MUST). The Limitations section MUST name: circularity (drafter and auditor
  same model family), not SOTA on factuality, small n on the seed mode, author-built labels
  with adjudication and kappa, LLM-as-judge ceiling on hard hallucinations (FaithBench
  shows ~50% accuracy on hard cases), severity calibration (REVISE vs BLOCK) as the named open
  problem.
- **PAP-STR-04** (MUST). The Experiments section MUST report the four conditions
  (none / freeform / contract / judge), both suites (easy and hard), and the four metrics
  (exact accuracy, recall, specificity, **rule-ID attribution**). The headline is at-equal-
  recall **specificity** and **rule-ID traceability**, not raw recall.

## 6. Voice and format (PAP-FMT)

- **PAP-FMT-01** (MUST). Plain language. Write like to a colleague: name the file, say what
  changes, stop. No tier tables, no risk labels, no "speculative / verified" framings, no
  corporate hedging. (Memory: `feedback_plain_language`.)
- **PAP-FMT-02** (MUST NOT). No em-dashes (—) or en-dashes (–) in body prose. Hyphens stay in
  compounds and identifiers (e.g. `Claude-Web`, `rule-ID`). (Memory: `feedback_no_em_dashes`.)
- **PAP-FMT-03** (MUST). Pass the `paper-ai-detector` at **≤ 2/10**. Boilerplate (ceremonial
  openers, hollow padding, rule-of-three cadence, empty transitions, reflexive promotion) is a
  BLOCK above that score.
- **PAP-FMT-04** (MUST). Use model aliases (`opus`, `sonnet`, `haiku`) when discussing the
  experimental setup or any infrastructure; never pin a model ID like `claude-opus-4-7`.
  (Memory: `feedback_use_model_aliases`.)
- **PAP-FMT-05** (MUST NOT). No meta apologetics in the paper body ("we did not have time
  to", "limited resources prevented", "future work will"). Limitations go in §Limitations,
  not scattered across the prose.

## 7. Quality gate and verdict mapping (PAP-QUA)

- **PAP-QUA-01** (MUST). A section is shippable only when:
  `paper-bias-judge` returns no BLOCKERS,
  `paper-ai-detector` ≤ 2/10,
  the contract check in `/write-paper` returns PASS on every MUST and MUST NOT clause above.
- **PAP-QUA-02** Verdict vocabulary mirrors the AI Integrity Contract: PASS / ASK APPROVAL /
  REVISE / FAIL (Auditors may use PASS / FLAG / BLOCK for the judge layer; the Lead maps
  FLAG → REVISE and BLOCK → FAIL when reporting to the Principal).
- **PAP-QUA-03** (MUST). On any BLOCK / FAIL, the responsible judge MUST return a
  paste-ready fix (exact replacement sentence, missing proof step, citation to add). A verdict
  without proposed fixes is itself an incomplete review and is sent back.

## 8. Working draft template

Every section delivered by the Writer follows this shape:

```
## <Section name>

<the section text, plain language, no em-dashes, no AI tells,
 every load-bearing claim grounded or tagged [UNVERIFIED]>

---
WRITER NOTES (not part of the paper)
- changes vs input: <bullets>
- grounded against: <files/IDs>
- open [UNVERIFIED] tags: <list, or "none">
```

## 9. Short generation checklist

The final paper MUST:

- match the structure in PAP-STR-01;
- ground every load-bearing claim, with all citations resolving;
- carry **no** em/en-dashes and no AI-writing tells (score ≤ 2/10);
- include the §Limitations content listed in PAP-STR-03;
- report exact-accuracy, recall, specificity, and **rule-ID attribution** for each condition;
- distinguish the trace-based-assurance line of work from this paper's epistemic-integrity
  scope (PAP-SCO-04);
- omit the four unverified citations until they are confirmed (PAP-SRC-03).

## 10. Worked example pointer

There is no published exemplar paper yet. The stylistic baseline is the prose in
`paper/proposal.md` and `experiments/seed-selective-evidence.md`: short, file-naming, no
hedge-tower, every claim either grounded or `[UNVERIFIED]`. When in doubt about tone or
density, conform to those two documents.

## 11. Sources

- `paper/proposal.md` (thesis, hybrid benchmark plan, vetted citation list).
- `references/prior-art.md` (honest placement, three method families).
- `experiments/seed-selective-evidence.md` (results, the headline numbers and the open
  calibration problem).
- `contracts/ai-integrity-contract.md` (the system being described in the paper).
- RFC 2119 / RFC 8174.

## 12. Amendments and changelog

Principal only. Amend by editing this file, bumping the version, and updating the changelog.
Amendments take effect at the next draft, never mid-section.

- **1.0** (2026-05-24) Initial paper writing contract. Five clause groups (PAP-SCO, PAP-SRC,
  PAP-STR, PAP-FMT, PAP-QUA), mapped to council Auditors.
- **1.1** (2026-05-26) PAP-SRC-03 rewritten as a general rule pointing to the
  `paper/proposal.md` to-verify list, rather than naming four specific citations. The four
  (AgentDojo 2406.13352, InjecAgent 2403.02691, RAGTruth 2401.00396, ImpossibleBench
  2510.20270) have been verified and are now citable.
