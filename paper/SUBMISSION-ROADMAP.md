# EthicalAI resource paper: staged improvement roadmap to submission-ready

One concrete improvement per stage. Each stage: improve one thing in
`paper/ethicalai-benchmark.md`, validate (zero em/en dashes, every verified number still
reconciles with the source files, `build-paper-page.py` runs clean), commit referencing #12,
mark the stage done here with a one-line note, and report what improved. Honesty guardrails on
every stage: no fabricated citation, no over-claim beyond one project's artifact, no SOTA claim,
model aliases only, preserve the honest scoping.

Target venue: a workshop or arXiv preprint on AI safety / evaluation / research integrity.

## Stages

- [x] **S1 Citation integrity sweep.** DONE (v1.5). All 12 references resolved to real papers on
  arXiv: titles, authors and years confirmed; fixed Agrawal's author list (added Suzgun); confirmed
  Spracklen's 2025 is the USENIX venue year, not an arXiv-year error. Added a §8 note that every
  reference was resolved to its source before inclusion.
- [x] **S2 Strengthen the headline result.** DONE (v1.6). Ran the probe with deepseek-chat: it
  never declined (0/45, vs gpt-4o's 85%) and fabricated 7 of 8 verified suggestions, reusing one
  arXiv id across unrelated modes and echoing the prompt's example id. Two opposite failure styles
  (over-cautious vs over-confident), same unreliable result. Updated the abstract, the Section 3
  probe paragraph, and experiments/llm-citation-probe.md with both models.
- [x] **S3 Add a figure.** DONE (v1.7). Figure 1: an inline SVG bar chart of the five-class
  citation-failure distribution (surface-match 14 dominates down to wrong-population 2), injected
  after the Section 3.1 table with a caption and an in-text reference. Counts match the table.
- [x] **S4 Adversarial council pass.** DONE (v1.8). Four reviewers: peer MINOR REVISION (up from
  major, all 4 prior blockers resolved), methods (every number reconciles), ai-writing 2/10,
  groundedness BLOCK. Applied: re-grounded the probe to saved data (gpt-4o 40/45 declined, 5/5
  fabricated; deepseek 7 of 8), committed both per-prompt jsonls; moved Figure 1 into the markdown
  source; consolidated the repeated scope disclaimer to abstract + Limitations; cut the Section 3
  meta-announcement; reframed the surface-match/machine link as a contrast; fixed the 29-vs-35 seam.
  Rejected one groundedness flag after checking: 1,175/1,036 is correct at the pinned commit 3b9b500
  (the reviewer counted current HEAD). Writing polish (three-tools list, X-not-Y density) deferred to S5.
- [x] **S5 Abstract, title, and length.** DONE (v1.9). Differentiated the conclusion from the
  abstract (removed the verbatim finding restatement; it now ends on the forward-looking rule plus
  the machine contrast); pinned the OWASP living-document citation with an accessed date. Length
  5,219 words, fits a workshop/preprint; title already signals the finding.
- [ ] **S6 Submission artifact.** Produce a LaTeX/PDF build (pandoc) that is arXiv/workshop ready;
  check it renders and carries the references.
- [ ] **S7 Independent error-label re-audit (human-gated).** The one item an agent cannot fully
  supply: a second human rater on the hard-vs-minor error labels for a random subsample, reported
  as inter-rater agreement. Interim: a clearly-labelled model-based second-rater proxy, with the
  human step marked pending.

## Done log

(stages move here as completed, newest first)
