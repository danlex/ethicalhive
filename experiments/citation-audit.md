# Citation audit

A running record of failure modes whose cited paper does **not** support the
claim, caught while grounding examples by reading the source rather than trusting
the reference. This is the source-fabrication failure mode found in our own
artifact: each entry is held back from the grounded-examples set until it gets a
paper that genuinely supports it, or is reclassified as an analogy with no direct
AI evidence yet.

Method: for each mode, the cited paper (from `catalogue-papers.json`) was read in
full-text HTML. A mismatch means the paper is about a different phenomenon, draws
the opposite conclusion, or carries no evidence for the behaviour as defined.

| Mode | Cited paper | Why it does not support the mode |
|---|---|---|
| Introspection illusion | arXiv:2606.32038 | Argues the **opposite**: with the right training, model self-explanations can be faithful to their own computation (introspective coupling, r=0.89). Evidence against the illusion, not for it. |
| Perceptual filling-in | arXiv:2409.17173 | About **detecting** hallucinations via a fill-in-the-blank exam, not about the model inventing content to fill a perceptual gap. Different phenomenon. |
| Metacognitive monitoring | arXiv:2608.15400 | A proof-of-concept framework with a demo UI. No empirical calibration study, no case where confidence diverges from correctness. No evidence. |
| Base-rate neglect | arXiv:2406.11634 | About answer-**label** probability bias (preferring option A/B/C/D) in multiple-choice testing, not neglect of statistical priors in reasoning. Different phenomenon. |
| Belief perseverance | arXiv:2104.08401 | Covers uncorrected inconsistent beliefs the model will not self-fix, and the paper itself states these are **not** classic perseverance (clinging to a belief after its evidence is retracted). |
| Hard-easy effect | arXiv:2509.26306 | About dynamic interaction strategy and IRT difficulty estimation, not overconfidence on hard items / underconfidence on easy ones. No calibration-by-difficulty result. |

## Disposition

Each held mode needs one of:

1. **Re-cite** — find and read a paper that genuinely demonstrates the behaviour,
   then ground three examples from it (removes it from this table).
2. **Reclassify** — if no direct AI evidence exists, mark the mode as an analogy
   with no measured AI instance yet, so the page does not imply grounding it
   lacks.

This table is the authority for the "Citation drift" item in the site's
"What building this is turning up" section; keep the two in sync.
