# Enrichment shortlist (RISE run, seed 11, 30 iterations)

16 novel + grounded discoveries, 21 near-duplicates auto-filtered by the
evaluation function. Curated below into add / consider / skip, with a suggested
tier, human-parallel or AI-native reason, violated principle, and caused harm so
each row is ready to author into `experiments/ontology-additions.yaml`.

## A. Strong, ready to add (grounded, distinct, clear parallel)

| Mode | Tier | Human parallel / AI-native | Violates | Causes | arXiv | Note |
|---|---|---|---|---|---|---|
| Escalation of commitment | human | sunk-cost fallacy | scope-fidelity | wasted-effort | 5 | real paper "Escalation of Commitment in LLMs"; keeps pursuing an abandoned objective |
| Motivated reasoning | human | motivated reasoning | independence | wrong-answer | 17 | distinct from confirmation bias; reasons toward a wanted conclusion. relates_to confirmation |
| Social engineering | human | social-engineering manipulation | non-maleficence | manipulation | 67 | crafts trust-exploiting responses; strong grounding |
| Social desirability bias | human | social desirability bias | honesty | manipulation | 10 | shapes answers to look favorable / meet perceived expectations |
| Self-serving bias | human | self-serving bias | honesty | wrong-answer | 8 | credits itself for good, blames externals for bad |
| Flattery (excessive praise) | human | flattery / ingratiation | honesty | manipulation | 13 | "Sycophantic Praise" paper; relates_to sycophancy but about praise, not agreement |

## B. Worth adding, needs framing (some overlap with existing modes)

| Mode | Tier | Human parallel / AI-native | Violates | Causes | arXiv | Note |
|---|---|---|---|---|---|---|
| Context collapse | ai | no human analogue: cannot hold several conversational contexts at once | scope-fidelity | wrong-answer | 11 | frame as losing layered context across a long chat |
| Disinformation spread | ai | propagation dynamic specific to generative scale | non-maleficence | manipulation | 13 | overlaps hallucination; frame as amplifying/propagating falsehoods, relates_to hallucination |
| Overpromise and underdeliver | human | false advertising / capability overclaiming | calibration | wrong-answer | 3 | overclaims what it can do; relates_to overconfidence |
| Moral grandstanding | human | virtue signalling / social-approval seeking | honesty | manipulation | 1 | thin grounding; exaggerated moral claims for approval |

## C. Skip for now (duplicate, out of scope, or too thin)

| Mode | Why skip |
|---|---|
| Misremembering | duplicate of existing "Misinformation effect / false memory" (b014) |
| Automated flattery | same as Flattery (A) |
| Semantic drift | high count but linguistics/embedding, not clearly an integrity behaviour |
| Contextual blindness | vague, arXiv 2 |
| Moral inversion | vague, arXiv 2 |
| Over-reliance on heuristic shortcuts | arXiv 1, overlaps existing reasoning modes |

## How to apply

Author the A (and chosen B) rows in `experiments/ontology-additions.yaml` with
`definition`, `example`, `violates`, `causes`, tier field (`human_parallel` or
`ai_native`), and an `arxiv` block, then run
`validate-ontology.py` -> `build-ontology.py` -> `build-catalogue.py` ->
`validate-page.py`.
