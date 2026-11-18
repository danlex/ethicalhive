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

## Second model: deepseek-chat

Run with the same prompt and sample (n=45), deepseek-chat failed from the opposite side. It
never declined: it returned a citation for all 45 prompts, where gpt-4o declined on 85 percent.
And the citations were overwhelmingly fabricated. On a verified subsample of eight, seven bound a
plausible title to an arXiv id for an unrelated paper:

| Mode | Title the model claimed | What the id actually is |
|---|---|---|
| Controlled hallucination | "Language Models are Few-Shot Learners" | 2305.14627 = Enabling LLMs to Generate Text with Citations (ALCE) |
| Dual-process, System 1/2 | "LLMs Cannot Self-Correct" | 2305.14627 = the same ALCE id, reused |
| Anchoring, Obedience, Default-mode | three different titles | 2402.01768 = Physics-Informed Neural Networks for Poisson-Nernst-Planck systems, reused three times |
| Prompt injection | "Prompt Injection Attacks Against GPT-4" | 2307.04721 = Large Language Models as General Pattern Machines |
| Side-effect blindness | "The Reversal Curse" | 2305.15334 = Gorilla: LLM Connected with Massive APIs |
| Theory of mind | "Assessing Theory of Mind in LLMs" | 2404.01234 = GFLean, an autoformalisation framework; this id was the example in the prompt, echoed back |
| Metacognitive monitoring | "Can LLMs Monitor Their Own" | 2402.00829 = The En Route Truck-Drone Delivery Problem |
| Dual-process moral judgment | "The Moral Machine Experiment: LLMs" | 2305.14325 = Improving Factuality through Multiagent Debate |

One suggestion did resolve correctly: for working-memory capacity, deepseek named 2307.03172,
which genuinely is "Lost in the Middle: How Language Models Use Long Contexts" and is on topic.
The same id reused for several different titles, and the prompt's own example id handed back as an
answer, are the clearest tells of fabrication.

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

The two models fail in opposite styles. gpt-4o is over-cautious: it declines most of the time and
fabricates only when it commits. deepseek is over-confident: it never declines and fabricates
almost every time, reusing one id across unrelated modes. The useful point is that the two
opposite dispositions land in the same place: a citation a reviewer cannot trust without
resolving the source. Caution does not prevent the fabrication, it only rations it.

## Limits

Two models (gpt-4o, deepseek-chat), one temperature, a few dozen modes each, 18 suggestions
verified by hand (10 for gpt-4o, 8 for deepseek). A small probe, not a rate over models or
prompts. gpt-4o's ~85% decline rate is the charitable condition created by the "only cite what
you are confident of" instruction; a prompt that pushes for an answer would lower it. deepseek
ignored that instruction entirely. The direction is clear across both; the magnitudes are
illustrative.

## Reproduce

```
python3 experiments/llm-citation-probe.py generate --n 45 --model openai/gpt-4o
# then resolve each suggested arXiv id against the real paper
```
