# Paper AI Pattern Report

Date: 9 November 2026. Council role: editorial pattern review of the revised manuscripts. The scores below describe prose quality under the repository's rubric; they are not probabilities of AI authorship and do not certify the research claims. The separate evidence council is responsible for those claims.

Before reviewing, this reader consulted `paper/proposal.md`, `references/prior-art.md`, `experiments/seed-selective-evidence.md`, `contracts/paper-writing-contract.md` and `contracts/ai-integrity-contract.md`, followed by the complete revised manuscripts. The frozen result summary and the official arXiv citation-metadata check were also available. Historical proposal and seed language was not treated as the current manuscript.

Targeted follow-up rounds: after the complete reading, the methods manuscript received a correction of what the generated summary stores, an explicit qualification of the exploratory p-values, and the emitted-identifier micro scores. A final one-paragraph follow-up clarifies the date scope of the main hard-set and supplemental legacy filenames. These rounds reread the changed passages in their section context without repeating the full source audit. The catalogue manuscript is unchanged.

## Methods manuscript

### Pattern Score

**1 out of 10. PASS for the prose gate.** No required prose rewrite.

### Source

`paper/draft.md`, *Contracts Between Humans and AI Agents: An Advisory Integrity Agreement for Agentic Coding*, revision dated 2026-11-09.

Latest reviewed SHA256: `289a39e43f13f2d524ce3d80026058d100cfcc4a248dd04095880d44a99089fb`.

The complete reading covered SHA256 `84fbb91a60588e1e6bcbafa142e330fabba67d4cf7366981089da631e126950e`. The first targeted round covered the delta to `7313d3b07059104701f74f12666a5838b3819c235f3435e0b48062967d61dec0`; the final one-paragraph check covers the subsequent delta to the latest hash.

### Highlighted Text

No suspicious text is marked. Representative passages explain why a low score is appropriate:

- Abstract: "A coding agent can give a technically plausible answer while omitting contrary evidence, retaining a disproved framing, or exceeding the user's request."
- Introduction: "Coding agents can fail in what they report even when their commands execute successfully."
- Method: "The released harness, `experiments/run-suite.sh`, makes one top-level Claude Code CLI call per case and reviewer condition, except for `none`."
- Conclusion: "A written integrity contract gives a reviewer a stable obligation to cite and gives the human an artifact to inspect and amend."

### Detected Patterns

No combination of the rubric's tell categories warrants a flag. The introduction uses a concrete coding-review problem rather than a generic account of recent AI progress. The methods distinguish the implemented text harness from a proposed verification workflow. The experiments discuss the unnamed control's missed case, the false-alarm denominator, exact rule matching and severity disagreement. Those details prevent the discussion from becoming generic praise of the method.

The abstract and conclusion necessarily share the known-target-review finding. The conclusion is short and interprets that scope rather than reproducing the abstract's numerical sequence. This was a qualitative comparison; no embedding-similarity measurement is claimed.

### Targeted Final Review

The score remains **1 out of 10, PASS** after the final methods delta:

- "Counts in the generated summary keep these denominators visible." This states the artifact's role directly and removes the earlier claim that its output stores Wilson intervals.
- "These exploratory p-values are unadjusted for the comparisons shown." This is a specific statistical qualification, not a filler hedge. Its placement immediately after the paired-test comparisons makes the scope clear.
- "Micro precision is therefore 37/84 and micro recall 37/37 under this literal scoring rule." The surrounding paragraph identifies the true-positive-case subset and the extracted and gold identifier counts. It distinguishes identifier-level scores from the 32/32 case-level match count without presenting either as an overall appropriateness judgment.

The warning about additional identifiers appears in both the table explanation and the new paragraph. This is minor local repetition, not a prose blocker. If further shortening is needed, the final sentence of the new paragraph can be omitted because the table explanation already states the same limit. No change is required for this gate. The underlying identifier recount remains the evidence council's check; this review assesses the clarity of its presentation.

The last paragraph check also preserves **1 out of 10, PASS**. In section 3.2, "The main seven-condition hard-set filenames carry October and November 2026 timestamps; the supplemental legacy `contract` files include May dates" now separates the two file groups. "These are recorded filenames, not independently verified execution dates" attaches the date limitation to both groups. The passage is direct and specific, with no new prose issue. This editorial check does not independently verify the dates inside those filenames.

### Citation Audit

**In-text author-year mentions:** 22, in 21 bracket groups. **Bibliography entries:** 17.

All checked author-year mentions have a corresponding bibliography entry. The RFC citation has an official URL; the other entries carry an arXiv identifier or DOI. The revised FaithBench and ELEPHANT bylines agree with the supplied official metadata check. MiniCheck and SelfCheckGPT bylines also match that check. The clustered 2023-2026 references are expected for this CS topic and are not themselves an anomaly.

**Pure-fabrication candidates found in this light audit:** none. **Wrong-attribution candidates identified from prose alone:** none. This is a format and metadata check, not a full-text verification of every cited work. The distinction between a preprint's submission year and a later conference year must remain attached to the cited edition.

**Manual verification needed for this prose gate:** none. Retain the separate source council's evidence review for substantive claims.

### Main Diagnosis

The revised methods paper reads as a bounded pilot report. Its condition names, fractions and concrete failure case carry the argument. Claims of general auditing efficacy and universal method superiority have been replaced by statements tied to the recorded comparisons. Missing historical settings are stated directly rather than concealed with polished methodology language.

### Summary of Priority Fixes

No mandatory prose fix. Keep the existing separation between the observed pilot procedure and the proposed multi-stage workflow when applying any evidence-council revisions. Preserve the short discussion of the unnamed control and the limits of exact identifier overlap.

## Catalogue manuscript

### Pattern Score

**1 out of 10. PASS for the prose gate.** No required prose rewrite.

### Source

`paper/ethicalai-benchmark.md`, *EthicalAI: An Evidence-Linked Catalogue for AI Integrity*, revision dated 2026-11-09.

Reviewed SHA256: `74d3b26eef4ae0bae46fb01ad24e40ec1d999706edbf67cfcd14e0c58a77b946`.

### Highlighted Text

No suspicious text is marked. Representative passages:

- Abstract: "EthicalAI organises integrity failures and related behavioural patterns as definitions linked to evidence, obligations, harms and neighbouring concepts."
- Introduction: "An AI assistant can cite a nonexistent case, retain a user's mistaken framing after finding contrary evidence, or extend a coding task without disclosing the extra changes."
- Representation: "The historical catalogue contains 207 records."
- Conclusion: "Its historical construction records show why a plausible citation and an accurate worked example need separate checks."

### Detected Patterns

No combination of tell categories warrants a flag. The manuscript explains the historical evidence cohort before introducing the current bibliography. Its examples keep numerators, denominators and source scope together. The limitations concerning category labels, clinical terms, the model-based codebook check and author-selected incidents are substantive rather than generic future-work boilerplate.

Several sections repeat the historical-versus-current distinction. That repetition is warranted by the risk of interpreting the 434-record release as the cohort of the 186-record checking exercise. It does not currently read as padding. If the paper is shortened again, consolidate repeated qualifications carefully rather than removing the distinction itself.

The conclusion shares topic terms with the abstract, but does not repeat its audit figures or sentence structure. This was a qualitative comparison; no embedding-similarity measurement is claimed.

### Citation Audit

**In-text scholarly-source mentions:** 7. **Bibliography entries:** 7. Immutable snapshot links are additional artifact references, not counted as scholarly citations.

Each checked mention has a bibliography entry. Five entries carry arXiv identifiers, NIST has an official DOI, and OWASP has its official project URL. NIST and OWASP are framework resources, so absence of a journal venue or arXiv identifier is appropriate. The Spracklen citation retains an explicit arXiv version, and its prose preserves the package-recommendation denominator.

**Pure-fabrication candidates found in this light audit:** none. **Wrong-attribution candidates identified from prose alone:** none. The checking-history claims are explicitly attributed to project records; this review does not convert them into an independent replication.

**Manual verification needed for this prose gate:** none. Retain the source council's checks of historical counts and snapshot consistency.

### Main Diagnosis

The catalogue paper is specific about the artifact and the evidence behind its claims. It distinguishes a useful reference vocabulary from a set of validated mechanisms. Its construction errors, source-access limits and later expansion are part of the argument rather than a promotional narrative. The revised graph description avoids implying a causal result from a field name.

### Summary of Priority Fixes

No mandatory prose fix. Preserve the historical/current release distinction, the package denominator and the meaning of the harm-association edges during any later edits. No new claim of validated coverage, completeness or independent mechanisms is warranted by prose improvement.

## Validation Check

| Check | Methods manuscript | Catalogue manuscript |
|---|---|---|
| Em or en dashes in body prose | Pass; none found | Pass; none found |
| Generic abstract opener | Pass | Pass |
| Cookie-cutter contribution list | Pass | Pass |
| Filler hedges | Pass | Pass |
| Repetitive methodology rhythm | Pass | Pass |
| Pure-fabrication citation candidates | Pass; none found in light audit | Pass; none found in light audit |
| Wrong-attribution citation candidates from prose | Pass; none identified | Pass; none identified |
| Citation-cluster escalation trigger | Pass; no unresolved cluster identified | Pass; no unresolved cluster identified |
| Suspicious numerical-pattern presentation | Pass; counts have denominators and provenance | Pass; audit counts retain their cohort |
| Operational-detail absence as an authorship cue | Pass; unavailable API-run metadata is disclosed | Pass; no model-training setup is claimed |
| Conclusion merely restates abstract | Pass on qualitative reading | Pass on qualitative reading |
| Definition by tautology | Pass | Pass |
| Padding or hedge stacking | Pass | Pass |
| Marketing residue | Pass | Pass |
| Stylistic verb or adjective skew | Pass; no dense cluster found | Pass; no dense cluster found |
| Tortured phrases | Pass | Pass |

The historical model backend, temperature, seed, CLI version, cost and execution-date uncertainties remain reproducibility limitations. They are not evidence that results were fabricated, and GPU details are not a suitable authorship test for an API/CLI reviewer study. The prose review does not close those evidence gaps.

Editorial pattern judgments can unfairly penalize non-native English writing. Uniform rhythm, familiar scientific vocabulary and punctuation are weak single signals, so none was treated as evidence of authorship here. The reported score is an editorial rating only. Publication readiness still depends on the evidence and contract checks, not this score alone.
