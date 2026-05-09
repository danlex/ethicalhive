---
name: 2026-05-09 research survey — AI text detection for LinkedIn-style short-form writing
description: 2024-2026 literature on LLM-output stylometric and lexical markers, with emphasis on what is defensible for a rubric-based detector targeting LinkedIn / blog / web content. Inputs to v1.1 of linkedin-ai-detector.
---

Scope: peer-reviewed and arxiv work from 2023–2026 on stylometric, lexical, and rhetorical markers of LLM output. Watermarking and classifier-training research excluded — out of scope for a rubric-based detector. Unverified industry sources flagged as such.

## 1. Stylometric markers

- **Human writing is more variable on almost every measurable axis.** Tang et al. (arXiv:2412.03025, Dec 2024) — interpretable-feature classifier hits 87% on cross-corpus binary detection. Humans win on lexical diversity, proper-noun rate, emotional range; LLMs win on syntactic depth, subordinating-conjunction count, Coleman-Liau readability.
- **Sentence-length variance is consistently lower in LLM text.** Muñoz-Ortiz, Gómez-Rodríguez & Vilares (arXiv:2308.09067, Springer 2024) — "humans have more scattered sentence length distributions, more variety of vocabulary, distinct use of dependency and constituent types".
- **Stylometry works on short text, with some degradation.** Przystalski et al. (arXiv:2507.00838, Expert Systems 2025) — 79–100% accuracy via phrase patterns, POS bigrams, function-word unigrams in short samples. Kumarage et al. (arXiv:2303.03697, 2023) showed stylometric features add value beyond pretrained-classifier baselines on tweets.
- **Burstiness and perplexity are weak alone and collapse under paraphrasing.** Cheng et al. (arXiv:2506.07001, NeurIPS 2025) — adversarial paraphrasing reduces TPR by mean 87.88% across detector types. Pangram Labs analysis: perplexity-based detectors misclassify the Declaration of Independence as AI; ~61% FPR on non-native English (matches Stanford finding).
- **Detector landscape (upper-bound references, not competitors):** Fast-DetectGPT (Bao et al., ICLR 2024), Ghostbuster (Verma et al., NAACL 2024), Binoculars (Hans et al., ICML 2024), PHD intrinsic-dimension (Tulchinskii et al., NeurIPS 2023). None is rubric-based; none specifically targets LinkedIn.

**Implication for our detector:** keep "uniform paragraph rhythm" (well-grounded). Don't lean on perplexity/burstiness — they're paraphrase-fragile and biased. Rhetorical-pattern checks are more durable.

## 2. Phrase-level signatures

- **Quantified excess-vocabulary list.** Kobak et al. (arXiv:2406.07016, Science Advances 2025) — analyzed 15M PubMed abstracts 2010–2024; estimate ≥13.5% of 2024 abstracts LLM-processed (40% in some subcorpora).
- **Specific overused-word rankings with effect sizes.** Juzek & Ward (arXiv:2412.11385, COLING 2025) — 21 "focal words" overused by ChatGPT-3.5 in scientific abstracts (2020 → 2024 occurrences-per-million):

| Word | 2020 opm | 2024 opm | Increase |
|---|---|---|---|
| delves | 0.21 | 14.38 | **+6,697%** |
| surpassing | 1.37 | 10.50 | +667% |
| intricate | 6.22 | 44.22 | +611% |
| underscore | 7.42 | 36.40 | +391% |
| advancements | 12.49 | 47.17 | +278% |

  Plus: showcasing, boasts, garnered, emphasizing, realm, groundbreaking, aligns, comprehending, intricacies, surpasses, underscores, showcases, underscoring, delve, delved, delving, tapestry, unlocking, meticulous, commendable.

- **"Delve" specifically is now culturally marked.** Juzek & Ward 201-participant survey: wariness toward "delve" in opening sentences but inconsistent reactions to other focal words — "delve" has crossed into common-knowledge AI-tell status.
- **Stylistic-token shift, not content shift.** Lin et al. (arXiv:2312.01552) — alignment training shifts stylistic / discourse tokens (transitional phrases like "However", "Moreover", "In conclusion", "Remember") rather than content tokens.
- **Lexicon is decaying.** Liang et al. (Nature Human Behaviour 2025; arXiv:2502.09606, arXiv:2504.12317) — "intricate" and "delve" frequencies began *decreasing* after March-April 2024 once they became publicly known AI tells.

**Implication for our detector:** the focal-word list is the strongest empirical anchor available. Add a weighted lexicon hit-rate check. Make the list data-loadable (lexicon decays in 6–12 months).

## 3. The em dash question

- **Em dash use spiked in AI output.** GPT-4o uses ~10× more em dashes than GPT-3.5; GPT-4.1 more still. Claude, Gemini, Meta.ai use them sparingly.
- **Quantified shift in published text post-ChatGPT.** Em-dash relative frequency in English-language ecology abstracts more than doubled 2021 → 2025; no comparable change for any other character. (*pieceofk.fr* 2025 — corpus analysis, not peer-reviewed.)
- **Em dash is long-standing in professional journalism.** NYT, Atlantic, Washington Post house styles use em dashes liberally. ChatGPT trained on Pulitzer-nominee corpora.

**Implication for our detector:** treat em dash as a **density** check, not presence. Threshold: >1 per 75 words OR ≥3 in a post under 250 words. Single em dash should never flag alone. Note model-aware skew: GPT-4o/4.1/Copilot/Deepseek run high; Claude and Gemini do not.

## 4. LinkedIn / engagement-content specifics

- **LinkedIn skews majority AI on long-form posts.** Originality.AI estimate: 53.7% of long LinkedIn posts in 2025 are likely AI; AI posts receive 45% less engagement on average (industry, not peer-reviewed).
- **Three opening patterns dominate AI LinkedIn posts.** Vega Research 500-post sample: 411/500 (82%) use one of three opening templates. (Industry, not peer-reviewed.)
- **Cross-platform AI prevalence rising fast on text-first platforms.** Sun et al. (arXiv:2412.18148, ACL 2025) — Jan 2022 → Oct 2024: Medium AI rate 1.77 → 37.03%, Quora 2.06 → 38.95%, Reddit 1.31 → 2.45%.
- **"Standardized six-paragraph format" in LLM persuasion output.** Lapesa et al. (arXiv:2508.09614) — GPT-4o defaults to a six-paragraph rhetorical mold (intro/thesis, two supporting, two refuting, conclusion). LinkedIn "hook + 3-bullet body + slogan" is the same rhetorical-mold default at smaller scale.
- **"It is not X, it is Y" structure.** No peer-reviewed quantification of this pattern's frequency in human vs LLM corpora exists. Industry / rhetorical-analysis consensus is strong: Gorrie (deadlanguagesociety.com 2024) — antithesis abuse; tropes.fyi catalogs as "the single most commonly identified AI writing tell". **Honest gap:** strong qualitative support, no effect-size data.

## 5. False-positive risk

- **61.3% FPR on non-native English writers (Stanford).** Liang et al. (arXiv:2304.02819, *Patterns* 2023) — 7 detectors against TOEFL essays vs native English: native FPR ~3.2%, non-native 61.3%. At least 12 universities (Yale, Johns Hopkins) disabled AI detection software citing this bias.
- **OpenAI's own classifier retired for 9% FPR** (acknowledged July 2023).
- **Humans only 57–64% accurate at distinguishing AI from human writing** (multiple medical-essay and German-thesis studies, 2024–2025).
- **Short-passage degradation.** Pangram Labs published evaluation: even SOTA detectors degrade severely on <50-word passages. LinkedIn post length is in the danger zone.
- **Skilled human writers use the very devices we flag.** Em dash (journalists), tricolon (rhetoricians), antithesis ("not X but Y" appears throughout MLK, Churchill, Lincoln). Gorrie: "the problem is not that LLMs use these techniques: it's that they're so robotically consistent in how they use them."

**Implication for our detector:** penalize *combination/density*, not single instances. A LinkedIn post with one em dash and one tricolon is human; one with three em dashes, two tricolons, and a slogan closer in 200 words is AI. Length-gate the rubric below ~50 words.

## 6. Patterns the current taxonomy may be missing

The current 16-item taxonomy is well-aligned with the literature. Candidates worth considering:

- **6.1 Discourse-relation skew** — Kim et al. (arXiv:2402.10586, 2024) show LLM text overrepresents Background relations and underrepresents Joint and Temporal relations. Useful structural signature, harder to detect by rubric.
- **6.2 Hedging / epistemic markers** — Fewer "I think", "probably", "might" in LLM output unless prompted. Recent work on hedging (arXiv:2408.03319, 2024). **Add as "epistemic flatness"** — absence of personal-uncertainty markers in a post claiming personal experience is itself a tell.
- **6.3 Stylistic-token opening** — Lin et al. (arXiv:2312.01552): "However", "Moreover", "In conclusion", "It's important to note", "Remember" cluster at sentence starts. **Add as "discourse-marker opener density"**.
- **6.4 Six-paragraph / rhetorically-symmetrical structure** — Lapesa et al. (arXiv:2508.09614). Partially covered by "over-neat symmetry"; consider explicit "perfectly balanced argument structure" check.
- **6.5 Emotional flatness / narrowed affect range** — Tang et al. (arXiv:2412.03025): humans show much higher emotional variance, especially negative. LinkedIn posts with relentless positive affect are statistically AI-like. Partially covered by "marketing residue".
- **6.6 Tricolon density** — LLMs default to lists of three. Distinct from "list stacking" (bullet-based) and "over-neat symmetry" (full-post structure).

## Concrete proposed improvements (priority-ordered)

1. **Em-dash density, not presence.** Threshold: >1 per 75 words OR ≥3 in a post under 250 words. Note model-aware difference (GPT-4o high; Claude/Gemini low).
2. **Weighted focal-word lexicon hit-rate.** Use Juzek & Ward's 21 words plus Kobak excess-vocabulary list, weighted by published effect-size. Make data-loadable (decays in 6–12 months). "Delve" is near-deterministic.
3. **Discourse-marker opener check.** Sentence-initial "However", "Moreover", "Additionally", "In conclusion", "Furthermore", "It is important to note", "It's worth noting", "Remember". Density flag at >1 per 5 sentences.
4. **Combination-required scoring.** Require ≥2 distinct tell categories before flagging. Single-instance signals are unreliable per literature.
5. **Length-gate the rubric.** Below ~50 words, require ≥2 converging tells before any non-PASS verdict. SOTA detector behavior matches this.
6. **Negative-parallelism explicit detection.** Regex-detectable: `\bnot just\b.*\bbut\b`, `\bit's not\b.*\bit's\b`, `\bnot only\b.*\bbut also\b`, `\bnot a\b.*\bbut a\b`. Empirical effect-size data missing — flag as advisory until logged.
7. **Epistemic flatness check.** For posts claiming personal experience, count first-person uncertainty markers ("I think", "in my experience", "I'm not sure"). Absence in a 150+-word personal-claim post is suspicious.
8. **Tricolon density check.** Count list-of-three structures per 100 words. Flag at >1 per 100 words. Distinct from list-stacking.
9. **Narrowed affective range check.** Ratio of positive-valence to negative-valence emotion words. Flag posts with extreme positivity (>10:1) and zero negative content over 150+ words.
10. **Downweight non-native-English false-positive risks.** No lexical-density penalties. Generous interpretation of "uniform paragraph rhythm" on naturally short-paragraph styles.

## Honest gaps in the literature

- **No peer-reviewed quantification** of "It is not X, it is Y" frequency in human vs LLM corpora. Industry consensus strong; empirical anchor weak.
- **No LinkedIn-specific peer-reviewed study.** Originality.AI and Vega Research numbers are industry, not peer-reviewed.
- **No published "hidden-author" experiment by name.** Closest equivalents are Stanford TOEFL study and short-passage commercial-detector benchmarks.
- **The lexicon is decaying.** Liang/Stanford work shows "delve" and "intricate" frequencies dropped after public awareness in 2024. Phrase-list approaches have ~6-12-month half-life.

## Sources

- Stylometry recognizes human and LLM-generated texts in short samples — arXiv:2507.00838
- Why Does ChatGPT "Delve" So Much? — arXiv:2412.11385 (COLING 2025)
- Delving into ChatGPT usage in academic writing through excess vocabulary — arXiv:2406.07016 (Science Advances 2025)
- Spotting LLMs With Binoculars — arXiv:2401.12070 (ICML 2024)
- Fast-DetectGPT — arXiv:2310.05130 (ICLR 2024)
- Ghostbuster — arXiv:2305.15047 (NAACL 2024)
- Intrinsic Dimension Estimation for Robust Detection of AI-Generated Texts — arXiv:2306.04723 (NeurIPS 2023)
- Human Variability vs. Machine Consistency — arXiv:2412.03025
- Contrasting Linguistic Patterns in Human and LLM-Generated News Text — arXiv:2308.09067 (Springer 2024)
- Stylometric Detection of AI-Generated Text in Twitter Timelines — arXiv:2303.03697
- Are We in the AI-Generated Text World Already? — arXiv:2412.18148 (ACL 2025)
- Threads of Subtlety: Detecting Machine-Generated Texts Through Discourse Motifs — arXiv:2402.10586
- GPT detectors are biased against non-native English writers — arXiv:2304.02819 (Patterns 2023)
- Adversarial Paraphrasing — arXiv:2506.07001 (NeurIPS 2025)
- Quantifying large language model usage in scientific papers — Nature Human Behaviour 2025
- Examining Linguistic Shifts in Academic Writing Before and After ChatGPT — arXiv:2505.12218
- How Persuasive Could LLMs Be? — arXiv:2508.09614
- Rethinking Alignment via Token Distribution Shift — arXiv:2312.01552
- Training LLMs to Recognize Hedges in Spontaneous Narratives — arXiv:2408.03319
- The Rise of the Em Dash in Ecology Abstracts — pieceofk.fr 2025 (corpus analysis, not peer-reviewed)
- Why do AI models use so many em-dashes? — Sean Goedecke (industry)
- 50%+ of LinkedIn Posts were Likely AI in 2025 — Originality.AI (industry)
- I Analyzed 500 AI-Generated LinkedIn Posts — Vega Research, dev.to (industry)
- Why ChatGPT writes like that — deadlanguagesociety.com (qualitative)
- Why Perplexity and Burstiness Fail to Detect AI — Pangram Labs (industry)
- AI Detectors Biased Against Non-Native English Writers — Stanford HAI
- Artificial Writing and Automated Detection — Becker Friedman Institute, U Chicago
