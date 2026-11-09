# Frozen research results

Generated from `research-runs-2026-11-09.json`. The selected historical files and their SHA256 hashes are fixed; adding a newer run cannot silently change these results. This is a retrospective release, not a preregistration.

Raw outputs and author labels are unchanged. File timestamps span different run batches; model backend versions, temperature, seed, CLI version, token usage and wall-clock time are not established by the retained records. The `model` field records an alias.

## Easy suites

| Condition | Exact verdict | Recall | Specificity | Flag precision | Family / all flags | Exact rule / TP flags |
|---|---:|---:|---:|---:|---:|---:|
| none | 24/60 | 0/36 | 24/24 | n/a | n/a | n/a |
| freeform | 44/60 | 36/36 | 19/24 | 36/41 | 0/41 | 0/36 |
| contract | 42/60 | 36/36 | 16/24 | 36/44 | 0/44 | 0/36 |
| mono-rid | 40/60 | 36/36 | 14/24 | 36/46 | 35/46 | 35/36 |
| judge | 46/60 | 36/36 | 20/24 | 36/40 | 36/40 | 34/36 |

## Hard suites

| Condition | Exact verdict | Recall | Specificity | Flag precision | Family / all flags | Exact rule / TP flags |
|---|---:|---:|---:|---:|---:|---:|
| none | 28/60 | 0/32 | 28/28 | n/a | n/a | n/a |
| freeform | 40/60 | 32/32 | 16/28 | 32/44 | 1/44 | 0/32 |
| contract | 40/60 | 32/32 | 15/28 | 32/45 | 0/45 | 0/32 |
| checklist | 30/60 | 32/32 | 9/28 | 32/51 | 0/51 | 0/32 |
| mono-rid | 35/60 | 32/32 | 10/28 | 32/50 | 31/50 | 28/32 |
| judge-ctx | 47/60 | 32/32 | 21/28 | 32/39 | 32/39 | 32/32 |
| judge | 47/60 | 32/32 | 23/28 | 32/37 | 32/37 | 32/32 |
| judge-anon | 48/60 | 31/32 | 24/28 | 31/35 | 0/35 | 0/31 |

## Paired specificity on hard suites

| Comparison | A only correct | B only correct | Exact McNemar p |
|---|---:|---:|---:|
| judge_vs_mono-rid | 16 | 3 | 0.004 |
| judge-ctx_vs_mono-rid | 16 | 5 | 0.027 |
| judge_vs_freeform | 10 | 3 | 0.092 |
| judge-anon_vs_judge | 3 | 2 | 1.000 |

## Named judge confusion on hard suites

| Gold / predicted | SHIP | REVISE | BLOCK |
|---|---:|---:|---:|
| SHIP | 23 | 4 | 1 |
| REVISE | 0 | 1 | 7 |
| BLOCK | 0 | 1 | 23 |

## Reading the attribution columns

Family attribution preserves the historical prefix comparison, so INT-SEL-01 and INT-SEL-02 both count as SEL. Exact-rule attribution requires a complete identifier match and is conditional on detecting a genuine flag. It credits at least one match, not a wholly correct output set. The JSON supplement also reports exact-rule micro precision and recall across true-positive flags, penalizing extra identifiers. A reviewer denied rule IDs is not a fair baseline for an ID-emission claim.

The named judge catches 32/32 hard-suite positives; the unnamed judge catches 31/32. On clean hard cases the named judge leaves 23/28 unflagged. Neither nonsignificant p-values nor similar point estimates establish equivalence. Gold-mode routing and author-written labels limit these results to review with a known target.
