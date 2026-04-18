---
name: tvl-tech-bias-validator-research
description: Research citations (2023-2026) grounding each of the eight bias checks. Consult when a check needs justification or when extending the skill.
---

# Research grounding for tvl-tech-bias-validator

Each of the eight checks maps to peer-reviewed work from 2023 onward. Full list below.

## 1. Confabulation & semantic entropy
- **Farquhar, Kossen, Kuhn, Gal (2024). "Detecting hallucinations in large language models using semantic entropy." _Nature_ 630, 625–630.** Introduces meaning-level (not token-level) entropy as a detector for a subset of hallucinations called *confabulations* — arbitrary, incorrect generations. Evaluated on TriviaQA, SQuAD, BioASQ, NQ-Open, SVAMP, FactualBio. https://www.nature.com/articles/s41586-024-07421-0
- **Kossen et al. (2024). "Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs."** Linear probes on hidden states approximate semantic entropy at near-zero test-time cost. ICLR 2025 submission. https://arxiv.org/abs/2406.15927
- **Ma et al. (2025). "Semantic Energy: Detecting LLM Hallucination Beyond Entropy."** Extends semantic entropy via Boltzmann-inspired energy on penultimate-layer logits for cases where SE fails. https://arxiv.org/abs/2508.14496

## 2. Narrativity as a confabulation signal
- **Sui & Duede (2024). "Confabulation: The Surprising Value of Large Language Model Hallucinations." _ACL 2024_.** Hallucinated outputs exhibit *higher* narrativity and semantic coherence than veridical outputs — i.e. smooth fluent prose is the surface where confabulations hide. Motivates the "narrativity drift" check. https://aclanthology.org/2024.acl-long.770/

## 3. Sycophancy
- **Sharma et al. (2023). "Towards Understanding Sycophancy in Language Models."** First systematic study of agreement-biased LLM behavior. https://arxiv.org/abs/2310.13548
- **Malmqvist (2024). "Sycophancy in Large Language Models: Causes and Mitigations."** https://arxiv.org/abs/2411.15287
- **Chen et al. (2025). "When helpfulness backfires: LLMs and the risk of false medical information due to sycophantic behavior." _npj Digital Medicine_.** Up to 100% compliance with illogical prompts even when the model held knowledge to refuse. https://www.nature.com/articles/s41746-025-02008-z
- **Cheng et al. (2026). "ELEPHANT: Measuring and understanding social sycophancy in LLMs." _ICLR 2026_.** Taxonomy separating emotional validation, moral endorsement, indirect speech, etc. https://openreview.net/forum?id=igbRHKEiAs
- **Anon. (2025). "Sycophancy Is Not One Thing: Causal Separation of Sycophantic Behaviors in LLMs."** Shows sycophantic vs. genuine agreement are directionally distinct in middle-layer hidden space. https://arxiv.org/html/2509.21305v1

## 4. Confirmation bias in human-AI interaction
- **Journal of Medical Internet Research (2025). "Shoggoths, Sycophancy, Psychosis, Oh My: Rethinking Large Language Model Use and Safety."** Documents the user-side confirmation-bias loop: chatbots reflect user perspective → validation → more engagement → deeper bias. https://www.jmir.org/2025/1/e87367

## 5. Cognitive bias (general) in generative AI
- **NEJM AI (2024). "Cognitive Biases and Artificial Intelligence."** Generative AI exhibits human-like cognitive biases, with magnitudes sometimes larger than in practicing clinicians. https://ai.nejm.org/doi/abs/10.1056/AIcs2400639
- **Kumar et al. (2025). Systematic literature review on bias mitigation in generative AI. _AI and Ethics_, Springer.** Comprehensive review across text, image, audio, video generation. https://link.springer.com/article/10.1007/s43681-025-00721-9
- **PMC (2025). "Forewarning Artificial Intelligence about Cognitive Biases."** Explicit forewarning reduces overall bias by only ~6.9%; no bias was fully extinguished. Implication: a bias check must be structural (this skill), not a one-line warning. https://pmc.ncbi.nlm.nih.gov/articles/PMC12413502/
- **HBR (2026). "When AI Amplifies the Biases of Its Users."** Bidirectional amplification: AI biases reshape human judgment over time, not only vice versa. https://hbr.org/2026/01/when-ai-amplifies-the-biases-of-its-users
- **arXiv (2025). "Beyond Isolation: Towards an Interactionist Perspective on Human Cognitive Bias and AI Bias."** https://arxiv.org/html/2504.18759v1

## 6. Automation bias & cognitive reflection
- **ScienceDirect (2025). "Mitigating Automation Bias in Generative AI Through Nudges: A Cognitive Reflection Test Study."** Participants receiving faulty AI support performed significantly worse on CRT, indicating uncritical acceptance of AI output. https://www.sciencedirect.com/science/article/pii/S1877050925030042

## 7. Adversarial angle
- **Frontiers in AI (2025). "Weaponizing cognitive bias in autonomous systems: a framework for black-box inference attacks."** Documents that LLM cognitive biases are exploitable by adversaries — motivates treating bias audit as a security concern, not just quality. https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1623573/full

## Mapping to the eight checks

| Check | Primary citations |
| --- | --- |
| 1. Confabulation | Farquhar 2024, Kossen 2024, Ma 2025 |
| 2. Sycophancy | Sharma 2023, Malmqvist 2024, Chen 2025, Cheng 2026 |
| 3. Confirmation bias | JMIR 2025, HBR 2026 |
| 4. Anchoring | NEJM AI 2024, Kumar 2025 |
| 5. Automation / authority | ScienceDirect 2025, PMC Forewarning 2025 |
| 6. Overconfidence | Farquhar 2024 (semantic entropy), Ma 2025 |
| 7. Narrativity drift | Sui & Duede 2024 |
| 8. Scope creep | Chen 2025 (helpfulness → harm pathway) |
