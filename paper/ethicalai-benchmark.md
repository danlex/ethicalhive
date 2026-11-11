---
title: "EthicalAI: An Evidence-Linked Catalogue for AI Integrity"
author: "Alexandru Dan"
date: "2026-11-09"
abstract: |
  EthicalAI organises integrity failures and related behavioural patterns as
  definitions linked to evidence, obligations, harms and neighbouring concepts.
  This paper reports the construction and review of its historical 207-record
  study. The construction log classified 186 records as grounded in worked
  examples from source papers and retained 21 without that level of support.
  A citation audit recorded 29 repaired source mismatches among roughly fifty
  papers examined. A subsequent checking pass reported hard errors in 26 of
  the 186 grounded records and minor issues in 42. These are findings about
  the reviewed artifact, not error rates for AI research generally. A
  deterministic 33-record codebook check produced model-to-catalogue Cohen
  kappa values of 0.90 and 0.83; this is a model-based consistency check, not
  human validation. Twelve author-selected public incidents illustrate the
  vocabulary's use, including one partial fit. The later 434-record release
  adds 227 untested analogies and a broader bibliography, which are outside
  those historical evaluation denominators. The contribution is a reusable,
  evidence-linked reference in which each claim can be traced to the source
  passage and the scope in which it was observed, and whose own construction
  errors are documented rather than hidden. It is not offered as a validated
  set of distinct AI mechanisms.
---

# 1. Introduction

An AI assistant can cite a nonexistent case, retain a user's mistaken framing
after finding contrary evidence, or extend a coding task without disclosing the
extra changes. Each failure calls for a different check. Citation resolution
does not test whether the assistant updated its framing; correct framing does
not establish that an action stayed within the agreed scope. A catalogue can
make these distinctions available to a reviewer before they become a checklist,
an experimental label or an audit obligation.

EthicalAI collects such distinctions in one reference. Entries include a stable
identifier, an operational definition, evidence pointers, examples and typed
relations. Human cognitive concepts supply part of its vocabulary. The parallel
is a way to formulate a candidate behavioural test, not evidence that an AI
system has the corresponding human mental process. Other entries name attacks,
system properties or outcomes. These different kinds of record are useful to an
auditor, but their inclusion does not make them interchangeable scientific
constructs.

This paper examines the historical 207-record catalogue and the checking work
documented during its construction. It asks what the resource represents, what
its evidence supports, and what went wrong when examples were attached to
sources. Two smaller checks examine category-label recoverability and use on
public incidents. The companion advisory-auditing paper studies a separate
question: whether focused checks of named obligations help review coding-agent
drafts. Its six-clause pilot does not validate the catalogue as a whole.

The current release contains 434 records. Section 6 separates that later
expansion from the original study so that more entries and citations do not
silently enlarge the evidence claimed here.

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

The resource combines definitions and source records across these areas and
connects them to an advisory audit vocabulary. Its proposed value is that a
reviewer can find adjacent concepts and inspect the evidence behind an example
without assembling several separate lists. The historical checks below assess
parts of that reference; they do not establish that its organisation is uniquely
correct or that another taxonomy could not support the same uses.

# 3. Representation and construction

## 3.1 Records and categories

The historical catalogue contains 207 records. Its organising scheme assigns
168 to ten cognitive domains and 39 to an AI-native category. The domains are
labels for navigating the catalogue, not claims about brain localisation or
shared computational mechanisms.

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
systems, such as prompt injection and reward tampering. It should not be read
as proof that no human analogue exists. Reward hacking and scope creep have
recognisable human counterparts. The exclusive assignment is an operational
choice in the released schema, and its boundaries require further study.

Each record carries a stable slug and reference number, a definition, examples,
source pointers and relations. A number identifies a record rather than a
distinct mechanism. Synonyms, narrower variants and linked overlaps therefore
need explicit representation rather than being counted as independent findings.
The historical priority set highlights 26 records for auditing; it is an
author-selected worklist rather than a measured ranking of failure frequency.

## 3.2 Relation semantics

The graph distinguishes several relationships. `violates` points from a mode to
a catalogue obligation. `causes` points to a harm type, such as a wrong answer,
wasted effort or loss of oversight. Despite that field name, these edges record
author-judged harm associations, not estimated causal effects. `relates_to`
connects neighbouring modes; subtype and overlap relations express other
conceptual distinctions. Partial `maps_to` records connect entries with external
frameworks.

The released `causes` relation does not connect one mode to another. Consider the
dealership-chatbot incident discussed in Section 5. An analyst can describe it
as an instruction attack followed by compliant output and an unauthorised offer.
That is an interpretation of the reported sequence, not a three-mode causal path
encoded by the present graph. It would be possible to add a distinct relation
for event sequences, but its meaning and evidence would need to be specified.
The existing graph supports navigation and comparison; it does not demonstrate
how one failure produces another.

## 3.3 Evidence and examples

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
recommended through their extraction procedures. They classified 440,445 of
about 2.23 million recommended packages as hallucinations, or 19.7%. That figure
is a rate over package recommendations, not the percentage of code samples
containing a hallucination. It is also specific to the tested models, prompts
and package-registry snapshot.

# 4. Findings from construction

## 4.1 Citation mismatches

The running citation audit documents cases in which a plausible reference did
not support the catalogue's claim. Among roughly fifty papers examined during
grounding, 29 mismatches were repaired by changing the cited source. Other
mismatches led to records being held without a grounded AI example. The
approximate denominator and the distinction between repaired and held records
prevent treating 29 as an exact overall error rate.

The recorded problems include papers on a different phenomenon, a result in the
opposite direction, and an appropriate test with a null finding. For example,
one source attached to model agency concerned a human user's perceived control.
A source used for pragmatic over-accommodation instead reported under-use of
pragmatic inference. Some proposed bias analogies were tested without the
expected effect. These are different reasons to revise a claim, and a
bibliography entry alone does not distinguish them.

The audit supports a practical construction requirement: attach a claim to its
supporting passage and experimental scope, not just to a title or a search hit.
It does not estimate how often other catalogues contain such errors, because
the checked papers were not a random sample of research publications.

## 4.2 Rechecking worked examples

The subsequent verification report describes four checking batches covering the
186 historically grounded records and approximately 510 tagged examples. The
record, rather than a new full-text sweep for this revision, is the source of
the following counts.

| Recorded outcome | Records | Share of the 186-record cohort |
|---|---:|---:|
| No issue detected | 118 | 63% |
| Minor issue | 42 | 23% |
| Hard error | 26 | 14% |

A hard error meant that a figure was contradicted by, or absent from, the cited
paper. Minor issues included loose attribution, rounding and confusion between
experimental conditions. The report records no unreachable papers in this
cohort. These are outcomes of the checking procedure, not independently
adjudicated labels or a residual error estimate for the corrected release.

Several corrections changed a number or its interpretation: a city name, a
percentage, a measurement scale, or the observed and hidden reward labels in an
example. Six hard-error cases concerned quoted examples that were not found in
their cited papers. The record describes replacing these with supported material
or marking them as untagged illustrations. It records corrections to all 68
flagged entries, while leaving open whether an independent subsequent reader
would find further errors.

The two audits address different questions. Citation checking asks whether the
source concerns and supports the claimed phenomenon. Example checking asks
whether a particular statement is faithful to that source. Their combined lesson
is narrower than a general claim about AI reliability: this artifact needed both
checks, and initial source inspection did not prevent later transcription and
interpretation errors.

# 5. Checks of category use and incident mapping

## 5.1 A model-based codebook check

The codebook study used 33 records, three from each category. The sampling script
selects the first three records by reference number in each group, so the sample
is deterministic and balanced rather than random. Two separate language-model
calls received category descriptions and each record's name and definition,
without its stored category. Agreement was measured against the catalogue and
between the calls.

The sonnet rater agreed with the catalogue on 30/33 records, with Cohen kappa
0.90. The haiku rater agreed on 28/33, with kappa 0.83. Agreement between the
raters was kappa 0.93. There were eight rater-to-catalogue disagreements across
five records; three records were assigned differently by both raters. These
included cognitive miserliness, mind-wandering and scope creep, each near a
boundary between the supplied categories.

This shows that two model calls apply the codebook similarly to its author on a
balanced sample. It is a model-based consistency check, not a substitute for
blinded human annotation or evidence of construct validity, and shared training
can make model agreement less informative than independent human agreement.

## 5.2 An incident-mapping exercise

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
hallucination label covered the false answer, while the available labels did
not cleanly capture treating a joke or satirical source as authoritative. The
record proposed source-genre credulity as a possible refinement. This is a
candidate distinction arising from the exercise, not evidence that it is a new,
independent mechanism.

Because the incidents were selected by the author and mapped manually, the
exercise demonstrates possible uses of the vocabulary. It cannot establish
coverage of future incidents or superiority to another taxonomy. A stronger
test would specify the sampling frame and matching rules in advance and have
independent annotators score both fit and failure to fit.

# 6. Release versions and reuse

The historical study and the current catalogue have different scopes. The
207-record study is retained as a versioned baseline; the current version 1.3
contains those records plus 227 proposed human-behaviour analogies, for 434 in
total. None of the additional records enters the denominators of 186 checked
records, 33 codebook items or twelve incidents above. Nor do the companion
method paper's six-clause pilot results evaluate those 227 analogies.

The November 9, 2026 bibliography snapshot has 1,175 selected citation bindings
across 1,036 publication identifiers. Of the 434 records, 359 have three selected
references and 75 have fewer, including nine with none. These are bibliography
availability counts. They are not counts of independently confirmed mechanisms
or replications. Preprints, theoretical articles, empirical studies and reviews
must be interpreted according to their individual access and relevance notes.

The current row totals are separately recorded arXiv metadata-query matches in
cs.AI, cs.CL and cs.LG. They are not full-text citation counts or an exhaustive
count of relevant research. Keyword matches can include unrelated uses, and
human research cited in a record can fall outside that AI-domain query. The
query, filters and retrieval date travel with the total.

Stable slugs and reference numbers permit reuse across releases. A retained
overlap or retired concept should keep its identifier with an explicit
relationship, rather than being silently deleted or renumbered. Consumers can
use the catalogue for retrieval, annotation proposals or advisory audits while
retaining the source passage and evidence status of each claim.

# 7. Limitations

The construction and checking records are a single project's audit trail. They
do not provide an independent human replication of the 186 grounding decisions,
the hard-versus-minor classification or the corrected examples. The reported
26/186 hard-error proportion belongs to that historical cohort and procedure.
It should not be used as a population estimate for the present 434 records,
other catalogues or AI-generated research generally.

The catalogue mixes behaviours, properties, attacks and outcomes, and its
categories and links reflect author judgments. Shared labels do not establish
shared mechanisms between people and AI. Clinical terms do not diagnose a
model's feelings, unconscious motives or intent. Likewise, a source's score for
internal reasoning and a model's output accuracy are different measurements;
their divergence alone does not demonstrate deliberate deception.

The model-based codebook check cannot substitute for blinded human annotation.
The incident exercise uses salient public cases and a permissive matching task.
Neither measures how accurately a reviewer can distinguish close alternatives,
how often the catalogue misses an externally sampled failure, or whether its
graph improves auditing over a flat list. Those questions require separate
evaluation. The resource makes no completeness or state-of-the-art detection
claim.

# 8. Availability and reproducibility

The machine-readable catalogue is `ontology/ethical-ai.yaml`, with field and
relation semantics in `ontology/SCHEMA.md`. The historical version-1.0 catalogue
is pinned at [commit 8798134](https://github.com/danlex/ethicalhive/blob/8798134341ea386da80fb5602bc7dd06ef81cf24/ontology/ethical-ai.yaml);
the later version-1.3 bibliography described in Section 6 is pinned at
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

# 9. Conclusion

EthicalAI provides definitions, evidence pointers and conceptual relations for
reviewing AI integrity. Its historical construction records show why a plausible
citation and an accurate worked example need separate checks. The 207-record
study also supplies small demonstrations of codebook use and incident mapping,
with their sampling and annotation limits stated. The later bibliography and
227 untested analogies extend the reference without extending those empirical
claims. Its practical value is that a reviewer can find an adjacent concept and
inspect, or correct, the exact relationship between a claim, its source and the
scope in which it was observed. The construction audit makes one lesson
concrete: a plausible citation and a faithful worked example are separate
properties, and a reusable catalogue has to check both, because inspecting the
source did not prevent later transcription and interpretation errors.

# References

- Malberg, S., Poletukhin, R., Schuster, C. M., and Groh, G. (2024).
  A Comprehensive Evaluation of Cognitive Biases in LLMs. arXiv:2410.15413.
- Slattery, P., Saeri, A. K., Grundy, E. A. C., Graham, J., Noetel, M., Uuk, R.,
  Dao, J., Pour, S., Casper, S., and Thompson, N. (2024). The AI Risk Repository:
  A Meta-Review, Database, and Taxonomy of Risks From Artificial Intelligence.
  arXiv:2408.12622.
- NIST (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0).
  NIST AI 100-1. https://doi.org/10.6028/NIST.AI.100-1
- OWASP (2025). OWASP Top 10 for Large Language Model Applications, 2025 release.
  https://genai.owasp.org/llm-top-10/
- Ji, Z., et al. (2022). Survey of Hallucination in Natural Language Generation.
  arXiv:2202.03629.
- Ravichander, A., Ghela, S., Wadden, D., and Choi, Y. (2025). HALoGEN: Fantastic
  LLM Hallucinations and Where to Find Them. arXiv:2501.08292.
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

Reward hacking is retained in the legacy AI-native category. That placement
does not deny human analogues such as gaming a performance target. Its harm
links express catalogue judgments and its relationship to other modes is not a
causal result about the sequence of a particular incident.
