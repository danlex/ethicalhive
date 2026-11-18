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
- [ ] **S3 Add a figure.** A clean diagram of the five-class failure typology and/or the
  human-auditor-vs-model contrast, rendered in the paper page (SVG/HTML, self-contained).
- [ ] **S4 Adversarial council pass.** Re-run the multi-judge panel (peer / impact / methods /
  ai-writing / groundedness) on the revised paper; apply the convergent fixes; confirm no regression.
- [ ] **S5 Abstract, title, and length.** One more sharpening pass on the abstract and title;
  check the paper fits a reasonable workshop length; cut any remaining dilution.
- [ ] **S6 Submission artifact.** Produce a LaTeX/PDF build (pandoc) that is arXiv/workshop ready;
  check it renders and carries the references.
- [ ] **S7 Independent error-label re-audit (human-gated).** The one item an agent cannot fully
  supply: a second human rater on the hard-vs-minor error labels for a random subsample, reported
  as inter-rater agreement. Interim: a clearly-labelled model-based second-rater proxy, with the
  human step marked pending.

## Done log

(stages move here as completed, newest first)
