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
- **mitigations** — how failures are caught (Chain-of-Verification, clause judges,
  the contract, human decision).
- **governance** — the approval bar for calibration vs constitutional changes.
- **families** — the catalogue groupings.
- **modes** — one record per failure mode. Fields: `id`, `num`, `name`,
  `definition`, `example`, `family`, `group_label`, `highlighted`
  (+`highlight_order`), `tag` (shipped | research | page | analogy), `origin`
  (discipline), `measurability` (draft | multi-turn | undetectable),
  `contract_clause` (if a shipped check), `same_as` (when two entries denote the
  same underlying failure), and `arxiv` (count + top-3 papers).

The page currently renders 130 mode records: 26 highlighted, 100 brain-parallel,
4 agentic/engineering. Thirteen highlighted modes restate a brain mode and carry a
`same_as` link; that overlap is the project's deliberate "featured on top,
catalogued below" structure, recorded explicitly rather than hidden.

## Editing

1. Edit `ethical-ai.yaml` (add or change a mode, principle, relation).
2. `python3 experiments/build-catalogue.py --write` rebuilds the catalogue grid
   in `docs/index.html` from the ontology.
3. `python3 experiments/validate-page.py` checks tag balance and counts.
4. Commit `ontology/ethical-ai.yaml` + `docs/index.html`.

## Provenance

`experiments/build-ontology.py` is a **one-time migration** that seeded this file
from the previously scattered sources (`shipped-checks.tsv`, `catalogue-extra.tsv`,
the neuroscience-parallels markdown, `catalogue-examples.tsv`, and the two papers
JSON files). Those files are retained for provenance and to allow a re-seed, but
they are no longer read by the page build. The ontology is authoritative.

## Next enrichment (not yet done)

Per-mode `relations` beyond `same_as`: `violates` (which principle), `causes`
(which harm), `relates_to` (adjacent modes), `root_of` / `opposite_of`. These turn
the catalogue into a navigable graph and let overlaps and gaps be found
mechanically instead of by eye.
