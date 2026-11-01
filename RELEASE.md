# Release and citation

This repository is intended to be a citable resource: a grounded catalogue of AI integrity
failure modes plus the auditing method built on it. This file is the checklist for turning
the current state into a versioned, DOI-bearing release, and it records the one decision
that needs the author's explicit sign-off: the license.

## The one decision that needs your sign-off: license

The repository is public but has no license file, which under default copyright means all
rights reserved and no one may reuse the catalogue. A resource paper needs an explicit
license for the catalogue to be usable and cited. The recommendation, matching the project's
permissive, no-non-commercial stance:

- **Catalogue data** (`ontology/ethical-ai.yaml`, the rendered site, the references): **CC-BY-4.0.**
  Attribution-required, redistribution allowed, no non-commercial restriction. Attribution is
  what drives citation, which is the goal.
- **Code** (`experiments/`, build and audit scripts, judges): **Apache-2.0.** Permissive, with
  an explicit patent grant.

Nothing in the repo asserts this license as operative yet. `CITATION.cff` and the ontology
`meta.license` carry it as a provisional recommendation only. On your sign-off, the single
remaining step is to add the `LICENSE` file(s); until then do not publish or mint a DOI.

If you prefer different terms (CC0 for maximum reuse, or CC-BY-SA for copyleft), say so and
the two files above get updated in one pass.

## Release checklist

1. Confirm the license (above). Add `LICENSE` (Apache-2.0, root) and `LICENSE-data` or a
   `docs/LICENSE` note (CC-BY-4.0 for the catalogue).
2. Confirm `meta.version` and `CITATION.cff` version agree (currently 1.0) and the dates are
   current.
3. Run the full build and gate: `build-ontology` to `validate-ontology` to `build-catalogue --write`
   to `build-ontology-map` to `validate-page`, all passing, zero em or en dashes.
4. Tag the release: `git tag -a v1.0 -m "EthicalAI catalogue v1.0"` and push the tag.
5. Mint the DOI. Connect the GitHub repo to Zenodo (zenodo.org, GitHub integration, toggle the
   repo on), then publish the v1.0 GitHub release. Zenodo mints a DOI automatically and a
   version-independent concept DOI. Add the DOI back into `CITATION.cff` (`doi:` field) and the
   ontology `meta`.
6. Post the paper to arXiv with the Zenodo DOI cited as the artifact, and the GitHub release
   tag in the paper's reproducibility note.

Steps 4 to 6 are author actions (they publish outward and are hard to reverse); this file
prepares everything up to them. Steps 1 to 3 are in-repo and reversible.

## What a citing reader gets

- A stable catalogue with stable `id` and `num` per mode (see `ontology/SCHEMA.md`, stability
  contract).
- A machine-readable file (`ontology/ethical-ai.yaml`) and a human-readable site.
- A documented schema and an eight-type relation graph.
- Provenance: every grounded mode tied to a primary paper, with the citation-drift and
  verification-sweep records (`experiments/citation-audit.md`, `experiments/verification-report.md`)
  stating how reliable that grounding is.
