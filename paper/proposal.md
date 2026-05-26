# Paper proposal: clause-grounded advisory auditing of AI integrity

Status: draft proposal, 2026-05-23. For discussion, not submission.
Decisions locked with the author: thesis = contract-grounded auditing; benchmark = hybrid
(reuse + author); scope = workshop / short paper.

## Working title

Primary: **"From Prompts to Clauses: Contract-Grounded Advisory Auditing of AI Integrity
Failure Modes in Agentic Coding."**

Alternatives:
- "The AI Integrity Contract: Clause-Traceable Advisory Auditing for Coding Agents."
- "Clause-Grounded Self-Review: An Advisory, Human-in-the-Loop Integrity Audit."

## The one-sentence claim

Representing an agent's integrity obligations as a natural-language RFC 2119 contract, whose
clauses map one to one to an epistemic-failure taxonomy and to per-clause LLM-judge auditors,
yields advisory verdicts that are clause-traceable, no worse on recall than free-form
self-review, and better on specificity (fewer false flags on clean drafts), while keeping the
human as the final decision maker.

We do NOT claim state of the art hallucination detection. Our own prior-art note rules that out
(see `references/prior-art.md`): this is a prose-rubric self-review method, architecturally
weaker than sampling and probe methods on pure factuality. The contribution is breadth,
traceability, specificity, and stance, not raw factuality AUROC.

## Why this is novel (honest positioning)

Contract-grounded auditing of agents is not new. We must cite and distinguish:

- **Trace-Based Assurance Framework for Agentic AI** (arXiv 2603.18096). Step and trace
  contracts, machine-checkable verdicts, localizes the first violating step. Closest prior art.
  Difference: it targets multi-agent orchestration (non-termination, role drift, untrusted
  context, fault containment) via instrumented Message-Action Traces, stress testing, and
  runtime governance that can block or rewrite. No human-in-the-loop advisory element.
- **RFCAudit** (arXiv 2506.00714) and **SPECA**: conformance of implementations to RFC /
  natural-language specs. Functional bugs, not epistemic failure of the agent's own claims.
- **AgentVerify** (preprints 202604.1029): LTL model checking of agent control flow. Formal
  safety properties, not honesty.

Our un-taken slice, the parts none of the above cover together:

1. **Epistemic-integrity target, not functional/safety.** The 14 clauses are about how the
   agent reasons and what it claims (hallucination, sycophancy, capitulation, anchoring,
   selective evidence, scope creep, ...), grounded in a cognitive-science taxonomy.
2. **Natural-language RFC 2119 clauses with stable rule IDs** (INT-HAL-01 ...), each auditable
   by an LLM judge, rather than assertion or trace contracts or LTL.
3. **Advisory and human-in-the-loop by design.** The auditor reports a verdict; it does not
   block or rewrite. The Principal decides. This is a deliberate stance, not a limitation.
4. **Clause-traceable verdicts.** Each finding cites the rule ID it relies on, so a human or a
   downstream agent can act on it. Free-form self-review cannot do this structurally.
5. **A governance loop** for evolving the contract: a model-tier-diverse judge council (Opus +
   Sonnet + Haiku) gates changes, so the spec cannot silently drift.

## The artifact: the AI Integrity Contract

Already written: `contracts/ai-integrity-contract.md`. RFC 2119 / 8174, 14 failure-mode clauses
(Section 8), each with stable rule IDs and a named judge-agent Auditor, verdicts PASS / ASK
APPROVAL / REVISE / FAIL, three enforcement layers (self, auditor, principal), per-turn binding,
fail-closed for irreversible actions. The 14 judge agents exist in `judges/`. This is the
paper's central object.

## Benchmark design (hybrid, workshop scale)

Target size: 100 to 150 cases. Domain: agentic coding (drafts produced while working in a real
repo), because that is where the auditor can verify claims with Read / Grep against ground truth.

Each case: `{ id, user_ask, repo_context, draft, evidence[], conversation?,
gold_clauses[] (INT-* rule IDs, multi-label), gold_verdict (SHIP | REVISE | FAIL),
rationale }`. This extends the existing `experiments/cases/*.json` schema, which already has
`{user_ask, draft, evidence, expected:{verdict, rationale}}`.

Crucial design choice: roughly 40 percent **clean cases that should SHIP**, so we can measure
over-flagging. Most detection papers omit this and cannot report specificity.

Per-mode sourcing:

| Clause | Existing benchmark to reuse / recast | Authoring needed |
|---|---|---|
| Hallucination (INT-HAL) | FaithBench, RAGTruth (recast to repo claims) | some |
| Confabulation (INT-CFB) | Semantic-Entropy datasets (TriviaQA etc.) | some |
| Source Fabrication (INT-SRC) | none agentic-coding specific | yes |
| Narrativity Drift (INT-NAR) | Sui & Duede signal (weak, may cut) | yes / reconsider |
| Sycophancy (INT-SYC) | SycEval, ELEPHANT (2505.13995) | recast |
| Capitulation (INT-CAP) | SycEval pressure / regressive subset | some |
| Confirmation Bias (INT-CNF) | cognitive-bias evals (2410.15413, 2509.22856) judgment-level | yes (coding) |
| Selective Evidence (INT-SEL) | none | yes |
| Anchoring (INT-ANC) | anchoring-effect study (2505.15392) judgment-level | yes (in-session) |
| Automation Bias (INT-AUT) | none agentic-coding specific | yes |
| Overconfidence (INT-OVR) | calibration literature | yes (completeness claims) |
| Prompt Injection (INT-INJ) | AgentDojo, InjecAgent, Agent-SafetyBench | reuse |
| Scope Creep (INT-SCP) | none | yes |
| Specification Gaming (INT-GAM) | EvilGenie (2511.21654), SpecBench (2605.21384), ImpossibleBench | reuse |

Honest tension to flag in the paper: reused items come from other domains (summarization, chat,
general agents). Recasting them into the agentic-coding + clause-labeled schema is partly
re-authoring. We will be explicit about which cases are imported verbatim, recast, or original,
and report results split by provenance.

Labeling: two annotators, gold by adjudication, report inter-annotator agreement (Cohen kappa)
per clause. Address the obvious threat that the authors built both the method and the labels.

## Experimental design

Conditions (keep to the method + 2 baselines for workshop scope):
1. **No audit.** The raw draft. Measures base rate of each failure mode in drafts.
2. **Free-form self-review.** "Review your draft for problems and list them." Same model, no
   contract, no clause structure. The honest baseline our prior-art note demands.
3. **Contract-grounded clause audit (ours).** CoVe verification stage, then per-clause judges,
   producing clause-traceable verdicts.

Optional stretch (likely cut for workshop): a CoVe-only condition for the factuality clauses,
and a cross-family auditor using a local permissive-license open-weight model to probe the
circularity threat (no external API, per project constraint).

Auditor model: Claude run through the Claude Code CLI harness (local, no external API). The
existing `experiments/run-suite.sh` already does this and records per-case verdicts.

Metrics:
- **Per-clause detection**: precision / recall / F1 vs gold clause labels (multi-label).
- **Verdict agreement**: agreement with gold SHIP/REVISE/FAIL, and with the held-out human.
- **Specificity / over-flag rate**: false positives on clean SHIP cases. The headline
  differentiator.
- **Rule-ID attribution accuracy**: when the audit flags, does it cite the correct INT-* rule?
  Unique to contract-grounding; free-form review scores zero here by construction.
- Optional: calibration of the audit's own confidence; cost (tokens, latency) per audit.

Expected, honest headline: contract-grounding matches or slightly beats free-form review on
recall, clearly beats it on specificity and on rule-ID attribution, while remaining advisory.
A null or negative result on recall is publishable given the specificity and traceability gains.

## Seed results (so far)

Four modes have been run end to end (Sonnet, all four conditions, easy + hard suites
each). The pattern splits cleanly along audit-target type:

| Mode | Hard suite specificity (judge vs freeform vs v5) | ruleID (judge vs others) | Open problem |
|---|---|---|---|
| Selective Evidence (INT-SEL) | 1.00 vs 0.50 vs 0.50 | 1.00 vs 0.00 | Severity calibration |
| Scope Creep (INT-SCP) | 1.00 vs 0.50 vs **0.00** | 1.00 vs 0.00 | Severity calibration |
| Capitulation (INT-CAP) | 1.00 vs 0.80 vs 0.60 | 1.00 vs 0.00 | Severity calibration |
| Source Fabrication (INT-SRC) | **0.60** vs 0.80 vs **1.00** | 0.71 vs 0.00 | Re-runs tools against real FS |

On reasoning-pattern clauses (SEL, SCP, CAP), at equal recall the clause judge wins on
specificity and rule-ID traceability. On a verification-heavy clause (SRC) the same
structure flips: the judge over-flags clean SHIP cases when the verification target is
provided text rather than a real artifact in the repo. The diagnosis and three honest
readings are in `experiments/seed-source-fabrication.md`. Severity calibration
(REVISE vs BLOCK) is the named open problem on the reasoning-pattern modes: free-form
under-grades, the clause judge over-grades on REVISE boundary cases. Full per-suite
writeups in `experiments/seed-selective-evidence.md`, `experiments/seed-scope-creep.md`,
`experiments/seed-source-fabrication.md`, and `experiments/seed-capitulation.md`. All
suites are clause-labeled and ~40% clean by design.

## Paper structure (4 to 8 pages, workshop)

1. Introduction. A confident answer and a correct answer look identical to the reader.
2. The AI Integrity Contract. RFC 2119 clauses, rule IDs, auditors, verdicts.
3. Method. Clause-grounded audit, CoVe stage, advisory stance, governance loop (brief).
4. Benchmark. Hybrid construction, 14 clauses, clean negatives, labeling, provenance.
5. Experiments. Conditions, metrics, results.
6. Related work. Prose-rubric self-review (CAI, Self-Refine, CoVe); sampling and probes
   (SelfCheckGPT, Semantic Entropy, SEPs, MiniCheck); agentic contracts and assurance
   (Trace-Based Assurance, RFCAudit, AgentVerify); per-mode benchmarks. Distinguish clearly.
7. Limitations. Circularity, same-family auditor, not SOTA factuality, small n, author-built
   labels, LLM-judge ceiling (FaithBench shows hard hallucinations near 50 percent).
8. Conclusion.

## Candidate venues

Workshop tracks where this fits: a NeurIPS / ICLR safety, evaluation, or trustworthy-ML
workshop; an ACL / EMNLP workshop on evaluation or honesty. Decide nearer submission.

## Risks and mitigations

- **Novelty challenge from trace-based assurance work.** Mitigate by sharp scoping to epistemic
  output integrity + advisory stance + cognitive taxonomy, and by citing it up front.
- **Author-built benchmark bias.** Mitigate with two annotators, kappa, provenance split, and
  releasing the benchmark.
- **LLM-as-judge unreliability.** Report agreement with humans; do not over-claim.
- **Circularity.** Name it; offer the local cross-family auditor as future work or a small probe.

## Next steps (status as of 2026-05-26)

1. ~~Verify and complete the related-work citation list.~~ **Done** in commit `43a1c63`.
   The to-verify list in this document is empty; the four held citations (AgentDojo,
   InjecAgent, RAGTruth, ImpossibleBench) are now confirmed and citable.
2. ~~Lock the benchmark schema and the clause labeling guide.~~ **Done.** Suites follow
   `{id, mode, user_ask, draft, evidence[], expected{verdict, rationale}, gold_clauses[],
   provenance}` (extends `experiments/cases/case-schema.json`). The labeling guide lives
   in each clause judge under `judges/*-judge.md`. The Capitulation suites embed the
   prior agent position and the user's pushback in `user_ask`, so no schema extension
   was needed; the earlier note here is obsolete.
3. ~~Author seed cases for one no-benchmark clause and validate end to end.~~ **Done** for
   Selective Evidence (commit `8be4bc1`, results commit `9363b5f`-adjacent).
4. ~~Run the conditions on the seed set with `run-suite.sh`.~~ **Done** for four modes via
   `experiments/run-conditions.sh` (SEL, SCP, SRC, CAP).
5. **In progress:** scale to additional modes. The Sycophancy suite is authored
   (`experiments/cases/suite-sycophancy.json`) and ready to run; other reasoning-pattern
   modes (Confirmation Bias, Anchoring, Overconfidence, Automation Bias) can reuse the
   current schema and `run-conditions.sh` directly. Verification-heavy modes
   (Hallucination, Confabulation) inherit the SRC structural caveat and need either a
   judge-prompt fix or a case-design rule before running.
6. **Then:** draft the paper sections via `/write-paper` (in a fresh Claude Code session
   so the council loads). The Experiments section can be drafted from the four
   completed modes; the cross-mode story (three reasoning-pattern wins + one
   verification-heavy counter-finding) is the headline.

## References to verify before citing (do not cite unchecked)

Confirmed in this scan (URL retrieved):
- Trace-Based Assurance Framework for Agentic AI, arXiv 2603.18096
- RFCAudit, arXiv 2506.00714
- AgentVerify, preprints.org 202604.1029
- AgentHarm (ICLR 2025), arXiv 2410.09024
- Agent-SafetyBench, arXiv 2412.14470
- OS-Harm, arXiv 2506.14866
- Evaluation and Benchmarking of LLM Agents: A Survey, arXiv 2507.21504
- ELEPHANT (social sycophancy), arXiv 2505.13995
- SycEval (Fanous, Goldberg et al.), Semantic Scholar
- EvilGenie, arXiv 2511.21654
- SpecBench, arXiv 2605.21384
- Reward Hacking Benchmark, arXiv 2605.02964
- Benchmarking Reward Hack Detection in Code Environments, arXiv 2601.20103
- A Comprehensive Evaluation of Cognitive Biases in LLMs, arXiv 2410.15413
- The Bias is in the Details, arXiv 2509.22856
- Benchmarking Cognitive Biases in LLMs as Evaluators, ACL Findings 2024 (2024.findings-acl.29)
- Understanding the Anchoring Effect of LLM, arXiv 2505.15392
- Cognitive Biases in LLMs: A Survey and Mitigation, arXiv 2412.00323
- FaithBench (NAACL 2025), arXiv 2410.13210
- Benchmarking LLM Faithfulness in RAG with Evolving Leaderboards, arXiv 2505.04847
- FaithJudge, github.com/vectara/FaithJudge
- AgentDojo (NeurIPS 2024 Datasets & Benchmarks), arXiv 2406.13352 -- Debenedetti, Zhang, Balunovic, Beurer-Kellner, Fischer, Tramèr. 97 tasks, 629 security cases over prompt injection.
- InjecAgent (ACL 2024 Findings), arXiv 2403.02691 -- Zhan, Liang, Ying, Kang (UIUC). 1,054 indirect-prompt-injection cases across 17 user tools and 62 attacker tools.
- RAGTruth (ACL 2024), arXiv 2401.00396 -- Niu, Wu, Zhu, Xu, Shum, Zhong, Song, Zhang. ~18k word-level hallucination annotations on RAG outputs.
- ImpossibleBench (preprint), arXiv 2510.20270 -- Zhong, Raghunathan, Carlini. Title: "ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases." Reward-hacking via mutated tests on LiveCodeBench / SWE-bench.

Verified on 2026-05-26; the previous "Named but arXiv ID / authors NOT yet verified" list is now empty. PAP-SRC-03 no longer holds these four citations out.

Already verified in repo prior-art (`references/prior-art.md`):
- Constitutional AI 2212.08073, Self-Refine 2303.17651, Reflexion 2303.11366,
  CoVe 2309.11495, SelfCheckGPT 2303.08896, Semantic Entropy (Nature 2024),
  SEPs 2406.15927, Semantic Energy 2508.14496, MiniCheck (EMNLP 2024),
  Sui & Duede narrativity (ACL 2024).
