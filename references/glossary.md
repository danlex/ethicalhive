---
name: tvl-tech-bias-validator-glossary
description: Related terms clustered by concept — use when disambiguating user requests or extending the skill to new failure modes.
---

# Related terms glossary

Terms that cluster around **confabulation**, **confirmation bias**, and **hallucination**. Grouped by conceptual family so you can pick the precise one for a given situation.

## Family A — fabricated or incorrect output (generation-side failures)

| Term | Precise meaning |
| --- | --- |
| **Hallucination** | Umbrella term: any generated content not supported by source or reality. |
| **Confabulation** | Subset of hallucination: *arbitrary, inconsistent* wrong output — re-sample the same prompt, get a different wrong answer (Farquhar 2024). |
| **Fabrication** | Inventing concrete specifics (names, quotes, citations, URLs) that do not exist. |
| **Faithfulness failure (intrinsic hallucination)** | Output contradicts the supplied context / source document. |
| **Factuality failure (extrinsic hallucination)** | Output contradicts real-world knowledge beyond the prompt. |
| **Post-rationalized attribution** | Citing a source that does not actually support the claim — looks grounded but is not. |
| **Citation / reference hallucination** | A specific fabrication mode: inventing non-existent papers, cases, or URLs. |
| **Ungrounded generation** | Output produced without retrieval / evidence anchoring. |
| **Over-generation** | Adding claims beyond what the prompt / context licenses. |
| **Dropout / under-generation** | Omitting required content (less famous sibling of hallucination). |

## Family B — agreement-side / user-pleasing failures

| Term | Precise meaning |
| --- | --- |
| **Sycophancy** | Excessive agreement / flattery; aligning with user's stated view over truth. |
| **Social sycophancy** | Emotional validation, moral endorsement, indirect speech softening (Cheng 2026, ELEPHANT). |
| **Sandbagging** | Deliberately performing worse when it matches user's apparent preference. |
| **Politeness bias** | Hedging or softening true statements to avoid disagreement. |
| **Yes-biased / affirmation bias** | Tendency to answer "yes" or confirm over "no" or refute. |
| **Helpfulness-over-correctness** | Complying with illogical asks because the RLHF signal rewarded helpfulness (Chen 2025). |

## Family C — reasoning / evidence-use failures

| Term | Precise meaning |
| --- | --- |
| **Confirmation bias** | Preferentially seeking or weighting evidence that supports the favored hypothesis. |
| **Anchoring bias** | Over-weighting the first piece of information encountered. |
| **Availability bias** | Preferring solutions / examples that come to mind first. |
| **Base-rate neglect** | Ignoring prior probabilities in favor of vivid specifics. |
| **Framing effect** | Answer shifts based on how the question is worded. |
| **Belief perseverance** | Retaining a conclusion even after its evidence has been discredited. |
| **Motivated reasoning** | Reasoning shaped by desired conclusion (in LLMs: shaped by reward signal). |
| **Narrativity drift** | Smooth story-form outputs mask evidence gaps (Sui & Duede 2024). |

## Family D — source-trust failures

| Term | Precise meaning |
| --- | --- |
| **Automation bias** | Over-trusting automated-system output. |
| **Authority bias** | Over-trusting a source because it is labeled authoritative. |
| **Echo chamber effect** | Reinforcement loop between user and model each re-stating the other's position. |
| **Source amnesia** | Remembering a claim but not whether the source was credible. |
| **Deference cascade** | Each step in a chain trusts the previous step without re-verification. |

## Family E — calibration failures

| Term | Precise meaning |
| --- | --- |
| **Overconfidence** | Confidence exceeds accuracy. |
| **Miscalibration** | Stated probability ≠ empirical frequency. |
| **Epistemic vs. aleatoric uncertainty** | Uncertainty from missing knowledge vs. inherent randomness — conflating them is a common failure. |
| **Semantic entropy** | Farquhar 2024: meaning-level (not token-level) uncertainty; high SE → likely confabulation. |
| **Semantic energy** | Ma 2025: Boltzmann-style refinement of SE on penultimate logits. |

## Family F — scope / behavior failures

| Term | Precise meaning |
| --- | --- |
| **Scope creep** | Answering beyond the ask. |
| **Feature creep** | Adding unrequested functionality to code changes. |
| **Specification gaming** | Satisfying the literal metric while violating the intent. |
| **Goal misgeneralization** | Pursuing a learned proxy goal when distribution shifts. |

## Quick mapping to the eight checks

- Check 1 (Confabulation) → Family A
- Check 2 (Sycophancy) → Family B
- Check 3 (Confirmation) → Family C
- Check 4 (Anchoring) → Family C
- Check 5 (Automation) → Family D
- Check 6 (Overconfidence) → Family E
- Check 7 (Narrativity drift) → Family A + C
- Check 8 (Scope creep) → Family F
