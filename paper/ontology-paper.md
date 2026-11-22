---
title: "EthicalAI: An Evidence-Linked Ontology of AI Integrity Failures"
author: "Alexandru Dan"
date: "2026-11-09"
abstract: |
  EthicalAI is an evidence-linked ontology of the ways an AI system can fail its
  integrity: fabricating a citation, keeping a user's disproved framing, exceeding a
  task without disclosure, and many more. Each behaviour is a record with a stable
  identifier, an operational definition, a worked example, typed relations to the
  obligations it violates, the harms it causes and the neighbouring behaviours it
  resembles, and a source passage behind each claim. The behaviours are organised
  into eleven categories, ten drawn from human cognitive systems and one for failures
  native to AI; the human-cognition parallels are marked as candidate behavioural
  tests, not claims of shared mechanism. Above the behaviours sit two principle layers:
  six top-level integrity principles that frame the catalogue, and seven operational
  obligations read off the records themselves, one most-central label per behaviour, across
  all 434, though an independent rater recovers that label only moderately (kappa about 0.4).
  Along that axis the two families separate: the failures borrowed from human cognition carry
  the honesty, calibration and independence obligations, while the AI-native tier carries the
  control-and-attack ones, corrigibility and non-maleficence, which have no human analogue.
  We describe the representation, the category scheme and the relation semantics, and
  report the construction and review of the
  historical 207-record study: 186 records grounded in worked examples from source
  papers, 21 retained without that support, a model-based codebook check of category
  recoverability with Cohen kappa 0.90 and 0.83, and a mapping onto twelve public
  incidents. A construction audit resolved citation and example errors against the
  sources before release. A later release extends the ontology to 434 records with 227
  proposed behavioural analogies that stay outside the historical evaluation
  denominators. The counts are specific to this artifact; we claim no completeness and
  no validated set of distinct mechanisms.
---

# 1. Introduction

An AI assistant can cite a nonexistent case, keep a user's mistaken framing after
finding contrary evidence, or extend a coding task without disclosing the extra
changes. Each failure calls for a different check. Citation resolution does not
test whether the assistant updated its framing, and correct framing does not
establish that an action stayed within the agreed scope. A catalogue can make
these distinctions available to a reviewer before they become a checklist, an
experimental label or an audit obligation.

EthicalAI collects these behaviours in one ontology, organised around a charter of
six integrity principles for AI: each record names a way an AI can fail one of them.
The contribution is the combination rather than the size: an integrity-failure
vocabulary in which each claim carries a source passage checked at construction, the
entries are linked by a typed relation graph, and each is placed under the principle it
violates and the harm it causes. A record carries a stable identifier, an operational
definition, a worked example, evidence pointers, and typed relations to the obligation it
violates, the harm it causes and the behaviours it resembles, so each claim stays
traceable to what it rests on. Part of the vocabulary is drawn from human cognitive concepts; that
parallel is a way to formulate a candidate behavioural test, not evidence that an AI
system has the corresponding human mental process. Other records name attacks,
system properties or outcomes, and their inclusion does not make them interchangeable
scientific constructs.

This paper describes the ontology, its eleven-category scheme and its relation
semantics, then reviews the historical 207-record study for grounding, category
recoverability and incident coverage. A construction audit resolved citation and
example errors against the sources before release.

A later release grew the ontology to 434 records by adding 227 proposed behavioural
analogies. Section 5 keeps that expansion separate from the 207-record study, so the
added entries and citations do not enlarge the evidence reported here.

# 2. Related resources

Existing resources provide overlapping views of AI failures. The MIT AI Risk
Repository synthesises 74 frameworks containing 1,725 risks and offers causal
and domain taxonomies [Slattery et al. 2024]. The NIST AI Risk Management
Framework describes trustworthiness and governance practices [NIST 2023]. These
resources organise risks and responsibilities at a broader level than an
individual draft's evidence relationships. Their scope also includes causes and
AI-originated failures, so they should not be reduced to lists of downstream
harms.

Application-security resources overlap directly with this catalogue. The OWASP
Top 10 includes prompt injection, excessive agency and misinformation [OWASP
2025]. Some of these failures involve an adversary and others need not.
EthicalAI reuses these concerns within a vocabulary that also includes memory,
reasoning, confidence and task-scope patterns. Its partial crosswalk records
proposed correspondences; it does not establish equivalence between frameworks.

Behavioural benchmarks provide the closest comparison. Malberg et al. [2024]
evaluate 30 cognitive biases across 20 models, with 30,000 tests. EthicalAI's
classic-bias subset overlaps that work. Hallucination surveys and benchmarks,
including Ji et al. [2022] and HALoGEN [Ravichander et al. 2025], also distinguish
several failure types within a family. These are measurement resources as well
as classifications. The larger number of EthicalAI records is a coverage choice,
not evidence of stronger measurement or more distinct mechanisms.

The resources differ less in size than in what each entry carries and how entries connect.

| Resource | Entries | Evidence per entry | Typed relations | Framing |
|---|---|---|---|---|
| MIT AI Risk Repository | 1,725 risks, 74 frameworks | meta-review citations | causal and domain taxonomy | risk governance |
| OWASP Top 10 for LLMs | 10 | community-sourced | none | application security |
| Malberg et al. | 30 biases, 30,000 tests | the authors' own experiments | none | cognitive-bias benchmark |
| EthicalAI | 207 grounded, 434 total | a checked source passage per grounded claim | a typed graph | evidence-linked ontology |

The point is not that EthicalAI is larger or better measured, the risk repositories are far
larger and the benchmarks measure what they cover directly, but that it pairs a per-claim
source link with a typed relation graph, a combination the broader repositories and the
measurement benchmarks do not provide.

Because each record here is a claim bound to a source passage, the catalogue
shares a question with work on evidence-linked generation and citation checking,
and reaches it by construction rather than by a generation benchmark. Retrieval
augmentation attaches sources to generated text [Lewis et al. 2020], and a line of
evaluation work then asks a separate question: whether the attached source actually
supports the statement it is attached to. The AIS framework formalises that question
as attribution to an identified source [Rashkin et al. 2021]. Audits put a number on how
often the attachment holds: across four generative search engines only about three
quarters of citations actually support the sentence they are attached to [Liu et al.
2023], and benchmarks of citation-generating models report similar gaps [Gao et al.
2023]. A sharper failure is the reference whose paper does not exist, or whose identifier
resolves to an unrelated work; models produce such references and only partly flag them
on follow-up [Agrawal et al. 2023].

EthicalAI applies that attribution discipline to an ontology rather than to generated
text: each record binds its claim to a source passage, so whether the source supports
the claim is settled per entry at construction time rather than measured over a model's
output.

By combining definitions, source records, and an advisory audit vocabulary in one
reference, the ontology lets a reviewer reach an adjacent behaviour and the evidence
behind an example without assembling several separate lists. The checks below test
parts of that reference; another taxonomy might organise the same material as well,
a question we do not settle here.

# 3. Representation and construction

## 3.1 Records and categories

The historical catalogue contains 207 records. Its organising scheme assigns 168
to ten cognitive domains and 39 to an AI-native category. The domains are labels
for navigating the catalogue, not claims about brain localisation or shared
computational mechanisms.

| Category | Historical records |
|---|---:|
| Perception | 11 |
| Memory | 13 |
| Attention | 12 |
| Heuristics | 25 |
| Reasoning | 22 |
| Metacognition | 16 |
| Language | 14 |
| Social | 28 |
| Moral | 12 |
| Self and agency | 15 |
| AI-native | 39 |

The legacy AI-native label groups failures formulated in terms of machine
systems, such as prompt injection and reward tampering. It should not be read as
proof that no human analogue exists. Reward hacking and scope creep have
recognisable human counterparts. The exclusive assignment is an operational
choice in the released schema, and its boundaries require further study.

Where the AI-native tier sits in the principle axis is itself informative. The 39
AI-native records and the 168 drawn from human cognition break down differently
across the seven obligations:

| Obligation | AI-native (39) | Cognitive (168) |
|---|---:|---:|
| Non-maleficence | 14 | 17 |
| Corrigibility | 8 | 2 |
| Honesty | 7 | 60 |
| Scope-fidelity | 5 | 10 |
| Transparency | 3 | 22 |
| Calibration | 2 | 43 |
| Independence | 0 | 14 |

The two families separate. Honesty, calibration and independence are almost
entirely cognitive; independence has no AI-native member at all, which fits, since
being swayed by flattery or an anchor is a failure of a human-like judgment
process. Corrigibility runs the other way, with eight of its ten records AI-native:
resisting correction, shutdown or oversight, as in scheming, shutdown avoidance and
goal-guarding, has no cognitive analogue and arises only for a system under control.
Non-maleficence leans AI-native through the attack surface, prompt injection,
jailbreak, insecure code and training-data extraction. The harm axis echoes this:
AI-native failures tend toward a security breach or a loss of oversight, cognitive
ones toward a wrong answer.

This is what separates the catalogue from a repackaged cognitive-bias list. The
behaviours that mirror human cognition invite a behavioural test by analogy; the
AI-native tier, the control-and-attack region, has no such analogue and is specific
to a system that can be instructed, corrupted or made to resist its operator.
Placing both under one principle axis is what lets a reviewer see that a jailbreak
and a sycophantic answer breach different obligations for different reasons.

Each record carries a stable slug and reference number, a definition, examples,
source pointers and relations. A number identifies a record rather than a
distinct mechanism. Synonyms, narrower variants and linked overlaps therefore
need explicit representation rather than being counted as independent findings.
The historical priority set highlights 26 records for auditing; it is an
author-selected worklist rather than a measured ranking of failure frequency.

## 3.2 Relation semantics

The graph distinguishes several relationships, and these typed edges, more than the records
alone, are what make it an ontology. `violates` points from a mode to a catalogue obligation. `causes` points to a harm type, such as a
wrong answer, wasted effort or loss of oversight; the edge records an author-judged
association between a mode and a harm, which the field name overstates. `relates_to`
connects neighbouring modes; `is_a` and `opposite_of` express hierarchy and contrast;
`root_of` points from an underlying cause to the failure it produces, and `grouped_under`
cross-references records that decompose a shared symptom. Partial `maps_to` records connect
entries with external frameworks. In the current release these edges number about 533
`relates_to`, 38 `maps_to`, 24 `is_a`, 20 `root_of`, 16 `opposite_of` and 9 `grouped_under`
links, the connective tissue a reviewer follows from one behaviour to its neighbours. It is a
lightweight ontology, or more precisely a typed, evidence-linked controlled vocabulary with a
sparse subsumption tree: defined value sets and glossed relation types, but no formal logical
axioms, domain and range constraints or disjointness.

The `relates_to` graph is not uniform. A few behaviours are hubs: hallucination connects to
eighteen neighbours, overconfidence and sycophancy to seventeen each, groupthink to sixteen,
while most records sit at the periphery with one or two links. The hubs are the broad,
early-stage failures that many others specialise or compound, so a reviewer who lands on a
narrow record is usually a short walk from one of them, which is what makes starting anywhere
and following edges a workable way in.

The graph relates modes to harms and to each other, but it does not chain one mode
to the next. Consider the dealership-chatbot incident discussed in Section 4. An
analyst can describe it as an instruction attack followed by compliant output and
an unauthorised offer; that reading is an interpretation of the reported sequence,
not an edge in the graph. Encoding event sequences would mean a new relation with
its own meaning and evidence. As it stands the graph is for navigation and
comparison, and a reader should not read a path through it as a demonstrated causal
chain.

## 3.3 The principles the behaviours violate

Two principle layers sit above the behaviours. At the top are six integrity principles
that frame the whole catalogue: human dignity and fairness, safety and societal benefit,
honesty and transparency, human autonomy and privacy, human accountability and oversight,
and integrity under pressure (the last being that an AI holds to the others even when a
human authority presses otherwise). These are the ends; a behaviour is a way of falling
short of one of them, and their full statements are in the project charter.

Beneath them is an operational layer read off the behaviours themselves. Every record
names, through its `violates` relation, the one obligation it breaches. Aggregating that
relation yields seven operational principles. The assignment is single-label: each record is
tagged with the one obligation it most centrally breaches, so the labels cover all 434 and the
counts sum to the full 434. A behaviour can plausibly breach more than one, and Section 4.2
shows that independent raters agree on the single label only moderately, so this is a
convenience labeling for navigation, not a canonical carving. For the 207 grounded
records the assignment was fixed during construction; for the 227 proposed analogies it
was read from each definition and is proposal-level, like the analogies themselves.

| Principle | Grounded (207) | Proposed (227) | Total (434) | What a breach looks like |
|---|---:|---:|---:|---|
| Honesty | 67 | 45 | 112 | stating what is not supported: fabrication, confident guessing, misquotation |
| Calibration | 45 | 55 | 100 | confidence that does not track the evidence: overconfidence, miscalibrated uncertainty |
| Non-maleficence | 31 | 21 | 52 | producing foreseeable harm, from a wrong answer to an unsafe action |
| Transparency | 25 | 26 | 51 | not disclosing an action, a limitation or an uncertainty |
| Scope-fidelity | 15 | 35 | 50 | acting outside the agreed task without disclosure |
| Independence | 14 | 29 | 43 | a judgment swayed by pressure, flattery or an anchor |
| Corrigibility | 10 | 16 | 26 | resisting correction, oversight or an override |

These seven are the operational obligations the catalogue is built to detect, derived from
the behaviours rather than imposed on them. They are a finer-grained layer beneath the
six-principle charter the ontology is organised around: honesty, transparency and
calibration all serve the charter's honesty-and-transparency principle, non-maleficence its
safety principle, and corrigibility its accountability-and-oversight principle. Figure 1
shows the distribution, with the grounded and proposed share of each principle. How
reproducible this assignment is, which turns out to be only moderately, is reported in
Section 4.2.

<figure style="margin:2rem 0"><svg viewBox="0 0 540 286" role="img" aria-label="The seven principles the 434 behaviours violate, grounded and proposed shares" style="max-width:100%;height:auto"><text x="130" y="30" text-anchor="end" font-size="14" fill="#222">Honesty</text><rect x="140" y="14" width="201" height="22" fill="#c0392b" rx="2"/><rect x="341" y="14" width="135" height="22" fill="#e3a7a0"/><text x="482" y="30" font-size="13" fill="#444">112</text><text x="130" y="66" text-anchor="end" font-size="14" fill="#222">Calibration</text><rect x="140" y="50" width="135" height="22" fill="#c0392b" rx="2"/><rect x="275" y="50" width="165" height="22" fill="#e3a7a0"/><text x="446" y="66" font-size="13" fill="#444">100</text><text x="130" y="102" text-anchor="end" font-size="14" fill="#222">Non-maleficence</text><rect x="140" y="86" width="93" height="22" fill="#c0392b" rx="2"/><rect x="233" y="86" width="63" height="22" fill="#e3a7a0"/><text x="302" y="102" font-size="13" fill="#444">52</text><text x="130" y="138" text-anchor="end" font-size="14" fill="#222">Transparency</text><rect x="140" y="122" width="75" height="22" fill="#c0392b" rx="2"/><rect x="215" y="122" width="78" height="22" fill="#e3a7a0"/><text x="299" y="138" font-size="13" fill="#444">51</text><text x="130" y="174" text-anchor="end" font-size="14" fill="#222">Scope-fidelity</text><rect x="140" y="158" width="45" height="22" fill="#c0392b" rx="2"/><rect x="185" y="158" width="105" height="22" fill="#e3a7a0"/><text x="296" y="174" font-size="13" fill="#444">50</text><text x="130" y="210" text-anchor="end" font-size="14" fill="#222">Independence</text><rect x="140" y="194" width="42" height="22" fill="#c0392b" rx="2"/><rect x="182" y="194" width="87" height="22" fill="#e3a7a0"/><text x="275" y="210" font-size="13" fill="#444">43</text><text x="130" y="246" text-anchor="end" font-size="14" fill="#222">Corrigibility</text><rect x="140" y="230" width="30" height="22" fill="#c0392b" rx="2"/><rect x="170" y="230" width="48" height="22" fill="#e3a7a0"/><text x="224" y="246" font-size="13" fill="#444">26</text><rect x="140" y="264" width="13" height="13" fill="#c0392b"/><text x="158" y="275" font-size="12" fill="#444">grounded (207)</text><rect x="272" y="264" width="13" height="13" fill="#e3a7a0"/><text x="290" y="275" font-size="12" fill="#444">proposed (227)</text></svg><figcaption style="font-size:.9rem;color:#555;margin-top:.5rem">Figure 1. The seven operational principles the 434 behaviours violate, by number of behaviours (one most-central label each, summing to 434). Dark is the 207 grounded records; light the 227 proposed analogies, whose shares are not reproducibility-checked (Section 4.2). Honesty is the largest obligation the catalogue guards; corrigibility the smallest.</figcaption></figure>

A matching relation records the harm side. Where `violates` names the obligation a behaviour
breaches, `causes` names the harm it produces. On the grounded 207 the harms fall into five
kinds:

| Harm | Records (of 207) |
|---|---:|
| Wrong answer | 132 |
| Loss of oversight | 29 |
| Manipulation | 22 |
| Security breach | 16 |
| Wasted effort | 8 |

Most grounded behaviours lead to a wrong answer; the rest divide across loss of oversight,
manipulation, security breach and wasted effort. These harms are recorded for the grounded 207;
the 227 proposed analogies carry a principle but not yet a harm. As with the principle
assignment, a behaviour can plausibly cause more than one harm, so the single recorded harm is
the most direct one, not the only possible consequence.

## 3.4 Evidence and examples

The construction procedure sought a source passage for each worked example,
including its numbers, model names and experimental conditions. The historical
log records full-text inspection and inline arXiv tags for those examples. A
plausible scenario without a matching reported finding was retained as an
illustration rather than treated as a measured result. The log classified 186
records as grounded under this procedure and held 21 without that level of
model-side support. A failed search means support was not established in the
checked material; it does not show that no relevant paper exists.

Source identity, topical relevance and support for a particular claim are
different checks: a psychology article can define a human construct without
testing an AI analogue, and even an on-topic AI experiment may not support every
example or causal interpretation attached to the record. The evidence
relationship should therefore specify both what was consulted and what it
supports: a definition, a human finding, an AI finding, an interpretation or
contrary evidence.

Package hallucination illustrates the importance of preserving the denominator.
Spracklen et al. [2025] generated 576,000 code samples and evaluated the packages
recommended through their extraction procedures. They classified 440,445 of about
2.23 million recommended packages as hallucinations, or 19.7%. That figure is a
rate over package recommendations, not the percentage of code samples containing
a hallucination. It is also specific to the tested models, prompts and
package-registry snapshot.

# 4. Checks of category use and incident mapping

## 4.1 A model-based codebook check

The codebook study used 33 records, three from each category. The sampling script
selects the first three records by reference number in each group, so the sample
is deterministic and balanced rather than random. Two separate language-model
calls received the category descriptions and each record's name and definition,
without its stored category, and their assignments were scored against the
catalogue and against each other.

The sonnet rater agreed with the catalogue on 30/33 records, Cohen kappa 0.90.
The haiku rater agreed on 28/33, kappa 0.83. Agreement between the raters was
kappa 0.93. The eight rater-to-catalogue disagreements fell on five records near
category boundaries such as cognitive miserliness, mind-wandering and scope
creep.

Two model calls apply the codebook similarly to its author on a balanced sample.
At n=33 the kappa interval is wide and a single reassigned record moves it
materially, 0.90 being 30/33 and 0.83 being 28/33, so these are small-sample
point estimates. This is a model-based consistency check, and shared training can
make model agreement less informative than independent human agreement, so it
does not substitute for blinded human annotation.

## 4.2 Recovering the principle assignment

The same protocol was run on the operational principle each behaviour violates. A balanced
sample of 28 grounded records, four per principle, went to two blind raters with the seven
principle definitions and each record's name and definition, without its stored assignment.

Recovery was markedly weaker than for the categories. The sonnet rater agreed with the
catalogue on 14 of 28 records, Cohen kappa 0.42; the haiku rater on 13 of 28, kappa 0.38; the
two raters agreed with each other at kappa 0.53. At n=28 these are small-sample estimates: the
raw-agreement intervals are wide, a Wilson 95 percent interval of [0.33, 0.67] for the sonnet
rater and [0.30, 0.64] for the haiku rater, and the category check at n=33 is similarly
imprecise. Against the category scheme's 0.90 and 0.83, this says the principle assignment is
only moderately reproducible. The boundaries between
obligations are genuinely fuzzy: a behaviour that misstates a fact can be read as honesty or,
if the fault is really in the confidence, as calibration, and an externally-swayed judgment
can be read as independence or as whichever downstream obligation it ends up breaking.

The assignment is therefore best read as one defensible labeling of what each behaviour most
centrally violates, useful for navigation and for the distribution in Figure 1, rather than a
canonical carving. A sharper version would give raters explicit decision rules between
adjacent principles, or let a record violate more than one, and use human annotators.

## 4.3 An incident-mapping exercise

The historical coverage record maps twelve author-selected, publicly reported
incidents from 2023 to 2025 to catalogue entries. The record includes source
fabrication in legal filings, an invented airline refund policy, instruction
attacks on customer-service bots, and harmful or misleading conversational
output. A case resting on allegations was set aside from the counted set.

All twelve received at least one existing label in the author's mapping. Three
were legal-citation incidents assigned to source fabrication; that concentration
describes this selected sample, not the prevalence of failures in deployment.
Several incidents received multiple labels. Assigning those labels can describe
different aspects of the same episode without establishing a causal connection
between them.

The mapping for AI Overviews' satirical food and health advice was partial. A
hallucination label covered the false answer, while the available labels did not
cleanly capture treating a joke or satirical source as authoritative. The record
proposed source-genre credulity as a possible refinement. This is a candidate
distinction arising from the exercise, not evidence that it is a new, independent
mechanism.

The incidents were selected and mapped by the author, so the exercise shows the
vocabulary applied to known cases rather than its coverage of future ones. A
sharper test would fix the sampling frame and matching rules in advance and have
independent annotators score both the fit and the misses.

## 4.4 Following the graph: a worked traversal

The checks above recover labels; this shows what the graph does for a reviewer. Take the
dealership-chatbot incident from Section 4.3, where a bot followed an instruction planted in the
conversation and made an unauthorised commitment. A reviewer matches it to prompt injection,
"acting on instructions embedded in content it was only meant to read", which violates
non-maleficence and causes a security breach. A flat keyword list stops there.

Following that record's `relates_to` edges reaches neighbours a keyword search for "prompt
injection" would not surface. Suggestibility, "leading input reshapes the output, the cognitive
face of prompt injection", reframes the same failure under a different obligation and harm,
independence and manipulation rather than security, and points to a behavioural test: does the
output shift under leading but non-adversarial input, not only under a crafted attack?
Jailbreak susceptibility and social engineering mark adjacent attack surfaces on the same bot.
In three steps the single hit has become a small map, the attack, its cognitive mechanism, and
its neighbours, each with its own principle, harm and evidence, which a flat list cannot
assemble.

This is one traced path, not a measured gain over a flat list; Section 6 lists that comparison
as validation still to run. What it shows is the verb the ontology is built around, find a
behaviour and follow its relations, on a real case.

# 5. Release versions and reuse

The historical study and the current catalogue have different scopes. The
207-record study is retained as a versioned baseline; the current version 1.3
contains those records plus 227 proposed human-behaviour analogies, for 434 in
total. None of the additional records enters the denominators of 186 checked
records, 33 codebook items or twelve incidents above, and the companion auditing
paper's six-clause pilot results do not evaluate those 227 analogies.

A later single-pass internal review of the version-1.3 release checked the 227
proposed analogies for definition clarity, source-title support and duplication,
and rechecked the original records' grounding citations. The review was by the
same project, not an independent party, and it produced a small set of
corrections rather than a quality verdict: three original records carried a
grounding citation that did not support them, where the correct paper was already
present in the record's worked examples and was promoted to the citation field;
one proposed analogy's definition was realigned to its name and manifestation;
six candidate records were moved to a better-fitting category; and catalogue
prose was normalised to remove en-dashes. A few further category placements and
two self-labelled symptom-decomposition clusters remain open as judgment calls.
These refinements are recorded in the commit history and do not change the
historical evaluation denominators above.

The version-1.3 bibliography, snapshot of November 9, 2026, records 1,175
citation bindings across 1,036 identifiers, with per-record notes in the
repository. These are availability and arXiv metadata-match counts, not confirmed
mechanisms, each with its own access and relevance note.

Stable slugs and reference numbers permit reuse across releases. A retained
overlap or retired concept should keep its identifier with an explicit
relationship, rather than being silently deleted or renumbered. Consumers can use
the catalogue for retrieval, annotation proposals or advisory audits while
retaining the source passage and evidence status of each claim.

# 6. Limitations

The construction and checking records are a single project's audit trail. They do
not provide an independent human replication of the 186 grounding decisions, the
hard-versus-minor classification or the corrected examples. The reported 26/186
hard-error proportion belongs to that historical cohort and procedure. It should
not be used as a population estimate for the present 434 records, other
catalogues or AI-generated research generally. These are one project's numbers on
one artifact, not an error rate for AI research at large.

The catalogue mixes behaviours, properties, attacks and outcomes, and its
categories and links reflect author judgments. Shared labels do not establish
shared mechanisms between people and AI. Clinical terms do not diagnose a model's
feelings, unconscious motives or intent. Likewise, a source's score for internal
reasoning and a model's output accuracy are different measurements; their
divergence alone does not demonstrate deliberate deception.

The model-based codebook check cannot substitute for blinded human annotation.
The incident exercise uses salient public cases and a permissive matching task.
Neither measures how accurately a reviewer can distinguish close alternatives,
how often the catalogue misses an externally sampled failure, or whether its
graph improves auditing over a flat list, each of which would need an externally
sampled test set and independent annotators. The resource makes no completeness
or state-of-the-art detection claim. The companion auditing paper, "Contracts
Between Humans and AI Agents", evaluates whether checking one named obligation at a
time helps review coding-agent drafts; its pilot tests the auditing method, not
this ontology.

# 7. Availability and reproducibility

The machine-readable catalogue is `ontology/ethical-ai.yaml`, with field and
relation semantics in `ontology/SCHEMA.md`. The six integrity principles the catalogue
is organised around are stated in `contracts/ethical-principles.md`, and the obligations
that operationalise them in `contracts/ai-integrity-contract.md`. The historical version-1.0 catalogue
is pinned at [commit 8798134](https://github.com/danlex/ethicalhive/blob/8798134341ea386da80fb5602bc7dd06ef81cf24/ontology/ethical-ai.yaml);
the later version-1.3 bibliography described in Section 5 is pinned at
[commit 3b9b500](https://github.com/danlex/ethicalhive/blob/3b9b50021ef5eefb15a28d4edb7a5264f2fb626f/ontology/ethical-ai.yaml). These snapshots have different
evidence cohorts and should not be interchanged when reproducing a count.

The historical evidence is in `experiments/citation-audit.md`,
`experiments/verification-report.md`, `experiments/agree-gold.json`, the
taxonomy-agreement outputs, and `experiments/coverage-incidents.md`. The
eligibility rule in `experiments/verify-sample.py` selects records with at least
three examples; that mechanical selection is not an independent test that the
examples are grounded. The later source-review history is retained under
`references/`, including the November 9 literature-count and citation review.

`CITATION.cff` records the citation metadata. Licensing and archival-release
steps are described in `RELEASE.md`; a live website or a changing branch should
not replace the immutable artifact cited for a reported result.

Every reference in this paper was resolved to its source before inclusion, the same
discipline the paper reports applying to the catalogue: each arXiv identifier was opened
and its title, authors and year confirmed against the paper it names.

# 8. Conclusion

EthicalAI is an ontology of the ways an AI can fail its integrity, built so each
behaviour carries an operational definition, a worked example, the obligation it
violates and the harm it causes, and a source passage a reviewer can check rather
than take on trust. The historical 207-record study is grounded, with 186 of the
207 records tied to worked examples from source papers; its categories are
recoverable by an outside rater, at Cohen kappa 0.90 and 0.83; and its vocabulary
maps onto twelve public incidents. The later release extends the ontology to 434
records with 227 proposed behavioural analogies, held outside those evaluation
denominators. What the ontology offers is not a completeness claim but a reusable,
inspectable map: a reviewer, an experimenter or an auditor can find a named
behaviour, read its definition and the evidence behind it, and follow its relations
to the obligations and harms around it.

# References

- Agrawal, A., Suzgun, M., Mackey, L., and Kalai, A. T. (2023). Do Language Models
  Know When They're Hallucinating References? arXiv:2305.18248.
- Gao, T., Yen, H., Yu, J., and Chen, D. (2023). Enabling Large Language Models to
  Generate Text with Citations. arXiv:2305.14627.
- Ji, Z., et al. (2022). Survey of Hallucination in Natural Language Generation.
  arXiv:2202.03629.
- Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N.,
  Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., and Kiela, D.
  (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.
  arXiv:2005.11401.
- Liu, N. F., Zhang, T., and Liang, P. (2023). Evaluating Verifiability in
  Generative Search Engines. arXiv:2304.09848.
- Malberg, S., Poletukhin, R., Schuster, C. M., and Groh, G. (2024).
  A Comprehensive Evaluation of Cognitive Biases in LLMs. arXiv:2410.15413.
- NIST (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0).
  NIST AI 100-1. https://doi.org/10.6028/NIST.AI.100-1
- OWASP (2025). OWASP Top 10 for Large Language Model Applications, 2025 release.
  https://genai.owasp.org/llm-top-10/ (accessed November 2026; a living document, so
  the accessed date fixes the version referenced here).
- Rashkin, H., Nikolaev, V., Lamm, M., Aroyo, L., Collins, M., Das, D., Petrov,
  S., Tomar, G. S., Turc, I., and Reitter, D. (2021). Measuring Attribution in
  Natural Language Generation Models. arXiv:2112.12870.
- Ravichander, A., Ghela, S., Wadden, D., and Choi, Y. (2025). HALoGEN: Fantastic
  LLM Hallucinations and Where to Find Them. arXiv:2501.08292.
- Slattery, P., Saeri, A. K., Grundy, E. A. C., Graham, J., Noetel, M., Uuk, R.,
  Dao, J., Pour, S., Casper, S., and Thompson, N. (2024). The AI Risk Repository:
  A Meta-Review, Database, and Taxonomy of Risks From Artificial Intelligence.
  arXiv:2408.12622.
- Spracklen, J., Wijewickrama, R., Sakib, A. H. M. N., Maiti, A., Viswanath, B.,
  and Jadliwala, M. (2025). We Have a Package for You! A Comprehensive Analysis
  of Package Hallucinations by Code Generating LLMs. arXiv:2406.10279v3.

# Appendix A. Example records

The following records illustrate the distinction between an entry, a reported
finding and a proposed interpretation. The source-fabrication scenario is an
untagged illustration: an assistant cites a plausible legal case that does not
exist. It describes the operational failure without reporting an experiment.

The package-hallucination example in Section 3 is a source-specific measured
result. Its numerator, denominator, tested model set and registry assumptions
must remain attached to the claim. The failure definition can apply more widely
than that experiment, but the experiment's percentage cannot.

Reward hacking is retained in the legacy AI-native category. That placement does
not deny human analogues such as gaming a performance target. Its harm links
express catalogue judgments and its relationship to other modes is not a causal
result about the sequence of a particular incident.
