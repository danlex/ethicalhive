# Verification sweep

An adversarial re-check of the grounded examples: for a sample of modes, a
fact-checker re-read the cited paper and confirmed whether the specific numbers,
model names, and claims in each example actually appear in it. Run as a 50-agent
workflow (`verify-grounding`), one skeptical checker per mode, each instructed to
mark NOT_FOUND rather than give the benefit of the doubt.

This is the honesty gate on the resource, and it is itself a result: even careful
grounding from reading the source carries a measurable error rate on exact figures.

## Result (sample of 50 modes, ~140 tagged examples)

| Outcome | Modes | Share |
|---|---|---|
| Clean (all examples supported) | 30 | 60% |
| Minor issue (number off / loose attribution / mislocated) | 11 | 22% |
| **Hard error (a figure contradicted or not in the paper)** | **9** | **18%** |
| Paper unreachable | 0 | 0% |

All 20 flagged modes were corrected in the same pass. The hard errors were genuine
over-reads, not fabrications of whole findings: in every case the behaviour and the
paper were right and the direction held, but a specific number was wrong.

## Hard errors found and fixed

| Mode | What was wrong | Fix |
|---|---|---|
| Tool over-privilege | "zero privilege bias with no prior error" | paper: 5 selections at PED=0, not zero |
| Hallucination | wrong city given as "Jeddah" | paper's example says "Dammam" |
| Spotlight vs zoom-lens | conditional accuracy "0%" | paper: 2.6% for BM25 |
| Moral disengagement | "10 to 15% of criminal-trait distribution" | not in paper; replaced with frame-up finding |
| Mere-exposure effect | "lift grows with exposure" | exposure fixed at 5, no dose-response; claim dropped |
| Self-contradiction | 5+5x5=50 attributed to the hallucination survey | not in that paper; example un-tagged (illustrative) |
| Over-refusal | "6.4% overall, 52% fictional privacy" | paper: 6% and 45% |
| Prompt leaking | recovered Claude 3 prompt "verbatim" | high fidelity, a few sentences off |
| Diversity collapse | collapse attributed to the across-prompt axis | paper: the sharp collapse is per-prompt |

## Minor issues found and fixed

Semantic override (33.3% in all three models, not two); Priors overriding evidence
(a confirmation-bias line was Xie et al.'s, re-worded as illustrative); Anchoring
(62.2% was a specific condition, generalised away); Overprecision (used the
verified 0.61-0.87 range); False-belief tracking (standard-vs-transparent mislocated
and an 85% baseline that was GPT-3.5's); Semantic satiation (dropped an unstated
"500" count); Deceptive alignment (12% -> 14%); Overpromise (dropped an unsupported
"still signalling completion" rider); Chain-of-thought unfaithfulness ("426" -> "400+",
"never" -> "almost never, one instance"); Negation blindness ("type of" -> "kind of").

## Reading

A ~18% hard-error rate on exact figures, from grounding done by actually reading
the papers, is the same lesson as the citation audit at the next level down: even
with the right paper in hand, specific numbers drift on transcription. The sweep
converts that from an unknown into a measured, corrected quantity. A full sweep of
all 186 grounded modes (not just the 50-mode sample) would extend this; the sampled
rate is the planning estimate for how many corrections that would surface.
