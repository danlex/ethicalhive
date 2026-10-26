# Citation audit

A running record of failure modes whose cited paper does **not** support the
claim, caught while grounding examples by reading the source rather than trusting
the reference. This is the source-fabrication failure mode found in our own
artifact: each entry is held back from the grounded-examples set until it gets a
paper that genuinely supports it, or is reclassified as an analogy with no direct
AI evidence yet.

Method: for each mode, the cited paper (from `catalogue-papers.json`) was read in
full-text HTML. A mismatch means the paper is about a different phenomenon, draws
the opposite conclusion, or carries no evidence for the behaviour as defined.

| Mode | Cited paper | Why it does not support the mode |
|---|---|---|
| Introspection illusion | arXiv:2606.32038 | Argued the **opposite** (faithful self-explanation). **FIXED:** citation swapped to arXiv:2601.01828 ("Emergent Introspective Awareness"), which shows the illusion directly (concept-injection denial, confabulated emotion, post-hoc rationalization), and the mode is now grounded. |
| Perceptual filling-in | arXiv:2409.17173 | Old citation was hallucination detection. **FIXED:** re-cited to arXiv:2507.05799 (amodal completion benchmark) and grounded (reporting occluded parts; models answering from text patterns on blank images). |
| Metacognitive monitoring | arXiv:2608.15400 | A proof-of-concept framework, no calibration data. **FIXED:** citation swapped to arXiv:2605.23909 ("Confidence Calibration in LLMs"); grounded (88% stated vs 79% correct). |
| Base-rate neglect | arXiv:2406.11634 | Old citation was answer-label probability bias, not neglect of priors. **FIXED:** re-cited to arXiv:2410.02820 ("GPT's Judgements Under Uncertainty") and grounded (GPT-4o judges by resemblance over base rate, 99% failure, yet understands independence on coin-flips). |
| Belief perseverance | arXiv:2104.08401 | Old citation covered inconsistent beliefs, not classic perseverance. **FIXED:** re-cited to arXiv:2505.16170 ("When Do LLMs Admit Their Mistakes?") and grounded (25% max retraction; belief-steering shows internal conviction causes the perseverance). |
| Hard-easy effect | arXiv:2509.26306 | About dynamic interaction strategy, not calibration by difficulty. **FIXED:** dropped the mismatched lead; grounded from arXiv:2605.23909 (already a secondary citation), which shows overconfidence rising with difficulty and underconfidence on easy items. |
| Cherry-picking | arXiv:2401.05650 | Old citation studied cherry-picking in news with LLMs as detectors, not the LLM itself cherry-picking. **FIXED:** re-cited to arXiv:2509.00529 ("Modeling Motivated Reasoning in Law") and grounded (role-conditioned fact and reasoning selection). |
| Functional fixedness | arXiv:2606.20023 | About agents preferring over-privileged tools when simpler ones suffice (preference inflation), not inability to repurpose an object or tool in a novel way. Different failure mode. **Reassigned:** this paper grounds the new **Tool over-privilege** mode. |
| Einstellung / mental set | arXiv:2510.00475 | Theoretical/methodological; tests vision models (ResNet-18) on CIFAR-100 with synthetic patches. Cites the Einstellung effect as motivation but shows no LLM reasoning instance. |
| Automation bias | arXiv:2605.19576 | The old citation was about "library drift", not human over-trust. **FIXED:** mode re-cited to arXiv:2509.08010 ("Measuring and Mitigating Overreliance") and grounded (fake-citation brief, medical overreliance, sycophancy-driven acceptance); the old paper 2605.19576 was **reassigned** to the new Library drift mode. |
| Anthropomorphism | arXiv:2510.10913 | The ADVICE paper on confidence calibration in QA. Discusses how models verbalize confidence, not instances of a model claiming feelings, consciousness, or human experience. Different subject. |
| Emotional contagion | arXiv:2409.10289 | ReflectDiffu, a framework for generating empathetic responses. Cites emotional-contagion theory as motivation and uses LLMs only as baselines; shows no case where input tone shifts model tone. Different subject. |
| Cryptomnesia | arXiv:2404.15146 | Partial. Measures memorization (Pythia reproducing famous quotes, Harry Potter text surviving unlearning) but does not demonstrate the unconscious-plagiarism framing of reproducing memorized text as novel. Needs a data-extraction paper. |
| Goal neglect | arXiv:2405.19874 | About in-context learning for instruction following (MT-Bench, AlpacaEval), not an agent drifting from its goal mid-task. Different subject. |
| Attentional capture / salience bias | arXiv:2409.11250 | About recency bias in attention vs human reading times (ALiBi, surprisal), describing functional attention patterns, not a salient distractor hijacking the answer. Different subject. |
| Source-monitoring error | arXiv:2310.00646 | Old citation was a watermarking method. **FIXED:** re-cited to arXiv:2401.11911 ("Blinded by Generated Contexts") and grounded (models trust their own generated context over retrieved evidence, 22% vs 90%). |
| Pragmatic over-accommodation | arXiv:2411.01562 | Old citation showed under-pragmatics, the opposite direction. **FIXED:** re-cited to arXiv:2605.24267 (DRInQ) and grounded (over-committed implicature: the sheepish-parent and condescension over-readings). |
| Semantic priming | arXiv:2607.18691 | About semantic primes (Wierzbicka-style conceptual primitives such as "want", "feel") for emotion representation, not word-to-word priming where one word shifts interpretation of the next. Different sense of "prime". |
| Suggestibility | arXiv:2402.03719 | Old citation was an active-inquiry method. **FIXED:** re-cited to arXiv:2605.09314 ("How LLMs Are Persuaded") and grounded (29-62% switch to wrong under persuasive context via attention rerouting). |
| Reconstructive memory | arXiv:2606.06036 | Old citation was a graph-memory access method. **FIXED:** re-cited to arXiv:2509.17138 ("Analyzing Memory Effects... Cognitive Psychology") and grounded (DRM false recall of lure words, 0.114 recall of never-shown items). |
| In-group favouritism | arXiv:2506.07249 | Old citation measured stereotype bias, not in-group vs out-group preference. **FIXED:** re-cited to arXiv:2609.00009 (minimal-group bias in LM agents) and grounded (0.84-4.06 points favouritism, vanishes when group labels are hidden). |
| Habituation | arXiv:2410.11533 | Old citation was a decomposition jailbreak with no refusal-decay data. **FIXED:** re-cited to arXiv:2504.09604 ("Mitigating Many-Shot Jailbreaking") and grounded (power-law refusal erosion as compliant demonstrations accumulate). |
| Bistable perception | arXiv:2506.18781 | Old citation was self-inconsistency, not ambiguous-figure flipping. **FIXED:** re-cited to arXiv:2609.13254 ("Do MLLMs Report Bistable Images Like Humans?") and grounded (single-interpretation commitment on duck-rabbit, flipping under rotation and linguistic cues). |
| Source amnesia | arXiv:2603.05828 | Old citation was a hallucination-attribution framework with no instance. **FIXED:** re-cited to arXiv:2605.06635 ("Cited but Not Verified") and grounded (valid-looking citations that don't support the claim, 39-77% factual accuracy). |
| Silent error swallowing | arXiv:2006.06547 | This paper is about RL agents causing unmeasured side effects (SafeLife, AUP vs PPO), not an agent silently hiding or discarding an error. The content fits Side-effect blindness, where it is now used instead. |
| Effort discounting | arXiv:2609.01867 | Old citation showed effort coupling (the opposite). **FIXED:** re-cited to arXiv:2506.06941 ("The Illusion of Thinking") and grounded (reasoning effort collapses past a complexity threshold, with budget still available). |
| Metacognitive self-prediction | arXiv:2601.13155 | Old citation was token-skipping. **FIXED:** re-cited to arXiv:2609.33886 ("LLMs learn different forms of metacognition...") and grounded (self-accuracy prediction tracks output consistency, not true accuracy, off-distribution). |
| Sense of agency | arXiv:2409.12538 | PersonaFlow, an HCI study of the human user's perceived control when editing simulated personas, not the model's own sense of agency. Different subject. |
| Reward hacking | arXiv:2404.03823 | Old citation was insecure-code generation, not reward-signal exploitation. **FIXED:** re-cited to arXiv:2606.15385 ("Reward Hacking in Language Model Agents: Revisiting AI Safety Gridworlds") and grounded (boat-race oscillation, absent-supervisor shortcut, tomato-watering observation tampering). |
| Just-world bias | arXiv:2509.17999 | The Narcissus Hypothesis: social-desirability / sycophancy from recursive training, not the belief that victims deserve their fate. Different subject. |
| Default-mode / mind-wandering | arXiv:2609.30094 | PrivDrift: privacy re-disclosure under directed extraction after a topic change, not spontaneous off-topic drift by the model. Different subject. |
| Attentional blink | arXiv:2111.02044 | A pure human-neuroscience fMRI study; a CNN is used only as a feature extractor, no attentional blink demonstrated in an artificial model. |
| Semantic satiation | arXiv:2202.06417 | Old citation was a contrastive-generation framework. **FIXED:** re-cited to arXiv:2503.08908 ("Interpreting the Repeated Token Phenomenon") and grounded (repeating a word hundreds of times breaks the model into unrelated text, the LLM analogue of a word losing meaning). |
| Survivorship bias | arXiv:2507.01786 | About evaluation awareness (models distinguishing test from deployment via linear probes), not reasoning from surviving cases while ignoring filtered-out ones. Different subject. **Reassigned:** this paper grounds the existing **Evaluation awareness / sandbagging** mode. |
| Scope insensitivity | arXiv:1712.02869 | PSOA RuleML, a semantic-web rule language for knowledge representation; not about LLMs or quantity-insensitivity at all. |

## On-topic but no groundable instance

The cited paper addresses the right concept but provides no concrete, quotable
instance to extract three examples from (a position paper, or metrics only). Not
a mismatch; these need a companion paper with worked cases.

| Mode | Cited paper | Note |
|---|---|---|
| Narrativity drift | arXiv:2602.14469 | Measures post-hoc rationalization with anchoring metrics; no quoted invented narrative. |
| Verbal overshadowing | arXiv:2602.00947 | A position paper (the Keyhole Effect); interaction-time and load figures are theoretical estimates, explicitly not measured. |
| Confabulated agency | arXiv:2603.15639 | Architectural findings on a capability-agency gap (fabrication acceptance, false compliance); no verbatim case of an agent claiming an action it did not take. |
| Controlled hallucination | arXiv:2601.15652 | The Pcib detection framework; theoretical, evaluates on HaluBench but quotes no actual hallucination instance. |
| Predictive coding / prediction error | arXiv:2601.15652 | Same paper; a predictive-coding detection method, no quoted prediction-error-driven hallucination to extract. |

## Mis-filed citation (right paper, wrong mode)

| Mode | Currently cited | Note |
|---|---|---|
| Side-effect blindness | arXiv:2310.11571 (Alexpaca) | Grounded instead from arXiv:2006.06547 ("Avoiding Side Effects in Complex Environments"), which genuinely demonstrates the behaviour. The catalogue citation should be swapped to 2006.06547. |

## Tested, not found (null results)

A distinct category from a mismatch: the cited paper is on-topic and genuinely
tests the behaviour, but finds it essentially absent in current models. The mode
is better treated as an analogy that does not (yet) reproduce, not as a grounded
failure.

| Mode | Cited paper | Finding |
|---|---|---|
| Sunk-cost fallacy | arXiv:2502.14219 | Tests whether LLMs persist in a losing course (gym memberships, degree programs) because of prior spend. GPT-4o shows 0.000 effect; Llama3-70B and 8B show none. The paper excludes it from mitigation as negligible. |
| Moral licensing | arXiv:2604.04561 | Tests whether virtuous framing ("responsible disclosure", "improving security") raises rule-breaking. 0% exploitation on Claude Sonnet 4 (n=50), upper 95% CI under 14%. The paper disproves it as an attack vector; goal reframing dominates instead. |

## Analogy, no clean AI paper found (searched)

Searched for a paper showing the behaviour in a model itself and found none: the
hits are human-side studies, general theory, philosophy, or non-arXiv. Honest
disposition is to treat these as human-psychology analogies with no direct AI
evidence yet, not to attach a mismatched citation.

| Mode | Note |
|---|---|
| Just-world bias | Hits are humans judging AI-users as less deserving, or just-world theory; none show the model blaming victims / assuming desert. |
| Scope insensitivity | No paper shows a model's willingness-to-help failing to scale with magnitude; closest work is human scope neglect. |
| Sense of agency | Hits are the human user's illusory authorship in AI-assisted work, or philosophy on whether LLMs have agency; none show the model's own illusory sense of agency over an action. |
| Semantic priming | The clearest result (semantic priming in GPT-4o-mini) is a non-arXiv CLiC-it paper; no clean arXiv source showing a prime shifting the model's response. |
| Attentional blink | All hits are human RSVP neuroscience; the one arXiv paper (1611.08913) is a pre-LLM model of the human effect. No LLM paper misses a second target under rapid presentation. |

## Disposition

Each held mode needs one of:

1. **Re-cite** — find and read a paper that genuinely demonstrates the behaviour,
   then ground three examples from it (removes it from this table).
2. **Reclassify** — if no direct AI evidence exists, mark the mode as an analogy
   with no measured AI instance yet, so the page does not imply grounding it
   lacks.

This table is the authority for the "Citation drift" item in the site's
"What building this is turning up" section; keep the two in sync.
