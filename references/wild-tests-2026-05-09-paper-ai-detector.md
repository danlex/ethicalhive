---
name: 2026-05-09 in-the-wild tests — paper-ai-detector v1.1 against real arxiv papers
description: Sanity-check of paper-ai-detector v1.1 against three published arxiv papers across CS and biomedical domains. Companion to research-2026-05-09-paper-ai-detection-literature.md and the synthetic test corpus in that note.
---

After v1.1 of `paper-ai-detector` shipped (commit `fec8414`, closes #8), the synthetic test corpus had three results — T1: 9/10 AI-templated, T2: 1/10 human-written, T3: 7/10 mid-templated. This note records a separate in-the-wild test against three real published abstracts to confirm the detector behaves sensibly on content it was not designed against. Issue tracking: #9.

## Test selection

Three papers, abstract-only inputs (full bibliographies were not pulled — the Citation Audit was correctly marked **skipped** in each report). Domain mix: CS / ML and biomedical.

| # | Source | Domain | Why selected |
|---|---|---|---|
| W1 | [arXiv:2406.07016](https://arxiv.org/abs/2406.07016) — Kobak et al., *"Delving into LLM-assisted writing in biomedical publications through excess vocabulary"* (Science Advances 2025) | Biomedical | Recursive interest — paper itself studies AI signatures in biomedical abstracts. We cite it heavily in our v1.1 lexicon. Does the detector flag it? |
| W2 | [arXiv:2401.12070](https://arxiv.org/abs/2401.12070) — Hans et al., *"Spotting LLMs With Binoculars"* (ICML 2024) | CS / ML | Peer-reviewed top-venue paper; if the detector behaves well, it should pass with mild flags only. |
| W3 | [arXiv:2503.15772](https://arxiv.org/abs/2503.15772) — Rao et al., *"Detecting LLM-Written Peer Reviews"* (2025) | CS / ML | Recent 2025 paper on a similar topic. Tests the detector's ability to spot the "LLM-assisted draft" pattern in genuine peer-reviewed work. |

## Results

| # | Pattern Score | Patterns flagged | Citation Audit | Detector's read |
|---|---|---|---|---|
| **W1** Kobak | **3 / 10** | 3: partial generic opener, marketing residue ("unprecedented"), formulaic framing ("we present") | skipped | *"Careful, methodologically grounded academic prose."* Notably absent: filler hedges, cookie-cutter contributions, future-work boilerplate, none of the high-effect-size Kobak lexicon (*delves, showcasing, meticulous, intricate, pivotal, realm*). Sentence rhythm varies (interrogative, declarative, compound-declarative). |
| **W2** Binoculars | **4 / 10** | 3: filler-hedge opener, marketing residue cluster ("novel" + "state-of-the-art" in consecutive sentences), filler adverb / scope-assertion ("We comprehensively evaluate") | skipped | *"Competent, technically specific, and largely non-templated. None of these individually constitutes strong evidence of AI generation — in CS/arXiv prose, 'novel' and 'state-of-the-art' are long-standing native idioms... The score of 4 reflects mostly natural writing with isolated boilerplate phrases; it does not imply fabricated content."* |
| **W3** Rao | **4 / 10** | 5: generic abstract opener (×2), cookie-cutter contribution / marketing residue, padding / hedge-stacking (mild), repetitive methodology rhythm ("find" across three consecutive sentences) | skipped | *"Split character consistent with LLM-assisted drafting rather than full LLM generation. The first three sentences follow the canonical motivation template with high fidelity... The abstract recovers substantially in its technical middle: indirect prompt injection, font-based embedding, obfuscated prompts, family-wise error rate, Bonferroni correction, and hypothesis-test specificity are all named precisely and correctly, which argues against wholesale fabrication. The results block then regresses into unanchored qualitative language ('high success rates,' 'resilient to common reviewer defenses') while simultaneously repeating the verb 'find' across three consecutive sentences, a mechanical rhythm tell."* |

## Observations

**The detector behaves as designed in the wild.** All three scores fell in the 3–4 band, which the rubric characterizes as *"mostly natural with isolated formulaic elements"* / *"noticeable patterns; readers may sense templating"*. None of the three papers is flagged as AI-generated; all are correctly read as polished academic writing with the kind of register issues common to peer-reviewed venues.

**Domain calibration is working.** On the two CS/ML abstracts, the detector explicitly invoked the v1.1 calibration note that *"In this paper, we propose..."* and *"novel" / "state-of-the-art"* are native CS idiom predating ChatGPT. The patterns were flagged but not over-weighted; the verdict is in the right zone.

**The "LLM-assisted, not LLM-generated" diagnosis on W3 is the single most useful output.** The detector identified the specific shape — *"LLM scaffolding for motivation + human-authored technical core + LLM-flavored results summary"* — that is empirically the most common form of AI assistance in 2024–2026 peer-reviewed work (Liang et al., *Nature Human Behaviour* 2025; ICLR 2024 review estimate ~15.8%). This is the regime the v1.1 calibration was specifically built for and the detector handled it well.

**ESL fairness disclaimer fired on every report.** v1.1's calibration note included it automatically, even when the abstract gave no obvious ESL signal. That is the safer default given the Stanford 61% TOEFL FPR.

**Citation Audit being skipped on three of three abstracts is expected.** The arxiv abs pages do not surface bibliographies; the user-facing path is to upload the full PDF or paste the bibliography. Worth documenting in the README.

## Honest limitations

- **Abstract-only inputs cannot exercise the full v1.1 detector.** Methods, results, conclusion, and bibliography sections all have section-specific checks (operational-detail absence, conclusion-vs-abstract overlap, citation cluster batching) that don't fire on abstracts. Tests against full PDFs are the natural next step.
- **Three papers is not a benchmark.** This is a sanity check that the v1.1 rubric produces sensible reports on real prose. A proper benchmark would need a labeled corpus and is out of scope here.
- **No false-negative case in the wild test.** All three papers are likely human-authored or human-edited. We do not have an in-the-wild AI-generated published paper to test against in this set; the synthetic T1 case is the closest proxy.

## Conclusion

The v1.1 calibration is robust enough to produce nuanced, defensible reports on real published work. No blocking false positives observed. The "LLM-assisted draft" diagnosis on W3 is the cleanest demonstration of the rubric's intended use case in real peer-reviewed content.
