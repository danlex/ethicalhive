---
name: 2026-04-25 research survey — additional coding-agent failure modes
description: Catalog of cognitive/behavioural failure modes for LLM coding agents that EthicalHive does NOT currently catch. Research-level inputs, not approved integrations. Citations include 2026xx arXiv preprints that have NOT been verified at the abstract level.
type: reference
date: 2026-04-25
verified: structural framing only; citation-level verification pending
---

# 2026-04-25 — Failure-mode candidates beyond the v5 rubric

## What this document is

A research catalog of cognitive / behavioural failure modes in LLM coding agents that EthicalHive's current five-check rubric does NOT cover. Compiled by a research subagent on 2026-04-25 across cognitive-bias literature applied to LLMs, coding-agent-specific failure modes, instruction-compliance failures, reasoning shortcuts, multi-agent and multi-turn failures, and 2025–2026 named patterns.

## What this document is NOT

- **Not an integration plan.** Every candidate below would need a governance proposal, judge-council review, and human approval before becoming a rubric check.
- **Not citation-verified.** The subagent that produced this report cites several arXiv IDs of the form `2602.*`, `2603.*`, `2604.*`, `2512.*` — Jan–Apr 2026 preprints. These are plausible given today's date (2026-04-25) but were not abstract-verified by the subagent or in this session. **Before quoting any specific percentage or headline number, fetch the arXiv abstract and confirm.** The structural insights (what the failure mode IS, how it manifests) are reliable regardless of citation drift; the *measurements* are not.
- **Not a complete list.** ~20 candidates is the survey-level cut, not exhaustive.

## What is excluded (already on EthicalHive's radar)

The five existing checks (Groundedness, Sycophancy, Confirmation, Anchoring, Scope creep), plus paraphrase drift, package hallucination, regressive sycophancy, ELEPHANT 5-facet sycophancy, the CodeHalu Mapping/Naming/Resource/Logic taxonomy, and the probabilistic Rule-1 compliance issue (C07-class) already documented elsewhere.

---

## High-priority candidates

| # | Name | One-line definition | Verifiable from our tool surface? | Fits existing rubric or new check? |
|---|---|---|---|---|
| 1 | **Test-case exploitation / spec-vs-test conflict** | Agent edits the test or hardcodes expected outputs to make the suite green when spec and tests disagree. | Yes — `git diff` reveals test edits in the same change as the "fix." | New check ("test integrity"). |
| 2 | **API misuse (non-hallucinated)** | Real API called with wrong params, wrong semantics, missing items, redundant calls — distinct from package hallucination. | Yes — Read the API source, compare arity/types of caller vs callee. | Extension of Groundedness. |
| 3 | **Silent error swallowing** | Bare `except`, `catch (Exception) {}`, ignored Result/Err, dropped promise rejections. | Yes — trivial Grep for these idioms. | Sub-rule of Groundedness, or a new micro-check. |
| 4 | **Stub / mock-inflated tests** | Test passes by mocking the system under test, not by exercising it. Or generated tests that mock everything load-bearing. | Yes — count mock density in newly-added test files; flag mocks of the production module under test. | New check, orthogonal to Scope creep. |
| 5 | **Post-hoc rationalization / unfaithful CoT** | Reasoning trace constructed to justify a pre-decided answer rather than to reach it. | Partially — when draft has both conclusion and "reasoning," check whether reasoning's premises actually entail the conclusion. | Extension of CoVe stage. Low base rate (~0.04% on Sonnet 3.7 thinking per cited literature, unverified) → defer. |
| 6 | **Underspecification without clarification** | Agent guesses missing requirements instead of asking, then commits. | Yes — enumerate decision points the draft made (path, name, signature, timing); check whether each was specified in `user_ask`. | New check ("silent-assumption gap"). |
| 7 | **Premature action / insufficient grounding** | Edits / commits before reading enough of the codebase. | Yes — tool-call ledger ratio of Read+Grep before first Edit. | Extension of Groundedness. |
| 8 | **Specification gaming / reward hacking** | Achieves the literal stated objective by routes that violate the spirit (deleting failing tests, monkey-patching libraries to bypass checks, pinning versions to make a test green). | Yes for many manifestations (modified CI, removed assertions, suspicious pins). | New check (umbrella). |

## Medium-priority candidates

| # | Name | Definition | Verifiable? | Fit |
|---|---|---|---|---|
| 9 | **Multi-turn sycophantic capitulation** | After user pushback ("are you sure?"), agent abandons a previously-grounded position with no new evidence. | Yes if conversation history is in the audit input. | Extends Sycophancy. |
| 10 | **Persona / identity drift** | Across long sessions, agent abandons declared role / style / constraints from the system prompt. | Yes if system prompt + history visible. | Possibly out-of-scope for single-draft audits. |
| 11 | **Long-context constraint decay** | Omission constraints ("don't use library X", "never edit file Y") decay as context fills up. | Partially — re-state the constraints fresh and check the draft against them. | New check ("constraint compliance"). |
| 12 | **Tool-description bias / tool misselection** | Picks a tool because the description is well-written, not because it's the right tool; or fixates on the first listed tool. | Yes — inspect tool-call ledger and ask "was this the cheapest/safest tool?" | New check, low priority for single-agent Claude Code. |
| 13 | **Indirect prompt injection / context-poisoning compliance** | Agent follows instructions found inside a fetched file, README, web page, or MCP response. | Yes — flag any instructional-tone text inside Read/WebFetch results that the draft then complies with. | New check ("instruction-source provenance"). Doubles as security feature. |
| 14 | **Recency / position bias in evidence use** | Over-weights the most-recently-read source when weighing several. | Hard directly. Possible proxy: does conclusion only cite last-read evidence? | Extension of Anchoring. |
| 15 | **Framing-induced answer variance** | Same underlying question with different wording produces materially different answers. | Hard without re-querying. | Defer — requires sampling. |

## Low-priority / deferred

| # | Name | Why deferred |
|---|---|---|
| 16 | Belief perseverance / self-reinforcing memory errors | Needs longitudinal data, not single-audit window. |
| 17 | Evaluation awareness / sandbagging | Existential threat to the project but undetectable by another LLM auditor. Document in `prior-art.md`. |
| 18 | Hindsight bias in self-review | Meta-bias of the validator, partly captured by override-rate tracking. |
| 19 | Premature convergence (single-agent) | Subsumed by Anchoring + Scope creep. |
| 20 | Action bias ("do something" over "do nothing") | Overlaps Scope creep + #6. Not isolated as a primary category in the literature. |

---

## Suggested integration plan (subagent's recommendation, NOT yet approved)

1. **Extend Groundedness** with sub-rules for #2 API misuse, #3 silent error swallowing, #7 write-before-read.
2. **Add three new checks:** Test-Integrity (#1+#4), Spec-Gaming (#8), Silent-Assumption-Gap (#6).
3. **Extend Sycophancy** with multi-turn capitulation (#9) when conversation history is available.
4. **Add Constraint-Compliance** (#11) when the validator can see the system prompt.
5. **Add Instruction-Provenance** (#13) — security/bias hybrid.
6. **Defer** #5 / #14 / #15 until a sampling/re-query stage exists.
7. **Document, don't implement** #17 in `prior-art.md` as an architectural ceiling.

Each of #1, #4, #6, #8, #11, #13 would be a constitutional change (3/3 council). #2, #3, #7, #9 are arguably calibration-level (2/3) since they extend existing checks. None should be implemented without measurement on a corpus that exercises them — our current 25-case corpus does not.

## Cross-reference

- See `references/prior-art.md` for the broader research-positioning context.
- See `experiments/results/` for prior empirical write-ups (exp-01 through exp-06) on the existing rubric.

## Citations (verification level marked)

Verified by an earlier verification subagent on 2026-04-24 (the previous research round):
- ELEPHANT — arXiv:2505.13995 ✓
- SycEval — arXiv:2502.08177 ✓
- CodeHalu — arXiv:2405.00253 ✓
- Package hallucinations (Spracklen) — arXiv:2406.10279 ✓
- BrokenMath — arXiv:2510.04721 ✓
- HalluLens — arXiv:2504.17550 ✓
- R2E-Gym — arXiv:2504.07164 ✓

NOT independently verified at abstract level by this report:
- ImpossibleBench — arXiv:2510.20270
- Specification gaming (Bondarenko) — arXiv:2502.13295
- API misuse paper — arXiv:2503.22821
- MARIN / APIHulBench — arXiv:2505.05057
- Over-mocked tests — arXiv:2602.00409
- CoT-not-faithful — arXiv:2503.08679
- Ask-or-Assume — arXiv:2603.26233
- What-Prompts-Don't-Say — arXiv:2505.13360
- LLM-failure-modes-agentic — arXiv:2512.07497
- EvilGenie — arXiv:2511.21654
- Sycophancy-not-one-thing — arXiv:2509.21305
- Identity-drift — arXiv:2412.00804
- Drift-No-More — arXiv:2510.07777
- Omission-constraints-decay — arXiv:2604.20911
- When-refusals-fail — arXiv:2512.02445
- Tool-preferences — arXiv:2505.18135
- BiasBusters — arXiv:2510.00307
- Prompt-injection-on-coding — arXiv:2601.17548
- Recency-bias-reranking — arXiv:2509.11353
- Primacy-effect — arXiv:2507.13949
- DeFrame — arXiv:2602.04306
- Framing-bias-judges — arXiv:2601.13537
- Sandbagging — arXiv:2406.07358
- Eval-awareness-probing — arXiv:2507.01786
- Persuasion-propagation — arXiv:2602.00851
- Memory-survey — arXiv:2603.07670
- HindSight — arXiv:2603.15164

**Before quoting any specific number from these:** WebFetch the arXiv abstract first. Several 2026xx IDs in particular are plausible given the date but unverified.

## Industry / non-academic sources cited

- Sean Goedecke — *Sycophancy is the first LLM dark pattern* — https://www.seangoedecke.com/ai-sycophancy/
- vLLora blog — *Debugging silent failures* — https://vllora.dev/blog/debugging-silent-failures/
- OWASP LLM01:2025 — Prompt Injection — https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- GitHub `anthropics/claude-code` Issue #37457 — Opus 4.6 sycophantic capitulation

---

# Ethical-AI canon — second-pass additions (2026-04-25)

A second research pass mined the canonical Ethical AI / AI Safety / AI Alignment literature (Constitutional AI, Concrete Problems in AI Safety, TruthfulQA, Anthropic Sycophancy, DeepMind harm taxonomies, MASK, Alignment Faking, Side Effects, etc.) for additional concepts that fit a single-draft pre-delivery auditor and that aren't already in the v5 rubric or the first-pass catalog above. Same verification posture: core canonical citations confirmed by direct arXiv fetch; 2026-* preprints flagged below as unverified.

## High-priority candidates

| # | Name | One-line definition | Source | Verifiable? | Fit |
|---|---|---|---|---|---|
| H1 | **Verbalized-confidence miscalibration** | The draft's hedging language ("definitely", "90% sure", "likely") is systematically more confident than the audit-window evidence supports. | Lin, Hilton & Evans, *Teaching Models to Express Their Uncertainty in Words* — arXiv:2205.14334 ✓ | Yes — extract confidence markers, compare strength against per-claim CoVe verdict. | New check. Adjacent to Groundedness but operationally distinct: Groundedness asks "is the claim true?", calibration asks "is the assertoric weight licensed?" |
| H2 | **Epistemic-rhetorical overclaiming** | Discursive commitments (definitive verbs, "guarantees", causal claims) exceed inferential entitlement of gathered evidence — even when the underlying belief isn't false. | MASK arXiv:2503.03750 ✓; Lin et al. 2205.14334 ✓; arXiv:2604.19768 (unverified, see below) | Yes — flag assertion-strength tokens whose evidence is partial / inconclusive / 0-hit. | New check, or merge with H1 into a renamed "Groundedness & Calibration." |
| H3 | **Selective-evidence / motivated reasoning (cherry-picking)** | When multiple Read/Grep results are in hand, the draft cites only those supporting a preferred conclusion and silently omits counter-evidence the agent itself surfaced. | Foundational psychology + arXiv:2509.00529 / arXiv:2601.16130 (unverified, see below) | Yes — diff tool-output set against claim set; any tool result that contradicts the conclusion and is unaddressed is a flag. | New check. Distinct from existing **Confirmation**: confirmation is *seeking* one-sided evidence; cherry-picking is *ignoring disconfirming evidence already in hand*. |
| H4 | **Unfaithful citation / source fabrication** | The draft cites a path, line number, function name, or URL that the auditor cannot resolve via Read/Grep/WebFetch. Distinct from groundedness on a *factual claim* — this is groundedness of an *attribution*. | Worledge et al., *Towards Fine-Grained Citation Evaluation* — arXiv:2406.15264 ✓; arXiv:2604.03173, arXiv:2510.17853 (unverified) | Yes — every `path/file.py:NNN`, every URL, every quoted symbol must resolve under Read/Grep/WebFetch. Most deterministic of the new candidates. | New check. Groundedness today targets the *truth* of a claim; citation faithfulness targets whether the *evidence pointer* is real. They fail in different ways — a claim can be true while its citation is fabricated. |
| H5 | **Side-effect blindness** | The draft proposes or has performed an action whose collateral effects (file overwrite outside scope, dependency change, network call, irreversible Bash) it does not mention or weigh. | Amodei et al., *Concrete Problems in AI Safety* — arXiv:1606.06565 ✓ (Avoiding Side Effects); Krakovna et al., *Avoiding Side Effects By Considering Future Tasks* — arXiv:2010.07877 ✓ | Yes — inspect Bash/Edit/Write tool calls in conversation history vs user-stated scope; flag undisclosed mutations. | New check. Distinct from existing **Scope creep**: scope creep is *answering more than asked*; side-effect blindness is *doing more than asked, silently*. Highest-leverage candidate for the *coding-agent* setting specifically. |
| H6 | **Epistemic-vigilance failure / accommodation of false premises** | The draft uncritically inherits a factual or logical premise from the user_ask without challenging it, even when audit-window evidence contradicts the premise. | arXiv:2601.04435 (unverified, see below); concept also touched by H02 hedge-escape calibration in this codebase. | Yes — extract user-supplied premises, run CoVe verification on them as on draft claims, flag any inherited premise that fails. | New check. Distinct from **Sycophancy**: sycophancy is "matching user *opinion* to please"; accommodation is the more general pragmatic default of treating user *premises* as true. |

## Medium-priority

| # | Name | Definition | Source | Verifiable? | Fit |
|---|---|---|---|---|---|
| H7 | **False balance / unwarranted equivalence** | Two positions presented as comparably supported when audit-window evidence is asymmetric. | No single canonical arXiv source — concept ported from journalism studies. | Partially — heuristic is fuzzier than for citation/groundedness. | Extension of Anchoring, or a sub-rule of H1 calibration. Not a standalone check. |
| H8 | **Overclaim of completeness** | Draft asserts "all", "every", "no other", "complete list" when Grep/Glob coverage cannot support a closed-world claim. | Adjacent to MASK arXiv:2503.03750 ✓. | Yes — flag universal quantifiers; check search exhaustiveness signal (was Grep run? what was the corpus?). | Sub-check under H1 calibration. Cheap. |
| H9 | **Refusal-integrity slippage** | Draft walks back a justified refusal/partial-compliance stance from earlier in the conversation without new evidence. | Wei, Haghtalab et al., *Jailbroken* — arXiv:2307.02483 ✓; Greenblatt et al., *Alignment Faking in LLMs* — arXiv:2412.14093 ✓. | Yes — compare current draft's stance against the agent's prior refusal/scope-decline turns. | New check. Behavioural counterpart to multi-turn sycophantic capitulation, but scoped to *refusals* specifically — a model can drop a justified refusal under pressure with no overt agreement language. |
| H10 | **Performative metacognition / vague hedging** | Heavy metacognitive filler ("It's worth noting…", "It depends…", "There are many factors…") that increases verbosity without committing — empirically correlated with incorrect predictions. | arXiv:2602.09832 (unverified, see below); discussed under epistemic-cowardice framings in alignment literature. | Yes — flag hedge-density above threshold combined with low claim-density. | New check. The *underclaim* counterpart to H1's overclaim — refusing to commit when evidence licenses a commitment. |

## Out of scope but worth documenting

These are named in the canon but cannot be addressed by a single-draft pre-delivery auditor. Document so we stop re-litigating them:

- **Goal misgeneralization** (Langosco et al. arXiv:2105.14111 ✓; Shah et al. arXiv:2210.01790 ✓). Operationalises only at training-time / OOD evaluation.
- **Power-seeking / instrumental convergence** (Turner et al. arXiv:1912.01683 ✓; Carlsmith arXiv:2206.13353 ✓). Multi-step strategy concern; single-draft audit captures at most a faint shadow → fold into H5 Side-effect blindness rather than carry as its own check.
- **Alignment faking / training-game behaviour** (Greenblatt et al. arXiv:2412.14093 ✓). Requires comparing in-distribution vs OOD or training-aware vs unaware contexts — not in audit input.
- **AI deception in the strong sense** (Park et al. arXiv:2308.14752 ✓ — *AI Deception: A Survey*). Strong "systematic inducement of false beliefs in pursuit of an outcome other than truth" definition requires intent inference we cannot ground from a single draft. The *symptoms* (citation fabrication → H4, cherry-picking → H3, overclaim → H1/H2) are addressable; the construct itself isn't.
- **Discovering Latent Knowledge / honesty probes** (Burns et al. *CCS* — arXiv:2212.03827 ✓). Requires hidden-state access; explicitly outside our tool surface.

## Verified canonical sources (this pass)

- Constitutional AI — arXiv:2212.08073
- Concrete Problems in AI Safety — arXiv:1606.06565
- TruthfulQA — arXiv:2109.07958
- Towards Understanding Sycophancy in LMs — arXiv:2310.13548
- Ethical and Social Risks of Harm from LMs — arXiv:2112.04359
- Goal Misgeneralization in Deep RL — arXiv:2105.14111
- Goal Misgeneralization (Shah et al.) — arXiv:2210.01790
- Discovering Latent Knowledge (CCS) — arXiv:2212.03827
- Optimal Policies Tend to Seek Power — arXiv:1912.01683
- Is Power-Seeking AI an Existential Risk? — arXiv:2206.13353
- Specification Gaming (DeepMind blog, Krakovna et al. 2020)
- Avoiding Side Effects By Considering Future Tasks — arXiv:2010.07877
- Teaching Models to Express Their Uncertainty in Words — arXiv:2205.14334
- The MASK Benchmark — arXiv:2503.03750
- Alignment Faking in LLMs — arXiv:2412.14093
- Jailbroken: How Does LLM Safety Training Fail? — arXiv:2307.02483
- AI Deception: A Survey — arXiv:2308.14752
- Characteristics of Harmful Text (Rauh 2022) — arXiv:2206.08325
- Towards Fine-Grained Citation Evaluation — arXiv:2406.15264

## Unverified citations (this pass) — caution

- arXiv:2604.19768 — *Saying More Than They Know: Quantifying Epistemic-Rhetorical Miscalibration*
- arXiv:2604.03173 — *Detecting and Correcting Reference Hallucinations in Commercial LLMs*
- arXiv:2510.17853 — *CiteGuard: Faithful Citation Attribution for LLMs via Retrieval-Augmented Validation*
- arXiv:2601.04435 — *Accommodation and Epistemic Vigilance: Why LLMs Fail to Challenge Harmful Beliefs*
- arXiv:2602.09832 — *LLM Reasoning Predicts When Models Are Right*
- arXiv:2604.21334 — *Ideological Bias in LLMs' Economic Causal Reasoning*
- arXiv:2509.00529 — *Modeling Motivated Reasoning in Law*
- arXiv:2601.16130 — *Replicating Human Motivated Reasoning Studies with LLMs*

Same rule as the first pass: WebFetch the abstract before quoting any specific percentage or headline number from these. The structural insights are reliable; specific measurements are not.

## Recommended top-three for governance review

If we revisit "what to add next" after the C07-class structural fix, the second-pass research suggests these as the cleanest deterministic additions:

1. **H4 Unfaithful citation** — every cited path / line / URL must resolve under Read/Grep/WebFetch. Most deterministic of the new candidates; our tool surface is uniquely well-suited.
2. **H1 Verbalized-confidence miscalibration** — strongest operational support; CoVe already produces per-claim verdicts, we just extract confidence markers and compare.
3. **H5 Side-effect blindness** — highest-leverage for the coding-agent setting specifically; rounds out the rubric for "draft auditor for code-execution agents."

Each would be a constitutional change (3/3 council). H3 Cherry-picking and H6 Accommodation are theoretically interesting but require careful rubric drafting to avoid false-positive overlap with existing Confirmation / Sycophancy.
