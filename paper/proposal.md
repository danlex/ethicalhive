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

## Next steps (proposed)

1. Verify and complete the related-work citation list (a few arXiv IDs below still need
   confirmation, do not cite unverified).
2. Lock the benchmark schema (extend `experiments/cases/case-schema` style) and the clause
   labeling guide.
3. Author 10 seed cases for one no-benchmark clause (suggest Selective Evidence) end to end to
   validate the pipeline before scaling.
4. Run the 3 conditions on the seed set with `run-suite.sh`, sanity-check metrics.
5. Scale to 100 to 150 cases, then write.

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

Named but arXiv ID / authors NOT yet verified (confirm before citing):
- AgentDojo, InjecAgent, RAGTruth, ImpossibleBench

Already verified in repo prior-art (`references/prior-art.md`):
- Constitutional AI 2212.08073, Self-Refine 2303.17651, Reflexion 2303.11366,
  CoVe 2309.11495, SelfCheckGPT 2303.08896, Semantic Entropy (Nature 2024),
  SEPs 2406.15927, Semantic Energy 2508.14496, MiniCheck (EMNLP 2024),
  Sui & Duede narrativity (ACL 2024).
