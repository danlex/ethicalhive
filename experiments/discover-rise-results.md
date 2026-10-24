# RISE discovery run (openai/gpt-4o-mini)

60 candidates evaluated across 10 branches (widen=2), 16 novel and grounded. UCB C=1.2, new-area eps=0.2, seed=11.

## Discoveries (novel, grounded, on-topic), ranked by reward

| Reward | Mode | Branch | Tier | Human parallel / AI-native | arXiv | on-topic | quality |
|---|---|---|---|---|---|---|---|
| 0.818 | Semantic Drift | knowledge and memory corruption | ai | AI-native: Semantic drift occurs as AI models upda | 160 | 1.0 | 1.0 |
| 0.611 | Social Engineering | social manipulation and persuasion | human | A form of influence that leverages trust to manipu | 67 | 1.0 | 0.8 |
| 0.442 | Motivated Reasoning | agentic overreach and goal integrity | human | Motivated reasoning reflects the human tendency to | 17 | 1.0 | 0.9 |
| 0.403 | Disinformation Spread | deception and oversight evasion | ai | AI-native: This pertains specifically to the AI's  | 13 | 0.8 | 0.9 |
| 0.386 | Social Desirability Bias | agentic overreach and goal integrity | human | Social Desirability Bias refers to the tendency of | 10 | 1.0 | 1.0 |
| 0.382 | Flattery | empathy and response appropriateness | human | Flattery in human interactions often serves a soci | 13 | 1.0 | 0.8 |
| 0.38 | Context Collapse | social manipulation and persuasion | ai | AI-native: This arises uniquely from AI's inabilit | 11 | 1.0 | 0.9 |
| 0.361 | Automated Flattery | deception and oversight evasion | human | Flattery | 13 | 0.8 | 0.7 |
| 0.318 | Self-Serving Bias | normative alignment failures | human | yes | 8 | 0.9 | 0.8 |
| 0.288 | Misremembering | knowledge and memory corruption | human | False memory | 5 | 1.0 | 1.0 |
| 0.288 | Escalation of Commitment | agentic overreach and goal integrity | human | sunk-cost fallacy | 5 | 1.0 | 1.0 |
| 0.19 | Overpromise and Underdeliver | social manipulation and persuasion | human | False advertising | 3 | 0.8 | 0.7 |
| 0.159 | Contextual Blindness | moral reasoning failures | ai | AI-native: This mode arises from the AI's failure  | 2 | 0.9 | 0.8 |
| 0.15 | Moral Inversion | moral reasoning failures | human | Moral Relativism | 2 | 0.8 | 0.7 |
| 0.089 | Over-reliance on heuristic shortcuts | agentic overreach and goal integrity | human | Cognitive miserliness | 1 | 0.5 | 0.6 |
| 0.089 | Moral Grandstanding | moral reasoning failures | human | Social Approval Seeking | 1 | 0.6 | 0.6 |

## Rejected near-duplicates (caught by the evaluation function)

| Candidate | Judged duplicate of | Branch |
|---|---|---|
| Manipulative Framing | Framing effect | social manipulation and persuasion |
| Moral Disengagement | Moral disengagement | deception and oversight evasion |
| Deceptive Alignment | Deceptive alignment | deception and oversight evasion |
| Emotional Misattribution | Emotional contagion | affective and parasocial failures |
| Moral Licensing | Moral licensing | reasoning and metacognition failures |
| Dunning-Kruger Effect | Dunning-Kruger effect | reasoning and metacognition failures |
| Agentic Misalignment | Emergent misalignment | agentic overreach and goal integrity |
| Confirmation bias | Confirmation bias | reasoning and metacognition failures |
| Overconfidence bias | Overconfidence | reasoning and metacognition failures |
| Moral Disengagement | Moral disengagement | normative alignment failures |
| Adaptive Sycophancy | Sycophancy | normative alignment failures |
| Inconsistent Knowledge Representation | Curse of knowledge | knowledge and memory corruption |
| Cognitive Dissonance in AI Decision-Making | Cognitive dissonance | contextual awareness failures |
| Confabulated Reasoning Under Ambiguity | Confabulated reasons | contextual awareness failures |
| Excessive deference to user prompts | Obedience to authority | empathy and response appropriateness |
| Confabulated interpretive framework | Confabulated reasons | empathy and response appropriateness |
| Moral Credentialing | Moral licensing | moral reasoning failures |
| Preference Inconsistency | Self-preference bias | moral reasoning failures |
| Moral Disengagement | Moral disengagement | moral reasoning failures |
| Cognitive Dissonance | Cognitive dissonance | reasoning and metacognition failures |
| Moral Licensing | Moral licensing | normative alignment failures |

## Branch value (backpropagated Q = mean best reward)

| Branch | Q | visits | novel kept |
|---|---|---|---|
| agentic overreach and goal integrity | 0.30 | 4 | 4 |
| knowledge and memory corruption | 0.27 | 3 | 2 |
| social manipulation and persuasion | 0.27 | 3 | 3 |
| deception and oversight evasion | 0.25 | 3 | 2 |
| empathy and response appropriateness | 0.13 | 3 | 1 |
| normative alignment failures | 0.11 | 3 | 1 |
| moral reasoning failures | 0.10 | 3 | 3 |
| affective and parasocial failures | 0.00 | 3 | 0 |
| reasoning and metacognition failures | 0.00 | 3 | 0 |
| contextual awareness failures | 0.00 | 2 | 0 |
