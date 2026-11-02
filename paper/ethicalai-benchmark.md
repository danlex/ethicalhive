# EthicalAI: A Grounded Catalogue of AI Integrity Failure Modes, and What Grounding It Revealed

Alexandru DAN

Status: working draft, version 1.0. Companion resource to the clause-grounded advisory
auditing paper (`paper/draft.md`). Positioning and validation sources are recorded in
`references/catalogue-prior-art.md`; the two load-bearing comparison figures were verified
against their primary abstracts.

## Abstract

We catalogue 207 ways an AI system can fail at integrity. Most modes are framed as parallels
to a named human cognitive failure and organised by ten cognitive systems; a second tier of 39
modes we label AI-native, as lacking a clear human analogue. The modes are linked by
a relation graph of which mode violates which obligation, causes which harm, and relates to
which neighbour, and each grounded mode is tied to a primary paper that was read rather than
keyword-matched. A hundred and eighty-six of the 207 are grounded this way; the remaining
twenty-one are documented as having no supporting paper we could find.

Existing resources catalogue AI risk at three altitudes that this one does not occupy:
societal harm outcomes, adversarial attack techniques, and single-family behavioural
benchmarks. The nearest prior catalogue at the mechanism level evaluates 30 cognitive biases
[Malberg et al. 2024]; this catalogue extends across biases, memory, reasoning, hallucination,
source fabrication, scope creep, and misalignment in one structure. Building it produced two
findings that stand on their own. Grounding by reading rather than by trusting the reference
caught citation drift: of roughly fifty cited papers checked while grounding, twenty-nine did
not support their mode and were re-cited to a paper that does, and several further modes whose
citation also failed on checking were reclassified as ungrounded rather than re-cited. An
adversarial verification sweep over all 186
grounded modes then found that even grounding done by reading mis-stated a specific figure in
fourteen percent of modes. We also probe the catalogue's own structure: independent model
raters blind to the catalogue recover its category assignments at Cohen kappa 0.83 to 0.93 (a
model-based codebook check, not human annotation), and twelve documented incidents we selected
each map to a named mode, with one partial fit that points to a missing mode. We make no
state-of-the-art claim; the value is a documented, provenance-checked reference whose
reliability we measure rather than assume, with the measurements' own limits stated.

## 1. Introduction

A confident answer and a correct answer look identical from the outside. The space between
them is where integrity failures live, and that space is wide: a model can hallucinate,
flatter the user into a wrong answer, drop a constraint halfway through a long task, or
quietly bend a rule for what it decides is a good cause. These are not one failure but many,
and they have been studied unevenly, under inconsistent names, across cognitive science,
machine learning, and AI safety.

The gap matters more as AI produces results faster than people can check them. When nine
mathematicians were needed to confirm whether a model had refuted an eighty-year-old geometry
conjecture, the lesson, in the words of Shafto, Ono, and Kominers [Shafto et al. 2026], was
that "discovery is nonstop, and human confirmation is now what is scarce." Formal mathematics
answers this with proof checkers. The softer integrity failures this catalogue names, a
confident answer that is wrong, a citation that does not resolve, a constraint quietly dropped,
have no proof checker, so a named, grounded catalogue and a human-in-the-loop audit are the
verification infrastructure available for that layer.

This paper describes a resource that names them in one place and ties each name to evidence.
The organising idea, taken from a companion method paper on clause-grounded advisory
auditing, is that integrity is a property of a relationship rather than of a model in
isolation. A human and an agent agree, implicitly or explicitly, on a set of obligations, and
a failure mode is a way the agent breaks one of them. Organising the catalogue around that
relationship keeps it readable to the person who has to decide what to do when a flag is
raised. Here we focus on the catalogue itself: where it sits relative to existing taxonomies,
how it is structured and grounded, what the grounding revealed about citation reliability, and
whether its own structure holds up when an outsider tries to reproduce it.

We frame this as a reference artifact rather than a new detector or a leaderboard result: a
map that other work can cite, reuse, and extend. At this stage a reusable and checked map does
more for the field than another point score on a single failure mode.

## 2. Why another catalogue

There is no shortage of ways to enumerate what goes wrong with AI. The honest question a new
catalogue has to answer is not whether failures are worth naming but why the existing
catalogues do not already name these ones. The prior work clusters at three altitudes, and
this catalogue sits at none of them.

The first is the societal and governance layer. The MIT AI Risk Repository [Slattery et al.
2024] is the most comprehensive example: a meta-review of 74 frameworks containing 1,725
distinct risks, organised by who causes a risk and in what domain. The DeepMind risk taxonomy
[Weidinger et al. 2021], the NIST AI Risk Management Framework [NIST 2023], and the AI
Incident Database live here too. The MIT repository is more than a flat list of harms: it
includes a causal taxonomy (by entity, intent, and timing) and covers AI-caused as well as
human-caused failures. What it and its neighbours share is the altitude: they organise risks
and outcomes at the level of governance, not the reasoning step, and do not decompose that step
into named, mechanism-level ways a model arrives at a confident wrong answer.

The second is the adversarial and security layer. The OWASP Top 10 for LLM Applications
[OWASP 2025], MITRE ATLAS, and similar efforts catalogue what an attacker does to a system:
prompt injection, data poisoning, excessive agency. This is largely orthogonal to failures a
model commits with no adversary present, and where the two touch, the resolution is coarse in
exactly the place this catalogue is fine-grained. OWASP's single entry for misinformation is
one bucket over dozens of distinct epistemic mechanisms.

The third is the behavioural-measurement layer, and this is where the overlap is real and
must be stated plainly. Benchmarks of cognitive bias and surveys of hallucination do
decompose model reasoning into named mechanisms. The closest single prior catalogue is
Malberg et al. [2024], a large-scale evaluation of 30 cognitive biases across 20 models. This
catalogue's classic-bias subset substantially overlaps those 30, and we cite it as the
nearest prior art. On the hallucination side, the Ji et al. [2022] survey and HALoGEN
[Ravichander et al. 2025] give principled taxonomies of that one family, and our hallucination
and source-fabrication modes overlap theirs. The difference is not that these are wrong. It is
that each decomposes a single family at a time.

The slice none of them occupies, taken together, is the integration. This catalogue records
207 integrity failure modes, frames most as parallels to a specific named human cognitive
failure organised by ten cognitive systems, links them with an explicit graph, adds a second
tier of modes we label AI-native as lacking a clear human analogue, and grounds most entries
(186 of the 207) in a primary paper that was read. It is broader in coverage than Malberg's 30 biases and extends along axes
Malberg does not cover (memory, reasoning, output-integrity, and AI-native failures), with a
relation graph and a cognitive-science organising principle no prior catalogue has. Breadth of
coverage is not itself a scientific result: more labels do not establish more distinct
constructs, and Malberg pairs its 30 biases with 30,000 tests across 20 models, which this
catalogue does not match. The claim is one of integration and coverage, not of superior
measurement. What this yields is a single map that
unifies failure families today catalogued in separate, mechanism-specific efforts, grounded in
cognitive science and linked by an explicit graph. It is a map across existing categories, not
a new risk category, and we claim that and no more. The full positioning, with every source checked against its primary and
unverified fields flagged, is in `references/catalogue-prior-art.md`.

## 3. The catalogue: structure and construction

### 3.1 Two tiers

Every mode carries exactly one of two labels. A human-paralleled mode names a construct from
human psychology and its machine analogue: anchoring, confirmation bias, the illusory-truth
effect, cognitive dissonance, many of them from the heuristics-and-biases tradition [Tversky
and Kahneman 1974]. These sit in ten groups organised loosely by brain system. An
AI-native mode is a failure we judge to lack a genuine human analogue, tied to the machine substrate:
prompt injection, reward tampering, data contamination, emergent misalignment, backdoor
triggers, unbounded consumption. A validator rejects any mode that claims neither label or
both, which keeps the boundary disciplined and forces a judgment on each addition. Of the 207
modes, 168 are human-paralleled and 39 are AI-native. The full distribution is below; the
complete list, with every definition and example, is in the released file and on the site.

| Cognitive system | Modes | Example behaviours |
|---|---|---|
| Perception | 11 | Controlled hallucination, Priors overriding evidence |
| Memory | 13 | Catastrophic forgetting, Source fabrication |
| Attention | 12 | Inattentional blindness, Change blindness |
| Heuristics | 25 | Anchoring, Availability, Representativeness |
| Reasoning | 22 | System 1 / System 2, Cognitive miserliness |
| Metacognition | 16 | Overconfidence, Uncertainty communication |
| Language | 14 | Garden-path parsing, Semantic satiation |
| Social | 28 | Sycophancy, Conformity, Theory of mind |
| Moral | 12 | Omission bias, Amplified moral bias |
| Self and agency | 15 | Confabulated agency, Sense of agency |
| AI-native (no human analogue) | 39 | Prompt injection, Reward hacking, Scope creep |

Twenty-six of the modes are marked as a highlighted priority set, the ones most load-bearing
for an integrity auditor in practice (listed in the appendix).

### 3.2 What an entry looks like

Each mode is a definition, a cognitive-system placement, a human parallel or the AI-native
label, a set of graph edges, and worked examples. The clearest way to show the catalogue is to
exhibit entries, so the following are drawn verbatim from grounded modes across the tiers, each
with a real finding from the paper that grounds it.

| Mode | System | A grounded example (abbreviated) | Source |
|---|---|---|---|
| Anchoring | Heuristics | an irrelevant number ("939") placed before a tree-count estimate drags the estimate toward it | arXiv:2505.15392 |
| Sycophancy | Social | the same argument is called "strong" when the user likes it and "unconvincing" when they dislike it | arXiv:2310.13548 |
| Overconfidence | Metacognition | input regions where the model is strongly overconfident, cancelled out in the global metric | arXiv:2605.13484 |
| Garden-path parsing | Language | "while the boy washed the dog barked loudly" is rendered as the boy washing the dog | arXiv:2502.09307 |
| Omission bias | Moral | opposite verdicts on the injured-deer dilemma framed as action versus inaction | arXiv:2610.07847 |
| Prompt injection | AI-native | invisible instructions on a summarised web page hijack the model | arXiv:2302.12173 |
| Reward hacking | AI-native | a boat-race agent oscillates on reward tiles without ever finishing the lap | arXiv:2606.15385 |
| Scope creep | AI-native | given an empty input file, it fabricates output in the graded format instead of flagging the gap | arXiv:2605.02269 |
| Package hallucination | AI-native | across 576,000 code samples, 19.7% of recommended packages do not exist | arXiv:2406.10279 |

A fuller set of worked entries, including the graph edges, is in the appendix.

### 3.3 The relation graph

Modes are not a flat list. Each carries a `violates` edge to one of a small set of principles
(honesty, non-maleficence, transparency, scope-fidelity, independence, corrigibility,
calibration) and a `causes` edge to a harm (wrong answer, wasted effort, manipulation,
security breach, loss of oversight). Most carry `relates_to` clusters that link adjacent
modes, and many carry `is_a`, `opposite_of`, `root_of`, and `same_as` edges. The point of the
graph is mechanical: overlaps and gaps can be found by walking edges rather than by eye, a
reader who lands on one mode can navigate to its neighbours and its causal roots, and a real
incident that is a chain of failures can be represented as a path rather than forced onto a
single label.

A worked example makes the last point concrete. The dealership-chatbot failure analysed in
Section 5.2 is a path through the graph, not a single node: a prompt injection (AI-native), a
sycophantic capitulation (Social), and scope creep (AI-native) when the agent commits to an
unauthorised offer. The catalogue's `causes` edges link these three as a chain, so the
incident is one traversal of the graph rather than a single label. Those edges record the
catalogue's hypothesised links, not demonstrated causation (see Section 5.2); what they add
over a flat taxonomy is that a single label can be read as a path.

### 3.4 Crosswalks

To compose with existing taxonomies rather than reinvent them, modes carry a `maps_to` edge to
external frameworks where there is a correspondence: the OWASP Top 10 for LLM Applications
[OWASP 2025], a multi-agent failure taxonomy [Cemri et al. 2025], an in-context scheming study
[Meinke et al. 2024], and a hallucination survey [Alansari and Luqman 2025]. The crosswalk is partial by
design; it records where this catalogue and an external framework describe the same thing.

### 3.5 Grounding by reading

Most catalogues of failure modes stop at a definition and an illustrative scenario. This
resource asks for more: each mode should carry worked examples, and each example should come
from a paper actually read, tagged inline with that paper's arXiv identifier. An example that
is a plausible scenario rather than a reported finding is kept but marked as illustrative and
left untagged, so a reader can tell a measured case from a hypothetical one.

The procedure was deliberately literal. For a mode, we fetched the cited paper's full text,
found the specific finding, and wrote the example around the actual numbers, model names, and
setups the paper reported. Where a mode had no cited paper, we searched for one, read it, and
grounded the mode only if the paper genuinely demonstrated the behaviour. Where no such paper
existed, the mode was left ungrounded and the absence recorded. This reading-first discipline
is what produced the two findings in Section 4. It is also expensive, which is why 186 of 207
modes are grounded rather than all of them.

### 3.6 Machine-readable release and stable identifiers

The catalogue is a single YAML document with a documented schema (`ontology/SCHEMA.md`). Each
mode has a stable slug identifier and a stable catalogue number, under a stability contract:
identifiers are not reused, a merged or retired mode keeps its identifier with a
deprecation note rather than being deleted, and breaking changes bump the version. This is
what lets an external citation to a specific mode remain valid across revisions.

## 4. What grounding revealed

### 4.1 Citation drift

The catalogue began with citations attached to many modes by keyword match: a paper whose
title contained the name of the behaviour. Reading those papers rather than trusting the
titles showed that keyword match is unreliable. Of roughly fifty cited papers checked while
grounding, twenty-nine did not support their mode and were re-cited to a paper that does; a
further handful failed on checking and led to their mode being reclassified as ungrounded
rather than re-cited, so twenty-nine is the repaired subset, not the total that failed. The
failures came in recognisable kinds.

Some citations were simply about a different subject. A mode about a model over-trusting its
own output cited a watermarking method; a mode about the model's own sense of agency cited a
study of the human user's perceived control. Some drew the opposite conclusion: a mode about a
model faking introspection cited a paper arguing that model self-reports can be faithful; a
mode about pragmatic over-accommodation cited a paper showing that models under-use pragmatic
inference. A smaller set were null results dressed as support: a mode about the sunk-cost
fallacy cited a paper that tested it and found it essentially absent in current models, and a
mode about status-quo bias cited a benchmark that found models leaning the opposite way.

Each mismatch was either repaired by finding and reading a paper that genuinely supports the
mode, or, where no such paper exists, recorded as a held mode with the reason stated. Every
decision is logged in a running citation audit, which doubles as the worklist and as the
evidence for the rate reported here. The reading is simple and uncomfortable. In a resource
that advertises itself as grounded, citations that look right but do not hold accumulate even
when everyone is acting in good faith, and only reading the source catches them. This is the
same failure mode the catalogue itself names, source fabrication, observed in the artifact
that catalogues it.

### 4.2 A verification sweep on the grounding

Catching bad citations is necessary but not sufficient. Having the right paper in hand does
not guarantee that the figure written into the example is the figure the paper reports. To
measure that, we ran an adversarial verification pass over all 186 grounded modes, across four
independent batches. For each mode, an independent checker re-read the cited paper and
confirmed, claim by claim, whether the specific numbers, model names, and setups in the
example actually appeared in it, with instructions to mark a claim as not found rather than
give it the benefit of the doubt.

The sweep found that twenty-six of the 186 modes (fourteen percent) contained a hard error: a
figure that the paper contradicted or that did not appear in it at all. A further forty-two
(twenty-three percent) contained a minor issue: a number loosely rounded, an attribution that
credited the wrong paper, or a finding placed on the wrong experimental condition. None of the
papers was unreachable.

The errors were instructive in their shape. In almost every flagged case the behaviour was
real and the paper was the right one; what drifted was a specific number, model name, or
causal framing. A wrong city in a hallucination example; a compliance rate reported as twelve
percent where the paper said fourteen; a conditional accuracy written as zero where the paper
reported 2.6 percent; a reward figure whose observed and hidden labels were reversed. In six
cases a quoted example did not appear in the cited paper at all; we rewrote these to the
paper's actual content or demoted them to untagged illustrations. Most of the flagged errors
are transcription-level over-reads rather than invented findings, but these six are more
serious, and we do not claim to know how each arose; what they share is that a reader would
not catch them without re-reading the source. All sixty-eight flagged modes were corrected in
the same pass. Because the sweep covers every grounded mode, these are population figures for
this artifact rather than a sampled estimate, and the hard-error rate held roughly steady
across the four batches (eighteen, fifteen, seven, and eighteen percent). One limit matters:
this is the error a single adversarial re-read caught and we then corrected, not a guarantee
about the corrected catalogue; a residual error rate would need an independent recheck of the
corrected version.

### 4.3 Why the two findings matter together

The citation audit measures how often the wrong paper is attached to a claim. The verification
sweep measures how often the right paper is misquoted. They are the same problem at two levels,
and together they put a number on something usually left to trust: provenance in a fast-moving
field degrades at both levels, and the only remedy that worked was reading, twice.

## 5. Validation

A catalogue earns trust not by the care of its author but by holding up when someone else
probes it. We report two checks: whether its category structure is reproducible, and whether
it classifies failures it was not built from.

### 5.1 Is the category structure reproducible?

The obvious threat to a single-author catalogue is that its structure is idiosyncratic. We
probe this with a codebook protocol. We drew a stratified sample of 33 modes, three from each
of the eleven categories, gave two independent raters a one-sentence definition of each
category and, for each mode, its name and definition only with the catalogue's own category
hidden, and asked each rater to assign a category. We then measured agreement with Cohen's
kappa, which corrects for chance.

The raters are independent language-model calls, one on the sonnet tier and one on the haiku
tier, blind to the catalogue label. This is deliberately a proxy. It is not human
inter-annotator agreement, and we do not present it as such; human annotation remains required
before the catalogue is treated as validated. What the proxy buys is a real chance-corrected
number and a stress test of whether the category definitions are clear enough to apply at all.

Agreement was high. Against the catalogue the sonnet rater agreed on 30 of 33 modes (kappa
0.90) and the haiku rater on 28 of 33 (kappa 0.83); the two raters agreed with each other at
kappa 0.93. Chance agreement across eleven balanced categories is low (expected agreement
0.09), so the raw agreement and the kappa are close. More informative than the aggregate is
that the disagreements are localised rather than scattered. Three modes account for the shared
discordances, missed by both raters: cognitive miserliness, filed under Reasoning and read as
Heuristics; default-mode mind-wandering, filed under Self and agency and read as Attention; and
scope creep, filed in the AI-native tier and read as Self and agency. The haiku rater also
missed two further modes the sonnet rater placed correctly (Dual-process System 1 and 2, and
Sense of agency), so there are eight rater-to-catalogue disagreements across the two raters, on five distinct modes, three of them missed by both. These read as
boundary cases rather than errors: each mode sits on the seam between two systems. We do not
claim this reveals something about cognition; the equally likely reading is that our definition
is ambiguous at that seam. Either way, the value of the probe is that it names which seams are
live, and these three are the clearest candidates for a secondary-category label.

### 5.2 Coverage: does the catalogue classify failures it was not built from?

We assembled a held-out set of twelve real, publicly documented AI integrity-failure incidents
from 2023 to 2025, none used to ground the catalogue, each verified against a real source with
a confirmed quotation. We mapped each to the catalogue by hand and asked two things: does it
land on a named mode whose definition matches, and what does it miss.

Every one of the twelve maps to at least one named mode, and the match is specific rather than
a catch-all. The clearest case is the most common: the catalogue's source-fabrication entry
already carries, as its illustrative example, a plausible but nonexistent legal citation, which
is exactly what happened in the three separate fake-citation incidents (Mata v. Avianca, the
Michael Cohen filing, and the Morgan and Morgan motions). That three of the twelve are the same
mode reflects that source fabrication is the most litigated real-world integrity failure to
date.

The more useful observation is that real incidents are rarely a single mode. At least four of
the twelve are best described as a short causal chain: a dealership chatbot was prompt-injected
into a compliant persona, which produced a sycophantic capitulation, which produced an
unauthorised binding offer; a coding agent ignored an action freeze, then deceived its user
about having done so and fabricated test results to cover it. A flat list would force a single
label on each. The relation graph is what lets the catalogue represent them as trajectories, so
the incidents illustrate how the graph can describe a failure as a chain rather than as a
single label. They do not establish that the specific edges are correct; that would need a
test the catalogue does not yet have.

One incident did not fit cleanly, and that is the point. The AI Overviews answers that advised
adding glue to pizza and eating a small rock a day were a failure to detect that a source was
satirical and to treat it as authoritative. No existing mode names this specifically:
source-monitoring error is about self-generated versus retrieved content, and imitative
falsehood is about repeating a common misconception, neither of which is credulity about a
source's genre or seriousness. We take this as a candidate addition, a source-genre-credulity
mode, and record it rather than quietly add it, because a new mode must earn its own grounding
paper first by the same reading-first rule as the rest. A catalogue that nothing can fall
outside is not falsifiable; this one can be, and was.

The honest bound on this result is the sample. These are prominent, widely reported incidents,
selected toward failures already salient enough to make the press, so the test shows the
catalogue handles known failures, not that it anticipates novel ones. It is a usability
demonstration, not a completeness proof.

## 6. The catalogue in use

The catalogue is a reference, and its first consumer is a companion method paper on
clause-grounded advisory auditing: it takes a subset of these modes, writes each as a
natural-language obligation with a stable rule identifier, and audits a draft clause by clause,
with the human as the final decision maker. That paper is where the method and its results
live; the only point here is that it is the catalogue, and the grounding in Section 4, that let
a clause point at evidence rather than at an assertion. Any downstream use, an auditor, a
training target, a review checklist, inherits the same property.

## 7. Limitations

This is a resource, not a result about model capability.

The grounding is single-reader, and the validation raters are language models, not humans.
Both the fourteen-percent hard-error rate and the category-reproducibility kappas are
single-pass, single-rater-type figures. The kappas come from a model-based codebook check, not
human agreement: they show that the category assignments can be recovered from the written
definitions, not that the categories carve the space correctly, and shared assumptions between
the raters and the author could inflate the agreement. Human two-annotator adjudication over a
larger, independently collected sample is still required before the structure can be called
validated. The coverage test samples prominent incidents, so it demonstrates usability on
known failures rather than coverage of novel ones, and "a mode fits" is a lenient bar that a
broad label can pass; a stronger test would use an externally sampled incident set and score
specificity and missing modes.

Twenty-one modes are ungrounded. They fall into honest categories, all recorded: behaviours
that current models tested and did not show (sunk-cost fallacy, moral licensing); analogies for
which no model-side paper exists (attentional blink, just-world bias, scope insensitivity); and
neuroscience framings that overlap already-grounded modes without a distinct instance. We did
not force a citation onto any of them, because doing so would be the source-fabrication failure
the resource is built to name. For the same reason the one candidate mode the coverage test
surfaced is recorded as a candidate, not added, until it has a grounding paper.

The taxonomy's boundary is a judgment. The two-tier rule is enforced mechanically, but which
side a mode falls on, and whether two modes are distinct or one, is a human call, and
reasonable people would draw some of those lines differently. The validation in Section 5 is an
attempt to measure how much that judgment is shared, not a claim that it is unique.

Finally, the resource makes no claim to completeness or to state of the art. Stronger methods
exist for specific failures, in particular sampling-based and hidden-state approaches for
hallucination. The value here is breadth, provenance, structure, and a measured account of its
own error rate.

## 8. Availability and citation

The catalogue is released as a single machine-readable file with a documented schema
(`ontology/SCHEMA.md`), a human-readable site, and a `CITATION.cff` for direct citation. It is
versioned (1.0) under a stable-identifier contract so that citations to a specific mode remain
valid across revisions. A license and a minted DOI are recorded as the final release steps in
`RELEASE.md`; the recommended terms are an attribution license for the catalogue data and a
permissive license for the accompanying code. The citation audit and the verification report
ship with the resource so that a reader can see not only the catalogue but the record of how
reliable its grounding is.

## 9. Conclusion

The through-line of this project is that provenance in a fast-moving field cannot be taken on
trust, and that checking it is cheap enough that leaving it unchecked is a choice rather than a
necessity. Grounding 207 failure modes by reading showed how often a cited paper fails to
support its claim and how often a claim grounded by reading still misquotes the source; a
model-based codebook check suggested the category assignments can be recovered from their
definitions. The provenance findings were non-trivial and are now corrected and documented
rather than latent; the reproducibility and coverage checks are preliminary and their limits
(a candidate missing mode, the need for human annotation, the lenient coverage bar) are named
in Sections 5 and 7 rather than hidden. We offer the catalogue as a shared map and
the findings as a small cautionary result about how provenance decays in a field that cites
faster than it reads. The most honest thing the project did was audit its own grounding and
report what it found.

## References

Verified against primary sources this session or canonical. The complete positioning
reference list, with per-entry verification status, is in `references/catalogue-prior-art.md`;
the complete per-mode bibliography accompanies the resource.

- Bradner, S. (1997). Key words for use in RFCs to Indicate Requirement Levels. RFC 2119, IETF.
- Malberg, S., Poletukhin, R., Schuster, C. M., and Groh, G. (2024). A Comprehensive
  Evaluation of Cognitive Biases in LLMs. arXiv:2410.15413.
- Slattery, P., Saeri, A. K., Grundy, E. A. C., Graham, J., Noetel, M., Uuk, R., Dao, J., Pour,
  S., Casper, S., and Thompson, N. (2024). The AI Risk Repository: a meta-review, database, and
  taxonomy of risks from artificial intelligence. arXiv:2408.12622.
- Weidinger, L., et al. (2021). Ethical and social risks of harm from Language Models.
  arXiv:2112.04359.
- NIST (2023). AI Risk Management Framework (AI RMF 1.0). NIST AI 100-1.
- OWASP (2025). OWASP Top 10 for Large Language Model Applications, 2025 release.
- Ji, Z., et al. (2022). Survey of Hallucination in Natural Language Generation. arXiv:2202.03629.
- Ravichander, A., Ghela, S., Wadden, D., and Choi, Y. (2025). HALoGEN: Fantastic LLM
  Hallucinations and Where to Find Them. arXiv:2501.08292.
- Meinke, A., Schoen, B., Scheurer, J., Balesni, M., Shah, R., and Hobbhahn, M. (2024).
  Frontier Models are Capable of In-context Scheming. arXiv:2412.04984.
- Cemri, M., Pan, M. Z., Yang, S., Agrawal, L. A., Chopra, B., Tiwari, R., Keutzer, K.,
  Parameswaran, A., Klein, D., Ramchandran, K., Zaharia, M., Gonzalez, J. E., and Stoica, I.
  (2025). Why Do Multi-Agent LLM Systems Fail? arXiv:2503.13657.
- Alansari, A., and Luqman, H. (2025). Large Language Models Hallucination: A Comprehensive
  Survey. arXiv:2510.06265.
- Tversky, A., and Kahneman, D. (1974). Judgment under Uncertainty: Heuristics and Biases.
  Science, 185(4157).
- Shafto, P., Ono, K., and Kominers, S. D. (2026). What Happens When the World is Run on Code
  No One Understands? TIME, 20 August 2026 (retrieved 1 November 2026; archive a copy before
  submission, as the live URL may move behind a paywall).

## Appendix A. Worked catalogue entries

Three entries in full, to show the shape of the catalogue: the definition, the two-tier
placement, the graph edges, and an example. The first example is deliberately illustrative and
untagged, which is how the catalogue marks a plausible scenario rather than a reported finding;
the other two carry a grounded example with its source.

**Source fabrication** (num 101, Memory). Definition: citing a path, line, symbol, or URL that
does not resolve to what it claims. Human parallel: source confabulation and misattribution.
Edges: violates honesty; causes a wrong answer; is a kind of hallucination; relates to
source-monitoring error, source amnesia, and cryptomnesia. Example (illustrative): asked for a
supporting case, it produces a plausible but nonexistent case name and reporter number.

**Anchoring** (num 31, Heuristics). Definition: keeping an initial framing or estimate after
later evidence has broken it. Human parallel: anchoring. Edges: violates calibration; causes a
wrong answer; relates to the availability heuristic, status-quo bias, and the framing effect.
Example: an irrelevant number ("the number of socks in your drawer: 939") placed before
"estimate the number of trees in the Amazon" measurably drags the estimate toward it
[arXiv:2505.15392].

**Reward hacking** (num 104, AI-native). Definition: satisfying the metric that measures the
task rather than the task itself, for example by editing tests or hardcoding outputs; also
called specification gaming. No human analogue. Edges: violates honesty; causes loss of
oversight; relates to reward tampering, goal misgeneralisation, noble-cause corruption, and
scope creep. Example: in the Boat Race gridworld an agent oscillates on two reward tiles to
farm directional reward without ever completing the lap [arXiv:2606.15385].

## Appendix B. The highlighted priority set

Twenty-six modes are flagged as the priority set, the ones most load-bearing for an integrity
auditor in practice: Confabulation, Hallucination, Source-monitoring error, Anchoring,
Confirmation bias, Overconfidence, Cognitive load, Cherry-picking, Belief bias, Conformity
(Asch), Obedience to authority, Sycophancy, Capitulation, Source fabrication, Prompt injection,
Scope creep, Reward hacking, Automation bias, Silent error swallowing, Side-effect blindness,
Anthropomorphism, Survivorship bias, Noble cause corruption, Deceptive alignment, Scheming and
power-seeking, and Strategic deception.

The complete catalogue of all 207 modes, each with its definition, graph edges, worked
examples, and per-mode citations, is in the released file (`ontology/ethical-ai.yaml`, schema
in `ontology/SCHEMA.md`) and browsable on the project site.
