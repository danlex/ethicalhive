# Why another catalogue

Staged draft of the positioning section for the map-led resource paper. Slots in as
Section 2. Every citation here is backed by `references/catalogue-prior-art.md`; the two
load-bearing numbers (Malberg's 30, the MIT Repository's 1,725) were verified against the
primary abstracts. No em dashes, counts not decimals, overlap stated plainly.

---

There is no shortage of ways to enumerate what goes wrong with AI. The honest question a
new catalogue has to answer is not whether failures are worth naming, but why the
existing catalogues do not already name these ones. The prior work clusters at three
altitudes, and this catalogue sits at none of them.

The first is the **societal and governance layer**. The MIT AI Risk Repository
(Slattery et al., 2024) is the most comprehensive example: a meta-review of 74 frameworks
containing 1,725 distinct risks, organized by who causes a risk and in what domain. The
DeepMind risk taxonomy (Weidinger et al., 2021), the sociotechnical-harm taxonomy of
Shelby et al. (2023), the NIST AI Risk Management Framework (2023), and the AI Incident
Database all live here too. These are catalogues of harm outcomes, trustworthiness
properties, and real-world incidents. They treat the model's reasoning as a black box
that produces a harm, and they are right to, because their job is governance. They do not
decompose the reasoning step itself into named, mechanism-level ways a model arrives at a
confident wrong answer, and an auditor that has to check one specific obligation cannot
act on "causes societal harm."

The second is the **adversarial and security layer**. The OWASP Top 10 for LLM
Applications (2025), MITRE ATLAS, and the Microsoft failure-modes taxonomy (Siva Kumar
et al., 2019) catalogue what an attacker does to an AI system: prompt injection, data
poisoning, model extraction, excessive agency. This is largely orthogonal to the failures
a model commits with no adversary present. Where the two touch, the resolution is coarse
in exactly the place this catalogue is fine-grained: OWASP's single entry LLM09
Misinformation is one undifferentiated bucket over dozens of distinct epistemic
mechanisms that a reasoning-level catalogue separates.

The third is the **behavioral-measurement layer**, and this is where the overlap is real
and must be stated plainly. Benchmarks of cognitive bias in LLMs and surveys of
hallucination do decompose model reasoning into named mechanisms. The closest single
prior catalogue is Malberg et al. (2024), a large-scale evaluation of 30 cognitive biases
across 20 models. Our catalogue's classic-bias subset substantially overlaps those 30,
and we cite it as the nearest prior art. On the hallucination side, Ji et al. (2022),
HALoGEN (Ravichander et al., 2025), and HalluLens (Bang et al., 2025) give principled
taxonomies of that one family, and our hallucination and source-fabrication modes overlap
theirs. The difference is not that these are wrong. It is that each decomposes a single
family at a time. No one of them unifies cognitive bias, hallucination, source
fabrication, sycophancy, scope creep, reward hacking, and scheming into one structure.

The slice none of them occupies, taken together, is the integration. This catalogue
records 207 integrity failure modes, frames most of them as parallels to a specific named
human cognitive failure organized by ten cognitive systems, links them with an explicit
graph of which mode violates which obligation, causes which other mode, and relates to
which neighbor, adds a second tier of AI-native modes that have no human analogue
(reward hacking, prompt injection, scheming, and the like), and grounds every entry in a
primary paper that was read rather than keyword-matched. Against Malberg's 30 biases that
is roughly a sevenfold extension in count, and it extends along axes Malberg does not
cover (memory errors, reasoning errors, output-integrity failures, and the AI-native
tier) with a relation graph and a cognitive-science organizing principle that no prior
catalogue has.

The contribution is therefore not a new risk category. It is a unifying,
cognitively-grounded, relationally-structured map across failure families that are today
catalogued in separate, mechanism-specific efforts. We claim that, and no more. The two
findings that come out of building it, reported in Section 5, are about the reliability of
the grounding itself, and they are the reason a reader should trust the map rather than
take its coverage on faith.
