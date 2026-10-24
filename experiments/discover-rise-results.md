# RISE discovery run (openai/gpt-4o-mini)

48 candidates evaluated across 10 branches (widen=2), 15 novel and grounded. UCB C=1.2, new-area eps=0.2, seed=77.

## Discoveries (novel, grounded, on-topic), ranked by reward

| Reward | Mode | Branch | Tier | Human parallel / AI-native | arXiv | on-topic | quality |
|---|---|---|---|---|---|---|---|
| 0.434 | Cultural bias in language processing | cultural and contextual sensitivity failures | human | In-group bias | 19 | 0.9 | 0.8 |
| 0.41 | Emotional Manipulation | emotional intelligence failures | ai | AI-native: This typically involves using emotional | 16 | 1.0 | 0.8 |
| 0.347 | Affective Conditioning | theory of mind and perspective-taking failures | human | Affective Conditioning refers to emotional respons | 10 | 0.8 | 0.8 |
| 0.34 | Contextual Inflexibility | cultural and contextual sensitivity failures | ai | AI-native: Specific to AI's processing of contextu | 11 | 0.8 | 0.7 |
| 0.315 | Impression Management | moral reasoning failures | human | Self-presentation theory | 9 | 0.6 | 0.7 |
| 0.259 | Unjustified Certainty | creativity and originality failures | human | The tendency for individuals to overestimate their | 5 | 0.8 | 0.8 |
| 0.201 | Emotional Miscalibration | emotional intelligence failures | human | Misattribution of Emotion | 3 | 1.0 | 0.8 |
| 0.19 | Contextual irrelevance | cultural and contextual sensitivity failures | human | Context blindness | 3 | 0.7 | 0.7 |
| 0.159 | Aesthetic Inconsistency | aesthetic and stylistic failures | ai | AI-native: Specific to AI-generated outputs lackin | 2 | 0.9 | 0.8 |
| 0.159 | Illusion of Transparency | self-awareness and reflexivity failures | human | Yes | 2 | 1.0 | 0.8 |
| 0.15 | Insufficient Stylistic Adaptation | aesthetic and stylistic failures | human | Failure to adapt communication style | 2 | 0.8 | 0.7 |
| 0.1 | Emotional Leakage | emotional intelligence failures | human | Emotional Leakage refers to the unconscious expres | 1 | 0.8 | 0.8 |
| 0.1 | Excessive Politeness Effect | social cues and interaction dynamics failures | human | Politeness Theory | 1 | 1.0 | 0.8 |
| 0.095 | Spatial reasoning error | spatial and embodied reasoning failures | human | Spatial neglect | 1 | 0.5 | 0.7 |
| 0.089 | Emotional Misinterpretation | emotional intelligence failures | human | Misreading social cues | 1 | 0.5 | 0.6 |

## Rejected near-duplicates (caught by the evaluation function)

| Candidate | Judged duplicate of | Branch |
|---|---|---|
| Illusory Truth Effect | Illusory truth effect | theory of mind and perspective-taking failures |
| Social Engineering | Social engineering | theory of mind and perspective-taking failures |
| Affective Misalignment | Emergent misalignment | aesthetic and stylistic failures |
| Hyperbole Misalignment | Emergent misalignment | humor and figurative language failures |
| Social Desirability Bias | Social desirability bias | theory of mind and perspective-taking failures |
| Moral Disengagement | Moral disengagement | moral reasoning failures |
| Self-Deception | Self-contradiction | self-awareness and reflexivity failures |
| Cognitive Load Theory | Cognitive load | social cues and interaction dynamics failures |
| Moral Grandstanding | Moral grandstanding | moral reasoning failures |
| Moral Licensing | Moral licensing | moral reasoning failures |

## Branch value (backpropagated Q = mean best reward)

| Branch | Q | visits | novel kept |
|---|---|---|---|
| cultural and contextual sensitivity failures | 0.26 | 3 | 3 |
| emotional intelligence failures | 0.24 | 3 | 4 |
| creativity and originality failures | 0.13 | 2 | 1 |
| theory of mind and perspective-taking failures | 0.12 | 3 | 1 |
| moral reasoning failures | 0.10 | 3 | 1 |
| aesthetic and stylistic failures | 0.08 | 2 | 2 |
| self-awareness and reflexivity failures | 0.08 | 2 | 1 |
| social cues and interaction dynamics failures | 0.05 | 2 | 1 |
| spatial and embodied reasoning failures | 0.05 | 2 | 1 |
| humor and figurative language failures | 0.00 | 2 | 0 |
