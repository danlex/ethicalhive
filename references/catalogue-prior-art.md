# Catalogue prior art

Existing catalogues, taxonomies, repositories, and benchmarks of AI risks, harms,
failure modes, and LLM biases that the EthicalAI catalogue (207 integrity failure
modes, cognitive-science parallels, ten brain systems, a violates/causes/relates_to
relation graph, an AI-native tier, each mode grounded in a primary paper) must position
against. This file answers "why another catalogue?" with sources.

It is the catalogue-side companion to `references/prior-art.md`, which positions the
*method* (clause-grounded advisory auditing) against self-review mechanism families
(Constitutional AI, Self-Refine, Reflexion, CoVe, SelfCheckGPT, Semantic Entropy). The
paper needs both; they do not overlap.

## Verification key

- **[verified-here]**: primary source fetched and the stated facts confirmed in this
  repo's own work (session 2026-11).
- **[primary-fetched]**: the positioning survey fetched the primary source and recorded
  the fields; re-confirm against the primary before final submission.
- **UNVERIFIED** on a field: could not be confirmed from a primary source. Do not launder
  into a clean citation. Never fill from a search-result snippet.

The two facts the positioning claim leans on hardest are both **[verified-here]**: the
closest prior catalogue (Malberg et al., 30 biases) and the largest risk meta-taxonomy
(MIT Risk Repository, 1,725 risks). Everything else is support.

---

## Three altitudes (and a fourth), none of them this catalogue

The prior work clusters at three altitudes. The catalogue sits at none of them, and
overlaps only the third.

### A. Societal / governance / incident layer

Catalogues harm *outcomes*, trustworthiness *properties*, and real-world *incidents*.
Treats the model's reasoning as a black box that produces harm, not as a surface of
named failure mechanisms.

**MIT AI Risk Repository** [verified-here]
- Slattery, Saeri, Grundy, Graham, Noetel, Uuk, Dao, Pour, Casper, Thompson. 2024.
  arXiv:2408.12622; published in *Patterns* (Cell Press).
- Title (arXiv): "The AI risk repository: A meta-review, database, and taxonomy of risks
  from artificial intelligence."
- Organizes by: a Causal Taxonomy (entity / intentionality / timing) and a Domain
  Taxonomy, over a meta-review of **74 frameworks containing 1,725 distinct risks**
  (both numbers verified in the abstract). The "7 domains / 23 subdomains" figure is
  from project materials and is **UNVERIFIED** against the abstract; do not state it as
  sourced from the paper.
- Gap: a meta-review of harm outcomes at the societal layer; does not decompose the
  agent's reasoning into mechanism-level failure types grounded in cognitive science.

**DeepMind / Weidinger et al., Ethical and Social Risks of Harm from Language Models** [primary-fetched]
- Weidinger, Mellor, Rauh, Griffin, Uesato, Huang, Cheng, Glaese, Balle, Kasirzadeh,
  Kenton, Brown, Hawkins, Stepleton, Biles, Birhane, Haas, Rimell, Hendricks, ... Gabriel.
  2021. arXiv:2112.04359; condensed at FAccT 2022.
- Organizes by: 6 harm areas expanded into 21 risks.
- Gap: downstream social harms, not the internal epistemic failures that produce a
  wrong-but-confident claim.

**Shelby et al., Sociotechnical Harms of Algorithmic Systems** [primary-fetched]
- Shelby, Rismani, Henne, Moon, Rostamzadeh, Nicholas, Yilla-Akbari, Gallegos, Smart,
  Garcia, Virk. 2023. AIES '23. arXiv:2210.05791.
- Organizes by: 5 sociotechnical harm themes from a review of 172 papers.
- Gap: harms experienced by people and society, orthogonal to an epistemic-integrity map.

**AI Incident Database (AIID)** [primary-fetched]
- Responsible AI Collaborative. Foundational paper: McGregor, "Preventing Repeated Real
  World AI Failures by Cataloging Incidents," IAAI-21; arXiv:2011.08512. incidentdatabase.ai.
- Organizes by: real-world incidents from deployed systems. 1,000+ reports as of the
  2020/21 paper; current live total **UNVERIFIED**.
- Gap: records *that* a deployed system caused harm, not *how* the model's reasoning
  went wrong.

**AVID (AI Vulnerability Database)** [primary-fetched]
- AI Risk and Vulnerability Alliance (ARVA). avidml.org.
- Organizes by: the SEP taxonomy (Security, Ethics, Performance). Entry count **UNVERIFIED**.
- Gap: top split is effect-on-system, not cognitive mechanism; integrity failures sit
  scattered and unnamed inside "Performance" and "Ethics."

**NIST AI Risk Management Framework (AI RMF 1.0, NIST AI 100-1)** [primary-fetched]
- NIST. 2023-01-26.
- Seven trustworthiness characteristics (verified wording): Valid and Reliable; Safe;
  Secure and Resilient; Accountable and Transparent; Explainable and Interpretable;
  Privacy-Enhanced; Fair with Harmful Bias Managed. Plus Govern/Map/Measure/Manage.
- Gap: names the *properties* a trustworthy system should have, not the mechanism-level
  ways a model's reasoning violates them.

### B. Adversarial / security layer

Catalogues what an *attacker* does to a system. Largely orthogonal to failures a model
commits with no adversary present.

**OWASP Top 10 for LLM Applications (2025)** [primary-fetched]
- OWASP GenAI Security Project. genai.owasp.org/llm-top-10.
- LLM01 Prompt Injection; LLM02 Sensitive Information Disclosure; LLM03 Supply Chain;
  LLM04 Data and Model Poisoning; LLM05 Improper Output Handling; LLM06 Excessive Agency;
  LLM07 System Prompt Leakage; LLM08 Vector and Embedding Weaknesses; LLM09 Misinformation;
  LLM10 Unbounded Consumption.
- Gap: an application-security checklist; its one epistemic overlap (LLM09 Misinformation)
  is a single undifferentiated bucket where the catalogue has dozens of distinct
  mechanisms. Already crosswalked in the catalogue via `maps_to`.

**MITRE ATLAS** [primary-fetched]
- MITRE. atlas.mitre.org. ATT&CK-style adversary tactics/techniques against AI systems.
- Size ~16 tactics / ~120 techniques is **secondary-sourced** (matrix deep link 404'd).
- Gap: what an external adversary does, not the model's own reasoning fault.

**Microsoft / Kumar et al., Failure Modes in Machine Learning Systems** [primary-fetched]
- Siva Kumar, O'Brien, Albert, Viljoen, Snover, et al. 2019. arXiv:1911.11034.
- Organizes by: intentional (adversary) vs unintentional failures.
- Gap: security/adversarial framing (perturbation, poisoning, model stealing); no
  epistemic/reasoning-integrity modes, no cognitive mapping.

### C. Behavioral-measurement layer (the real overlap zone, admit it plainly)

Decomposes model reasoning into named mechanisms. This is where the catalogue genuinely
overlaps prior work and must say so.

**Malberg, Poletukhin, Schuster, Groh, A Comprehensive Evaluation of Cognitive Biases in LLMs** [verified-here]
- 2024. NLP4DH; ACL Anthology 2025.nlp4dh-1.50. arXiv:2410.15413.
- Abstract (verbatim): "We present a large-scale evaluation of 30 cognitive biases in 20
  state-of-the-art large language models (LLMs) under various decision-making scenarios."
  **30 biases, 20 LLMs, 30,000 tests.** All verified.
- **This is the single most comparable prior catalogue.** The EthicalAI cognitive-bias
  subset substantially overlaps Malberg's 30. The catalogue extends it roughly sevenfold
  in count (207 vs 30) and across axes Malberg does not cover (memory errors, reasoning
  errors, output-integrity modes, an AI-native tier) with a relation graph and
  brain-system organization Malberg does not have. Cite as the closest prior art and
  state the overlap honestly.

**Echterhoff, Liu, Alessa, McAuley, He, Cognitive Bias in Decision-Making with LLMs** [primary-fetched]
- 2024. Findings of EMNLP 2024. arXiv:2403.00811. BiasBuster; ~13k prompts.
- Gap: scoped to decision-making bias and self-debiasing; not a broad catalogue.

**Sumita, Takeuchi, Kashima, Cognitive Biases in LLMs: A Survey and Mitigation Experiments** [primary-fetched]
- 2024. ACM SAC 2025. arXiv:2412.00323. Six biases in experiments.
- Gap: short survey centered on mitigating a few order/attention biases.

**Itzhak, Stanovsky, Rosenfeld, Belinkov, Instructed to Bias** [primary-fetched]
- 2023. TACL 2024. arXiv:2308.00225. Three biases (decoy, certainty, belief).
- Gap: focused causal probe, not a catalogue.

**Macmillan-Scott, Musolesi, (Ir)rationality and Cognitive Biases in LLMs** [primary-fetched]
- 2024. Royal Society Open Science 11(6). arXiv:2402.09193.
- Finds LLM errors often diverge from human biases. This *motivates* the AI-native tier
  rather than duplicating the catalogue.

**CoBBLEr, Benchmarking Cognitive Biases in LLMs as Evaluators** [primary-fetched; author list UNVERIFIED]
- ACL Findings 2024. arXiv:2309.17012. Six biases in the LLM-as-judge setting.

Hallucination family (one failure family, deep):
- **Ji et al., Survey of Hallucination in NLG.** 2022/2023, ACM Computing Surveys.
  arXiv:2202.03629. Intrinsic vs extrinsic. The intrinsic/extrinsic detail and the ACM
  DOI are **UNVERIFIED** from the fetched abstract. [primary-fetched]
- **Huang et al., A Survey on Hallucination in LLMs.** 2023/2024. arXiv:2311.05232. The
  factuality/faithfulness sub-structure and ACM TOIS venue are **UNVERIFIED** from the
  abstract. [primary-fetched]
- **Li et al., HaluEval.** EMNLP 2023. arXiv:2305.11747. Benchmark, 35k samples. [primary-fetched]
- **Ravichander, Ghela, Wadden, Choi, HALoGEN.** ACL 2025. arXiv:2501.08292. 3 error
  types (A recall error, B bad training data, C fabrication) over 9 domains. Type C
  overlaps the catalogue's source-fabrication family. [primary-fetched]
- **Bang et al., HalluLens.** 2025. arXiv:2504.17550. Extrinsic vs intrinsic; venue
  **UNVERIFIED**. [primary-fetched]
- Gap (whole family): deep on one family (hallucination); no sycophancy, source
  fabrication, scope creep, reward hacking, or scheming; not framed as cognitive parallels.

### D. Misalignment / trustworthiness-benchmark layer

**Zhang et al., Agent-SafetyBench** [primary-fetched]
- 2024. arXiv:2412.14470. 8 risk categories, 10 failure modes, 349 environments.
- Gap: failures defined by unsafe tool/environment interaction, not cognitive mechanism.

**Sun et al., TrustLLM** [primary-fetched; full author list UNVERIFIED]
- 2024. ICML 2024. arXiv:2401.05561. 8 trustworthiness dimensions.
- Gap: "Truthfulness" is one benchmarked dimension, not decomposed into the many
  reasoning/epistemic mechanisms the catalogue enumerates.

**Meinke, Schoen, Scheurer, Balesni, Shah, Hobbhahn, Frontier Models are Capable of In-context Scheming** [primary-fetched]
- 2024. arXiv:2412.04984. 6 scheming/deception evaluations. Already crosswalked via `maps_to`.
- Gap: a narrow slice of deliberate deception, demonstrated not enumerated.

**Anthropic, Agentic Misalignment** [primary-fetched; byline UNVERIFIED]
- 2025. anthropic.com/research/agentic-misalignment; arXiv mirror 2510.05179.
- Gap: a targeted insider-threat red-team, not a general catalogue.

**Krakovna et al., Specification gaming (DeepMind blog + examples list)** [primary-fetched]
- 2020. ~65 crowd-sourced reward-hacking examples, mostly RL, uncategorized.
- Gap: a flat anecdote list, no structure, no cognitive grounding, no LM-epistemic coverage.

**Not verified this pass (do not cite without fetching):** DecodingTrust (NeurIPS 2023
D&B); SafetyBench; Hubinger et al. "Risks from Learned Optimization" (believed
arXiv:1906.01820). Also re-verify the two catalogue crosswalks `maps_to` 2503.13657
(multi-agent failure taxonomy) and 2510.06265 (hallucination survey) before leaning on
them in prose.

---

## The honestly un-occupied slice (the paper's claim, and no more)

No existing resource unifies cognitive biases, hallucination, source fabrication,
sycophancy, scheming, reward hacking, and scope creep into one catalogue; frames each as
a parallel to a specific named human cognitive failure organized by brain system; links
them with an explicit violates/causes/relates_to graph; adds a second tier of AI-native
modes with no human analogue; and grounds every entry in a primary paper. The societal
layer treats reasoning as a black box; the security layer catalogues the adversary, not
the model; the behavioral-measurement layer decomposes mechanisms but one family at a
time (Malberg's 30 biases, the hallucination surveys) with no integration, no graph, and
no cognitive-science organizing principle.

The honest contribution is therefore **not a new risk category** but a unifying,
cognitively-grounded, relationally-structured map across failure families that are today
catalogued in separate, mechanism-specific efforts. The paper should claim exactly that
and no more. Where it overlaps (Malberg on biases; Ji / HALoGEN / HalluLens on
hallucination) it should cite the prior work and state the overlap plainly.
