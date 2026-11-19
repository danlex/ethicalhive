# Self-Improvement Memory for the paper-improvement loop

A small, faithful instance of Self-Improvement Memory (SIM) from Yu et al., "Self-Improvement
Memory Enables Continual Recursive Self-Improvement", arXiv:2611.18856 (submitted 13 Nov 2026),
applied to this repository's staged paper-improvement loop.

Why: the loop is continual recursive self-improvement on the paper. Across rounds the AI-slop
score bounced 2 -> 3 -> 4 -> 2 -> 4 -> 2, because each new round (an agent-orchestra rewrite, a
section restructure, a principles framing) reintroduced a pattern an earlier round had already
fixed. That is the CRSI failure the paper names: continuing without a record of *why* an edit
was made and *whether it worked* re-solves the same class of problem.

SIM is memory for the optimizer, not the artifact. The optimizer here is the loop deciding the
next edit; the artifact is `paper/ontology-paper.md` (renamed from ethicalai-benchmark.md on 2026-11-19; the benchmark paper is paper/benchmark-paper.md, renamed from draft.md). Before each round, read this file so a
pattern already known to cause slop is not reintroduced, and so a fix known to work is reused.
After each round, append the outcome. Entries are grouped by recurring problem; each records
rationale, predicted outcome, observed outcome, and evaluation context, per SIM.

## Recurring problem: defensive disclaimer cadence

The scope disclaimer ("one project's numbers on one artifact, not an error rate for AI research
at large") and the "X, not Y" construction recur at section boundaries.

- Rationale: honest scoping requires the caveat. Predicted: stating it lowers over-claim risk.
  Observed (v1.1): consolidated once, slop 2/10. Context: ai-writing judge.
- Observed (v1.4): the agent-orchestra restructure reintroduced per-section disclaimers, slop
  back to 4/10. Context: council re-review.
- Observed (v1.11): consolidated to abstract + Section 7, reworded the count-not-rate line out of
  "X not Y"; slop 2/10. Context: ai-writing judge re-run.
- LESSON: any structural edit (orchestra, section move, added framing) reintroduces this. Re-run
  the slop judge after any restructure, specifically for per-section disclaimer tails.

## Recurring problem: bolted-on framing / manifesto

A frame (audience signpost, contribution list, principles charter) added to one paragraph and
not used again reads as AI slop.

- Rationale (v1.12 first attempt): ground the paper in the Six Principles charter. Predicted:
  foundational framing. Observed: slop 4/10, "charter invoked once then dropped", plus a
  normative declaration ("requires an AI to...") in a descriptive paper. Context: paper-ai-detector.
- Observed (v1.12 fix): restated the principle as descriptive motivation, anchored the charter in
  Section 8 as well as the intro; resolved. Context: same judge.
- LESSON: a framing must appear in at least two places (motivation + artifacts/availability) and
  be descriptive, not normative. Name a principle as what the finding bears on, never as a
  requirement the design is said to fulfil.
- Observed (2026-11-19, benchmark paper): grounded paper/benchmark-paper.md in principles 5 and 6 applying
  this LESSON up front, descriptive ('answers to the accountability principle', 'serves the
  integrity-under-pressure principle') and anchored in two places (intro + Section 2). No 'requires
  an AI' normative declaration, numbers intact. The lesson prevented repeating the v1.12 4/10 slop.

## Recurring problem: contribution enumeration

"This paper delivers X, Y, Z" / "gives three things to reuse: the first... the second..." is the
canonical AI contribution list.

- Observed (v1.11): cut the "three things to reuse" list and "This paper delivers" sentence,
  folded the deliverables into prose. Slop dropped. Context: ai-writing judge.
- LESSON: do not reintroduce a numbered or "first/second/third" deliverable list, even reworded
  as "tools" or "things". Fold deliverables into the argument where each becomes relevant.

## Recurring problem: number reconciliation after edits

Edits can silently break a verified count, or a reviewer can count the wrong snapshot.

- Observed (S4): a groundedness reviewer flagged "1,175/1,036" as wrong; verification showed it
  is correct at the pinned commit 3b9b500, the reviewer had counted current HEAD (drifted after
  citation fixes). Did not change a correct number.
- Observed (S2, S4): the probe numbers were re-grounded to the saved run data (gpt-4o 40/45, 5/5;
  deepseek 7/8) after the n=20 pilot file was lost.
- LESSON: after any edit, re-run the reconciliation check against the SOURCE FILES and, for
  release counts, against the PINNED commit named in the sentence, not current HEAD.

## How the loop uses this

Each iteration: (1) read this file; (2) make the next edit without reintroducing a LESSON above;
(3) validate (numbers reconcile, zero dashes, build clean); (4) if a slop judge ran, append the
observed score and context to the relevant problem; (5) if a new recurring problem appears, add a
section for it. This is the SIM loop: group by recurring problem, record predicted vs observed,
reuse what worked.

- Observed (2026-11-19, benchmark paper align+de-slop): the benchmark paper was 4/10, same
  disclaimer cadence plus internal-reference leakage (a contracts/ethical-principles.md file path
  in the intro argument, a desk-reject tell). Fixed by applying the ontology lesson: the principle
  is the design rationale stated in plain terms, the charter file path stays out of the argument.
  Cut seven "X not Y" disclaimers to one scope statement, compressed the Section 3.2 metadata
  paragraph and the Section 3.1 unimplemented-components list into one-line pointers to Limitations,
  and added the reciprocal cross-reference naming the companion ontology paper.
- LESSON (cross-paper): a principle grounding must read as the design's own rationale in reader-
  evaluable terms; never cite an internal governance file path in the body of an external paper
  (keep it in availability/artifacts only). Keep the two companion papers aligned: one scope
  register, consistent "companion ... paper" naming, a reciprocal cross-reference each way.

- Observed (2026-11-19, benchmark citations): the slop judge flagged four 2025/2026 preprint
  citations for manual verification. Verified on the primary source: Cheng 2505.13995 (ELEPHANT),
  Paduraru 2603.18096 (Trace-Based Assurance), Zheng 2506.00714 (RFCAudit) all confirmed correct
  on arXiv. Fang AgentVerify (DOI 10.20944/preprints202604.1029.v1) resolves but the preprints.org
  page is bot-blocked (403), so the author name could not be re-read today; left as the prior
  primary-source correction, not changed (never rewrite a citation from a WebSearch summary). Added
  the ontology paper's "every reference resolved to its source" note to the benchmark paper, scoped
  to arXiv identifiers, for alignment.
