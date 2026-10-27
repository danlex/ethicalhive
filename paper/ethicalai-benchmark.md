# EthicalAI Benchmark: A Grounded Ontology of AI Integrity Failure Modes, and What Grounding It Revealed

Alexandru DAN

Status: working draft. Companion resource to the clause-grounded advisory auditing
paper (`paper/draft.md`). Not for submission without a full verification sweep.

## Abstract

This paper presents an ontology of 207 ways an AI system can fail at integrity. Each
mode is defined in plain language, placed in a relation graph, cross-walked to existing
safety frameworks, and, where the evidence allows, illustrated with three worked
examples taken from a paper we read rather than cited at second hand. A hundred and
eighty-six of the 207 modes are grounded this way; the rest are documented as having
no supporting paper that we could find.

Building the resource produced two results that stand on their own. First, grounding
by reading rather than by trusting the reference caught a non-trivial rate of citation
drift: of the roughly fifty cited papers we checked while grounding, twenty-nine did
not support the mode they were attached to and were replaced with a paper that does.
Second, an adversarial re-check of a fifty-mode sample found that even our own
grounding, done by reading the source, mis-stated a specific figure in about eighteen
percent of modes. Both numbers are small-sample and we report them as such, but they
quantify a failure that is usually left implicit: plausible but wrong provenance
accumulates even in good faith, and reading the source does not by itself guarantee the
number is right. We make no state-of-the-art claim. The contribution is a documented,
provenance-checked resource and an honest measurement of its own reliability.

## 1. Introduction

A confident answer and a correct answer look identical from the outside. The space
between them is where integrity failures live, and that space is wide: a model can
hallucinate, flatter the user into a wrong answer, drop a constraint halfway through a
long task, or quietly bend a rule for what it decides is a good cause. These are not
one failure but many, and they have been studied unevenly, under inconsistent names,
across cognitive science, machine learning, and AI safety.

This paper describes a resource that tries to name them in one place and tie each name
to evidence. It is the shared artifact behind a companion method paper on clause-grounded
advisory auditing, where a subset of these modes becomes the clauses of a contract between
a human and an agent. Here we focus on the taxonomy itself: how it is structured, how it
was grounded, and what the grounding process revealed about the reliability of citations
in a field that moves fast.

The framing we take from the companion work is that integrity is a property of a
relationship, not of a model in isolation. A human and an agent agree, implicitly or
explicitly, on a set of obligations; a failure mode is a way the agent breaks one of
them. Organising the taxonomy around that relationship, rather than around model
internals, keeps it readable to the person who has to decide what to do when a flag is
raised.

## 2. The ontology

### 2.1 Two tiers

Every mode carries exactly one of two labels. A human-paralleled mode names a construct
from human psychology and its machine analogue: anchoring, confirmation bias, the
illusory-truth effect, cognitive dissonance. These sit in ten groups organised loosely
by brain system. An AI-native mode is a failure with no genuine human analogue, tied to
the machine substrate: prompt injection, reward tampering, data contamination, emergent
misalignment, backdoor triggers, denial-of-wallet consumption. A validator rejects any
mode that claims neither label or both, which keeps the boundary disciplined and forces
a judgment on each addition. Of the 207 modes, 168 are human-paralleled and 39 are
AI-native.

### 2.2 The relation graph

Modes are not a flat list. Each carries a `violates` edge to one of a small set of
principles (honesty, non-maleficence, transparency, scope-fidelity, independence,
corrigibility, calibration) and a `causes` edge to a harm (wrong answer, wasted effort,
manipulation, security breach, loss of oversight). Most carry `relates_to` clusters that
link adjacent modes, and many carry `is_a`, `opposite_of`, `root_of`, and `same_as`
edges. The point of the graph is mechanical: overlaps and gaps can be found by walking
edges rather than by eye, and a reader who lands on one mode can navigate to its
neighbours, its causal roots, and its opposites.

### 2.3 Crosswalks

To avoid reinventing existing taxonomies, modes carry a `maps_to` edge to four external
frameworks where there is a correspondence: the OWASP Top 10 for LLM Applications
[OWASP 2025], a multi-agent failure taxonomy [arXiv:2503.13657], an in-context scheming
study [arXiv:2412.04984], and a hallucination survey [arXiv:2510.06265]. The crosswalk is
partial by design; it records where this ontology
and an external framework describe the same thing, so the resource composes with prior
work rather than competing with it.

### 2.4 Grounding by reading

Most catalogues of failure modes stop at a definition and an illustrative scenario. This
resource asks for more: each mode should carry three worked examples, and each example
should come from a paper we actually read, tagged inline with that paper's arXiv identifier. An
example that is a plausible scenario rather than a reported finding is kept, but marked
as illustrative and left untagged, so a reader can tell a measured case from a
hypothetical one.

The procedure was deliberately literal. For a mode, we fetched the cited paper's full
text, found the specific finding, and wrote the example around the actual numbers,
model names, and setups the paper reported. Where a mode had no cited paper, we searched
for one, read it, and grounded the mode only if the paper genuinely demonstrated the
behaviour. Where no such paper existed, the mode was left ungrounded and the absence was
recorded. This reading-first discipline is what produced the two results below. It is
also expensive, which is why 186 of 207 modes are grounded rather than all of them.

## 3. What grounding revealed

### 3.1 Citation drift

The resource began with citations attached to many modes by keyword match: a paper whose
title contained the name of the behaviour. Reading those papers rather than trusting the
titles showed that keyword match is unreliable. Of roughly fifty cited papers we checked
while grounding, twenty-nine did not support the mode they were attached to. The failures
came in recognisable kinds.

Some citations were simply about a different subject. A mode about a model over-trusting
its own output cited a watermarking method; a mode about the model's own sense of agency
cited a study of the human user's perceived control. Some drew the opposite conclusion:
a mode about a model faking introspection cited a paper arguing that model self-reports
can be faithful; a mode about pragmatic over-accommodation cited a paper showing that
models under-use pragmatic inference. A smaller set were null results dressed as support:
a mode about the sunk-cost fallacy cited a paper that tested it and found it essentially
absent in current models, and a mode about status-quo bias cited a benchmark that found
models leaning the opposite way, toward change.

Each mismatch was either repaired by finding and reading a paper that genuinely supports
the mode, or, where no such paper exists, recorded as a held mode with the reason stated.
Every one of these decisions is logged in a running citation audit, which doubles as the
worklist and as the evidence for the rate reported here.

The reading is simple and uncomfortable. In a resource that advertises itself as grounded,
citations that look right but do not hold accumulate even when everyone is acting in good
faith, and only reading the source catches them. This is the same failure mode the
ontology itself catalogues, source fabrication, observed in the artifact that catalogues
it.

### 3.2 A verification sweep on the grounding

Catching bad citations is necessary but not sufficient. Having the right paper in hand
does not guarantee that the figure written into the example is the figure the paper
reports. To measure that, we ran an adversarial verification pass over all 186 grounded modes,
across four independent batches. For each mode, an independent checker re-read the cited
paper and confirmed, claim by claim, whether the specific numbers, model names, and setups
in the example actually appeared in it, with instructions to mark a claim as not found
rather than give it the benefit of the doubt.

The sweep found that twenty-six of the 186 modes (fourteen percent) contained a hard error:
a figure that the paper contradicted or that did not appear in it at all. A further
forty-two (twenty-three percent) contained a minor issue: a number loosely rounded, an
attribution that credited the wrong paper, or a finding placed on the wrong experimental
condition. None of the papers was unreachable.

The errors were instructive in their shape. In almost every flagged case the behaviour was
real and the paper was the right one; what drifted was a specific number, model name, or
causal framing. A wrong city in a hallucination example (the paper's case used one city, the
example another); a compliance rate reported as twelve percent where the paper said fourteen;
a conditional accuracy written as zero where the paper reported 2.6 percent; a reward figure
whose observed and hidden labels were reversed; a ratio reported on the wrong scale. In two
cases a quoted example did not appear in the cited paper at all and was rewritten to the
paper's actual content or demoted to an untagged illustration. These are transcription-level
over-reads, not invented findings, but they are exactly the errors a reader would never catch
without re-reading the source, and they would quietly undermine a resource that invites
citation. All sixty-eight flagged modes were corrected in the same pass.

Because the sweep now covers every grounded mode, these are population figures for this
artifact, not a sampled estimate. The hard-error rate held roughly steady across the four
batches (eighteen, fifteen, seven, and eighteen percent), so it is a property of single-pass
grounding rather than an artifact of any one sample.

### 3.3 Why the two findings matter together

The citation audit measures how often the wrong paper is attached to a claim. The
verification sweep measures how often the right paper is misquoted. They are the same
problem at two levels, and together they put a number on something usually left to trust:
provenance in a fast-moving field degrades at both levels, and the only remedy that worked
was reading, twice.

## 4. A note on the probes

Alongside the taxonomy we ran a small set of behavioural probes on current frontier model
tiers (the Opus, Sonnet, and Haiku families), reusing classic integrity tests such as
abstention on unanswerable questions and reversal of a correct answer under user pushback.
On the clear-cut versions of these tests the current tiers pass outright: they abstain when
they should and hold a correct answer when pushed. These runs are small and preliminary, a
single blind run of a handful of clear-fact items per probe, so they are a floor result,
not a leaderboard, and we report them only to set expectations rather than as a measured
behavioural finding. With that caveat, the honest reading is not that these models are safe
but that the measurable boundary has moved. The failures that remain live in ambiguous
cases and under stronger pressure, which is where a useful probe now has to aim: the easy
integrity probes floor, and a benchmark built on them would report a ceiling that says
little about deployment behaviour.

## 5. Relationship to clause-grounded auditing

The companion method paper takes a subset of these modes, writes each as a natural-language
obligation with a stable rule identifier in the style of RFC 2119 [Bradner 1997], and
assigns each a per-clause auditor. The claim there is narrow and testable: a named clause
yields advisory findings that are clause-traceable and more specific than free-form review
at equal recall, with the human as the final decision maker. This resource is the taxonomy
that method draws its clauses from, and the grounding here is what lets a clause point at
evidence rather than at an assertion. The two papers share an artifact; this one documents
the artifact and its reliability, and the other evaluates a method built on top of it.

## 6. Limitations

This is a resource, not a result about model capability.

The grounding is single-reader. Each example was written by one pass over one paper. The
verification sweep is a single adversarial re-read per mode: it covers every grounded mode
but is not a multi-reader consensus, so the fourteen-percent hard-error rate is a floor on
the true drift rather than a tight estimate of it.

Twenty-one modes are ungrounded. They fall into honest categories, all recorded: behaviours
that current models tested and did not show (sunk-cost fallacy, moral licensing); analogies
for which no model-side paper exists (attentional blink, just-world bias, scope
insensitivity); and neuroscience framings that overlap already-grounded modes without a
distinct instance. We did not force a citation onto any of them, because doing so would be
the source-fabrication failure the resource is built to name.

The taxonomy's boundary is a judgment. The two-tier rule is enforced mechanically, but which
side a mode falls on, and whether two modes are distinct or one, is a human call, and
reasonable people would draw some of those lines differently.

Finally, the resource makes no claim to completeness or to state of the art. Stronger
methods exist for specific failures, in particular sampling-based and hidden-state
approaches for hallucination. The value here is breadth, provenance, and a measured account
of its own error rate; it does not make claims about detection performance.

## 7. Conclusion

We built a grounded ontology of 207 AI integrity failure modes and, in grounding it,
measured two things that are usually assumed away: how often a cited paper fails to support
the claim attached to it, and how often a claim grounded by reading still misquotes the
source. Both rates were non-trivial and both are now corrected and documented rather than
latent. We hope the resource is useful as a shared map, and we offer the two findings as a
small cautionary result about how provenance decays in a field that cites faster than it
reads. The most honest thing the project did was audit its own grounding and report what it
found.

## References

- Bradner, S. (1997). Key words for use in RFCs to Indicate Requirement Levels. RFC 2119,
  Internet Engineering Task Force.
- OWASP (2025). OWASP Top 10 for Large Language Model Applications, 2025 release.
  https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Multi-agent failure taxonomy. arXiv:2503.13657.
- In-context scheming in frontier models. arXiv:2412.04984.
- A survey of hallucination in large language models. arXiv:2510.06265.
- Tversky, A., and Kahneman, D. (1974). Judgment under Uncertainty: Heuristics and Biases.
  Science, 185(4157).

A complete, machine-generated bibliography of every paper the ontology cites (several
hundred works) accompanies the resource and is the authoritative reference list; the three
entries above are the anchors the prose leans on directly. Per-mode citations and the
running citation audit record which paper grounds which mode and which citations were
repaired.
