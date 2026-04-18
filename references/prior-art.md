---
name: tvl-tech-bias-validator-prior-art
description: Honest comparison of tvl-tech-bias-validator against existing self-review / hallucination-detection methods. Read before making claims about novelty or performance.
---

# Prior art — where tvl-tech-bias-validator actually sits

The eight-check rubric is a member of the "LLM reviews LLM output using a prose rubric" family. That family has prior art back to 2022. Claiming novelty without this context is dishonest. Claiming SOTA is dishonest regardless. This document catalogues what already exists, what each method actually does, and where tvl-tech-bias-validator's contribution ends.

## Method families

There are three operational families of self-review / hallucination mitigation in the literature. Bias-validator belongs only to the first.

### Family 1 — Prose-rubric self-review (what we are)

| Method | Mechanism | Targets | Reported headline |
| --- | --- | --- | --- |
| **Constitutional AI** (Bai et al., Anthropic 2022, arXiv 2212.08073) | Self-critique + revision against a list of written principles; used for RLAIF training | Harmlessness / safety | Used to train Claude; no single bias-detection AUROC |
| **Self-Refine** (Madaan et al. 2023, arXiv 2303.17651) | Same LLM generates draft → critiques own draft → revises; iterated | Task quality across 7 tasks | ~20% absolute task performance lift vs single-pass |
| **Reflexion** (Shinn et al. 2023, arXiv 2303.11366) | Verbal reflection on task feedback stored in episodic memory, reused across attempts | Agent task success (coding, decision-making) | 91% pass@1 on HumanEval (vs GPT-4's 80%) |
| **Chain-of-Verification (CoVe)** (Dhuliawala et al., Meta 2023, arXiv 2309.11495) | Draft → generate verification questions → answer them independently → revise | Factual hallucination in long-form generation | Headline numbers not in abstract — needs full-paper read |
| **tvl-tech-bias-validator** (this skill) | Subagent runs 8-check rubric against draft + evidence pointers | Confabulation, sycophancy, confirmation, anchoring, automation, overconfidence, narrativity, scope creep | **Not measured.** |

**Honest placement:** tvl-tech-bias-validator is closest to Constitutional AI's self-critique stage, generalised to cover bias classes beyond safety. It is strictly weaker than CoVe on factuality (we do not generate verification questions and answer them independently — we just look at the draft and "flag"), strictly weaker than Self-Refine as a quality lifter (we do not iterate by default — we block/revise/ship). It may add value on *sycophancy* and *anchoring* which CoVe does not target, but we have no evidence for that claim.

### Family 2 — Sampling-based uncertainty estimation

| Method | Mechanism | Signal |
| --- | --- | --- |
| **SelfCheckGPT** (Manakul et al. 2023, arXiv 2303.08896) | Sample K completions → measure inter-sample consistency via NLI / n-gram / BERTScore | Sentence-level + passage-level factuality; higher AUC-PR than grey-box baselines on WikiBio |
| **Semantic Entropy** (Farquhar, Kossen, Kuhn, Gal, *Nature* 2024) | Sample K≈5–10 completions → cluster by bidirectional entailment → compute entropy over clusters | Detects *confabulations* (inconsistent wrong answers); beats naive entropy + P(True) across TriviaQA, SQuAD, BioASQ, NQ-Open, SVAMP, FactualBio |

**Why tvl-tech-bias-validator is categorically weaker here:** sampling methods extract signal from the model's own distribution — the same output appearing under different random seeds is evidence of knowledge; divergent outputs are evidence of confabulation. Bias-validator does not sample. It cannot access this signal. The gap is architectural, not fixable by better prompts.

**What SE explicitly does not detect** (Farquhar 2024 blog): "cases where the model has been trained into an incorrect style of reasoning or set of facts", domain transfer failures, and deliberate deception. So even SE has a ceiling — but it's a higher ceiling than ours.

### Family 3 — Hidden-state / logit probes

| Method | Mechanism |
| --- | --- |
| **Semantic Entropy Probes (SEPs)** (Kossen et al. 2024, arXiv 2406.15927) | Linear probe on hidden states approximates SE without sampling; near-zero test-time cost |
| **Semantic Energy** (Ma et al. 2025, arXiv 2508.14496) | Boltzmann-style energy on penultimate-layer logits; refines SE where clustering fails |
| **MiniCheck** (Tang et al., EMNLP 2024) | Small fact-check model; state-of-the-art for grounding LLM output in source documents |

**Why tvl-tech-bias-validator cannot approach this family:** we have no access to hidden states or token logits through the Claude Code tool surface. Period.

## What Sui & Duede (ACL 2024) actually say about narrativity

Since our skill cites this paper, we owe it an honest summary.

- **Operational definition:** narrativity = softmax probability from a fine-tuned ELECTRA-large classifier trained on Antoniak et al. 2023's Reddit narrative-detection corpus. Classifier AUC ≈ 0.83–0.85.
- **Quantitative gap** (mean narrativity, hallucinated vs veridical):
  - FaithDial: 0.620 vs 0.518 — Δ 0.102
  - BEGIN: 0.658 vs 0.561 — Δ 0.097
  - HaluEval: 0.655 vs 0.638 — **Δ 0.017**
- **Their logistic regression:** narrativity coefficient 0.631 (p<0.01) on N=43,842. Statistically significant, but pseudo R² on the coherence model is 0.004 — near zero explanatory power.
- **What they refuse to claim:** "we must refrain from asserting that narrativity drives coherence."

**Implication for our skill:** the "narrativity drift" check is citing a real-but-modest signal measured by a real-but-specific tool, and we replaced both with unstructured prose inspection. On HaluEval, the real effect is Δ=0.017 — a human reviewer eyeballing "does this sound too smooth" is going to miss that entirely and fabricate false positives on perfectly fine drafts. The honest fix is to cut the check or replace it with something we can actually measure.

## What is plausibly novel in tvl-tech-bias-validator

Being maximally generous:

1. **Breadth of classes.** CoVe targets factuality, SelfCheckGPT targets factuality, SE targets confabulation, Reflexion targets task success. Bias-validator covers sycophancy, anchoring, scope creep, and narrativity drift in addition to confabulation. That is a combination, not a new mechanism.
2. **Subagent isolation.** Delegating the audit to a fresh-context subagent is a concrete deployment choice, not a research contribution. Similar to CoVe stage 3 ("answers questions independently so the answers are not biased").
3. **Integration with a coding agent's tool surface.** The subagent can verify file paths and symbols with Read/Grep during the audit. This is operational, not scientific.

Nothing here justifies a "state of the art" claim. The correct framing is: a deployment-oriented prose rubric that combines ideas from Constitutional AI, CoVe, and ELEPHANT's sycophancy taxonomy, with empirical performance currently unmeasured.

## Actions this forces

1. Do not publish this skill publicly without measurements.
2. Drop or rewrite the "narrativity drift" check — it is cargo-cult as currently written.
3. Collapse checks that overlap (confabulation / automation / overconfidence fire on the same signal in all my test cases).
4. Benchmark against a vanilla-self-review baseline before claiming any check adds value.
