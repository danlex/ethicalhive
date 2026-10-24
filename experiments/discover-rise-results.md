# RISE discovery run (openai/gpt-4o-mini)

44 candidates evaluated across 8 branches (widen=2), 14 novel and grounded. UCB C=1.2, new-area eps=0.2, seed=5.

## Discoveries (novel, grounded, on-topic), ranked by reward

| Reward | Mode | Branch | Tier | Human parallel / AI-native | arXiv | on-topic | quality |
|---|---|---|---|---|---|---|---|
| 0.767 | Failure to Generalize | autonomy and oversight evasion | ai | AI-native: This failure mode is specifically tied  | 272 | 0.5 | 0.7 |
| 0.653 | Information Overload | retrieval and grounding failures | human | Cognitive Overload | 117 | 0.8 | 0.7 |
| 0.519 | Coordination Failure | multi-agent coordination failures | human | Groupthink | 35 | 1.0 | 0.8 |
| 0.435 | Attention Bottleneck | long-horizon planning and memory failures | ai | AI-native: This failure arises from limitations in | 23 | 0.7 | 0.7 |
| 0.395 | Inconsistent Task Execution Bias | autonomy and oversight evasion | ai | AI-native: Arises from the AI's reliance on contex | 17 | 0.8 | 0.7 |
| 0.34 | Erosion of Trust | human-AI handoff and trust calibration | human | Trust erosion in interpersonal relationships | 11 | 0.8 | 0.7 |
| 0.333 | Overreliance on Consensus | multi-agent coordination failures | human | Groupthink phenomenon in social psychology where t | 9 | 1.0 | 0.8 |
| 0.333 | Lack of Contextual Awareness | retrieval and grounding failures | ai | AI-native: This failure mode is specific to AI's i | 9 | 0.9 | 0.8 |
| 0.309 | Semantic Incoherence | reasoning inconsistency failures | ai | AI-native: This is specific to language models and | 10 | 0.5 | 0.6 |
| 0.233 | Memory Leakage | long-horizon planning and memory failures | ai | AI-native: This reflects the AI's tendency to draw | 4 | 1.0 | 0.8 |
| 0.22 | Simulacra Effect | agentic tool-use failures | ai | AI-native: This mode arises specifically from gene | 4 | 0.6 | 0.7 |
| 0.207 | Overly Literal Interpretation | contextual empathy failure | human | Literal Interpretation Bias | 4 | 0.5 | 0.6 |
| 0.207 | Obliviousness to Temporal Context | long-horizon planning and memory failures | human | Temporal disorientation affects how individuals re | 4 | 0.5 | 0.6 |
| 0.201 | Contextual Misalignment | human-AI handoff and trust calibration | ai | AI-native: This mode primarily stems from the AI's | 3 | 0.9 | 0.8 |

## Rejected near-duplicates (caught by the evaluation function)

| Candidate | Judged duplicate of | Branch |
|---|---|---|
| Sycophancy | Sycophancy | agentic tool-use failures |
| Reward Hacking | Reward hacking | agentic tool-use failures |
| Deceptive alignment | Deceptive alignment | autonomy and oversight evasion |
| Context Collapse | Context collapse | retrieval and grounding failures |
| Data Contamination | Data contamination | retrieval and grounding failures |
| Sycophancy | Sycophancy | human-AI handoff and trust calibration |
| Exaggeration Bias | Illusory truth effect | agentic tool-use failures |
| Empathy Gap | Silent-assumption gap | contextual empathy failure |
| Deceptive Alignment | Deceptive alignment | retrieval and grounding failures |
| Inference Overreach | Value misgeneralisation | reasoning inconsistency failures |
| Context Collapse | Context collapse | reasoning inconsistency failures |

## Branch value (backpropagated Q = mean best reward)

| Branch | Q | visits | novel kept |
|---|---|---|---|
| autonomy and oversight evasion | 0.39 | 3 | 2 |
| multi-agent coordination failures | 0.28 | 3 | 2 |
| long-horizon planning and memory failures | 0.22 | 3 | 3 |
| retrieval and grounding failures | 0.22 | 3 | 2 |
| human-AI handoff and trust calibration | 0.11 | 3 | 2 |
| agentic tool-use failures | 0.11 | 2 | 1 |
| contextual empathy failure | 0.10 | 2 | 1 |
| reasoning inconsistency failures | 0.10 | 3 | 1 |
