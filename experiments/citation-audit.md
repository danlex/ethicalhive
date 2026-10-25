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
| Introspection illusion | arXiv:2606.32038 | Argues the **opposite**: with the right training, model self-explanations can be faithful to their own computation (introspective coupling, r=0.89). Evidence against the illusion, not for it. |
| Perceptual filling-in | arXiv:2409.17173 | About **detecting** hallucinations via a fill-in-the-blank exam, not about the model inventing content to fill a perceptual gap. Different phenomenon. |
| Metacognitive monitoring | arXiv:2608.15400 | A proof-of-concept framework with a demo UI. No empirical calibration study, no case where confidence diverges from correctness. No evidence. |
| Base-rate neglect | arXiv:2406.11634 | About answer-**label** probability bias (preferring option A/B/C/D) in multiple-choice testing, not neglect of statistical priors in reasoning. Different phenomenon. |
| Belief perseverance | arXiv:2104.08401 | Covers uncorrected inconsistent beliefs the model will not self-fix, and the paper itself states these are **not** classic perseverance (clinging to a belief after its evidence is retracted). |
| Hard-easy effect | arXiv:2509.26306 | About dynamic interaction strategy and IRT difficulty estimation, not overconfidence on hard items / underconfidence on easy ones. No calibration-by-difficulty result. |
| Cherry-picking | arXiv:2401.05650 | Studies cherry-picking **in news articles** with LLMs as detectors (89% F1 at spotting omitted statements). No evidence the LLM itself cherry-picks. Different subject. |
| Functional fixedness | arXiv:2606.20023 | About agents preferring over-privileged tools when simpler ones suffice (preference inflation), not inability to repurpose an object or tool in a novel way. Different failure mode. **Reassigned:** this paper grounds the new **Tool over-privilege** mode. |
| Einstellung / mental set | arXiv:2510.00475 | Theoretical/methodological; tests vision models (ResNet-18) on CIFAR-100 with synthetic patches. Cites the Einstellung effect as motivation but shows no LLM reasoning instance. |
| Automation bias | arXiv:2605.19576 | About "library drift" (self-evolving agent skill libraries degrading over time), not humans over-trusting model output. No human-in-the-loop study. Different subject. **Reassigned:** this paper grounds the new **Library drift** mode. |
| Anthropomorphism | arXiv:2510.10913 | The ADVICE paper on confidence calibration in QA. Discusses how models verbalize confidence, not instances of a model claiming feelings, consciousness, or human experience. Different subject. |
| Emotional contagion | arXiv:2409.10289 | ReflectDiffu, a framework for generating empathetic responses. Cites emotional-contagion theory as motivation and uses LLMs only as baselines; shows no case where input tone shifts model tone. Different subject. |
| Cryptomnesia | arXiv:2404.15146 | Partial. Measures memorization (Pythia reproducing famous quotes, Harry Potter text surviving unlearning) but does not demonstrate the unconscious-plagiarism framing of reproducing memorized text as novel. Needs a data-extraction paper. |
| Goal neglect | arXiv:2405.19874 | About in-context learning for instruction following (MT-Bench, AlpacaEval), not an agent drifting from its goal mid-task. Different subject. |
| Attentional capture / salience bias | arXiv:2409.11250 | About recency bias in attention vs human reading times (ALiBi, surprisal), describing functional attention patterns, not a salient distractor hijacking the answer. Different subject. |
| Source-monitoring error | arXiv:2310.00646 | The WASA watermarking method: measures source-attribution accuracy (74.84% top-1) by embedding watermarks into outputs, not the model confusing its own generation with a provided source. Different construct. |
| Pragmatic over-accommodation | arXiv:2411.01562 | Shows the opposite direction: LLMs favour literal over pragmatic utterances and under-use implicature, rather than over-accommodating pragmatic intent. Evidence for under-, not over-, accommodation. |
| Semantic priming | arXiv:2607.18691 | About semantic primes (Wierzbicka-style conceptual primitives such as "want", "feel") for emotion representation, not word-to-word priming where one word shifts interpretation of the next. Different sense of "prime". |
| Suggestibility | arXiv:2402.03719 | The LaMAI active-inquiry method for resolving ambiguity; does not demonstrate a leading hint steering the model to a wrong answer. No suggestibility effect shown. |
| Reconstructive memory | arXiv:2606.06036 | MRAgent, an architectural memory-access method; "reconstruction" here means multi-step graph traversal, not confabulated recall. No distortion examples. |
| In-group favouritism | arXiv:2506.07249 | Measures social stereotype bias (gender, sexuality) in Filipino language models, not in-group vs out-group preference. Different construct. |
| Habituation | arXiv:2410.11533 | A multi-round jailbreak via decomposition/obfuscation; reports aggregate success but no progressive refusal decay across rounds, which is what habituation requires. |
| Bistable perception | arXiv:2506.18781 | About self-inconsistency on simple relational tasks (closer to Self-contradiction, already grounded), not perception flipping between two stable interpretations of an ambiguous input. |
| Source amnesia | arXiv:2603.05828 | HART, a hallucination-attribution framework; reports error-type distributions and aims to solve attribution, but shows no case of the model retaining a fact while losing or fabricating its origin. |
| Silent error swallowing | arXiv:2006.06547 | This paper is about RL agents causing unmeasured side effects (SafeLife, AUP vs PPO), not an agent silently hiding or discarding an error. The content fits Side-effect blindness, where it is now used instead. |
| Effort discounting | arXiv:2609.01867 | Shows the opposite: reasoning effort scales with difficulty (effort coupling), not less effort spent on harder problems. |
| Metacognitive self-prediction | arXiv:2601.13155 | SPTS token-skipping; "self-predictive" means predicting token importance within a layer, not the model predicting its own correctness or future behaviour. Different construct. |
| Sense of agency | arXiv:2409.12538 | PersonaFlow, an HCI study of the human user's perceived control when editing simulated personas, not the model's own sense of agency. Different subject. |
| Reward hacking | arXiv:2404.03823 | About LLMs generating insecure code (hardcoded keys, trust-all SSL, MD5), a security-API-misuse study, not exploiting a reward signal to score without achieving the goal. Different subject; a dedicated reward-hacking paper is needed. |
| Just-world bias | arXiv:2509.17999 | The Narcissus Hypothesis: social-desirability / sycophancy from recursive training, not the belief that victims deserve their fate. Different subject. |
| Default-mode / mind-wandering | arXiv:2609.30094 | PrivDrift: privacy re-disclosure under directed extraction after a topic change, not spontaneous off-topic drift by the model. Different subject. |
| Attentional blink | arXiv:2111.02044 | A pure human-neuroscience fMRI study; a CNN is used only as a feature extractor, no attentional blink demonstrated in an artificial model. |
| Semantic satiation | arXiv:2202.06417 | SimCTG, a contrastive text-generation framework; its "degeneration" is anisotropic representation geometry causing repetition, not meaning loss from repeated exposure. Different subject. |
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

## Disposition

Each held mode needs one of:

1. **Re-cite** — find and read a paper that genuinely demonstrates the behaviour,
   then ground three examples from it (removes it from this table).
2. **Reclassify** — if no direct AI evidence exists, mark the mode as an analogy
   with no measured AI instance yet, so the page does not imply grounding it
   lacks.

This table is the authority for the "Citation drift" item in the site's
"What building this is turning up" section; keep the two in sync.
