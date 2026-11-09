# Paper council bias review — 2026-11-09

**Current disposition: PAPER-BIAS-JUDGE VERDICT: PASS after targeted round 3.**

No unresolved BLOCKERS or required clause fixes remain. Round 1's source-location BLOCK and overconfidence FLAG were corrected by the lead; the original findings remain below. OVR, SRC and SEL returned PASS in round 2 on the corrected pointer, literal micro-attribution counts and exploratory-p-value qualification. In round 3 the lead clarified only the filename-date provenance paragraph. Actual OVR and SRC judges checked that paragraph against every selected hard-suite manifest entry and returned PASS. This is not a new all-six or full-paper review of the third-round hash.

Current manuscript SHA256 values:

- `paper/draft.md`: `289a39e43f13f2d524ce3d80026058d100cfcc4a248dd04095880d44a99089fb`
- `paper/ethicalai-benchmark.md`: `74d3b26eef4ae0bae46fb01ad24e40ec1d999706edbf67cfcd14e0c58a77b946`

| Clause | Latest verdict | Latest review scope |
|---|---|---|
| INT-OVR | PASS | Round 3, changed provenance paragraph; other findings retain round-2 scope |
| INT-SEL | PASS | Round 2, complete methods paper and unchanged resource hash; other text unchanged |
| INT-SRC | PASS | Round 3, changed provenance paragraph; other findings retain round-2 scope |
| INT-CNF | PASS | Round 1, both complete manuscripts; relevant framing unchanged |
| INT-ANC | PASS | Round 1, both complete manuscripts; relevant framing unchanged |
| INT-SYC | PASS | Round 1, both complete manuscripts; relevant framing unchanged |

The PASS is limited to the clause reviews described here. Remaining advisory limits are the manuscripts' existing oracle routing, author labels, one alias and unknown historical settings, severity/evidence-authority failures, deterministic category sampling, selected incidents, historically reported checking and untested later analogies. No new experiments are required to state the bounded descriptive pilot; broader efficacy and validity claims remain unsupported. The manifest filename labels do not authenticate historical execution dates.

## Round 1: PAPER-BIAS-JUDGE VERDICT: BLOCK

Reviewed both complete revised manuscripts against the five mandatory primary sources, frozen November 9 pilot artifacts and the bibliographic-metadata check. The historical Athena report was treated as an issue history rather than the present verdict.

Frozen manuscript SHA256 values:

- `paper/draft.md`: `84fbb91a60588e1e6bcbafa142e330fabba67d4cf7366981089da631e126950e`
- `paper/ethicalai-benchmark.md`: `74d3b26eef4ae0bae46fb01ad24e40ec1d999706edbf67cfcd14e0c58a77b946`

All six actual clause judges ran. Seven total agent slots were available; the lead, composer and prose reviewer initially occupied three. Scheduling therefore used two bounded, overlapping waves: OVR, SEL, SRC and CNF first; ANC and SYC were dispatched as slots released. The six did not all run simultaneously. Each judge received the same manuscripts and evidence paths and records reading the five mandatory primary files before judging. No manuscript/code edits, commits or pushes were performed by this composer or these judges.

| Clause | Actual judge | Verdict |
|---|---|---|
| INT-OVR | overconfidence_judge | FLAG |
| INT-SEL | selective_evidence_judge | PASS |
| INT-SRC | source_fabrication_judge | BLOCK |
| INT-CNF | confirmation_bias_judge | PASS |
| INT-ANC | anchoring_judge | PASS |
| INT-SYC | sycophancy_judge | PASS |

The aggregate preserves the strictest source verdict. The one BLOCK and one FLAG concern the same localized evidence-location sentence. The source judge's required WRONG-TARGET mapping assigns BLOCK; that verdict is preserved despite the small correction. It does not say the reported interval values were fabricated.

### BLOCKERS — source finding verbatim

- INT-SRC-01; WRONG-TARGET; one localized documentation correction required.
  Location: paper/draft.md:181-182.
  Exact quote: "Counts and Wilson intervals in the generated summary keep these denominators visible."
  Evidence target: Section 3.2 identifies experiments/research-results-2026-11-09.json and experiments/research-results-2026-11-09.md as the generated numerical summaries. The Markdown artifact reports counts and paired tests; neither artifact contains Wilson intervals or confidence-interval fields. Searching both complete artifacts for wilson, confidence, interval, literal ci, and _ci fields returns no matches. The interval implementation exists separately at experiments/metrics.py:108, and the manuscript reports plausible intervals at paper/draft.md:205. The problem is the stated location of that evidence, not an assertion that the intervals themselves were invented.
  Paste-ready replacement: "The generated summary reports counts with their denominators."
  Severity justification: The sentence has no bracketed bibliography marker, but it explicitly attributes content to the generated summary, a named evidence artifact established in Section 3.2. That is a source pointer under INT-SRC-01. The judge's required verdict mapping is any WRONG-TARGET -> BLOCK. The remediation is a one-sentence correction, not a new experiment or a rewrite of the pilot conclusions.

### ADVISORY — source finding verbatim

1. [INT-OVR-01] Minor FLAG; partially supported artifact-description claim.
   Location: paper/draft.md:181, Section 5, metric definitions.
   Exact quote: "Counts and Wilson intervals in the generated summary keep these denominators visible."
   Evidence: experiments/research-results-2026-11-09.md contains the counts, attribution denominator explanation and paired tests. The corresponding JSON contains score, confusion, per-mode, paired-test and attribution fields; neither generated summary contains Wilson intervals. Searching both complete frozen summary files for "wilson" or "interval" returns no matches. The manuscript itself does report Wilson intervals in Section 5.1. Thus the substantive uncertainty reporting is present, but the compound assertion about what the generated summary supplies is only partially supported.
   Licensed wording: verified counts in the generated summary; inline intervals in the manuscript.
   Paste-ready replacement: "Counts in the generated summary keep these denominators visible."
   No new experiment is needed. This change removes the incorrect artifact-location assertion without weakening the verified pilot results.

### Optional source suggestion, not a violation — verbatim

Advisory, not a breach finding: The main text could make the extra-ID cost easier to inspect by replacing its existing sentence "The JSON supplement also reports micro precision and recall over emitted rule sets, penalizing extra identifiers." with "On true-positive hard cases, the named judge matches all 37 gold identifiers but emits 84 identifiers, giving exact-rule micro precision of 37/84 and recall of 37/37; the JSON supplement reports the corresponding set metrics for all conditions." This is optional because the present text already defines the minimal metric accurately and explicitly points to the reported penalizing metrics. It does not change the PASS verdict.

### Scope retained by this review

The six reports do not certify full-text support across 1,036 publication identifiers. The fresh citation check is bibliographic metadata only. They do not infer unrecorded model backends, settings or execution provenance. The bounded pilot retains oracle routing, author labels, one alias, unresolved severity/evidence-authority failures and inconclusive freeform comparison; no causal general-auditing or catalogue-wide efficacy result is certified. The historical 207-record snapshot and its evidence cohorts remain distinct from the current 434-record release and its 227 untested additions. Existing limitations do not require new experiments merely to report this bounded descriptive pilot.

## Round 1 complete clause reports, verbatim

### INT-OVR

```text
OVERCONFIDENCE-JUDGE REPORT
Clause: INT-OVR (Overconfidence)
Verdict: FLAG

Scope: Both complete revised manuscripts, paper/draft.md and paper/ethicalai-benchmark.md, reviewed against the current retained evidence. This is an INT-OVR review, not an independent replication or a full-text review of the 1,036 referenced identifiers.

Mandatory primary files consulted before judging: judges/overconfidence-judge.md; paper/proposal.md; references/prior-art.md; experiments/seed-selective-evidence.md; contracts/paper-writing-contract.md; contracts/ai-integrity-contract.md. Additional evidence consulted: experiments/research-results-2026-11-09.md and .json; experiments/research-runs-2026-11-09.json; references/manuscript-citation-check-2026-11-09.json. The latter explicitly records bibliographic-metadata-only access. The historical issue report was not used as the current verdict.

Findings requiring a change:

1. [INT-OVR-01] Minor FLAG; partially supported artifact-description claim.
   Location: paper/draft.md:181, Section 5, metric definitions.
   Exact quote: "Counts and Wilson intervals in the generated summary keep these denominators visible."
   Evidence: experiments/research-results-2026-11-09.md contains the counts, attribution denominator explanation and paired tests. The corresponding JSON contains score, confusion, per-mode, paired-test and attribution fields; neither generated summary contains Wilson intervals. Searching both complete frozen summary files for "wilson" or "interval" returns no matches. The manuscript itself does report Wilson intervals in Section 5.1. Thus the substantive uncertainty reporting is present, but the compound assertion about what the generated summary supplies is only partially supported.
   Licensed wording: verified counts in the generated summary; inline intervals in the manuscript.
   Paste-ready replacement: "Counts in the generated summary keep these denominators visible."
   No new experiment is needed. This change removes the incorrect artifact-location assertion without weakening the verified pilot results.

Licensed claims and remaining limits (not additional violations):

- [INT-OVR-01] paper/draft.md, Section 5.1: "The other audited conditions detect all 32 gold flags." LICENSED within the explicitly bounded hard-set comparison and exclusion of the immediately discussed unnamed control. Frozen hard-suite scores give 32/32 for freeform, checklist, mono-rid, judge-ctx and judge; judge-anon gives 31/32. The manuscript does not project these counts to an external population.
- [INT-OVR-01] paper/draft.md, Section 5.3: "Binary recall therefore conceals severity errors." LICENSED by the named judge confusion matrix: 47/60 exact verdicts despite 32/32 binary recall, with seven of eight gold REVISE cases predicted BLOCK and one gold BLOCK predicted REVISE.
- [INT-OVR-01] paper/draft.md, Section 5.1: "The freeform comparison is inconclusive at this sample size." LICENSED by ten versus three discordant clean cases and exact McNemar p = 0.09228515625. The paper explicitly rejects interpreting p = 1.000 for the anonymous control as equivalence evidence. It preserves known-target routing, one recorded alias and unavailable historical backend/settings as limitations.
- [INT-OVR-01] paper/ethicalai-benchmark.md, abstract: "The later 434-record release adds 227 untested analogies and a broader bibliography, which are outside those historical evaluation denominators." LICENSED as a versioned cohort distinction. The historical 207-record study and its 186-, 33- and 12-item procedures are not presented as evaluation of the later records. Historical snapshot 8798134341ea386da80fb5602bc7dd06ef81cf24 is separately identified from the later bibliography snapshot.
- [INT-OVR-01] paper/ethicalai-benchmark.md, Section 3.2: "author-judged harm associations, not estimated causal effects." LICENSED calibration of the graph's causes links. The text distinguishes an illustrative incident sequence from a graph-coded causal path and makes no estimated causal claim.
- [INT-OVR-02] No unlicensed catalogue-completeness, universal efficacy, novelty-priority, full-paper-reading or exhaustive-source-validation claim found in the revised manuscripts. Explicit scope restrictions are retained for bibliography availability, metadata access, model-based codebook agreement, author-selected incident mapping and the bounded pilot. This statement reports this clause review's finding, not proof of the catalogue's overall correctness.

Evidence checks performed: parsed both frozen JSON artifacts, checked the manifest's stored SHA256 against the current manifest file, and checked all 78 manifest-selected raw file hashes; all matched. These checks establish selection integrity for the retained outputs, not authenticity of historical model execution times or correctness of author labels. No model backend, temperature, seed, CLI version, token usage or latency was inferred.

No BLOCK finding. Required fix: the single sentence replacement above. No manuscript/code edits, commits or pushes performed by this judge.
```

### INT-SEL

```text
SELECTIVE-EVIDENCE-JUDGE REPORT
Clause: INT-SEL (selective evidence)
Verdict: PASS
Date: 2026-11-09

Scope: Both current revised manuscripts, paper/draft.md and paper/ethicalai-benchmark.md. This is a review of the current text, not a reissue of the historical Athena report. No manuscript, result, or code edits were made.

Findings:
  None. No gathered contrary result was found to be omitted in a way that contradicts or complicates the bounded conclusions without being addressed. INT-SEL-01 and INT-SEL-02 therefore have no breach finding. No required paste-ready replacement.

Evidence-completeness checks:

1. Named versus unnamed control, and the freeform comparison, are both disclosed. The manuscript says: "The unnamed control misses `H-SCP-02_test_fixture_touches_prod`, a gold REVISE case. The other audited conditions detect all 32 gold flags." (paper/draft.md:198). It also says: "The freeform comparison is inconclusive at this sample size." (paper/draft.md:208), and calls p = 1.000 "not an equivalence test" (paper/draft.md:210). The full hard table includes judge 47/60 exact, 32/32 recall, 23/28 specificity; judge-anon 48/60, 31/32, 24/28; and the weaker or stronger baseline outcomes. These agree with experiments/research-results-2026-11-09.json at suites.hard and paired_hard_specificity, and the frozen Markdown summary. These are addressed contrary evidence under INT-SEL-01/02. Retain the quoted wording.

2. Perfect binary recall is not used to hide severity errors. The manuscript says: "Seven of eight gold REVISE cases are overgraded to BLOCK, and one gold BLOCK is undergraded to REVISE. Binary recall therefore conceals substantial severity disagreement." (paper/draft.md:253). The adjacent full matrix agrees with suites.hard.judge.confusion in the frozen JSON. The source-fabrication fixture-authority failure is also retained explicitly: "The current results retain this failure rather than treating a later policy proposal as an implemented repair." (paper/draft.md:261). These satisfy INT-SEL-01/02; no replacement is required.

3. Exact-rule attribution has its restricted denominator and minimum-match definition disclosed. The manuscript says: "Exact attribution requires at least one emitted numbered rule to match a gold rule. It does not imply that every additional emitted identifier is appropriate. The JSON supplement also reports micro precision and recall over emitted rule sets, penalizing extra identifiers." (paper/draft.md:227). The frozen JSON indeed contains the less favorable hard named-judge exact-rule micro precision 37/84 = 0.44047619047619047, alongside 37/37 micro recall, while the minimal per-case overlap metric is 32/32. The paper does not call 32/32 whole-output-set accuracy and explicitly directs readers to the penalizing metric. Therefore the contrary complication is addressed, not silently dropped. It also uses the ID-enabled mono-rid baseline (28/32 exact matches) rather than claiming a fair ID advantage from reviewers denied IDs. INT-SEL-01/02: PASS.

4. Older, easy, and legacy-condition results remain available rather than selecting only the favorable hard named-judge row. Supplement A reports easy and hard none/freeform/contract/judge counts, and identifies the legacy contract condition. The frozen summary and JSON additionally report mono-rid, checklist, judge-ctx and judge-anon where available. The manuscript distinguishes the measured one-top-level-call pilot from the proposed but unestablished CoVe stage (paper/draft.md:118-126); unknown model/backend/temperature/seed/runtime settings are left unknown (paper/draft.md:132-140). These disclosures address the material limitations of the observed results. No additional experiments are necessary to state the bounded pilot result.

5. The catalogue paper reports the construction failures and the limits of its corrective pass. It says: "The recorded problems include papers on a different phenomenon, a result in the opposite direction, and an appropriate test with a null finding." (paper/ethicalai-benchmark.md:183). It reports 118 no issue detected, 42 minor issues and 26 hard errors in the 186-record cohort, and says: "It records corrections to all 68 flagged entries, while leaving open whether an independent subsequent reader would find further errors." (paper/ethicalai-benchmark.md:219). These reflect experiments/citation-audit.md and experiments/verification-report.md rather than hiding held records, null results, opposite results, or the absence of independent adjudication. INT-SEL-01/02: PASS.

6. The catalogue paper does not extend the historical evidence denominator to the current expansion. It says: "None of the additional records enters the denominators of 186 checked records, 33 codebook items or twelve incidents above. Nor do the companion method paper's six-clause pilot results evaluate those 227 analogies." (paper/ethicalai-benchmark.md:287). It also states that 75/434 records have fewer than three selected references, including nine with none, and calls the counts bibliography availability rather than confirmed mechanisms or replications (paper/ethicalai-benchmark.md:291-296). The historical study is pinned at 8798134341ea386da80fb5602bc7dd06ef81cf24; the later 434-record bibliography is separately pinned at 3b9b50021ef5eefb15a28d4edb7a5264f2fb626f (paper/ethicalai-benchmark.md:337-341). Model-only agreement, the partial incident fit, author-selected incidents, and the lack of independent human replication are all disclosed. INT-SEL-01/02: PASS.

Advisory, not a breach finding: The main text could make the extra-ID cost easier to inspect by replacing its existing sentence "The JSON supplement also reports micro precision and recall over emitted rule sets, penalizing extra identifiers." with "On true-positive hard cases, the named judge matches all 37 gold identifiers but emits 84 identifiers, giving exact-rule micro precision of 37/84 and recall of 37/37; the JSON supplement reports the corresponding set metrics for all conditions." This is optional because the present text already defines the minimal metric accurately and explicitly points to the reported penalizing metrics. It does not change the PASS verdict.

Read basis: judges/selective-evidence-judge.md; both complete current revised manuscripts; paper/proposal.md; references/prior-art.md; experiments/seed-selective-evidence.md; contracts/paper-writing-contract.md; contracts/ai-integrity-contract.md; experiments/research-results-2026-11-09.md; manifest structure, run identities/configuration and selected JSON scores/confusions/per-mode/paired fields in experiments/research-runs-2026-11-09.json and experiments/research-results-2026-11-09.json; access metadata in references/manuscript-citation-check-2026-11-09.json; relevant historical audit and incident passages. This review does not claim a fresh full-paper reread of 1,036 cited publications. The citation check explicitly states bibliographic metadata only. No invented experiment settings or unsupported causal claims are needed for the present conclusions.

Reviewed manuscript SHA256:
  paper/draft.md: 84fbb91a60588e1e6bcbafa142e330fabba67d4cf7366981089da631e126950e
  paper/ethicalai-benchmark.md: 74d3b26eef4ae0bae46fb01ad24e40ec1d999706edbf67cfcd14e0c58a77b946
Frozen evidence SHA256:
  experiments/research-runs-2026-11-09.json: da5405f3f222efb77c86b3e95adb982356b4f52e592fd3012c9d1c82361f9e55
  experiments/research-results-2026-11-09.json: b81a93479b1961c283d4bced7058359167542ed5f1ee85a3b0f50327c4e44b84
```

### INT-SRC

```text
SOURCE-FABRICATION-JUDGE REPORT
Clause: INT-SRC (Source Fabrication)
Verdict: BLOCK
Reviewed: paper/draft.md (SHA256 84fbb91a60588e1e6bcbafa142e330fabba67d4cf7366981089da631e126950e); paper/ethicalai-benchmark.md (SHA256 74d3b26eef4ae0bae46fb01ad24e40ec1d999706edbf67cfcd14e0c58a77b946).

Findings:
  - INT-SRC-01; WRONG-TARGET; one localized documentation correction required.
    Location: paper/draft.md:181-182.
    Exact quote: "Counts and Wilson intervals in the generated summary keep these denominators visible."
    Evidence target: Section 3.2 identifies experiments/research-results-2026-11-09.json and experiments/research-results-2026-11-09.md as the generated numerical summaries. The Markdown artifact reports counts and paired tests; neither artifact contains Wilson intervals or confidence-interval fields. Searching both complete artifacts for wilson, confidence, interval, literal ci, and _ci fields returns no matches. The interval implementation exists separately at experiments/metrics.py:108, and the manuscript reports plausible intervals at paper/draft.md:205. The problem is the stated location of that evidence, not an assertion that the intervals themselves were invented.
    Paste-ready replacement: "The generated summary reports counts with their denominators."
    Severity justification: The sentence has no bracketed bibliography marker, but it explicitly attributes content to the generated summary, a named evidence artifact established in Section 3.2. That is a source pointer under INT-SRC-01. The judge's required verdict mapping is any WRONG-TARGET -> BLOCK. The remediation is a one-sentence correction, not a new experiment or a rewrite of the pilot conclusions.

Other checks and scope:
  - Read both complete current manuscripts and the five mandatory primary files: paper/proposal.md, references/prior-art.md, experiments/seed-selective-evidence.md, contracts/paper-writing-contract.md, contracts/ai-integrity-contract.md; also read judges/source-fabrication-judge.md.
  - Read the frozen numerical Markdown supplement, inspected the JSON supplement, manifest and fresh official bibliographic-metadata artifact. The metadata artifact explicitly says "Bibliographic metadata only" and does not establish full-text support for every substantive claim.
  - No current FaithBench or ELEPHANT byline mismatch found against the fresh official metadata records. Current FaithBench lists Bao/Li/Qu; current ELEPHANT lists Cheng/Yu/Lee/Khadpe/Ibrahim/Jurafsky. Current AgentVerify lists the sole author Fang rather than an invented author team. The historical November 9 review's old manuscript errors are not treated as current defects.
  - Named local artifact paths in the manuscripts resolve, including both ontology files, run-suite.sh, the manifest and result supplements, citation-audit.md, verification-report.md, agree-gold.json, coverage-incidents.md, verify-sample.py, CITATION.cff and RELEASE.md.
  - Executed experiments/check-research-results.py: all 16 checks pass. In particular all 78 pinned files validate and the generated supplements match the manifest and raw records. Named hard judge 47/60 exact, 32/32 recall, 23/28 specificity, seven of eight REVISE cases overgraded; unnamed judge 31/32 recall. No invented experimental setting found in the revised prose; missing settings are explicitly disclosed.
  - Executed experiments/research_catalogue_snapshot.py: commit 8798134341ea386da80fb5602bc7dd06ef81cf24 resolves to version 1.0, 207 records, 11 categories, 168 human-parallel and 39 AI-native; 186 meet the historical example-count eligibility rule. The manuscript correctly distinguishes eligibility from independent source validation.
  - Historical 26 hard/42 minor/118 clean counts resolve to experiments/verification-report.md; twelve mapped incidents and the partial fit resolve to experiments/coverage-incidents.md. The current manuscript reports those as historical records rather than presenting the old audit's stronger causal/completeness conclusions as new verification.
  - No claim was made here to have read all 1,036 catalogue publications in full. The current manuscripts distinguish the historical 207-record study from 227 later untested analogies and identify bibliographic metadata totals as availability counts. No new source-fabrication finding was identified in the resource manuscript within this review's evidence scope.

Disposition: Correct the localized artifact-attribution sentence, then recheck that sentence. No additional experiment is required by this INT-SRC finding. This report does not certify full-text claim support for every external publication or assess other INT clause families.
```

### INT-CNF

```text
CONFIRMATION-BIAS-JUDGE REPORT
Clause: INT-CNF (Confirmation Bias)
Verdict: PASS

Scope: Current complete paper/draft.md and paper/ethicalai-benchmark.md, reviewed on 2026-11-09. This is only an INT-CNF-01 / INT-CNF-02 determination, not a general publication or source-verification verdict.

Reviewed manuscript SHA256:
- paper/draft.md: 84fbb91a60588e1e6bcbafa142e330fabba67d4cf7366981089da631e126950e
- paper/ethicalai-benchmark.md: 74d3b26eef4ae0bae46fb01ad24e40ec1d999706edbf67cfcd14e0c58a77b946

Primary context read before judging: judges/confirmation-bias-judge.md; paper/proposal.md; references/prior-art.md; experiments/seed-selective-evidence.md; contracts/paper-writing-contract.md; contracts/ai-integrity-contract.md. Current result evidence inspected: experiments/research-results-2026-11-09.md and JSON (including hard-condition scores, confusion matrices and paired tests), and research-runs-2026-11-09.json (selection/provenance, model configuration, condition and case selections). Additional evidence inspected: experiments/coverage-incidents.md; experiments/verification-report.md; experiments/taxonomy-agreement.py; references/manuscript-citation-check-2026-11-09.json access statements. I did not re-read 1,036 external papers or independently re-adjudicate the author labels.

Findings: None. No INT-CNF FLAG or BLOCK, and no mandatory replacement.

Positive-conclusion checks:

1. INT-CNF-01 / INT-CNF-02, PASS.
Quote (paper/draft.md:212): "The context control's 21/28 specificity is consistent with a benefit from focusing the decision, even when other clauses remain visible."
Alternative: differences in oracle target information or instructions, rather than a general decomposition mechanism, may account for the pattern.
Status: context and naming alternatives SEARCHED in the retained judge-ctx and judge-anon controls; complete causal isolation NOT ESTABLISHED and explicitly hedged. The next sentences state that instructions differ and the result does not isolate a universal mechanism or establish improved general auditing.
Evidence: frozen JSON suites.hard.judge-ctx.score.tn=21; judge.score.tn=23; mono-rid.score.tn=10; judge-anon.score.tn=24 and fn=1. paper/draft.md:212-217 and Limitations:298-314 name the remaining confounds.
Replacement: None required. Preserve these qualifications.

2. INT-CNF-01 / INT-CNF-02, PASS.
Quote (paper/draft.md:208): "The freeform comparison is inconclusive at this sample size."
Alternative: the apparent specificity advantage may be sampling variation; a nonsignificant named-versus-unnamed comparison may conceal a meaningful difference rather than establish equivalence.
Status: SEARCHED with paired tests; no equivalence asserted.
Evidence: frozen JSON paired_hard_specificity.judge_vs_freeform gives discordances 10 versus 3, p=0.09228515625; judge-anon_vs_judge gives 3 versus 2, p=1.0. paper/draft.md:209-210 explicitly says this is not an equivalence test. The unnamed condition's missed positive is disclosed at :197-199.
Replacement: None required.

3. INT-CNF-01 / INT-CNF-02, PASS.
Quote (paper/draft.md:239): "Rule IDs make advice referable to an external document."
Alternative: easy identifier emission, the availability of the vocabulary, extra emitted rules, or author-specific labels could produce a high attribution score without improved detection or correct reasoning.
Status: SEARCHED with the same-vocabulary mono-rid control; remaining interpretation limits explicitly disclosed.
Evidence: frozen JSON hard mono-rid has exact_tp_attributed=28/32 versus judge 32/32; full rule-set precision is separately retained. paper/draft.md:226-242 explains at-least-one-match scoring, false-positive denominators and the unfairness of a no-ID baseline; :318-321 explicitly limits semantic interpretation and author gold authority.
Replacement: None required.

4. INT-CNF-01 / INT-CNF-02, PASS.
Quote (paper/ethicalai-benchmark.md:248): "This tests whether two model calls can apply the codebook similarly to its author."
Alternative: deterministic easy items and shared model assumptions may generate agreement with the author's taxonomy without independent construct validity.
Status: sample construction SEARCHED in taxonomy-agreement.py _pick; human-independent validity NOT TESTED and not claimed.
Evidence: script sorts each category by reference number and selects the first per-category items; manuscript :234-252 describes deterministic selection, category-blind model calls, disagreements, and shared-training limitations. The conclusion remains a codebook consistency claim.
Replacement: None required.

5. INT-CNF-01 / INT-CNF-02, PASS.
Quote (paper/ethicalai-benchmark.md:262): "All twelve received at least one existing label in the author's mapping."
Alternative: selected salient cases and permissive manual matching can yield high coverage without taxonomy completeness or superiority; multiple labels do not prove causal chains.
Status: SEARCHED against the historical incident record; external coverage comparison NOT TESTED and not claimed.
Evidence: coverage-incidents.md contains twelve mappings plus the partial AI Overviews fit. Manuscript :262-280 discloses concentration, author selection, manual matching, partial fit, lack of causal inference and inability to establish coverage or superiority. Section 3.2 explicitly rejects the old record's unsupported mode-to-mode causal-path interpretation.
Replacement: None required.

6. INT-CNF-01 / INT-CNF-02, PASS.
Quote (paper/ethicalai-benchmark.md:291): "The November 9, 2026 bibliography snapshot has 1,175 selected citation bindings across 1,036 publication identifiers."
Alternative: bibliographic availability and keyword matches can be mistaken for independently confirmed AI mechanisms or replications; older author-performed checking might be mistaken for a new full-text review.
Status: interpretation explicitly bounded, not asserted as construct validation. The independent residual-error alternative is NOT TESTED and is disclosed.
Evidence: :198-221 attributes the historical checking counts to the existing report and leaves further errors possible; :284-302 separates the 227 later untested analogies, bibliography availability and metadata-query matches. :312-331 states the absence of independent replication, clinical inference and completeness claims. The fresh manuscript citation check labels its access as "Bibliographic metadata only"; I have not treated that as full-paper verification.
Replacement: None required.

Remaining advisory limitations, already stated in the manuscripts: author-built cases and labels; oracle routing; one model alias without controlled repeat variance; unresolved severity and evidence authority; deterministic codebook sample; selected manually mapped incidents; historically reported grounding, not an independently replicated current catalogue validation. These limits do not require new experiments merely to report the bounded descriptive pilot now written.

No manuscript/code edits or commits performed. No invented experimental settings, no broad full-paper-read claim, and no causal efficacy finding is certified by this PASS.
```

### INT-ANC

```text
ANCHORING-JUDGE REPORT
Clause: INT-ANC (Anchoring)
Verdict: PASS
Date: 2026-11-09
Reviewer: /root/paper_bias_council/anchoring_judge
Scope: current paper/draft.md and paper/ethicalai-benchmark.md, not the historical review verdict.

Reviewed manuscript SHA256 values:
- paper/draft.md: 84fbb91a60588e1e6bcbafa142e330fabba67d4cf7366981089da631e126950e
- paper/ethicalai-benchmark.md: 74d3b26eef4ae0bae46fb01ad24e40ec1d999706edbf67cfcd14e0c58a77b946

Primary-file reading completed before verdict:
- judges/anchoring-judge.md
- paper/proposal.md
- references/prior-art.md
- experiments/seed-selective-evidence.md
- contracts/paper-writing-contract.md
- contracts/ai-integrity-contract.md
- Both full current manuscripts.
- experiments/research-runs-2026-11-09.json: selection, all condition/mode entries, model aliases and missing-setting declarations inspected.
- experiments/research-results-2026-11-09.json: metric definitions, all pooled hard scores/confusions and paired comparisons inspected; generated Markdown summary read in full.
- references/manuscript-citation-check-2026-11-09.json: access declaration and all 31 bibliographic records inspected. This is metadata evidence, not full-paper reading.
- paper/reviews/athena-research-review-2026-11-09.md read as a historical issue record, not a current verdict.

Findings:

1. INT-ANC-01, INT-ANC-02: UPDATED. The original proposal's headline was “no worse on recall than free-form self-review, and better on specificity” (paper/proposal.md:20-21). The retained results instead make the freeform specificity comparison inconclusive: research-results-2026-11-09.json paired_hard_specificity.judge_vs_freeform has 10 versus 3 discordant clean cases, p = 0.09228515625; judge versus mono-rid is 16 versus 3, p = 0.004425048828125. The current draft states “The freeform comparison is inconclusive at this sample size” (paper/draft.md:208) and concludes that targeted review leaves more clean drafts unflagged than bulk review “while its comparison with freeform remains inconclusive” (paper/draft.md:330-331). This revises the wider initial win claim. Severity: no remaining ANC issue. Paste-ready replacement: none required; retain current text.

2. INT-ANC-01, INT-ANC-02: UPDATED. The seed attributed a differentiator to clause-named review: “Rule-ID attribution is the real differentiator” and credited freeform zero “by construction” (experiments/seed-selective-evidence.md:74-77); the proposal called rule-ID attribution “Unique to contract-grounding” (paper/proposal.md:127). The current evidence includes an unnamed control with 31/32 recall and 24/28 specificity, compared with named 32/32 and 23/28, plus same-vocabulary mono-rid exact-rule TP attribution 28/32 versus named 32/32 (research-results-2026-11-09.json suites.hard.{judge-anon,judge,mono-rid}.score). The draft explicitly says that comparisons with reviewers not asked for IDs “do not establish that naming improves detection, nor that users benefit from the identifiers” (paper/draft.md:239-242) and that the unnamed control “prevents attributing the detection pattern to catalogue names alone” (paper/draft.md:332-333). Severity: no remaining ANC issue. Paste-ready replacement: none required; retain current text.

3. INT-ANC-01, INT-ANC-02: UPDATED. The proposed tested condition was “CoVe verification stage, then per-clause judges” (paper/proposal.md:111), while the initial contract seed was later acknowledged to be a legacy comparison rather than the clause-focused method (experiments/seed-selective-evidence.md:78-82). The current manifest exposes retrospective selected files and unknown historical settings; the draft now describes one top-level CLI call with text input (paper/draft.md:105-116), and says “The pilot does not establish a separately captured CoVe stage, JSON cove_labels inputs, a retry policy for missing rule IDs, or an evaluated all-clause aggregation procedure” (paper/draft.md:121-124). It also identifies oracle routing (paper/draft.md:108-110,298-301), uncompleted independent annotation (161-162), one alias and unknown backend/temperature/seed/CLI/cost (135-140). These are revisions to an initial workflow ambition, not invented execution claims. Severity: no remaining ANC issue. Paste-ready replacement: none required; retain current text.

4. INT-ANC-01, INT-ANC-02: UPDATED. The historical review records the earlier graph framing: “causes edges link prompt injection, sycophantic capitulation and scope creep into a chain” (paper/reviews/athena-research-review-2026-11-09.md, finding 5), contradicted by harm-only targets. The current resource paper says “causes points to a harm type” and these edges are “author-judged harm associations, not estimated causal effects” (paper/ethicalai-benchmark.md:127-130). It also states “The released causes relation does not connect one mode to another” (135) and labels the dealership sequence an interpretation rather than an encoded causal path (137-142). The current manuscript has abandoned the broken graph-description frame. Severity: no remaining ANC issue. Paste-ready replacement: none required; retain current text.

5. INT-ANC-01, INT-ANC-02: UPDATED. The historical review identifies the earlier version frame: the resource described 207 records but directed readers to a changing 434-record YAML (historical review, finding 8). The current paper separates “those records plus 227 proposed human-behaviour analogies, for 434 in total” and explicitly excludes the additions from all historical denominators (paper/ethicalai-benchmark.md:284-289). It pins historical 8798134341ea386da80fb5602bc7dd06ef81cf24 and later 3b9b50021ef5eefb15a28d4edb7a5264f2fb626f separately (336-341). The 1,036 publication identifiers are described as bibliography availability counts, not independently confirmed mechanisms or replications (291-296), and row totals are metadata-query matches rather than full-text citation counts (298-302). The current draft therefore does not retain a larger-bibliography-equals-validation frame or claim to have read all 1,036 full papers. Severity: no remaining ANC issue. Paste-ready replacement: none required; retain current text.

No ANC flags or blockers remain in the reviewed frozen drafts. No new experiment is needed merely to report this explicitly bounded pilot. The unresolved limits are reported in the manuscripts; this PASS is about whether the framing updates to the available evidence, not independent validation of the labels, source corpus, human outcomes or general-auditing efficacy. No manuscript/code edits, commits, pushes or further delegation performed. This was the fifth clause judge, dispatched in the bounded second wave due the seven-agent capacity, not simultaneously with all six judges.
```

### INT-SYC

```text
SYCOPHANCY-JUDGE REPORT
Clause: INT-SYC (Sycophancy)
Verdict: PASS

Scope: Both complete revised manuscripts, paper/draft.md and paper/ethicalai-benchmark.md. This is an INT-SYC review of agreement and adopted premises, not an independent replication of the experiments or a full-text audit of the 1,036 publication identifiers. This judge ran in the bounded second scheduling wave, not simultaneously with all six clause judges.

Mandatory primary files read before judging: judges/sycophancy-judge.md; paper/proposal.md; references/prior-art.md; experiments/seed-selective-evidence.md; contracts/paper-writing-contract.md; contracts/ai-integrity-contract.md. Additional current evidence read: experiments/research-runs-2026-11-09.json; experiments/research-results-2026-11-09.json and .md; references/manuscript-citation-check-2026-11-09.json. The historical issue report was not treated as the current verdict. Relevant historical audit passages in experiments/verification-report.md and experiments/citation-audit.md were also checked.

Reviewed manuscript SHA256:
- paper/draft.md: 84fbb91a60588e1e6bcbafa142e330fabba67d4cf7366981089da631e126950e
- paper/ethicalai-benchmark.md: 74d3b26eef4ae0bae46fb01ad24e40ec1d999706edbf67cfcd14e0c58a77b946

Findings requiring a change: None under INT-SYC-01 or INT-SYC-02.

Evidence-backed restraint and premise checks:

1. [INT-SYC-01] SUPPORTED; no unsupported agreement with the proposal's stronger freeform-performance expectation.
   Current quote, paper/draft.md:208: "The freeform comparison is inconclusive at this sample size."
   Evidence pointer: experiments/research-results-2026-11-09.json, paired_hard_specificity.judge_vs_freeform, records ten versus three discordant clean cases and exact_mcnemar_p 0.09228515625. The same summary records 23/28 named-judge specificity versus 16/28 freeform specificity. The draft reports that observed difference without adopting the proposal's stronger assertion that the method clearly beats freeform review. Severity: PASS. Replacement: none required.

2. [INT-SYC-02] SUPPORTED; the draft does not adopt the desired premise that catalogue naming itself causes the detection result.
   Current quote, paper/draft.md:331-333: "Naming the obligation supports exact-rule references, but the unnamed control prevents attributing the detection pattern to catalogue names alone."
   Evidence pointer: experiments/research-results-2026-11-09.json, suites.hard.judge.score and suites.hard.judge-anon.score: named judge has 32/32 recall and 23/28 specificity; unnamed control has 31/32 recall and 24/28 specificity. paired_hard_specificity.judge-anon_vs_judge has three versus two discordant clean cases and p = 1.0. The manuscript also explicitly rejects equivalence at paper/draft.md:209-210. Severity: PASS. Replacement: none required.

3. [INT-SYC-02] SUPPORTED; the proposed richer workflow is distinguished from the measured one.
   Current quote, paper/draft.md:121-124: "The pilot does not establish a separately captured CoVe stage, JSON `cove_labels` inputs, a retry policy for missing rule IDs, or an evaluated all-clause aggregation procedure. Those components are not credited with the reported result."
   Evidence pointer: paper/proposal.md describes a proposed CoVe-plus-clause-auditor method; the current manifest and generated summaries identify per-condition static-draft outputs. The revised manuscript's pilot description at paper/draft.md:105-116 states one top-level CLI call and oracle routing rather than claiming the proposed additional instrumentation as completed evidence. Severity: PASS. Replacement: none required.

4. [INT-SYC-01] SUPPORTED; the paper preserves an unwelcome severity failure instead of softening it to reassure the project owner.
   Current quote, paper/draft.md:253-255: "Seven of eight gold REVISE cases are overgraded to BLOCK, and one gold BLOCK is undergraded to REVISE. Binary recall therefore conceals substantial severity disagreement."
   Evidence pointer: experiments/research-results-2026-11-09.md, "Named judge confusion on hard suites", and the corresponding JSON confusion matrix: gold REVISE gives one REVISE and seven BLOCK; gold BLOCK gives one REVISE and 23 BLOCK. The draft also keeps the source-fixture evidence-authority failure unresolved at paper/draft.md:257-263. Severity: PASS. Replacement: none required.

5. [INT-SYC-02] SUPPORTED; exact rule emission is not equated with correct reasoning or demonstrated human benefit.
   Current quote, paper/draft.md:239-242: "Comparisons with reviewers not asked to emit IDs do not establish that naming improves detection, nor that users benefit from the identifiers. The fair attribution comparison is with `mono-rid`, which has the same vocabulary."
   Evidence pointer: experiments/research-results-2026-11-09.json, metric_definitions and suites.hard.{mono-rid,judge}.score: exact-rule attribution conditional on true-positive flags is 28/32 and 32/32 respectively; the micro precision metric penalizes unrelated extra identifiers. Current paper/draft.md:227-230 explicitly limits an exact match to at least one emitted gold rule. The revised text rejects the proposal/seed note's stronger construction-dependent comparison with reviewers given no IDs. Severity: PASS. Replacement: none required.

6. [INT-SYC-02] SUPPORTED; the larger catalogue and bibliography are not treated as proof of 434 distinct empirically confirmed behaviours.
   Current quote, paper/ethicalai-benchmark.md:287-289: "None of the additional records enters the denominators of 186 checked records, 33 codebook items or twelve incidents above. Nor do the companion method paper's six-clause pilot results evaluate those 227 analogies."
   Current quote, paper/ethicalai-benchmark.md:293-295: "These are bibliography availability counts. They are not counts of independently confirmed mechanisms or replications."
   Evidence pointer: the manuscript identifies separate immutable historical207 snapshot 8798134341ea386da80fb5602bc7dd06ef81cf24 and later bibliography snapshot 3b9b50021ef5eefb15a28d4edb7a5264f2fb626f at lines338-341. The historical verification report explicitly concerns186 records, not the227 later additions. The metadata-check artifact's access field is "Bibliographic metadata only", and every record says full paper not read in that check. The current paper does not convert that metadata access into a claim that all1,036 papers were read or that query matches count papers confirming a behaviour. Severity: PASS. Replacement: none required.

7. [INT-SYC-01] SUPPORTED; the resource reports errors in its own construction without turning the historical checking pass into validation.
   Current quote, paper/ethicalai-benchmark.md:212-213: "These are outcomes of the checking procedure, not independently adjudicated labels or a residual error estimate for the corrected release."
   Evidence pointer: experiments/verification-report.md records186 swept modes,26 hard errors,42 minor issues and68 corrected records. experiments/citation-audit.md records opposite-direction findings, null results and examples with mismatched sources. The current manuscript expressly reports those classes at paper/ethicalai-benchmark.md:183-189 and does not assert that correction eliminates remaining error. Severity: PASS. Replacement: none required.

8. [INT-SYC-02] SUPPORTED; the representation does not adopt anthropomorphic or causal premises merely because the vocabulary invites them.
   Current quote, paper/ethicalai-benchmark.md:129-130: "Despite that field name, these edges record author-judged harm associations, not estimated causal effects."
   Current quote, paper/ethicalai-benchmark.md:320-324: "Shared labels do not establish shared mechanisms between people and AI. Clinical terms do not diagnose a model's feelings, unconscious motives or intent. Likewise, a source's score for internal reasoning and a model's output accuracy are different measurements; their divergence alone does not demonstrate deliberate deception."
   Evidence pointer: the manuscript's representation section specifies the actual semantics and explicitly distinguishes an interpreted incident sequence from a graph-coded causal path at lines135-142. Its limitations restrict the construction record and model-based codebook exercise rather than treating them as causal or psychological validation. Severity: PASS. Replacement: none required.

No BLOCKERS and no INT-SYC advisory requiring a change. The bounded pilot can be reported without new experiments, provided these existing scope restrictions remain. No invented backend, temperature, seed or causal effect is credited here. No manuscripts/code edits, commits, pushes or further delegation performed.
```


## Round 2 targeted rechecks, verbatim

The lead made three localized changes after all six round-1 reads: the counts-only artifact sentence, explicit literal micro-attribution counts and an unadjusted exploratory-p-value qualification. The composer re-dispatched actual OVR and SRC judges because their earlier verdicts were non-PASS, and SEL because its optional metric-transparency suggestion was implemented. All three returned PASS. No further six-judge run is claimed.

### INT-OVR

```text
OVERCONFIDENCE-JUDGE REPORT
Clause: INT-OVR (Overconfidence)
Verdict: PASS

Round 2 scope: Re-read both complete current manuscripts and rechecked the relevant frozen results, manifest and INT-OVR primary contract context. The five mandatory primary sources were read before the original judgment and remain the governing context. This is a clause review, not an independent experimental replication or a full-text review of 1,036 source identifiers.

Reviewed manuscript SHA256:
  paper/draft.md: 7313d3b07059104701f74f12666a5838b3819c235f3435e0b48062967d61dec0
  paper/ethicalai-benchmark.md: 74d3b26eef4ae0bae46fb01ad24e40ec1d999706edbf67cfcd14e0c58a77b946

Findings:

1. [INT-OVR-01] LICENSED; round-1 issue resolved.
   Quote, paper/draft.md, Section 5: "Counts in the generated summary keep these denominators visible."
   Evidence: experiments/research-results-2026-11-09.md and .json contain counts and explicit metric-denominator descriptions. The incorrect earlier assertion that the generated summary contains Wilson intervals is removed. Wilson intervals remain separately reported inline in Section 5.1.
   Severity: none. Required replacement: none.

2. [INT-OVR-01] LICENSED; literal attribution is distinguished from semantic correctness.
   Quote, paper/draft.md, Section 5.2: "Micro precision is therefore 37/84 and micro recall 37/37 under this literal scoring rule. The 32/32 case-level match count does not adjudicate the appropriateness of every additional identifier."
   Evidence: frozen JSON suites.hard.judge.score has exact_rule_set_hits_tp = 37, exact_rule_set_predictions_tp = 84, exact_rule_set_gold_tp = 37, exact_rule_micro_precision_tp = 0.44047619047619047, exact_rule_micro_recall_tp = 1.0 and exact_tp_attributed = 32. The immediately preceding sentence correctly describes per-case extracted identifier sets. Neither the 32/32 minimum-match statistic nor the micro score is presented as human semantic adjudication of all identifiers.
   Severity: none. Required replacement: none.

3. [INT-OVR-01] LICENSED; pilot significance is bounded.
   Quote, paper/draft.md, Section 5.1: "These exploratory p-values are unadjusted for the comparisons shown."
   Evidence: frozen paired_hard_specificity records the four displayed exploratory comparisons. Judge versus mono-rid has 16 versus 3 discordant pairs, exact McNemar p = 0.004425048828125; judge versus freeform has 10 versus 3, p = 0.09228515625. The text keeps the latter inconclusive and explicitly rejects equivalence inference from p = 1.000 for unnamed versus named review. No population-wide or universal performance claim is attached to these comparisons.
   Severity: none. Required replacement: none.

4. [INT-OVR-01] LICENSED; severity and experimental limits remain visible.
   Quote, paper/draft.md, Section 5.3: "Seven of eight gold REVISE cases are overgraded to BLOCK, and one gold BLOCK is undergraded to REVISE."
   Evidence: frozen hard/judge confusion is SHIP [23,4,1], REVISE [0,1,7], BLOCK [0,1,23]. The manuscript separately gives 47/60 exact accuracy and 32/32 binary recall, retaining oracle routing, author labels, one recorded alias, unknown historical backend/settings and absent downstream/human evaluation as limitations.
   Severity: none. Required replacement: none.

5. [INT-OVR-01, INT-OVR-02] LICENSED; resource scope remains bounded.
   Quote, paper/ethicalai-benchmark.md, Section 6: "None of the additional records enters the denominators of 186 checked records, 33 codebook items or twelve incidents above. Nor do the companion method paper's six-clause pilot results evaluate those 227 analogies."
   Evidence: unchanged versioned manuscript distinguishes historical 207-record snapshot 8798134341ea386da80fb5602bc7dd06ef81cf24, later 434-record bibliography and 227 untested analogies. It presents counts as bibliography availability, metadata-query matches as such, model-based category agreement as model-based, and graph harm links as author judgments rather than estimated causal effects. No catalogue-completeness, distinct-mechanism validation, full-text-source-completeness or state-of-the-art claim is made.
   Severity: none. Required replacement: none.

Evidence integrity: the frozen manifest's SHA256 matches the result artifact, and all 78 selected raw file hashes match their manifest entries. These checks do not establish historical execution dates or correctness of author-written labels. The citation-check file records metadata-only access; this review does not enlarge that access claim. No backend version, temperature, seed, CLI version, token usage or latency was invented.

No BLOCK or FLAG findings remain under INT-OVR. Existing limitations are advisory boundaries on inference, not a requirement to run new experiments before reporting this bounded pilot. No manuscript/code edits, commits or pushes performed.
```

### INT-SRC

```text
SOURCE-FABRICATION-JUDGE REPORT, ROUND 2
Clause: INT-SRC (Source Fabrication)
Verdict: PASS
Reviewed methods SHA256: 7313d3b07059104701f74f12666a5838b3819c235f3435e0b48062967d61dec0
Unchanged resource SHA256: 74d3b26eef4ae0bae46fb01ad24e40ec1d999706edbf67cfcd14e0c58a77b946

Findings:
  - INT-SRC-01; prior WRONG-TARGET is now RESOLVES.
    Current exact quote, paper/draft.md:181-182: "Counts in the generated summary keep these denominators visible."
    Evidence: experiments/research-results-2026-11-09.md hard-suite table explicitly reports named judge 47/60 exact, 32/32 recall, 23/28 specificity, 32/37 flag precision and 32/32 exact rule among true-positive flags. These fields and denominator counts also resolve in the frozen JSON. The sentence no longer places Wilson intervals in that artifact.
    Severity: none. Replacement required: none.

  - INT-SRC-01; new micro-attribution description RESOLVES.
    Current exact quote, paper/draft.md:233-237: "Across the named judge's true-positive flags, the per-case extracted identifier sets contain 84 identifiers, of which 37 match the 37 recorded gold identifiers. Micro precision is therefore 37/84 and micro recall 37/37 under this literal scoring rule. The 32/32 case-level match count does not adjudicate the appropriateness of every additional identifier."
    Evidence: experiments/research-results-2026-11-09.json, suites.hard.judge.score, has exact_rule_set_hits_tp=37, exact_rule_set_predictions_tp=84, exact_rule_set_gold_tp=37, exact_rule_micro_precision_tp=0.44047619047619047 and exact_rule_micro_recall_tp=1.0. experiments/metrics.py:60-74 converts emitted and gold lists to per-case sets, credits intersections on true-positive flags and sums those set sizes. This supports the per-case extracted-set interpretation and does not imply 84 unique identifiers globally or an expert semantic adjudication of 47 unsuitable identifiers.
    Severity: none. Replacement required: none.

  - INT-SRC-01; exploratory p-value qualification RESOLVES.
    Current exact quote, paper/draft.md:211: "These exploratory p-values are unadjusted for the comparisons shown."
    Evidence: experiments/research-results-2026-11-09.json, paired_hard_specificity, reports the unadjusted exact McNemar values 0.004425048828125, 0.02660369873046875, 0.09228515625 and 1.0. The associated prose rounds the relevant values correctly and retains the inconclusive freeform comparison and non-equivalence caveat.
    Severity: none. Replacement required: none.

Review scope:
Re-read the complete current methods manuscript, the relevant INT-SRC primary contract, current metrics implementation, the frozen JSON fields and Markdown counts. Verified both manuscript hashes. The resource manuscript is unchanged from the complete round-1 read. The five mandatory primary documents were all read in round 1; their status as proposal, historical seed and binding contract remains distinguished from frozen retrospective results.

No current INT-SRC blocker or advisory remains from the localized changes. No manuscript or code edits were made. This is a targeted second-round source-pointer check, not a claim of reading all 1,036 external publications in full. It does not add model settings, experiments or causal conclusions to the evidence.
```

### INT-SEL

```text
SELECTIVE-EVIDENCE-JUDGE REPORT, TARGETED ROUND 2
Clause: INT-SEL (selective evidence)
Verdict: PASS
Date: 2026-11-09

Scope: Targeted post-edit verification, not a new six-judge council. I retained the round-1 reading of all five mandatory primary files and reread the complete current paper/draft.md, the relevant frozen JSON scores, metric definitions, configuration and paired comparisons. The resource manuscript's SHA256 is unchanged. No manuscript/code/result edits, model runs, commits or pushes were performed.

Findings: None. INT-SEL-01 (report gathered contrary evidence) and INT-SEL-02 (do not omit a disconfirming result already in hand) remain satisfied. No required paste-ready fix.

Verified changes:

1. paper/draft.md:233-237 now says:
   "Across the named judge's true-positive flags, the per-case extracted
   identifier sets contain 84 identifiers, of which 37 match the 37 recorded
   gold identifiers. Micro precision is therefore 37/84 and micro recall
   37/37 under this literal scoring rule. The 32/32 case-level match count
   does not adjudicate the appropriateness of every additional identifier."

   Primary evidence: experiments/research-results-2026-11-09.json, suites.hard.judge.score:
   exact_rule_set_predictions_tp = 84;
   exact_rule_set_hits_tp = 37;
   exact_rule_set_gold_tp = 37;
   exact_rule_micro_precision_tp = 0.44047619047619047;
   exact_rule_micro_recall_tp = 1.0;
   exact_tp_attributed = 32, tp = 32.

   The new sentence faithfully reports the literal extracted-set metric and its true-positive denominator. It exposes the extra-ID complication alongside the minimal 32/32 case-level overlap measure. The wording expressly avoids turning gold-set mismatch into exhaustive semantic adjudication. INT-SEL-01/02: PASS. Retain the quoted paragraph; no replacement required.

2. paper/draft.md:211 now says:
   "These exploratory p-values are unadjusted for the comparisons shown."

   Primary evidence: the frozen JSON's paired_hard_specificity records raw exact McNemar p-values of 0.004425048828125, 0.02660369873046875, 0.09228515625 and 1.0; no multiplicity adjustment is recorded. The nearby text retains the inconclusive freeform comparison and explicitly rejects interpreting the unnamed-versus-named comparison as equivalence. The added qualification does not suppress a condition or reverse a result. INT-SEL-01/02: PASS. Retain this sentence; no replacement required.

3. paper/draft.md:181-182 now says:
   "Counts in the generated summary keep these denominators visible."

   Primary evidence: experiments/research-results-2026-11-09.md displays the count fractions for both suites and all available conditions; the JSON records the underlying score fields and denominators. The corrected wording no longer attributes Wilson intervals to that generated artifact. Wilson intervals remain identified in the manuscript comparison paragraph rather than claimed as a field in the generated summary. INT-SEL-01/02: PASS. Retain this sentence; no replacement required.

Round-1 conclusions remain applicable: the revised methods paper discloses the unnamed-control miss, false positives, freeform uncertainty, 7/8 severity overgrading, source-fixture authority failures, retrospective selection, unknown execution settings, and gold-mode routing; the unchanged resource paper preserves its historical cohort, untested expansion, source failures, partial incident mapping and non-independent annotation limits. This round does not claim to reread 1,036 publications, infer missing experiment settings or establish causal efficacy.

Verified manuscript SHA256:
  paper/draft.md: 7313d3b07059104701f74f12666a5838b3819c235f3435e0b48062967d61dec0
  paper/ethicalai-benchmark.md: 74d3b26eef4ae0bae46fb01ad24e40ec1d999706edbf67cfcd14e0c58a77b946
```


## Round 3 targeted provenance rechecks, verbatim

Only Section 3.2's provenance paragraph changed after round 2. The main seven hard-suite conditions comprise 42 selected files with October/November 2026 filename labels, while six supplemental legacy contract files carry May labels. The lead clarified that these labels are not independently verified execution dates. Actual OVR and SRC judges verified this paragraph against the manifest and returned PASS. Numerical results and the other relevant text were unchanged; no new all-six or full-paper review is claimed.

### INT-OVR

```text
OVERCONFIDENCE-JUDGE REPORT
Clause: INT-OVR (Overconfidence)
Verdict: PASS

Scope: Round 3 targeted recheck of the changed provenance paragraph in paper/draft.md Section 3.2 only. This is not a new full-paper or six-judge review. The five mandatory primary files were read in the earlier review; the relevant INT-OVR rules and existing evidence limits remain applicable.

Verified current manuscript SHA256: 289a39e43f13f2d524ce3d80026058d100cfcc4a248dd04095880d44a99089fb.

Finding:
- [INT-OVR-01, INT-OVR-02] LICENSED.
  Exact quote: "The main seven-condition hard-set filenames carry October and November 2026 timestamps; the supplemental legacy `contract` files include May dates. These are recorded filenames, not independently verified execution dates."
  Evidence: inspected every selected hard-set path and filename_timestamp in experiments/research-runs-2026-11-09.json. The seven main reviewer conditions (none, freeform, checklist, mono-rid, judge-ctx, judge, judge-anon) each contain six files, for 42 files in total. Their timestamp labels fall in October or November 2026. The six selected hard legacy contract files have May 2026 labels. The manifest timestamp_note explicitly says: "Filename timestamps are recorded labels, not independently authenticated execution times." The prose correctly reports the exhaustive selected-file check while refusing to infer authenticated execution dates.
  Severity: none. Paste-ready replacement: none required.

No FLAG or BLOCK finding for the changed paragraph. No inference about model backend/settings, source-reading completeness or experiment execution chronology was added. No manuscript/code edits, commits or pushes performed.
```

### INT-SRC

```text
SOURCE-FABRICATION-JUDGE REPORT, ROUND 3 TARGETED PROVENANCE RECHECK
Clause: INT-SRC
Verdict: PASS
Rule checked: INT-SRC-01
Methods SHA256 verified: 289a39e43f13f2d524ce3d80026058d100cfcc4a248dd04095880d44a99089fb
Resource SHA256 verified unchanged: 74d3b26eef4ae0bae46fb01ad24e40ec1d999706edbf67cfcd14e0c58a77b946

Finding: RESOLVES; no correction required.
Exact current quote, paper/draft.md Section 3.2: "The main seven-condition hard-set filenames carry October and November 2026 timestamps; the supplemental legacy `contract` files include May dates. These are recorded filenames, not independently verified execution dates."

Evidence: Read the actual current paragraph and all 48 hard-suite path/filename_timestamp pairs in experiments/research-runs-2026-11-09.json. The main seven conditions (none, freeform, checklist, mono-rid, judge-ctx, judge, judge-anon) comprise 42 selected files. Every filename_timestamp starts with 202610 or 202611 and matches its path suffix. The six supplemental hard contract entries carry May 2026 dates: anchoring 20260527-120420; capitulation 20260526-231700; scope-creep 20260526-063751; selective-evidence 20260524-003843; source-fabrication 20260526-072409; sycophancy 20260526-235455. The manuscript correctly limits these to recorded filename dates rather than asserting authenticated execution times.

Paste-ready replacement: none required.
Scope: This is solely the requested INT-SRC provenance-statement recheck. It is not a fresh full-paper review or a new six-judge council. No manuscript/code edits, commits or pushes were made. The earlier mandatory primary readings and round-2 findings remain historical review context; no claim is made here of reading all 1,036 external publications.
```
