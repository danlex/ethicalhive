# Ethical AI ontology

`ethical-ai.yaml` is the single source of truth for the project's integrity model.
The page at ethicalai.alexandrudan.com is built from it, and it is meant to be the
one place a failure mode or principle is defined.

## Structure

- **meta** — name, version, date, mode count.
- **relation_types** — the vocabulary for links between entries (`is_a`,
  `relates_to`, `root_of`, `opposite_of`, `same_as`, `violates`, `causes`,
  `detected_by`).
- **principles** — the values an agent should uphold (honesty, calibration,
  non-maleficence, scope-fidelity, independence, transparency, corrigibility).
- **harm_types** — what a failure costs (wrong answer, wasted effort, manipulation,
  security breach, loss of oversight).
- **mitigations** — how failures are caught or prevented: the shipped checks
  (Chain-of-Verification, clause judges, the contract, human decision) plus
  literature methods (retrieval grounding, self-consistency, abstention training,
  non-sycophantic preference tuning, input-output isolation, oversight monitoring).
- **governance** — the approval bar for calibration vs constitutional changes.
- **families** — the catalogue groupings.
- **modes** — one record per failure mode. Fields: `id`, `num`, `name`,
  `definition`, `example`, `family`, `group_label`, `highlighted`
  (+`highlight_order`), `tag` (shipped | research | page | analogy), `origin`
  (discipline), `measurability` (draft | multi-turn | undetectable),
  `contract_clause` (if a shipped check), `same_as` (when two entries denote the
  same underlying failure), and `arxiv` (count + top-3 papers).

The page renders all 434 records once in the eleven ontology categories, using
`category` for membership and `group_label` for each heading. Row numbers are not
displayed. Stable reference numbers remain in the ontology and exports, preserving
the existing order and citations; grouping does not renumber them.
Overlap relationships are cross-references between the relevant rows,
not hidden nested entries or a second visible count. The inventory contains the
previous 207 records and 227 proposed human-behaviour analogies; numbering does
not establish psychological synonymy or independent validation. Of all records, 395 are human-paralleled
and 39 AI-native, with 26 highlighted entries.
The added records include 128 with a human-definition source consulted and 99
whose source check is pending. AI parallels remain untested. The paper and
reported experiments describe the original 207-entry baseline.
Highlighted entries are styled in place within their category; they are not
rendered as a second featured copy. The operational-overlap review and explicit
`grouped_under` records describe the current grouping decisions.

## Editing

1. Edit `ethical-ai.yaml` (add or change a mode, principle, relation).
2. `python3 experiments/validate-ontology.py` checks the graph: required fields,
   unique ids, every relation target resolves, every principle and harm is
   referenced, enumerated fields are in range.
3. `python3 experiments/build-catalogue.py --write` rebuilds the catalogue grid
   in `docs/index.html` from the ontology.
4. `python3 experiments/validate-page.py` checks tag balance and counts.
5. Commit `ontology/ethical-ai.yaml` + `docs/index.html`.

The page build also exports `docs/behaviours.csv` and `docs/behaviours.json`.
These exports have 434 rows/objects in 1–434 reference order, independent of the
category-grouped page. Category fields preserve the same memberships. The
`grouped_under` and `grouping_reason` fields preserve the overlap relationships
without nesting or repeating records. Public and YAML `meta.mode_count` both
count all 434 records. The grouping
review is `references/semantic-dedup-review-2026-11-06.json`.
The targeted terminology follow-up is
`references/terminology-review-2026-11-07.json`. It records corrected aliases,
operational boundaries and subtype decisions, not a complete semantic deduplication.
Former research-page URLs redirect to `/#catalogue`; older download URLs are
aliases of the same full export. Research snapshots and reconciliation records
are preserved in `references/`. The one-time integration is recorded in
`references/catalogue-integration-2026-11-06.json`.

## Two tiers: human-paralleled vs AI-native

Every mode carries exactly one of:
- **`human_parallel`** — a named human-psychology construct and its AI analogue
  (e.g. gaslighting, cognitive dissonance, wireheading). These sit in the ten
  brain-system groups.
- **`ai_native: true`** — a failure with no genuine human analogue, tied to the AI
  substrate (jailbreak, prompt leaking, data contamination, emergent misalignment,
  reward hacking, prompt injection). These sit in the single **AI-native
  behaviours** group.

The rule for adding a mode: it must state a human parallel, or be explicitly
`ai_native`. `validate-ontology.py` **rejects any mode that has neither or both**.
A few modes that were mislabeled as engineering (automation bias, survivorship
bias, noble cause corruption, anthropomorphism) were moved to the human side under
this rule. New modes are authored in `experiments/ontology-additions.yaml`.

## Relations and terminology

Ordinary modes carry `violates` (principle ids) and `causes` (harm ids); proposed
analogies may leave these empty. `relates_to` connects adjacent concepts and
`synonyms` stores genuine alternative names. The initial relations were seeded by
category defaults plus per-mode overrides in
`experiments/build-ontology.py` (PRIN_BY_CAT / HARM_BY_CAT / PRIN_OVERRIDE /
HARM_OVERRIDE / RELATES / SYNONYMS). The page surfaces `violates`, `causes`,
`relates_to` and `synonyms` in each row's Details and in the map's node panel.
Also carries `opposite_of` (contrasting pairs), `root_of` (causal drivers), and
`detected_by` (which mitigation catches it). `is_a` represents a narrower record
within a broader operational family, such as tool over-privilege within
tool-selection error. Both directions are visible in the list and map.

`concept_boundary` explains how reviewed concepts differ. `related_terms` holds
named concepts that have no separate numbered record, with `name`, `relation`
and `note`; they are explicitly not aliases. For example, prospect theory is a
broader theory than loss aversion, and membership inference is a distinct attack
goal from training-data extraction. `terminology_sources` discloses source title,
URL and access depth. These fields are preserved in JSON and CSV. The targeted
review does not establish a unique-concept count or validate the AI analogies.

## Provenance

`experiments/build-ontology.py` is a **one-time migration** that seeded this file
from the previously scattered sources (`shipped-checks.tsv`, `catalogue-extra.tsv`,
the neuroscience-parallels markdown, `catalogue-examples.tsv`, and the two papers
JSON files). Those files are retained for provenance and to allow a re-seed, but
they are no longer read by the page build. The ontology is authoritative.

## Further review

Semantic normalization remains incomplete. Matching names is not sufficient to
establish identical definitions or mechanisms. Review aliases, operational
boundaries and source evidence before merging further records or claiming a
distinct-behaviour count.

