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

## The eleven categories

Ten cognitive systems: Perception, Memory, Attention, Heuristics, Reasoning,
Metacognition, Language, Social, Moral, Self & agency. Plus one tier with no human
analogue: AI-native. Category assignment reproducibility is reported in the paper
(Cohen kappa 0.83 to 0.93 between independent raters and the catalogue).

## Relations and external terminology

`is_a`, `relates_to`, `root_of`, `opposite_of`, `same_as`, `violates`, `causes`,
`detected_by`, plus the `grouped_under` operational-overlap cross-reference.
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

