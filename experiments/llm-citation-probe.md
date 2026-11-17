# Does an LLM's suggested citation fail the same way the human audit found?

A small probe testing the paper's hypothesis that the surface-match citation failure "is
consistent with what keyword-based or language-model-suggested citation would produce."

## Method

`llm-citation-probe.py generate` takes a stratified sample of grounded catalogue modes, gives
an independent LLM (GPT-4o via OpenRouter) ONLY the mode's definition, and asks it to name one
real arXiv paper that provides AI-side empirical evidence for the behaviour, with the explicit
caution "Only name a paper you are confident actually exists." Each suggested arXiv id was then
checked by reading the real paper on arXiv (Phase 2, by hand), comparing the id to the title the
model claimed for it and to the mode.

Two runs: n=20 and n=45 (temperature 0.3, so the deterministic sample overlaps and some modes
recur with different suggestions).

## Result

Two numbers, both striking.

**1. GPT-4o declines most of the time.** It returned no citation ("NO-ID") for 15/20 and 40/45.
Asked to cite only what it is confident of, it mostly, and correctly, will not.

**2. When it does cite confidently, the citation is fabricated.** Every confident suggestion
checked (10/10 across the two runs, 7 distinct modes) gave an arXiv id that resolves to a
completely different, real paper. The claimed title was often itself a real, famous paper, but
the id belonged to something else entirely:

| Mode | Title the model claimed | What the id actually is |
|---|---|---|
| Controlled hallucination | "On the Dangers of Stochastic Parrots" | 2303.12712 = Sparks of AGI (GPT-4) |
| Controlled hallucination (run 2) | "On the Origin of Hallucinations in Conversation" | 2303.12712 = Sparks of AGI (same wrong id) |
| Inattentional blindness | "LLMs Struggle to Learn Long-Tail Knowledge" | 2305.10601 = Tree of Thoughts |
| Catastrophic forgetting (both runs) | "Overcoming Catastrophic Forgetting in Neural Networks" | 1906.02629 = When Does Label Smoothing Help? |
| Working-memory capacity | "A Mathematical Framework for Transformer Circuits" | 2304.03439 = Evaluating Logical Reasoning of ChatGPT/GPT-4 |
| Working-memory capacity (run 2) | "The Capacity and Limitations of Transformers" | 2304.03439 = same, Logical Reasoning paper |
| Aphasia / paraphasia | "Word-Level Text Editing with Neural Sequence Models" | 2305.01118 = Contrastive Spatial Pre-Training (geospatial vision) |
| Scope creep | "Do As I Can, Not As I Say (SayCan)" | 2302.00923 = Multimodal Chain-of-Thought Reasoning |
| Dunning-Kruger effect | "Do Image Classifiers Generalize Across Time?" | 1906.08500 = Flow dynamics in an overexpanded rocket nozzle |

## Reading

The LLM's failure is not the human auditor's. The human citation audit's largest class was
surface match: a real paper whose title shares the mode's term while the paper studies a
different phenomenon. GPT-4o, when confident, does something sharper: it emits a plausible title
(sometimes a genuine, well-known paper) bound to an arXiv id that belongs to an unrelated paper
in a different field. A reviewer scanning titles would ratify "Overcoming Catastrophic
Forgetting" or "SayCan"; only resolving the id catches that it points at label-smoothing or
multimodal chain-of-thought, or in one case a rocket-nozzle fluid-dynamics paper. So the paper's
central rule holds with extra force for machine citation: the id and the title are separate
properties, and only resolving the source reconciles them.

## Limits

One model (GPT-4o), one temperature, 20+45 modes, 10 confident suggestions verified by hand. A
small probe, not a rate over models or prompts. The ~85% decline rate is the charitable
condition created by the "only cite what you are confident of" instruction; a prompt that
pushes for an answer would lower it and likely raise the fabrication count. The direction is
clear; the magnitudes are illustrative.

## Reproduce

```
python3 experiments/llm-citation-probe.py generate --n 45 --model openai/gpt-4o
# then resolve each suggested arXiv id against the real paper
```
