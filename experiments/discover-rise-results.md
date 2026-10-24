# RISE discovery run (openai/gpt-4o-mini)

44 candidates evaluated across 10 branches (widen=2), 12 novel and grounded. UCB C=1.2, new-area eps=0.2, seed=31.

## Discoveries (novel, grounded, on-topic), ranked by reward

| Reward | Mode | Branch | Tier | Human parallel / AI-native | arXiv | on-topic | quality |
|---|---|---|---|---|---|---|---|
| 0.653 | Information Overload | pragmatics and communication failures | human | Cognitive Overload | 117 | 0.8 | 0.7 |
| 0.564 | Value Misalignment | decision science and economic biases | ai | AI-native: This is specific to AI systems' operati | 39 | 1.0 | 0.9 |
| 0.486 | Cognitive Overload | metacognition failures | human | Cognitive Load Theory | 34 | 0.8 | 0.7 |
| 0.44 | Optimism Bias | cognitive dissonance in user-agent interaction | human | This cognitive bias reflects the tendency of indiv | 24 | 0.7 | 0.7 |
| 0.436 | Moral Framing | moral reasoning discrepancies | human | Framing effect in moral psychology | 14 | 1.0 | 1.0 |
| 0.31 | Temporal Discounting | temporal and planning cognition | human | Temporal Discounting in Behavioral Economics | 12 | 0.5 | 0.5 |
| 0.301 | User Manipulation | trust automation and complacency | ai | AI-native: This failure mode arises specifically f | 7 | 1.0 | 0.8 |
| 0.159 | Emotional Regulation Failure | emotional intelligence deficits | human | Difficulty managing emotional responses | 2 | 0.9 | 0.8 |
| 0.15 | Empathy Overgeneralization | emotional intelligence deficits | human | Empathetic overextending | 2 | 0.8 | 0.7 |
| 0.1 | Temporal Illusion | temporal and planning cognition | human | Temporal Bias | 1 | 1.0 | 0.8 |
| 0.1 | Planning Fallacy | temporal and planning cognition | human | Planning Fallacy in Psychology | 1 | 1.0 | 0.8 |
| 0.095 | Illusory Correlation | clinical and psychiatric parallels | human | The human tendency to perceive relationships betwe | 1 | 0.5 | 0.7 |

## Rejected near-duplicates (caught by the evaluation function)

| Candidate | Judged duplicate of | Branch |
|---|---|---|
| Cognitive Framing | Framing effect | clinical and psychiatric parallels |
| Deceptive Alignment | Deceptive alignment | clinical and psychiatric parallels |
| Context Collapse | Context collapse | decision science and economic biases |
| Task Misalignment | Emergent misalignment | pragmatics and communication failures |
| Automation Bias | Automation bias | trust automation and complacency |
| Sycophancy in AI | Sycophancy | trust automation and complacency |
| Victim Blaming | Identifiable-victim effect | cognitive dissonance in user-agent interaction |
| Omission Bias | Omission bias | cognitive dissonance in user-agent interaction |
| Illusory Truth Effect | Illusory truth effect | cognitive dissonance in user-agent interaction |
| Moral Dissonance | Cognitive dissonance | moral reasoning discrepancies |
| Introspection Illusion | Introspection illusion | metacognition failures |
| Moral Grandstanding | Moral grandstanding | moral reasoning discrepancies |
| Hyperbolic Discounting | Effort discounting | clinical and psychiatric parallels |
| Moral Disengagement | Moral disengagement | decision science and economic biases |
| Sunk-Cost Fallacy | Sunk-cost fallacy | group dynamics and diffusion of responsibility |
| Social projection | Social desirability bias | pragmatics and communication failures |
| Cognitive Dissonance | Cognitive dissonance | decision science and economic biases |
| Illusion of Control | Illusion of control | decision science and economic biases |

## Branch value (backpropagated Q = mean best reward)

| Branch | Q | visits | novel kept |
|---|---|---|---|
| metacognition failures | 0.24 | 2 | 1 |
| cognitive dissonance in user-agent interaction | 0.22 | 2 | 1 |
| moral reasoning discrepancies | 0.22 | 2 | 1 |
| pragmatics and communication failures | 0.22 | 3 | 1 |
| temporal and planning cognition | 0.21 | 2 | 3 |
| decision science and economic biases | 0.19 | 3 | 1 |
| trust automation and complacency | 0.15 | 2 | 1 |
| emotional intelligence deficits | 0.08 | 2 | 2 |
| clinical and psychiatric parallels | 0.05 | 2 | 1 |
| group dynamics and diffusion of responsibility | 0.00 | 2 | 0 |
