# Research paper revision record, 9 November 2026

The author requested improvements to both papers after the November 9 review.
This revision changes the manuscripts, their reporting and publication tools,
and the existing website's paper section. It does not alter raw model outputs,
case labels, ontology records, governance contracts or judge rubrics. No new
model experiments were run, and no academic submission was made.

## Canonical manuscripts

| Manuscript | SHA256 | PDF length |
|---|---|---:|
| `paper/draft.md` | `289a39e43f13f2d524ce3d80026058d100cfcc4a248dd04095880d44a99089fb` | 6 pages |
| `paper/ethicalai-benchmark.md` | `74d3b26eef4ae0bae46fb01ad24e40ec1d999706edbf67cfcd14e0c58a77b946` | 6 pages |

The Markdown YAML headers provide each title, author, date and abstract for PDF,
LaTeX and the catalogue's HTML rendering. PDF metadata includes the complete
source hash. Public downloads are `docs/methods-paper.pdf` and `docs/paper.pdf`.
The existing homepage links to both; its 434-record catalogue remains intact.

## Review findings and dispositions

The original review is retained in
`paper/reviews/athena-research-review-2026-11-09.md`. Its references describe the
pre-revision text. This record reports the resulting changes rather than
rewriting that historical assessment.

| Finding | Implemented correction and remaining boundary |
|---|---|
| Inconsistent result snapshots | A retrospective manifest pins 78 files, their hashes, exact reviewer names and case order. Every reported detection, attribution, confusion-matrix and supplementary table uses that selection. The named hard-set judge has 47/60 exact verdicts and 23/28 specificity, with 7/8 REVISE cases overgraded. The manifest does not establish which files produced the former static tables. |
| Ambiguous reviewer glob | Tables, figures, severity and paired tests share a strict manifest loader. `judge-ctx` and `judge-anon` cannot silently enter a `judge` selection. Hash, condition, label and case-identity failures are rejected. |
| Omitted unnamed-control miss | The abstract, table and discussion report 31/32 recall and identify `H-SCP-02_test_fixture_touches_prod`. Named review retains 32/32. |
| Clause family credited as exact rule | Family overlap, exact numbered-rule overlap and flag precision are separate. Among true-positive hard flags, `mono-rid` matches an exact gold rule in 28/32 cases and the named judge in 32/32. The latter's literal extracted-set micro precision is 37/84 and recall 37/37; neither metric adjudicates every extra ID semantically. |
| Unsupported causal graph path | The catalogue paper describes `causes` as links to harms and explicitly distinguishes an interpreted incident sequence from an encoded mode-to-mode causal path. The schema is unchanged. |
| Unsupported procedure and settings | The methods describe the observed single top-level text call and oracle routing. Multi-stage CoVe and aggregation are proposed rather than credited as executed. Backend, decoding and cost settings remain unknown. Filename labels are explicitly unauthenticated dates, including the legacy May subset. Construction order is not presented as preregistered. |
| Bibliographic drift | FaithBench, ELEPHANT, AgentVerify and the ancillary BibTeX records use checked primary metadata. `references/manuscript-citation-check-2026-11-09.json` records the metadata access; this is not a claim to have read every full paper. |
| Historical/current cohort conflation | The 207-record v1.0 catalogue is pinned to `8798134341ea386da80fb5602bc7dd06ef81cf24`; the 434-record v1.3 bibliography is pinned separately. The 227 later analogies do not enter the historical study denominators. Three selected references are not three replications. |
| Internal-state interpretation | The catalogue limitations explain that a reasoning score/output discrepancy alone does not demonstrate deliberate deception. This paper revision does not rewrite the underlying alignment-hallucination ontology entry or establish the source's proposed mechanism. |
| Contextual citations presented as validation | The catalogue distinguishes source identity, definition, human findings, AI findings, interpretation and contrary evidence. The selected bibliography and individual source-role fields are unchanged; a contextual citation is not upgraded into a behavioural experiment. |

The statistical discussion retains the inconclusive comparison with freeform,
states that the exploratory p-values are unadjusted, and does not treat the
unnamed-versus-named comparison as an equivalence test. Package hallucination's
19.7% denominator is package recommendations, not generated code samples.

## Council and writing-contract check

The local `skills/write-paper/SKILL.md` workflow was applied to revision work on
the two manuscripts. Its full methods-section structure applies to
`paper/draft.md`; the distinct catalogue resource paper retains its resource
study structure. No governance document was amended.

Six actual clause-review agents checked OVR, SEL, SRC, CNF, ANC and SYC, in
bounded overlapping waves because of the seven-agent limit. Round 1 found one
incorrect pointer to where confidence intervals were stored. That sentence was
corrected; the historical objection is preserved. Round 2 rechecked that change,
the literal micro-attribution counts and the p-value qualification. Round 3
rechecked only the final provenance paragraph with OVR and SRC. The accompanying
reports state the scope and manuscript hash of each round.

These are same-platform agent reviews with shared project context, not an
independent human replication or Odysseus's feedback.

| Gate | Result and interpretation |
|---|---|
| PAP-SCO-01..04 | PASS for the methods paper: clause-grounded advisory thesis, six-page budget, no factuality-SOTA claim, explicit distinctions from Trace-Based Assurance, RFCAudit and AgentVerify. |
| PAP-SRC-01..05 | PASS within the documented access and provenance bounds. Raw outputs and historical logs support the reported results; metadata checks support bibliography identity. Missing settings remain unknown, historical checking is attributed to its logs, and no unchecked claim is presented as newly verified. |
| PAP-STR-01..04 | PASS for the methods paper: required section order, related-work families, easy/hard four-condition supplement and separate metrics. Independent annotation/adjudication/kappa are named as missing work, not invented completed results. FaithBench's near-50% figure is limited to its hard summarization benchmark rather than asserted as a universal ceiling. |
| PAP-FMT-01..05 | PASS: plain prose, no en/em dashes, experimental aliases, no resource excuses. Both editorial pattern scores are 1/10, below the threshold of 2; these scores are not authorship probabilities. |
| PAP-QUA-01..03 | PASS after the scoped rechecks: no unresolved clause blockers; the original finding and concrete fix remain in the review history. |
| PAP-WORK-01..06 | Revisions, reusable committed scripts, generated publication artifacts and validation were completed without another approval gate. Publication verification remains a distinct check after merging. |

Reports:

- `paper/reviews/paper-council-bias-2026-11-09.md`
- `paper/reviews/paper-council-prose-2026-11-09.md`

## Validation and reproducibility

`experiments/check-research-results.py` passes 16 regression checks, including
shadow reviewer names, hash tampering, duplicate cases, order/identity changes,
invalid verdicts, exact-rule scoring and generated-summary reproduction.
`experiments/check-research-papers.py` checks all numerical tables against the
frozen results, the full source hash in PDF metadata, six-page PDF copies,
identical standalone LaTeX, and a byte-identical repeated PDF/HTML build.

The local browser check passed at 390, 768 and 1440 pixels with JavaScript
disabled: readable paper, two homepage paper cards, 434 catalogue records,
working PDF bodies and no horizontal overflow. All 17 internal page/asset
targets and their local fragments resolve, with no duplicate HTML IDs. The
existing structural page validator also passes with all 11 ontology categories.
The first browser attempts lacked sandbox socket access; repeating with the
environment's network grant passed without weakening TLS or browser checks.

For a deployed revision, run:

```bash
python3 experiments/check-research-results.py
python3 experiments/check-research-papers.py --rebuild --browser
python3 experiments/check-unified-catalogue.py
python3 experiments/validate-page.py
python3 experiments/check-research-papers.py --live https://ethicalai.alexandrudan.com/
```

The live command requires successful HTTPS responses and exact body hashes for
the tested pages and their linked assets. A push alone is not a verified
deployment. The arXiv build prepares a local source archive only; submission is
outside this revision.

## External feedback and remaining research

Odysseus was contacted through Maildown at 07:23 and 07:37 UTC on November 9.
The latest check during this revision still showed no new response. None of the
changes or council verdicts is attributed to him. A later reply can be assessed
against the pinned revised manuscripts rather than assumed to endorse them.

Independent human labels, held-out cases, blind clause routing or all-clause
aggregation, cross-family repeated runs, recorded backend/settings/costs,
severity calibration and downstream human-use evaluation remain uncompleted
research. The manuscripts now state those limits; editorial revision does not
replace these experiments.
