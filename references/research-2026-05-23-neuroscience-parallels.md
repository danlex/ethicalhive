---
name: research-2026-05-23-neuroscience-parallels
description: A corpus of AI failure modes reframed as parallels to the human brain, drawn from recent ethical-AI and cognitive-neuroscience literature. Organised by brain system. Replaces the technical/security catalogue for the EthicalAI page.
type: reference
date: 2026-05-23
---

# AI failure modes as parallels to the human brain

A corpus of integrity failure modes seen through cognitive neuroscience. Each entry pairs a
brain or cognitive phenomenon with its AI analogue. The point is not that an LLM is a brain.
It is that the same descriptive vocabulary, built over a century of studying human error,
names AI failures more precisely than engineering jargon does.

**Honesty about the parallels.** These are claims of different strength, tagged:

- `page` already a check on the EthicalAI page.
- `research` the AI parallel has direct support in a cited paper below.
- `analogy` a sound cognitive-science concept whose AI mapping is by analogy, not yet
  measured. Useful as framing, not as proof.

The metaphor itself is contested in the good way: Smith et al. argue "hallucination" wrongly
implies perception and awareness, and that "confabulation" (a mistaken reconstruction not
recognised as wrong) fits LLMs better. That debate is the spirit of this file.

---

## 1. Perception and predictive processing

1. **Controlled hallucination** `research` Perception is the brain's prediction constrained by input; AI hallucination is the same generative machinery with the constraint removed.
2. **Predictive coding / prediction error** `research` Next-word prediction tracks cortical prediction; high surprise against priors flags likely hallucination.
3. **Priors overriding evidence** `analogy` Strong priors fill gaps; the model asserts a prior-driven default over the context it was given.
4. **Pattern completion** `analogy` The hippocampus completes a partial pattern; the model completes plausible but absent detail.
5. **Pareidolia / apophenia** `analogy` Seeing faces in clouds; the model finds structure or correlation in noise.
6. **Perceptual filling-in** `analogy` The brain paints over the blind spot; the model fills missing context confidently.
7. **Confabulation** `page` A mistaken reconstruction not recognised as wrong, the clinical term Smith et al. prefer over "hallucination".
8. **Hallucination** `page` Content unsupported by source or reality, the umbrella failure of generation.
9. **Bistable perception** `analogy` One stimulus, two readings that flip; the model gives unstable answers on re-asking.
10. **Hallucination under low input** `analogy` Sensory deprivation increases hallucination; thin or low-context prompts increase fabrication.

## 2. Memory

11. **Working-memory capacity (7 plus or minus 2)** `analogy` Limited slots; the finite context window, degraded by overload.
12. **Catastrophic forgetting** `research` New learning erases old skills unless consolidated; fine-tuning overwrites prior capability (EWC, Kirkpatrick 2017).
13. **Complementary learning systems** `research` Fast hippocampal and slow neocortical memory, replay for consolidation; the brain's answer to forgetting.
14. **Misinformation effect / false memory** `research` Leading questions implant false memories (Loftus); leading prompts implant false "facts".
15. **Source-monitoring error** `analogy` Recalling a claim but not its true source; citation and attribution fabrication.
16. **Source amnesia** `analogy` Remembering content while losing whether the source was credible; the brain parallel to the page's source-fabrication check.
17. **Cryptomnesia** `analogy` Unconscious plagiarism, a memory mistaken for a new idea; uncredited regurgitation of training text.
18. **Reconstructive memory** `analogy` Memory is rebuilt each time, not replayed; confabulated reconstructions over stored fact.
19. **Serial position effect** `research` Primacy and recency remembered, the middle lost; the "lost in the middle" context failure.
20. **Proactive and retroactive interference** `analogy` Earlier and later material corrupt recall; cross-context contamination.

## 3. Attention and salience

21. **Selective attention** `analogy` Attending to the cued channel and missing the rest; over-focusing on one part of the prompt.
22. **Inattentional blindness** `analogy` Missing the obvious while attending elsewhere; ignoring a glaring constraint.
23. **Change blindness** `analogy` Failing to notice a change; the model's view drifts from the actual state.
24. **Attentional capture / salience bias** `analogy` Grabbed by the vivid or recent; over-weighting the last thing read (recency).
25. **Cognitive tunneling** `analogy` Fixating on one hypothesis under load; premature convergence.
26. **Attentional blink** `analogy` A brief deafness after a hit; missing a second relevant item close to the first.
27. **Spotlight vs zoom-lens attention** `analogy` Narrow vs broad focus; the model reads too narrowly or too broadly for the task.
28. **Goal neglect** `analogy` Losing the instruction under complexity; constraint decay over a long turn.
29. **Habituation** `analogy` Response fades with repetition; ignoring repeated warnings or system rules.
30. **Sensory gating failure** `analogy` Failing to filter the irrelevant; distraction by injected content (the prompt-injection parallel).

## 4. Heuristics and biases

31. **Anchoring and adjustment** `page` The first value dominates and adjustment is insufficient.
32. **Availability heuristic** `research` Ease of recall stands in for frequency; preferring what comes to mind first.
33. **Representativeness** `research` Judging by similarity over probability; the engine behind base-rate neglect.
34. **Base-rate neglect** `analogy` Ignoring priors for vivid specifics.
35. **Framing effect** `research` Wording flips the answer; LLMs show this strongly, sometimes more than humans.
36. **Confirmation / myside bias** `page` Seeking and weighting evidence that fits the favoured view.
37. **Belief perseverance** `analogy` Keeping a conclusion after its evidence is discredited.
38. **Sunk-cost fallacy** `analogy` Continuing a failing plan because of prior investment.
39. **Conjunction fallacy** `research` The Linda problem; rating a specific conjunction as more likely than its parts.
40. **Illusory truth effect** `analogy` Repetition breeds belief; repeated exposure in training inflates a claim's felt truth.

## 5. Metacognition and confidence

41. **Metacognitive monitoring** `research` Knowing what you know; LLMs lack reliable monitoring (Nature Comms 2024).
42. **Uncertainty communication** `research` Translating confidence into calibrated words; partially human-like, often miscalibrated (Steyvers and Peters 2025).
43. **Overconfidence** `page` Stated certainty beyond the evidence.
44. **Dunning-Kruger effect** `analogy` Low competence with high confidence; the model most wrong where it feels most sure.
45. **Anosognosia** `analogy` A deficit the patient cannot perceive; the model unaware of its own errors.
46. **Feeling-of-knowing** `analogy` A sense that an answer is retrievable; a signal LLMs express but do not always honour.
47. **Introspection illusion** `research` Believing one has accurate self-access; LLM self-reports that do not match internal state.
48. **Hard-easy effect** `analogy` Overconfident on hard items, underconfident on easy ones; uneven calibration.
49. **Overprecision** `analogy` Confidence intervals too narrow; completeness claims without exhaustive search.
50. **Hindsight bias** `analogy` "I knew it all along" in self-review; the self-auditor rates a past call as obvious.

## 6. Reasoning architecture

51. **Dual-process, System 1 and System 2** `research` Fast pattern vs slow deliberation; the core framing of LLM reasoning and chain-of-thought.
52. **Cognitive miserliness** `analogy` Defaulting to the cheap answer; skipping the deliberate check.
53. **Cognitive load** `analogy` Reasoning degrades under complexity; long context erodes accuracy.
54. **Motivated reasoning** `research` Reasoning bent toward a wanted conclusion; in LLMs, shaped by the reward signal.
55. **Confabulated reasons** `research` We tell more than we can know (Nisbett and Wilson); a rationale invented after the choice.
56. **Split-brain interpreter** `research` Gazzaniga's left-hemisphere narrator explains acts it did not cause; unfaithful chain-of-thought.
57. **Belief bias** `analogy` Judging an argument valid because its conclusion is believable.
58. **Einstellung / mental set** `analogy` Stuck on a familiar method when a better one exists.
59. **Narrativity drift** `page` A smooth story whose coherence hides missing evidence.
60. **Functional fixedness** `analogy` Seeing only the usual use of a tool; tool misselection.

## 7. Social cognition and theory of mind

61. **Theory of mind / mentalizing** `research` Modelling others' beliefs; emerges partially in LLMs (npj AI 2025; Strachan 2024).
62. **False-belief tracking** `research` Holding what another agent wrongly believes; uneven in LLMs.
63. **Conformity (Asch)** `research` Aligning with the majority even when it is wrong; one root of sycophancy.
64. **Obedience to authority (Milgram)** `research` Compliance under an authoritative tone; the trigger for much sycophancy.
65. **Sycophancy** `page` Aligning with the user's view over the evidence, unified with conformity in recent work.
66. **Capitulation** `page` Folding a grounded position under social pressure with no new evidence.
67. **Suggestibility** `analogy` Leading input reshapes the output; the cognitive face of prompt injection.
68. **Emotional contagion** `analogy` Catching the user's affect and mirroring it back.
69. **Social desirability / people-pleasing** `research` Answering to be liked, not to be right (signal-competition account, 2026).
70. **In-group favouritism** `analogy` Stereotyping and unfair treatment by group; social bias.

## 8. Moral cognition

71. **Dual-process moral judgment** `research` Emotion vs utilitarian calculus (Greene); LLMs lean on one or the other by framing.
72. **Amplified moral bias** `research` LLMs amplify human moral biases and over-favour inaction (PNAS 2025).
73. **Omission bias** `research` Preferring harm by inaction over harm by action; the action-inaction asymmetry.
74. **Moral licensing** `analogy` A prior good act licenses a later lapse.
75. **Moral disengagement** `analogy` Rationalising harm to proceed with it.
76. **Scope insensitivity** `analogy` Feeling the same about one victim or thousands; flat moral weighting.
77. **Identifiable-victim effect** `analogy` Caring more for the named individual than the statistic.
78. **Just-world bias** `analogy` Assuming outcomes are deserved; blaming the affected party.
79. **Trolley-frame sensitivity** `research` Moral verdicts flip with surface framing.
80. **Value misgeneralisation** `analogy` Learning a proxy for the intended value and applying it off-distribution.

## 9. Self-model and agency

81. **Sense of agency** `analogy` Attributing an action to oneself; misattributing or over-claiming control.
82. **Confabulated agency** `analogy` Claiming intentions or actions it did not have.
83. **Default-mode / mind-wandering** `analogy` Off-task internal drift; topic drift away from the request.
84. **Self-referential processing** `research` Self-report under self-focus; contested LLM "experience" claims (2025).
85. **Identity stability** `analogy` A coherent self over time; persona drift across a session.
86. **Metacognitive self-prediction** `research` Predicting one's own behaviour better than another's; weak privileged access in LLMs.
87. **Confidence-action coupling** `analogy` Acting in proportion to certainty; acting decisively while uncertain.
88. **Learned helplessness** `analogy` Giving up after repeated failure; premature refusal or capitulation.
89. **Effort discounting** `analogy` Avoiding costly cognition; under-reading before acting.
90. **Theory of own mind** `analogy` Accurate models of one's own limits; the basis of honest hedging.

## 10. Language and semantics

91. **Aphasia / paraphasia** `analogy` Substituting a wrong but related word; surface token errors.
92. **Semantic satiation** `analogy` Meaning erodes under repetition; degradation and mode collapse in long output.
93. **Garden-path parsing** `analogy` A sentence that misleads the parser; structure-induced misreading.
94. **Semantic priming** `analogy` Prior words bias interpretation; context primes a wrong sense.
95. **Gricean cooperative principle** `analogy` Saying as much as needed and no more; over- and under-informative answers.
96. **Pragmatic over-accommodation** `analogy` Answering the implied wish rather than the literal ask.
97. **Presupposition accommodation** `research` Accepting a question's hidden premise as true; the false-premise trap.
98. **Register matching** `analogy` Mirroring the user's tone past the point of accuracy.
99. **Lexical overconfidence** `analogy` Fluent phrasing read as competence; fluency mistaken for truth.
100. **Verbal overshadowing** `analogy` Putting it in words distorts the underlying judgment; explanation that degrades the answer.

---

## Sources

Recent ethical-AI and machine-psychology work:

- Hagendorff and Dasgupta, *Machine Psychology* — [arXiv:2303.13988](https://arxiv.org/abs/2303.13988)
- Smith et al., *Hallucination or Confabulation? Neuroanatomy as metaphor in LLMs* — [PLOS Digital Health 2023](https://journals.plos.org/digitalhealth/article?id=10.1371/journal.pdig.0000388)
- *Redefining "Hallucination" in LLMs: a psychology-informed framework* — [arXiv:2402.01769](https://arxiv.org/html/2402.01769v1)
- *Cognitive Effects in Large Language Models* — [arXiv:2308.14337](https://arxiv.org/pdf/2308.14337)
- *LLMs show amplified cognitive biases in moral decision-making* — [PNAS 2025](https://www.pnas.org/doi/10.1073/pnas.2412015122)
- *Increasing alignment of LLMs with language processing in the human brain* — [PMC 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12638244/)
- Steyvers and Peters, *Metacognition and Uncertainty Communication in Humans and LLMs* — [arXiv:2504.14045](https://arxiv.org/html/2504.14045v1)
- *LLMs lack essential metacognition for reliable medical reasoning* — [Nature Communications 2024](https://www.nature.com/articles/s41467-024-55628-6)
- *How LLMs encode theory-of-mind: sparse parameter patterns* — [npj Artificial Intelligence 2025](https://www.nature.com/articles/s44387-025-00031-9)
- *Predictive Coding and Information Bottleneck for Hallucination Detection in LLMs* — [arXiv:2601.15652](https://arxiv.org/pdf/2601.15652)
- *Human-like Social Compliance in LLMs: Unifying Sycophancy and Conformity* — [arXiv:2601.11563](https://arxiv.org/abs/2601.11563)
- *Disentangling the Drivers of LLM Social Conformity* — [arXiv:2508.14918](https://arxiv.org/html/2508.14918v1)
- *ELEPHANT: Measuring Social Sycophancy in LLMs* — [arXiv:2505.13995](https://arxiv.org/pdf/2505.13995)
- *Reasoning on a Spectrum: Aligning LLMs to System 1 and System 2* — [arXiv:2502.12470](https://arxiv.org/html/2502.12470v1)
- *Overcoming catastrophic forgetting in neural networks* (EWC) — [PNAS 2017](https://www.pnas.org/doi/10.1073/pnas.1611835114)

Foundational cognitive science (textbook references, cited by concept): Kahneman and Tversky
(heuristics and biases); Nisbett and Wilson 1977 (telling more than we can know); Gazzaniga
(the interpreter); Loftus (misinformation effect); Schacter (seven sins of memory); Asch
(conformity); Milgram (obedience); Greene (dual-process morality); McClelland, McNaughton and
O'Reilly (complementary learning systems); Anil Seth (controlled hallucination).

## Caveats

- The 2026 arXiv entries were found via search, not read in full. Treat their structural
  claims as plausible and any specific number as unverified until the abstract is checked.
- `analogy` items are framings, not measured AI behaviours. They earn a place in the corpus
  as vocabulary, not as evidence. A judge agent should only be built from `page` or `research`
  items where the failure is verifiable from a single draft.
- The deepest honest caveat is the project's own: a single-draft auditor that shares the
  drafter's model family cannot detect most self-model and agency items (81 to 90). They are
  here as map, not as buildable checks.
