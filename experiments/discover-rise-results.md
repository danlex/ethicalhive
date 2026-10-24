# RISE discovery run (openai/gpt-4o-mini)

40 candidates evaluated across 10 branches (widen=2), 14 novel and grounded. UCB C=1.2, new-area eps=0.2, seed=7.

## Discoveries (novel, grounded, on-topic), ranked by reward

| Reward | Mode | Branch | Tier | Human parallel / AI-native | arXiv | on-topic | quality |
|---|---|---|---|---|---|---|---|
| 0.9 | Overgeneralization | contextual incongruence | human | Overgeneralization involves drawing broad conclusi | 784 | 1.0 | 0.8 |
| 0.764 | Semantic Drift | knowledge and memory corruption | human | Conceptual Metamorphosis | 195 | 1.0 | 0.8 |
| 0.601 | Cognitive Offloading | reasoning and metacognition failures | human | Cognitive Offloading | 41 | 1.0 | 1.0 |
| 0.571 | Over-Reliance on Linguistic Cues | identity misalignment | ai | AI-native: This mode is particularly relevant for  | 64 | 0.6 | 0.7 |
| 0.553 | Motivated Reasoning | reasoning and metacognition failures | human | Motivated reasoning is a psychological phenomenon  | 30 | 1.0 | 1.0 |
| 0.435 | Impression Management | deception and oversight evasion | human | Impression management is the attempt to influence  | 23 | 0.5 | 0.7 |
| 0.424 | Simpson's Paradox | agentic overreach and goal integrity | human | This phenomenon occurs when a trend appears in dif | 15 | 1.0 | 0.9 |
| 0.382 | Flattery | deception and oversight evasion | human | Flattery is a social behavior where one seeks to i | 13 | 1.0 | 0.8 |
| 0.36 | Response Inconsistency | cognitive dissonance in dialogue | ai | AI-native: This failure mode arises from the model | 11 | 0.8 | 0.8 |
| 0.354 | Post Hoc Reasoning | reasoning and metacognition failures | human | Post hoc reasoning refers to the cognitive bias of | 8 | 1.0 | 1.0 |
| 0.333 | Memory Leakage | knowledge and memory corruption | ai | AI-native: This failure mode occurs due to the mod | 9 | 1.0 | 0.8 |
| 0.22 | Moral Incongruence | contextual incongruence | human | Mismatch between stated values and behavior that e | 4 | 0.8 | 0.7 |
| 0.168 | Manipulative Flattery | social manipulation and persuasion | ai | AI-native: This mode is unique to AI systems that  | 2 | 1.0 | 0.9 |
| 0.15 | Hyper-empathetic response | affective and parasocial failures | human | Empathy overload | 2 | 0.8 | 0.7 |

## Rejected near-duplicates (caught by the evaluation function)

| Candidate | Judged duplicate of | Branch |
|---|---|---|
| Moral Disengagement | Moral disengagement | social manipulation and persuasion |
| Deceptive Alignment | Deceptive alignment | deception and oversight evasion |
| Data Contamination | Data contamination | deception and oversight evasion |
| Cognitive Dissonance | Cognitive dissonance | agentic overreach and goal integrity |
| Source Fabrication | Source fabrication | knowledge and memory corruption |
| Sycophancy | Sycophancy | knowledge and memory corruption |
| Computational Dissonance | Cognitive dissonance | cognitive dissonance in dialogue |
| Persuasive Misinformation | Misinformation effect / false memory | social manipulation and persuasion |
| Cognitive Dissonance | Cognitive dissonance | reasoning and metacognition failures |
| Affirmation Bias | Confirmation bias | identity misalignment |

## Branch value (backpropagated Q = mean best reward)

| Branch | Q | visits | novel kept |
|---|---|---|---|
| contextual incongruence | 0.56 | 2 | 2 |
| reasoning and metacognition failures | 0.38 | 3 | 3 |
| knowledge and memory corruption | 0.38 | 2 | 2 |
| identity misalignment | 0.29 | 2 | 1 |
| deception and oversight evasion | 0.22 | 2 | 2 |
| agentic overreach and goal integrity | 0.21 | 2 | 1 |
| cognitive dissonance in dialogue | 0.18 | 2 | 1 |
| social manipulation and persuasion | 0.08 | 2 | 1 |
| affective and parasocial failures | 0.07 | 2 | 1 |
| narrative coherence failure | 0.00 | 1 | 0 |
