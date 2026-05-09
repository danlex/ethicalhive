---
name: 2026-05-09 research survey — AI text detection in academic papers
description: 2023-2026 literature on LLM-output detection in scholarly writing — section-specific signatures, citation hallucination rates, cross-domain differences, ESL false-positive risk, synthetic-results detection. Inputs to v1.1 of paper-ai-detector. Companion to research-2026-05-09-linkedin-ai-detection-literature.md.
---

Scope: 2023–2026 peer-reviewed and arxiv work on AI generation in academic content. Watermarking and classifier training excluded — out of scope for a rubric-based detector. Industry sources flagged as such.

## 1. Section-specific AI signatures

### Abstracts

- **Excess "style words" surge in 2023+ abstracts.** Kobak et al. analyzed 15M PubMed abstracts; 2024 excess words are 66% verbs and 18% adjectives (vs. COVID-era surges that were noun-heavy / content-driven). Highest frequency-ratios: *delves* (r=25.2), *showcasing* (r=9.2), *underscores* (r=9.1). Highest absolute deltas: *potential, findings, crucial, comprehensive, notably, particularly, intricate, meticulously, insights, exhibited, enhancing, within, additionally, across*. Lower-bound estimate: **13.5% of 2024 PubMed abstracts** are LLM-touched, up to **40%** in some subcorpora. *(arXiv:2406.07016, Science Advances 2025.)*
- **Cross-corpus extension to arXiv CS.** Liang et al. (Nature Human Behaviour 2025; arXiv:2404.01268) — CS papers reached **22.5% LLM-modified abstracts and 19.6% LLM-modified introductions by Sep 2024**. Math and Nature portfolio lagged at 4–9%. CS-specific markers: *realm, intricate, showcasing, pivotal*.

**For our detector:** the 2024+ verb/adjective skew is the strongest abstract-specific signal; treat the focal-word lexicon as domain-weighted (biomed and CS share *intricate*, *showcasing*; biomed adds *meticulous*, *delves*; CS adds *realm*, *pivotal*).

### Methods sections

- **Bigram-density signal.** xFakeSci (Hadi et al., *Sci. Rep.* 2024) — AI papers have **far fewer unique bigrams but those bigrams are over-connected** to the topic. Bigram-graph-density score: real abstracts ~0.16, AI abstracts ~0.27–0.30. Hits 94% accuracy on Alzheimer's and COVID datasets.
- **Sentence-length variance** is consistently lower in AI text (multiple sources, including *Connection Science* 2025).
- Pseudo-code formality and hyperparameter-listing patterns are **operator folklore** — no peer-reviewed isolation.

**For our detector:** existing item #4 ("Repetitive methodology rhythm") is grounded by xFakeSci's bigram density; the underlying mechanism is one published lever, not a robust multi-feature method. Be honest in the rubric.

### Results sections

- **Májovský et al. 2023** (PMC10267787): ChatGPT can produce fully fraudulent but coherent medical articles. Expert reviewers caught fakes mainly via **citation/reference inspection, not number patterns**.
- **Wiley AI screening pilot 2024** flagged 10–13% of submissions, partly via missing/anomalous statistical reporting.
- **Reproducibility-in-ML literature** (Semmelrock et al., *AI Magazine* 2025; arXiv:2406.14325) — real ML papers reliably include random seeds, hardware spec, GPU hours, library versions, data splits. **Systematic absence of these is a signal**, though not specifically an AI-tell.
- **No peer-reviewed paper specifically catalogs "round-number sample sizes" or "missing standard deviations" as AI-fabrication tells.** This is operator folklore (forensic-statistics tradition: GRIM test, SPRITE, statcheck) repurposed for the AI era. Use as heuristics but cite GRIM/SPRITE, not "AI detection literature."

**For our detector:** add an "operational-detail absence" sub-check under existing item #6. Flag absence of ≥3 of {GPU model+count, compute hours, random seed, library versions, dataset access, hyperparameter table} on papers claiming experimental results.

### Discussion / Future-Work / Conclusion

- **Sparse direct literature.** Liang's finding that LLM modification rates are higher for shorter papers and crowded research areas implies boilerplate discussion sections are the most common AI shortcut. Anecdotal sources (GPTZero, Pangram blogs) note AI conclusions paraphrase abstracts almost verbatim.

**For our detector:** existing item #8 (conclusion paraphrases abstract) is well-grounded. Replace qualitative "paraphrases" with a measurable threshold (normalized embedding cosine ≥ 0.85, OR chunked-Jaccard ≥ 0.4 if no embeddings). Currently subjective.

## 2. Citation hallucination / fabrication

### Empirical rates (2024-2026)

| Source | Result |
|---|---|
| **Chelli et al.** *JMIR Mental Health* 2025 (PMC12658395) | **19.9% of GPT-4o citations fabricated** across six simulated reviews; 46% on specialized topics |
| **Walters & Wilder** *Sci Rep* 2023 + 2024 follow-ups | GPT-3.5: **55% fabricated**; GPT-4: **18% fabricated**. Of *real* citations, GPT-3.5 **43%** and GPT-4 **24%** had substantive errors (wrong-attribution problem) |
| **GhostCite** arXiv:2602.06718 (2026) | 13 LLMs, 40 domains, 375K citations. Hallucination rates **14% (DeepSeek) to 95% (Hunyuan)**, mean 49.7% |
| **HalluCitation Matters** arXiv:2601.18724 (2026) | 300 hallucinated citations across ACL/NAACL/EMNLP papers; half from EMNLP 2025 |
| **GPTZero NeurIPS 2025 audit** | 100+ hallucinated citations across 53 papers from ~4,000 NeurIPS 2025 accepted |
| **Tay 2025 / *Nature* news 2026** | 80.9% increase in invalid citation rates in 2025 vs 2020-2024 baseline; 1.61% of papers in 2025 contain at least one invalid citation; **invalid citations cluster** — papers contaminate in batches |

### The wrong-attribution problem

The dominant form of hallucination on GPT-4-class output is **citation exists but doesn't say what's claimed** (Walters & Wilder). Detection requires retrieving the actual paper abstract and semantic-comparing the claim — currently subsumed under "fabricated citations" in our rubric but **qualitatively different and more common**.

### Detection heuristics beyond regex

- **GhostCite's CiteVerifier pipeline** — published SOTA. Parse → cascaded lookup (local cache → DBLP/Scholar → web search → LLM re-parse → Levenshtein title match θ=0.9).
- **Suspicious-DOI patterns** — bad-actor LLMs typically use real prefixes with fake suffixes; prefix-only checks miss most cases.
- **Plausible-but-fake author clusters** — LLMs stitch real surnames + plausible venue + plausible year, with title most fabricated (SPY Lab analysis).

**For our detector:**

1. **Distinguish wrong-attribution from fabrication** in the citation audit — they are different mechanisms with different verification needs.
2. **Citation-cluster batching:** if ≥2 citations fail title-match resolution, raise priors on all remaining and recommend full verification rather than sample.
3. **Title-match Levenshtein θ=0.9** against CrossRef/OpenAlex is a cheap automatic check worth wiring into the optional deep-verify path.
4. **Cap deep-verification at 10–15 citations** per audit to avoid runaway.

## 3. Cross-domain differences

### Hard data

- **Liang et al. 2025** (Nature Human Behaviour) — only large-scale cross-domain comparison: CS abstracts 22.5%, intros 19.6%; math 7.7%/4.1%; Nature 8.9%/9.4% by Sep 2024.
- **Kobak et al.** is biomedical-only (PubMed). 13.5% lower bound, 40% upper.
- **No SSRN-specific or humanities-specific** quantitative study found — clear gap.

### Domain-specific lexicons

- **Biomedical:** *delves, intricate, meticulously, underscores, showcasing, comprehensive, notably*
- **CS / arXiv:** *realm, intricate, showcasing, pivotal* — overlap with biomedical on *intricate, showcasing*
- **Humanities, legal, social-science:** no validated empirical lexicon. Conjecture only — likely *navigate, explore, complex tapestry, lens of, interrogate* — **not validated**.

### Field-specific norm differences

- **"We propose..." / "In this paper, we..."** are native to ML/CS abstract conventions and pre-date ChatGPT. Detector sensitivity must be **lower for CS**.
- **Nature-portfolio and clinical journals** historically use third-person passive ("In this study, X was investigated"); the same opener is more suspicious there.

**For our detector:** domain-aware sensitivity bands. Currently the rubric treats "In this paper, we propose..." as a uniform tell — it is not.

## 4. Non-native-English false-positive risk

- **Liang et al. 2023** (*Patterns*, arXiv:2304.02819) — 7 detectors classified **61.22% of TOEFL essays as AI**; 19% unanimously; 97% by at least one detector. Cause: perplexity/burstiness — non-native vocabulary range maps to "low perplexity = AI."
- **Pangram Labs** and **Originality.AI** claim newer detectors fix this; **no peer-reviewed cross-replication**.
- **Yu et al.** (arXiv:2502.19614, 2025) and **Rao et al.** (arXiv:2503.15772, 2025) — ICLR 2024 reviews ~15.8% AI-assisted; both note ESL-bias as an open concern but don't quantify it for academic prose specifically.
- **Vanderbilt, Curtin, NZ universities** disabled AI detection in high-stakes assessment as of 2024-25 partly on ESL-fairness grounds.

### Verdict

The 61% non-native FPR is **not directly replicated** for peer-reviewed academic writing — TOEFL essays are weaker than published academic prose. But the underlying mechanism (perplexity-as-AI-proxy penalizes restricted vocabulary) is **mechanistically the same**.

**For our detector:** keep an explicit ESL-disclaimer in the report. Down-weight perplexity-style flags ("uniform sentence length," "limited burstiness") on papers from non-native-English authors when that signal is available.

## 5. Synthetic experimental results detection

- **Májovský et al. 2023:** ChatGPT can produce fully fraudulent but coherent medical articles. Expert detection depends on cross-checking citations and missing operational detail, not the numbers themselves.
- **xFakeSci** (Hadi et al., *Sci. Rep.* 2024): bigram-graph density signal — strongest published method.
- **Reproducibility-in-ML** (Semmelrock et al., *AI Magazine* 2025): missing operational details (random seeds, hardware spec, library versions, hyperparameter tables) is a strong signal even though not specifically an AI-tell.

**For our detector:** add operational-detail-absence sub-check (see §1 Results).

## 6. Methodology-section AI cadence

Direct empirical literature is **thin**. xFakeSci's bigram-density signal is the closest peer-reviewed lever. Otherwise, mostly inferred from general burstiness/perplexity findings.

**For our detector:** existing item #4 is a heuristic with one published mechanism behind it (xFakeSci bigram density). Be honest about this in the rubric.

## 7. Patterns potentially missing from current 13-item taxonomy

Candidates to add or sharpen:

1. **Wrong-attribution citations** — different from pure fabrication; quantitatively dominant on GPT-4-class output (Walters & Wilder).
2. **Tortured phrases** (Cabanac et al., arXiv:2402.03370) — paraphrase-tool / translation-tool artifacts ("bosom peril" for breast cancer). Distinct mechanism from LLM stylistic markers; suggests paper-mill provenance.
3. **Operational-detail absence** in experimental sections (no GPU hours / no seed / no library version) — different from "synthetic results" because it's about *what's missing*, not what's present.
4. **Citation-cluster batching** — fabricated citations cluster; finding one should raise priors for others.
5. **Stylistic verb/adjective skew** — Kobak's specific finding that 2024 LLM excess words are 66% verbs and 18% adjectives.
6. **High-salience bigram ratio** — xFakeSci's signal; operationalizable as count of (topic-token, generic-academic-token) bigrams as a fraction.
7. **Sentence-length-variance collapse** in methods/results.
8. **Conclusion–abstract semantic similarity threshold** — make existing #8 measurable (cosine ≥ 0.85).
9. **Domain-aware lexicon weighting** — biomedical vs CS vs humanities differ.

### Likely overweighted in current 13

- **#13 Em dashes in formal sections.** *Washington Post* (April 2025), Sean Goedecke's analysis, and the OpenAI GPT-5.1 em-dash suppression (Nov 2025) all show this is **model-and-version-specific** (heavy in GPT-4o/4.1, near-zero in Claude/Gemini, suppressed in GPT-5.1+). Weak signal in 2026; many human writers use em dashes for decades. Keep but down-weight; mark as the lowest-confidence single-pattern flag.

## Test corpus results (2026-05-09 live runs on claude.ai with paper-ai-detector v1.0)

| Test | Source | Verdict | Notes |
|---|---|---|---|
| **T1** | Synthetic AI-templated abstract on anomaly detection (heavy banned-pattern usage; suspicious citations) | **9/10** | All expected tells caught: 2 generic openers, cookie-cutter contributions, 5× marketing residue, filler hedges, future-work boilerplate, padding, synthetic results (99.2% on `SYNTHETIC-1000`). Citation Audit: `[1] AICONF` and `[4] "Advanced Methods" / Journal of Computing Research` flagged for manual verification; Smith, J. concentration anomaly noted. |
| **T2** | Real human-written abstract on HTTP/3 over satellite (specific numbers, real RFC/SIGCOMM/IMC references, honest "we have not yet diagnosed" framing) | **1/10** | One mild em-dash flag noted as "used correctly and naturally as a resumptive dash, not as an AI fingerprint." All other validation items Pass. No false positives. |
| **T3** | Mid-templated — same factual content as T2 but with AI polish layered on (generic opener, cookie-cutter contributions, "novel"/"state-of-the-art"/"groundbreaking", future-work boilerplate, 86% improvement claim) | **7/10** | Caught 8 patterns. Diagnosis specifically identified the *"real paper underlies an AI-drafted abstract"* pattern: the technical content is plausible but the framing language was suppressing it. |

Detector calibration is in the right zone: high catch rate on heavily templated content, near-zero false-positive rate on grounded human writing, mid-range scoring on partially edited content.

## Concrete proposed improvements (priority-ordered)

1. **Replace generic "filler hedges" / "vague abstraction" lexicon with the empirically-grounded Kobak/Liang excess-word lists.** Specifically: *delves, showcasing, underscores, intricate, meticulous, comprehensive, notably, particularly, realm, pivotal, crucial, findings, potential, insights, exhibited, enhancing, additionally, across, within*. Weight by published effect-size.
2. **Add domain-aware sensitivity bands.** CS/arXiv: tolerate "we propose"/"in this paper" openers (native idiom). Biomed/clinical: full strictness on Kobak vocabulary. Math: very low base rate. Humanities/SSRN: literature is silent — generic detector with caveat.
3. **Wire title-match citation verification** into the optional deep-verify path. Implement GhostCite approach: parse references → CrossRef + OpenAlex (DBLP for CS) → Levenshtein θ=0.9 on normalized title. Cap at 10–15 citations per audit.
4. **Add a "wrong-attribution" sub-check** distinct from "fabricated citation." Cite Walters & Wilder; Chelli et al.
5. **Add a "citation-cluster batching" rule.** If ≥2 citations fail title-match resolution, raise the prior on remaining citations. Cite GhostCite, Tay 2025.
6. **Add "operational-detail absence" as an explicit experimental-results sub-check.** Required-fields list: GPU model+count, compute hours, random seed(s), library versions, dataset access (URL/DOI), hyperparameter table. Flag if ≥3 absent. Cite Semmelrock et al. (*AI Magazine* 2025).
7. **Add "tortured phrases" as item #14.** Use Problematic Paper Screener phrase list as seed. Distinct mechanism (paraphrase/translation tool, paper-mill) from LLM stylistic markers. Cite Cabanac et al.
8. **Down-weight item #13 (em dashes)** with explicit version/model note. Cite Sean Goedecke and *Washington Post* April 2025.
9. **Strengthen ESL-fairness disclaimer in the report.** Cite Liang 2023.
10. **Add measurable threshold** for the conclusion-paraphrases-abstract check (normalized embedding cosine ≥ 0.85, or chunked-Jaccard ≥ 0.4 fallback).

## Honest gaps in the literature

- **No peer-reviewed humanities/SSRN study** for AI lexicon or pattern frequency. CS and biomed dominate the evidence base.
- **No direct cross-replication of Stanford 61% TOEFL FPR for full-length academic prose.** Mechanism is identical but published academic-prose ESL studies don't quantify equivalent rates.
- **"Round-number sample sizes" / "missing CIs" as AI tells** — operator folklore, not peer-reviewed. Use as heuristic with GRIM/SPRITE attribution rather than "AI detection literature."
- **Methodology-section AI cadence** — bigram density is the only published lever; pseudo-code and hyperparameter-listing patterns are anecdotal only.
- **Em-dash signal decay.** OpenAI GPT-5.1 (Nov 2025) suppressed em dashes; the signal is model-and-version-specific and declining.

## Sources

- Kobak et al., "Delving into LLM-assisted writing in biomedical publications through excess vocabulary," arXiv:2406.07016 (Science Advances 2025)
- Liang et al., "Quantifying large language model usage in scientific papers," Nature Human Behaviour 2025
- Liang et al., "Mapping the Increasing Use of LLMs in Scientific Papers," arXiv:2404.01268
- Hadi et al., "Detection of ChatGPT fake science with the xFakeSci learning algorithm," Sci. Rep. 2024
- GhostCite, arXiv:2602.06718 (2026)
- HalluCitation Matters, arXiv:2601.18724 (2026)
- Chelli et al., "Influence of Topic Familiarity and Prompt Specificity on Citation Fabrication," JMIR Mental Health 2025 (PMC12658395)
- Walters & Wilder, "Fabrication and Errors in Citations Generated by ChatGPT," Sci Rep 2023
- Liang et al., "GPT detectors are biased against non-native English writers," arXiv:2304.02819 (Patterns 2023)
- Yu et al., "Is Your Paper Being Reviewed by an LLM?" arXiv:2502.19614 (2025)
- Rao et al., "Detecting LLM-Written Peer Reviews," arXiv:2503.15772 (2025)
- Aaron Tay, "Why Ghost References Still Haunt Us in 2025"
- *Nature* news 2026, "Hallucinated citations are polluting the scientific literature"
- GPTZero NeurIPS 2025 hallucination audit
- Cabanac et al., "Detection of tortured phrases in scientific literature," arXiv:2402.03370
- Semmelrock et al., "Reproducibility in machine-learning-based research," AI Magazine 2025 (arXiv:2406.14325)
- Májovský et al., "AI Can Generate Fraudulent but Authentic-Looking Scientific Articles," 2023 (PMC10267787)
- Pangram Labs, "Why Perplexity and Burstiness Fail to Detect AI"
- Sean Goedecke, "Why do AI models use so many em-dashes?"
- *Washington Post*, "AI writing tell — the em dash" April 2025
- Berkeley D-Lab, "AI Detection for Non-Native English Speakers"
- Richardson et al., "Revealing the Paper Mill Iceberg," bioRxiv 2025.08.29.673016
- SPY Lab, "Trends in LLM-Generated Citations on arXiv"
