# Verification sweep

An adversarial re-check of the grounded examples: for each mode, a fact-checker
re-read the cited paper and confirmed whether the specific numbers, model names,
and claims in each example actually appear in it. Run as a set of workflows
(`verify-grounding`), one skeptical checker per mode, each instructed to mark
NOT_FOUND rather than give the benefit of the doubt.

This is the honesty gate on the resource, and it is itself a result: even careful
grounding from reading the source carries a measurable error rate on exact figures.

## Coverage

Of the 186 grounded modes, **164 have now been swept** across three runs (a 50-mode
pilot sample plus two 68-mode batches). The remaining 22 modes were queued in the
second batch but hit a provider session limit before their checkers ran; they are
listed at the end and are the obvious next pass.

## Result (164 modes swept, ~470 tagged examples)

| Outcome | Modes | Share |
|---|---|---|
| Clean (all examples supported) | 107 | 65% |
| Minor issue (number off / loose attribution / mislocated) | 35 | 21% |
| **Hard error (a figure contradicted or not in the paper)** | **22** | **13%** |
| Paper unreachable | 0 | 0% |

All 57 flagged modes were corrected in the same pass. The hard errors were genuine
over-reads, not fabrications of whole findings: in almost every case the behaviour
and the paper were right and the direction held, but a specific number, model name,
or causal framing was wrong. Two hard errors (gaslighting, dual-process moral
judgment) were cases where a quoted example did not exist in the cited paper; those
examples were rewritten to the paper's actual content or demoted to untagged,
illustrative scenarios.

## Hard errors found and fixed (22)

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
| Source-monitoring error | DiffGR "0.66 to 0.70" | wrong scale; values are percentages (~68 to 85) |
| Serial position effect | "middle collapses to 28% vs 56% start" | numbers misassembled; the 28% is kg+CoT at one mid position |
| Representativeness | classic "feminist bank teller" as a model result | intro motivation only; generalised to the measured subset-over-superset error |
| Uncertainty communication | "identical TriviaQA ... training-data bias" | it is MMLU; no training-data-bias claim |
| Feeling-of-knowing | "elicit confidence after the answer" | reversed; paper distills a reliable pre-answer signal |
| Hindsight bias | "drops to near zero vs 5.5%" | masking reduces but does not erase; stays ~3 to 5% |
| Dual-process (S1/S2) | "the survey finds models default ..." | position paper, no such finding; reframed to CoT-as-coercion |
| Dual-process moral judgment | water dilemma + "identical rationales = post-hoc" | not in paper (paper treats the similarity as a benefit); rewritten |
| Pragmatic over-accommodation | reply attributed to "gpt-o3" | paper attributes it to a different model; generalised |
| Reward hacking | Boat Race "12.66 observed vs 9.43" | labels reversed; paper: 9.43 observed, 12.66 hidden |
| Gaslighting | flute and marriage examples | not in the paper; demoted to untagged illustrative |
| Collusion | "insider-trading scenario" | paper's example is a job-candidate evaluation; rewritten |
| Foot-in-the-door | "Claude most defensible at 83.3%" | 83.3% is an attack-success rate; GPT-4/Claude-2 resist best (~65-68%), ChatGLM-2 most vulnerable (98.3%) |

## Minor issues (35)

Thirty-five modes had a verdict of PARTIAL on at least one example: a number loosely
rounded, a mechanism label slightly off, a figure from an adjacent condition, or a
model attribution omitted. Representative fixes: Deceptive alignment 12% -> 14%;
Chain-of-thought unfaithfulness "426" -> "400+"; Emotional contagion rounded shares
corrected to 11.5 / 53.8 / 34.6; Identity stability start value 2.5 -> 1.5 and the
verbosity range restated as 1.5x to 10x; Bystander effect / Alignment hallucination
internal-vs-external pair corrected to 0.71 vs 0.37 (matched condition); Dark triad
average 85.6 -> 85.2; Performative hedging Gemini few-shot 0.70 -> 0.53; Flattery
figures attributed to GPT-5.4; Tangentiality "Barack Obama" (an authored illustration,
not a model output) dropped. All were corrected in place.

## Unverified (22 modes, session-limited)

Goal drift, Abstention failure, Jailbreak susceptibility, Oversight subversion,
Goal-guarding, Prompt infection, Emergent misalignment, Goal misgeneralization,
Data contamination, Package hallucination, Training-data extraction, Insecure code
generation, Sabotage, Shutdown avoidance, Reward-model overoptimization, Unbounded
consumption, Model collapse, Encoded reasoning, Attribute inference, Tool-selection
error, Knowledge-cutoff staleness, Low-resource language degradation. These were
queued but their checkers were cut off by a provider session limit; re-running them
completes the full-grounded sweep.

## Reading

A ~13% hard-error rate on exact figures, from grounding done by actually reading the
papers, is the same lesson as the citation audit at the next level down: even with
the right paper in hand, specific numbers and causal framings drift on transcription.
The sweep converts that from an unknown into a measured, corrected quantity. The rate
held roughly steady across three independent batches (18%, 15%, 7% hard on the pilot
and the two batches), which is the planning estimate for how many corrections the
final 22 modes will surface.
