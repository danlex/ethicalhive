# EthicalAI ontology schema

The machine-readable catalogue is `ontology/ethical-ai.yaml`, a single YAML document. This
file documents its structure so the catalogue can be reused without reading the build
scripts. `build-ontology.py` was a one-time migration; the YAML is now authoritative
and is validated by `experiments/validate-ontology.py`.

## Top-level keys

| Key | Type | What it holds |
|---|---|---|
| `meta` | object | name, version, updated date, author, repository, homepage, license, schema, cite |
| `relation_types` | object | catalogue edge types and a one-line gloss of each |
| `principles` | list | the integrity principles a mode can `violate` (id, name, statement) |
| `harm_types` | list | the harms a mode can `cause` (id, name, statement) |
| `mitigations` | list | the mitigations a mode can be `detected_by` (id, name, statement) |
| `governance` | object | the change-control rules for the catalogue itself |
| `families` | list | notes on the grouping into ten cognitive systems plus engineering groups |
| `modes` | list | the failure modes, one object each (see below) |

## A mode object

| Field | Type | Required | Meaning |
|---|---|---|---|
| `id` | string | yes | stable slug identifier, e.g. `b101-source-fabrication`; stable across versions |
| `num` | int | yes | stable reference shown as Reference ID in expanded entry/map details and retained in exports; absent from collapsed rows |
| `name` | string | yes | human-readable mode name |
| `definition` | string | yes | one-sentence operational definition |
| `category` | string | yes | one of the eleven categories (ten cognitive systems plus `AI-native`) |
| `family` | string | yes | finer grouping slug within a category |
| `group_label` | string | no | display label for the family |
| `tag` | string | yes | evidence status: `research` (grounded in a read paper), `analogy` (cognitive-science analogy), `shipped` (an active EthicalHive check), `page` |
| `origin` | string | no | provenance note |
| `measurability` | string | no | how the mode can be measured |
| `highlighted` | bool | no | surfaced on the site's highlighted set |
| `human_parallel` | string | no | the named human cognitive failure this parallels (empty for AI-native) |
| `example` | string | no | one illustrative or grounded example (grounded examples carry an inline `[arXiv:id]` tag) |
| `arxiv` | object | no | `{count, papers:[{id, year, title}]}` for the modes grounded in literature |
| `selected_papers` | list | yes | zero to three selected research citations; target three, with explicit shortfalls |
| `literature_search` | object | yes | independent measured query total with source, scope, query, filters, URL, date and status |
| `violates` | list | no | principle ids this mode breaches |
| `causes` | list | no | harm-type ids this mode produces |
| `is_a` | list | no | broader family-mode ids; must form an acyclic hierarchy |
| `synonyms` | list | no | genuine alternative names, not broader theories, subtypes or related concepts |
| `concept_boundary` | string | no | reviewed distinction from overlapping or adjacent concepts |
| `related_terms` | list | no | external named concepts: `{name, relation, note}`, explicitly not synonyms or additional catalogue records |
| `terminology_sources` | list | no | sources supporting distinctions: `{title, url, consulted}` with actual access depth |
| plus graph edges | list | no | `relates_to`, `root_of`, `opposite_of`, `same_as`, `detected_by`, `mitigated_by` per `relation_types` |

## Proposed human-behaviour analogies in the same list

The catalogue contains 434 records: 207 previous entries plus 227 integrated
research analogies. These are not 434 independently validated AI mechanisms.
The current view displays all 434 records in eleven ontology categories, without
visible row numbers. Internal `num` order is preserved within each category.
Reference numbers remain stable and exports retain global `num` order. Nine
overlap links remain explicit. A linked record carries `grouped_under`, `grouping_reason`
and `grouping_relation`; its stable ID, number, definition and sources remain.
This is an operational-overlap cross-reference, not an automatic `same_as` or
`is_a` assertion. Explicit subtype links may independently be assigned after review. Groups
must target a primary record directly; chains, cycles and missing targets fail
validation. Public JSON, CSV and YAML all retain the flat numbered registry.
New records carry `research_candidate: true`, `tag: analogy`, `source_check`,
`ai_evidence_status`, `proposed_ai_manifestation`, `research_boundary`, and
`definition_sources` with explicit access depth. Uploaded source claims remain in
`research_provenance`. Empty `violates` and `causes` lists are allowed for these
records: a named human process can be adaptive, and a harm or principle breach
must not be invented just to fill a graph field. Ordinary records retain the
existing validation requirements. `research_notes` can enrich an existing entry
when a candidate was already indexed as an alias.

Definition sources may carry `publication` metadata for a reviewed research-paper
link: `type` (`journal-article`, `proceedings-article`, or `posted-content`),
`authors`, `year`, `venue`, `doi` when available, `evidence_scope`,
`verification_url`, and `verified_date`. These legacy records are normalized into
canonical selections labelled **Human and related research**. Legacy `arxiv`
records supply the original **AI research** citations; new selections may also
include AI papers from other scholarly publishers. A publication record confirms a citation's
identity and stated relevance; it does not automatically change `source_check`,
the entry's analogy status, or establish empirical AI evidence. Access depth
remains explicit in `consulted`; books, chapters and reference pages are not
counted as research papers.

The catalogue CSV includes a derived `research_papers` JSON column containing
the typed human/related source records. `docs/source-coverage.json` and `.csv`
report coverage for all stable IDs. Their counts describe linked sources, not
an exhaustive search of all literature or a count of established AI mechanisms.
The Research papers and Missing papers filters use these linked citations.
Definitions to check still refers to pending definition-source review, which is
separate from bibliography availability. Recovered AI citations may disclose
`relevance`, `consulted`, `verified_date` and `verification_url`; `arxiv.count`
remains null when only individual citations were checked and no query total was
measured.
Row paper counts use `literature_search.count`, independently of the number of
selected citations. Current totals are arXiv metadata-query matches in cs.AI,
cs.CL and cs.LG. They are a reproducible search proxy, not full-text citation
counts, all-fields totals or manually verified topical-paper counts. Keyword
matching and stemming can include unrelated uses. Each record stores the actual
query, filters, API URL, retrieval timestamp, database and scope. An unavailable
total is `null` and displays a dash; a successful zero-result search displays 0.
Do not derive totals from a top-k response or a paper's cited-by count. Historical
`arxiv.count` values remain separately labelled with their missing search dates.

`selected_papers` is the canonical bibliography for the catalogue, map, index and
downloads. The target is three distinct publications per entry. Fewer selections
remain an explicit gap, not an invitation to add unrelated sources. Each record
contains `id`, `title`, `url`, `year`, `venue`, `authors` when available,
`publication_type`, `domain` (`ai` or `human-related`), `relevance`, `consulted`,
and `verification_url`. DOI/arXiv versions and matching publication titles are
deduplicated. Selected citations may include empirical, theoretical and review
papers or preprints; they need not all be positive evidence. Metadata-only access
is labelled as such. Books, chapters, reference pages, book reviews, meeting
abstracts and registry entries do not fill research-paper slots. Publication
identity and topical relevance do not establish an AI analogy or alter the
definition-source status. Legacy `arxiv.papers` and `definition_sources` remain
unchanged for historical traceability; `source_reference` records their origin.

The CSV includes `selected_papers` and `literature_search` JSON columns. Its older
`research_papers` column retains the legacy typed human/related source records.
Coverage exports report selected-link counts and independent search totals in
separate fields. `meta.literature_review.record` points to the selection/count
audit, including shortfalls, source access and rejected matches.

`meta.paper_source_review.record` points to the latest bibliography review. Its
`previous_review` pointer retains earlier reviews; `previous_record` in the meta
block exposes the immediately preceding record. Each increment records source
additions, citation access depth, rejected matches and retained paper gaps.
Definition-status changes additionally require an individual source ID, passage
locator and reason. A checked definition passage can come from a book or reference
page without closing the separate paper-link gap. AI recognition benchmarks do
not change an entry's untested-analogy status. Source-trace validation follows the
review history so earlier accepted citations remain accountable.

## Annual research timelines

`docs/literature-timelines.json` and `.csv` contain a separate, dated annual-search
snapshot keyed by stable mode ID. `experiments/literature-timelines.py fetch`
collects the actual scoped arXiv query recorded in `literature_search.url`;
`build` produces the public files. The existing catalogue row totals retain their
own retrieval dates. Different snapshots need not have identical totals.

The unit is matching publications per year of **first arXiv submission**, within
cs.AI, cs.CL and cs.LG. This is neither a count of individual word occurrences nor
a full-text citation count. Current indexed versions can contain terms added in a
later revision, so this graph cannot establish when a term was first used. The
year of retrieval is marked incomplete. A complete series must reconcile with
the provider's total; missing, failed or incomplete searches have no annual
counts and must not be plotted as zero. Complete zero-result searches are
distinct from unavailable data.

Large result sets use disjoint submission-year counts instead of a truncated
page. The snapshot retains queries, source URLs, retrieval dates, coverage status
and collection method. Raw publication identities and dates are retained in the
fetch cache for metadata-based series. The timeline does not alter a record's
selected bibliography, definition-source status or empirical AI evidence.
An existing exhaustive zero-result search can be reused with its **original**
retrieval date and an explicit `historical_zero_snapshot` marker. Its recorded
total determines all annual values in that dated interval; no fresh search is
claimed and years after that original retrieval year are not filled with zero.

## The eleven categories

Ten cognitive systems: Perception, Memory, Attention, Heuristics, Reasoning,
Metacognition, Language, Social, Moral, Self & agency. Plus one tier with no human
analogue: AI-native. Category assignment reproducibility is reported in the paper
(Cohen kappa 0.83 to 0.93 between independent raters and the catalogue).

## Relations and external terminology

`is_a`, `relates_to`, `root_of`, `opposite_of`, `same_as`, `violates`, `causes`,
`detected_by`, `maps_to` (crosswalk to an external framework), plus the `grouped_under`
operational-overlap cross-reference.
Glosses are in the `relation_types` block of the YAML. Together they form
the relation graph that lets the catalogue represent a real incident as a chain of modes
rather than a single label.

`related_terms.relation` currently allows `broader theory`, `broader concept`,
`distinct related concept`, `negative counterpart`, `proposed mechanism` and
`narrower variant`. These are relationships to named terms without numbered mode
ids, not extra graph nodes or entries. A term cannot be both a synonym and a
related non-synonym on the same record. The targeted terminology review in
`references/terminology-review-2026-11-07.json` preserves before/after values and
source-access limits. It does not establish a total of distinct concepts.

## Stability contract

`id` and `num` are stable identifiers: once assigned to a mode they are not reused for a
different mode. New modes take new ids and the next free num. A mode that is merged or
retired keeps its id with a `same_as` or a deprecation note rather than being deleted, so
external citations do not break. Breaking changes bump `meta.version`.

