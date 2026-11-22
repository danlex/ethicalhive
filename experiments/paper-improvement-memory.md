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

- Observed (2026-11-19, consistency pass): both papers re-confirmed at 2/10 (human register). Two
  accuracy touches: the benchmark's cross-reference now uses the companion's EXACT full title
  (it had dropped the subtitle, the very citation-accuracy error the paper studies), and the
  ontology's one vague Limitations close ("those questions require separate evaluation") was
  replaced with the concrete requirement (externally sampled test set + independent annotators).
  No substantive content change; the papers are stable and submission-ready.

- Observed (2026-11-19, benchmark figure + survivorship plan): a surfaced plan to add
  "survivorship bias" to the catalogue was checked against the real files FIRST (SIM number
  lesson) and found already executed and live (row 26, papers 2609.15996 + 2105.14149, both
  verified real on arXiv today); re-executing would have duplicated and broken the validator.
  Did not re-run. Instead added genuine content aligning the two papers: Figure 1 for the
  benchmark paper (specificity by condition from Table 2, bars transcribed exactly, 'none' omitted
  as trivially specific), matching the ontology paper's Figure 1. Bars verified against the table
  (9/10/16/21/23/24 of 28).
- LESSON: before executing any surfaced/older plan, verify the target files' CURRENT state; a plan
  from an earlier session may already be done, and blind re-execution duplicates and breaks builds.

- Observed (2026-11-21, derived principles): added a two-layer principle structure to the ontology
  paper, per the author. The seven operational principles are DERIVED from the data (aggregating the
  per-record `violates` field), a verified clean partition of the 207 (each behaviour breaches exactly
  one; 67+45+31+25+15+14+10 = 207; 227 analogies not yet assigned). The six top-level charter
  principles are presented descriptively (names + ends), not as an 'An AI must' manifesto (slop lesson).
  Added Figure 1 (the seven-principle distribution, grounded), which also replaces the typology figure
  cut in the reframe. Bars verified against the data.

- Observed (2026-11-21, extend partition to 434): the author asked why the partition was over 207
  when there are 434. The 227 later analogies had an empty violates field (untested proposals).
  Per the author's choice, classified all 227 into one of the seven principles from their
  definitions (via a reader agent), applied with experiments/assign-violates.py (deterministic
  line-pass, no YAML reformatting), and verified the partition now closes at 434 (each record
  exactly one; honesty 112, calibration 100, non-maleficence 52, transparency 51, scope-fidelity
  50, independence 43, corrigibility 26; sum 434, zero missing). Paper Section 3.3 now shows the
  grounded(207)/proposed(227)/total(434) split and a stacked Figure 1; the 227 assignments are
  marked proposal-level, distinct from the grounded 207.

- Observed (2026-11-22, three improvements for ethical-AI researchers; author approved all three):
  (1) Measurability axis from the existing `measurability` field: of the grounded 207, 193 are
  measurable from a single draft, 3 need multi-turn (exactly deceptive alignment, scheming,
  strategic deception), 11 are undetectable from output (10/11 are self-and-agency transparency
  failures). Added as a third axis in Section 3.3 with a table. Pure data, no citations.
  (2) Positioned the six-principle charter + seven obligations against the AI-ethics principles
  literature: Jobin, Ienca and Vayena 2019 (five-principle convergence) and Floridi and Cowls 2019
  (five principles). The charter restates the convergence at the level of ends; the operational
  layer adds three obligations the guideline-era convergence does not name (calibration,
  independence, corrigibility, all about interaction/control). (3) Eval-coverage map as a new
  Section 4.5: eight behaviours mapped to named public benchmarks (TruthfulQA, HALoGEN, Spracklen,
  Sharma sycophancy, JailbreakBench, InjecAgent, CyberSecEval, Carlini extraction, Meinke scheming),
  then the honest gaps (reward hacking / goal misgen / emergent misalignment / reward-model
  overopt demonstrated but unbenchmarked; the 11 undetectable have no output measurement).
- VERIFIED every new citation on source before writing: Jobin + Floridi identity via Crossref
  (publisher pages gated), Jobin five-principle finding quoted from the arXiv abstract; all seven
  eval benchmarks via their arXiv abs pages (title + first author + what they measure).
- LESSON: an absence claim ("no standardized benchmark for X") still has to be made carefully.
  Meinke et al. 2024 in-context scheming covers oversight-subversion / goal-guarding / self-exfil,
  so those could NOT be listed as gaps. Narrowed the gap list to the specification-gaming family
  and hedged with "as far as we found" / "records the benchmarks we verified, not every benchmark".
  Overclaiming a gap is as wrong as overclaiming a result.
