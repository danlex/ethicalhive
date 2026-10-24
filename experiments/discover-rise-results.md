# RISE discovery run (openai/gpt-4o-mini)

40 candidates evaluated across 10 branches (widen=2), 12 novel and grounded. UCB C=1.2, new-area eps=0.2, seed=88.

## Discoveries (novel, grounded, on-topic), ranked by reward

| Reward | Mode | Branch | Tier | Human parallel / AI-native | arXiv | on-topic | quality |
|---|---|---|---|---|---|---|---|
| 0.807 | Label Smoothing | Training Data Poisoning | ai | AI-native: This failure arises specifically from a | 150 | 1.0 | 1.0 |
| 0.786 | Data Poisoning | Misleading Prediction Models | ai | AI-native: This represents a specific type of atta | 170 | 1.0 | 0.9 |
| 0.619 | Overgeneralization | Misleading Prediction Models | human | Overgeneralization | 71 | 1.0 | 0.8 |
| 0.581 | Cognitive Overload | Bias-Induced Recommendations | human | Cognitive Strain | 36 | 1.0 | 1.0 |
| 0.524 | Value Misalignment | Bias-Induced Recommendations | human | Moral Dissonance | 25 | 1.0 | 1.0 |
| 0.354 | Response Inconsistency | Inconsistent Reasoning Patterns | ai | AI-native: This failure mode specifically arises f | 8 | 1.0 | 1.0 |
| 0.284 | Contextual Inference Error | Misinterpretation of User Intent | ai | AI-native: This refers specifically to an AI's ina | 7 | 0.8 | 0.7 |
| 0.284 | Contextual Role Confusion | Misinterpretation of User Intent | human | Role Confusion in Social Contexts | 7 | 0.5 | 0.7 |
| 0.201 | Technological Determinism | Scope Creep in Model Application | ai | AI-native: This failure mode reflects a belief tha | 3 | 0.6 | 0.8 |
| 0.141 | Contextual Inference Failure | Contextual Ambiguity Handling | human | Contextual reasoning errors in human cognition | 2 | 0.5 | 0.6 |
| 0.1 | Emotional Blackmail | Emotional Manipulation | human | Emotional Blackmail is a well-documented psycholog | 1 | 1.0 | 0.8 |
| 0.089 | Causal Misattribution | Misleading Prediction Models | human | The tendency to incorrectly link cause and effect  | 1 | 0.5 | 0.6 |

## Rejected near-duplicates (caught by the evaluation function)

| Candidate | Judged duplicate of | Branch |
|---|---|---|
| Strategic deception | Strategic deception | Deceptive Output Generation |
| Flattery | Flattery | Deceptive Output Generation |
| Data contamination | Data contamination | Training Data Poisoning |
| Retrieval poisoning | Retrieval poisoning | Training Data Poisoning |
| Moral Licensing | Moral licensing | Scope Creep in Model Application |
| Sycophancy | Sycophancy | Bias-Induced Recommendations |
| Contextual Drift | Narrativity drift | Contextual Ambiguity Handling |
| Domain Misalignment | Emergent misalignment | Scope Creep in Model Application |
| Overfitting to User Expectations | Obedience to authority | Deceptive Output Generation |
| Data Snooping | Data contamination | Training Data Poisoning |
| Conversation Drift | Narrativity drift | Contextual Ambiguity Handling |
| Social engineering | Social engineering | Emotional Manipulation |
| Moral Grandstanding | Moral grandstanding | Erroneous Ethical Reasoning |
| Self-Serving Bias | Self-serving bias | Erroneous Ethical Reasoning |
| Moral Licensing | Moral licensing | Erroneous Ethical Reasoning |
| Moral Disengagement | Moral disengagement | Erroneous Ethical Reasoning |

## Branch value (backpropagated Q = mean best reward)

| Branch | Q | visits | novel kept |
|---|---|---|---|
| Misleading Prediction Models | 0.44 | 2 | 3 |
| Training Data Poisoning | 0.40 | 2 | 1 |
| Bias-Induced Recommendations | 0.29 | 2 | 2 |
| Misinterpretation of User Intent | 0.28 | 2 | 2 |
| Inconsistent Reasoning Patterns | 0.18 | 2 | 1 |
| Scope Creep in Model Application | 0.10 | 2 | 1 |
| Contextual Ambiguity Handling | 0.07 | 2 | 1 |
| Emotional Manipulation | 0.05 | 2 | 1 |
| Deceptive Output Generation | 0.00 | 2 | 0 |
| Erroneous Ethical Reasoning | 0.00 | 2 | 0 |
