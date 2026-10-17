---
name: term-literature-map
description: For each EthicalHive failure-mode term, the AI-domain arXiv paper count and verified citations anchoring the term in the AI literature. Generated from the arXiv API; every citation is a real id returned by the query, not from memory.
type: reference
date: 2026-10-17
verified: counts and citations pulled live from the arXiv API on 2026-10-17; titles read to confirm AI-domain relevance and flag homonyms
---

# Term literature map

For each failure-mode term in the AI Integrity Contract (and the three proposed
additions), this records how established the term is in the AI literature and the
real papers that anchor it. Built to answer two questions before anything lands in
the paper or the contract: is this term the field's actual name for the concept,
and does it apply to AI systems rather than to human psychology.

## How this was produced

- Source: the **arXiv API**, categories `cs.AI OR cs.CL OR cs.LG` only. Reproduce
  with `experiments/arxiv_citations.py experiments/terms-clustered.tsv`.
- **Count** is arXiv's own `totalResults` for the query. It is a proxy for term
  prevalence on arXiv, not a census of AI literature (no conference-only or
  journal-only work), and a keyword hit is not a topic hit.
- **Relevance was verified by reading titles**, not assumed from the category tag.
  Two terms needed disambiguation because of homonyms *inside* AI (see notes);
  those re-queries live in `experiments/terms-disambig.tsv`.
- Every `arXiv:ID` below was returned by the API this run. None is from memory.

## What the counts show

Three tiers by how established the term is in AI:

1. **Heavily established** (safe to lead with, the field uses this exact name):
   hallucination, overconfidence, prompt injection, specification gaming (as
   "reward hacking"), sycophancy.
2. **Real but mid-sized**, often under a different field name: confirmation bias,
   anchoring, source fabrication, unfaithful reasoning, selective evidence,
   confabulation, automation bias, capitulation, side-effect blindness,
   silent-assumption gap, performative hedging.
3. **Essentially absent under this name**: scope creep (4 hits, none on topic).
   The concept is real; "scope creep" is a software-PM label the AI field does not
   use. Rename or define it explicitly in the paper.

## The map

| # | EthicalHive term | Clause | Field's term | AI count | Notes |
|---|---|---|---|---|---|
| 1 | Hallucination | INT-HAL | hallucination | 6526 | Clean. The field's exact word. |
| 2 | Confabulation | INT-CFB | confabulation | 86 | Mostly LLM; a few neural-dynamics papers use it differently. |
| 3 | Source fabrication | INT-SRC | citation / reference hallucination | 55 | Clean. Field says "citation hallucination", "citation faithfulness". |
| 4 | Narrativity drift | INT-NAR | unfaithful reasoning / CoT faithfulness | 59 | "Narrativity drift" is coined; the field's name is CoT (un)faithfulness. |
| 5 | Sycophancy | INT-SYC | sycophancy | 405 | Clean. The field's exact word. |
| 6 | Capitulation | INT-CAP | sycophantic capitulation / under pushback | 34 | Clean; small but growing (2026 papers). |
| 7 | Confirmation bias | INT-CNF | confirmation bias (reasoning) | 84 | Disambiguated: raw 155 was inflated by the pseudo-label homonym in semi-supervised learning. |
| 8 | Selective evidence | INT-SEL | motivated reasoning / cherry-picking | 61 | Disambiguated: raw 135 included generic cherry-picking (news, time-series). |
| 9 | Anchoring | INT-ANC | anchoring bias / effect | 55 | Clean. Papers study anchoring *in* LLMs. |
| 10 | Automation bias | INT-AUT | automation bias | 42 | Clean, but the classic sense is *humans* over-trusting automation; our sense (agent over-trusting its own tools) is adjacent. |
| 11 | Overconfidence | INT-OVR | overconfidence / miscalibration | 1447 | Broad: sweeps in general model-calibration work. |
| 12 | Prompt injection | INT-INJ | prompt injection | 827 | Clean. The field's exact word. |
| 13 | Scope creep | INT-SCP | (none established) | 4 | No AI literature under this name. Rename/define. |
| 14 | Specification gaming | INT-GAM | reward hacking | 642 | The field's name is "reward hacking"; "specification gaming" alone was 60. Name both. |
| 15 | Side-effect blindness | (proposed) | avoiding (negative) side effects | 47 | RL-safety framed (Krakovna lineage); our coding-agent framing is the applied case. |
| 16 | Silent-assumption gap | (proposed) | underspecification / clarification questions | 194 | The ask-vs-assume literature is the anchor. |
| 17 | Performative hedging | (proposed) | verbalized confidence / uncertainty | 138 | Overlaps overconfidence (same calibration axis, opposite direction). |

## Definitions and anchor citations

Clause definitions are condensed from Section 8 of
`contracts/ai-integrity-contract.md`; the proposed additions (15-17) from
`references/research-2026-04-25-additional-failure-modes.md`.

### 1. Hallucination (INT-HAL)
Stating as fact a claim not traceable to the supplied sources, tools, or context.
- arXiv:2509.21473 (2025) - Are Hallucinations Bad Estimations?
- arXiv:2507.20836 (2025) - First Hallucination Tokens Are Different from Conditional Ones

### 2. Confabulation (INT-CFB)
Supplying a confident specific (name, number, citation) that would differ on
re-asking; an ungrounded, arbitrary answer.
- arXiv:2406.04175 (2024) - Confabulation: The Surprising Value of Large Language Model Hallucinations
- arXiv:2511.07722 (2025) - Critical Confabulation: Can LLMs Hallucinate for Social Good?

### 3. Source fabrication (INT-SRC)
A cited path, line, symbol, or URL that does not resolve to what the agent says it
does. Groundedness of the *attribution*, not of the claim.
- arXiv:2502.10881 (2025) - CiteCheck: Towards Accurate Citation Faithfulness Detection
- arXiv:2605.08583 (2026) - Source or It Didn't Happen: A Multi-Agent Framework for Citation Hallucination Detection

### 4. Narrativity drift (INT-NAR)
Presenting an inferred or assumed step as verified fact; smoothing unverified
reasoning into a confident narrative. Field name: chain-of-thought faithfulness.
- arXiv:2405.15092 (2024) - Dissociation of Faithful and Unfaithful Reasoning in LLMs
- arXiv:2602.14469 (2026) - Measuring and Mitigating Post-hoc Rationalization in Reverse Chain-of-Thought Generation

### 5. Sycophancy (INT-SYC)
Agreeing with the user where evidence does not support it; adopting a user premise
without independent grounding.
- arXiv:2409.01658 (2024) - From Yes-Men to Truth-Tellers: Addressing Sycophancy in Large Language Models with Pinpoint Tuning
- arXiv:2608.26511 (2026) - Sycophancy Suppression Can Impair Rational Updating

### 6. Capitulation (INT-CAP)
Reversing a grounded position, or walking back a justified refusal, under pushback
with no new evidence.
- arXiv:2607.19629 (2026) - Adaptive Capitulation: A Structural Failure Mode of LLM Responses in Vulnerability Contexts
- arXiv:2608.21377 (2026) - Agentic Scaffolding Amplifies Sycophantic Behavior in Large Language Models

### 7. Confirmation bias (INT-CNF)
Reaching a positive conclusion without stating and testing the alternative
explanation. (Reasoning sense, not the semi-supervised pseudo-label homonym.)
- arXiv:2506.12301 (2025) - Unveiling Confirmation Bias in Chain-of-Thought Reasoning
- arXiv:2604.02485 (2026) - Failing to Falsify: Evaluating and Mitigating Confirmation Bias in Language Models

### 8. Selective evidence (INT-SEL)
Omitting disconfirming results the agent already gathered this session. Distinct
from confirmation bias (which is one-sided *searching*).
- arXiv:2601.16130 (2026) - Replicating Human Motivated Reasoning Studies with LLMs
- arXiv:2510.17057 (2025) - The Ends Justify the Thoughts: RL-Induced Motivated Reasoning in LLM CoTs

### 9. Anchoring (INT-ANC)
Retaining an initial framing after later evidence has broken it.
- arXiv:2505.15392 (2025) - Understanding the Anchoring Effect of LLM with Synthetic Data
- arXiv:2412.06593 (2024) - Anchoring Bias in Large Language Models: An Experimental Study

### 10. Automation bias (INT-AUT)
Treating a tool result or prior step as correct because a machine produced it,
without verifying the load-bearing part against the source.
- arXiv:2204.08859 (2022) - On the Influence of Explainable AI on Automation Bias
- arXiv:2508.07617 (2025) - Selective Prediction Reduces the Negative Effects of Automation Bias

### 11. Overconfidence (INT-OVR)
Stated confidence or completeness ("all", "every", "only") exceeding the evidence.
- arXiv:2508.11800 (2025) - Uncalibrated Reasoning: GRPO Induces Overconfidence for Stochastic Outcomes
- arXiv:2203.09852 (2022) - Decision-Making under Miscalibration

### 12. Prompt injection (INT-INJ)
Acting on instructions embedded in observed content (files, web pages, tool
results) instead of treating that content as data.
- arXiv:2403.04957 (2024) - Automatic and Universal Prompt Injection Attacks against Large Language Models
- arXiv:2410.05451 (2024) - SecAlign: Defending Against Prompt Injection with Preference Optimization

### 13. Scope creep (INT-SCP)
Answering or doing more than the request, undisclosed. No AI literature uses this
name; the nearest formal treatment is agent task-boundary / problem-framing work.
- arXiv:2602.19065 (2026) - Agentic Problem Frames: A Systematic Approach to Engineering Reliable Domain Agents
- (No direct "scope creep" AI citation exists; define the term in-paper.)

### 14. Specification gaming (INT-GAM)
Solving the metric that measures the task rather than the task; editing tests,
hardcoding outputs, suppressing errors. Field name: reward hacking.
- arXiv:2605.02269 (2026) - Towards Understanding Specification Gaming in Reasoning Models
- arXiv:2511.21654 (2025) - EvilGenie: A Reward Hacking Benchmark

### 15. Side-effect blindness (proposed)
Performing collateral effects (file overwrite outside scope, dependency change,
irreversible command) without disclosing or weighing them.
- arXiv:2006.06547 (2020) - Avoiding Side Effects in Complex Environments
- arXiv:2008.12146 (2020) - Avoiding Negative Side Effects due to Incomplete Knowledge of AI Systems

### 16. Silent-assumption gap (proposed)
Guessing unspecified requirements instead of asking, then committing to the guess.
- arXiv:2310.11571 (2023) - Alexpaca: Learning Factual Clarification Question Generation Without Examples
- arXiv:2006.05986 (2020) - ClarQ: A large-scale and diverse dataset for Clarification Question Generation

### 17. Performative hedging (proposed)
Vague, non-committal hedging when the evidence licenses a commitment; the
underclaim counterpart to overconfidence.
- arXiv:2510.10913 (2025) - ADVICE: Answer-Dependent Verbalized Confidence Estimation
- arXiv:2609.10996 (2026) - Rethinking Verbalized Confidence for LLM-as-a-Judge

## Caveats

- arXiv only. ACL Anthology, NeurIPS/ICML proceedings not cross-posted, and journal
  work are not counted. Treat counts as lower bounds on a term's real footprint.
- Counts drift as arXiv grows; the date in the frontmatter is the snapshot.
- Two homonym corrections were applied by reading titles. Others may remain; re-run
  `experiments/term-sample-titles.sh '<clause>'` before trusting any single count.
