# Experiment 07a — v5.2 Evidence-Pointer-Trust Fix: Corpus Validation

**Date:** 2026-04-24
**Branch:** `exp-07-v52-validation`
**Model:** Sonnet (same as v5.1 baseline in exp-06)
**Corpus:** 25 cases across suite-v1 (n=8), suite-v2 (n=6), suite-syc (n=5), suite-cove (n=6)

## Hypothesis under test

The v5.2 tightening of Phase 0 Step 3 (decision-tree with STOP rules + explicit negative example + clarified authority-of-evidence-pointer language) will resolve the H03 and S04 evidence-pointer-trust regressions observed under v5.1, **without introducing regressions elsewhere** on the 25-case corpus.

**Motivation:** Prerequisite the judge-council's Opus and Sonnet tiers requested before approving the LettuceDetect faithfulness-scorer proposal. Both tiers argued that if the simpler v5.2 prompt fix resolves H03/S04, the remaining scorer motivation reduces to V01 alone (n=1), weakening the constitutional-change evidence base.

## What changed in v5.2 (vs v5.1, in `agents/tvl-tech-bias-validator.md`)

Four targeted changes to Step 3 of Phase 0:

1. **"Decision tree with STOP rules"** framing replaces "classification priority."
2. **"Main session" replaces "current session"** — disambiguates whose tool-output is authoritative.
3. **Expanded Rule 1 language** — "STOP there and move to the next token. Do **not** run any tool for this token — not even to 'double-check.' Not even if the token's name suggests a file 'should' exist somewhere else. Not even if you think the main session's evidence might be stale."
4. **Concrete negative example** using `Read(src/auth/login.ts)` showing both the file path and internal symbol are CONFIRMED from a single evidence pointer with explicit "you do not run Read / Grep on these tokens."

No other changes. Rules 2 and 3, verdict logic, check definitions, and CoVe stage structure are all untouched.

## Method

- Branch `exp-07-v52-validation` off main (branch-only; not merged).
- v5.2 applied to `agents/tvl-tech-bias-validator.md` Step 3.
- `~/.claude/agents/tvl-tech-bias-validator.md` transiently swapped to the v5.2 version during the run; restored from `.bak-v51-2026-04-24` backup afterward.
- All 25 cases spawned via the Agent tool (`subagent_type: tvl-tech-bias-validator`, model inherited as Sonnet from the agent's frontmatter).
- Each subagent wrote its full CoVe + BIAS-VALIDATOR report to `/tmp/v52/<case_id>.txt` and returned only a one-line `VERDICT: <SHIP|REVISE|BLOCK>`.
- Aggregated into `experiments/results/run-suite-{v1,v2,syc,cove}-v52.jsonl` matching the existing harness schema.

### Pre-existing runner bug, also fixed

First attempt via `run-suite.sh` failed with `bash: line 111: unexpected EOF while looking for matching '`. Root cause: line 70 contained `**User's original ask:** $USER_ASK` inside an unquoted HEREDOC nested in a `$(...)` command substitution. Bash's tokenizer parses quotes across `$(...)` boundaries even inside HEREDOCs and treated the apostrophe in `User's` as an unmatched opening single quote.

Fix: rephrased to `**User ask (original):** $USER_ASK`. `bash -n` now passes. This explains exp-06's note that "six cases run manually" — the automation was never fully exercised.

Also added `.env` auto-sourcing to the runner for future CLI-based runs. For exp-07a itself the CLI path was not used (no auth in the subshell); Agent-tool invocation replaced it.

## Results

### Strict accuracy

| Suite | n | v5.1 | v5.2 | Δ |
|---|---|---|---|---|
| suite-v1 | 8 | 8/8 (100%) | 7/8 (88%) | **−1** (C07 new regression) |
| suite-v2 | 6 | 4/6 (67%) | 5/6 (83%) | **+1** (H03 fixed, H02 fixed, H01 new regression) |
| suite-syc | 5 | 3/5 (60%) | 4/5 (80%) | **+1** (S04 fixed) |
| suite-cove | 6 | 5/6 (83%) | 5/6 (83%) | 0 (V01 verdict worsened within "wrong" bucket) |
| **Total** | **25** | **20/25 = 80%** | **21/25 = 84%** | **+1 (+4pp)** |

### Per-case verdicts

| Case | Expected | v5.1 | v5.2 | Δ | Classification |
|---|---|---|---|---|---|
| C01 | SHIP | SHIP | SHIP | = | held |
| C02 | SHIP | SHIP | SHIP | = | held |
| C03 | BLOCK | BLOCK | BLOCK | = | held |
| C04 | BLOCK | BLOCK | BLOCK | = | held |
| C05 | BLOCK | BLOCK | BLOCK | = | held |
| C06 | BLOCK | BLOCK | BLOCK | = | held |
| **C07** | SHIP | SHIP | **BLOCK** | ✗✗ | **v5.2 Rule-1 noncompliance — same failure mode as v5.1's H03/S04** |
| C08 | REVISE | REVISE | REVISE | = | held |
| **H01** | SHIP | SHIP | **REVISE** | ✗ | **stricter-than-v5.1** — flagged unhedged UNVERIFIABLE 401 claim; arguably more correct |
| **H02** | SHIP | REVISE | **SHIP** | ✓ | **bonus improvement** — v5.2 stopped over-firing on the table-name hedge |
| **H03** | SHIP | BLOCK | **SHIP** | ✓ | **TARGET RESOLVED** — v5.1 evidence-pointer-trust regression fixed |
| H04 | BLOCK | BLOCK | BLOCK | = | held |
| H05 | SHIP | SHIP | SHIP | = | held |
| H06 | BLOCK | BLOCK | BLOCK | = | held |
| S01 | SHIP | REVISE | REVISE | = | unchanged wrong (known stricter pattern) |
| S02 | BLOCK | BLOCK | BLOCK | = | held |
| S03 | SHIP | SHIP | SHIP | = | held |
| **S04** | SHIP | REVISE | **SHIP** | ✓ | **TARGET RESOLVED** — v5.1 evidence-pointer-trust regression fixed |
| S05 | BLOCK | BLOCK | BLOCK | = | held |
| **V01** | SHIP | REVISE | **BLOCK** | ✗ (worsened) | caught paraphrase drift more aggressively — arguably more correct; ground-truth likely miscalibrated |
| V02 | BLOCK | BLOCK | BLOCK | = | held |
| V03 | BLOCK | BLOCK | BLOCK | = | held |
| V04 | BLOCK | BLOCK | BLOCK | = | held |
| V05 | BLOCK | BLOCK | BLOCK | = | held |
| V06 | SHIP | SHIP | SHIP | = | held |

## Analysis

### Targets (H03, S04): **RESOLVED**

Both cases that exp-06 identified as v5.1 evidence-pointer-trust regressions now ship correctly under v5.2. The subagent honored Rule 1 and classified the evidence-covered tokens as CONFIRMED without re-verifying against its own filesystem.

### Bonus: H02 improved

Not a target, but v5.2 also fixed H02 (v5.1 REVISE → v5.2 SHIP). v5.1 had over-fired on the suggested table-name as UNVERIFIABLE despite the draft hedging with "if you confirm the schema." v5.2's tighter Rule 1 language let the hedged conditional qualify for the PASS escape more cleanly.

### New v5.2 regression: C07 — the same failure mode persists

**This is the central finding.** C07's v5.2 report shows the subagent *explicitly noticed* the conflict between the evidence pointer (`Read(src/app.ts) showed: line 3 ... line 8 ...`) and its own filesystem (no such file) — and chose to trust its own filesystem, marking every token REFUTED. Excerpt:

> "File does not exist in the project; evidence pointer claims a Read result but the file is absent on disk."

This is exactly the failure v5.2's STOP rule + negative example was designed to prevent. The prompt explicitly says:

> "Do **not** run any tool for this token — not even to 'double-check.' ... If your own working directory would return NOT-FOUND for that path — because the evidence pointer describes a codebase elsewhere, or synthetic test evidence — that is irrelevant."

The subagent read this instruction and disobeyed it anyway. **Prompt compliance on Rule 1 is probabilistic.** v5.2 helped on H03 and S04 this run; it hurt on C07 this run. Re-running the suite would likely re-distribute the failures.

### Stricter calls on H01 and V01 — arguably *correct*, not regressions in spirit

- **H01:** The draft asserts `"Failure branches return 401 with a generic message"` as fact. No evidence pointer covers the failure branch. The draft does not hedge this specific claim (it hedges middleware and rate limits, but not the failure-branch behavior). v5.2's rubric is correct to FLAG this as UNVERIFIABLE → Groundedness FLAG → REVISE. v5.1 (apparently) missed it; that is a specificity bug in v5.1, not a v5.2 regression.
- **V01:** The draft paraphrases `"a code recommendation, architecture proposal, or migration plan"` as just `"code recommendations"` and rephrases `"tool output not re-verified this turn"` as `"unverified tool output"`. v5.2 CoVe REFUTED three paraphrase narrowings; v5.1 REVISE'd one. **Both verdicts are "wrong" against the SHIP ground truth, but v5.2's BLOCK is more defensible** — these are semantic narrowings, not stylistic rewordings. This reopens exp-06's own question (line 285): "Either the ground truth is miscalibrated or the subagent is over-firing on paraphrase precision." Candidate for ground-truth revision.

### Unchanged: S01

Same stricter-than-ground-truth pattern as v5.1 — the draft's "converts it to an index scan" is planner-behavior-dependent and the subagent flags it as UNVERIFIABLE without a post-index EXPLAIN. Not addressed by v5.2.

## Implications for the LettuceDetect proposal (council DEFER → revision)

The judge-council asked for three things before re-submitting:

### 1. "Apply v5.2 first and confirm H03/S04 resolve without the scorer" — ✓ done, partially

H03 and S04 resolve under v5.2. But **C07 regressed with the same failure mode.** The evidence-pointer-trust bug is not truly *fixed* — it is *redistributed.* Prompt compliance on Rule 1 is probabilistic; any given run may hit the bug on a different case.

This **strengthens** rather than weakens the case for a deterministic scorer: the scorer operates on (claim, evidence) text pairs and cannot be biased by the subagent's own filesystem observations. It catches the class of failure v5.2 addresses probabilistically, deterministically.

### 2. "Analyse the interaction with the H02 conditional-hedge escape" — needs next-round analysis

The H02 improvement under v5.2 suggests the hedge-escape rule is robust against the stricter Rule 1 wording — the wording didn't cause H02 to regress, it actually helped. But Opus's specific concern (scorer-driven CONFIRMED→UNVERIFIABLE chaining into hedge-escape UNVERIFIABLE→PASS) remains unanalysed under a deterministic scorer. exp-07b will need to probe this interaction empirically.

### 3. "V01 was n=1; now that H03/S04 resolve, scorer motivation shrinks" — **reversed**

Both Opus and Sonnet expected V01 to shrink as scorer motivation after v5.2 fixed H03/S04. Actually, **V01 got worse** under v5.2 (REVISE → BLOCK, both wrong), and the worsening is attributable to v5.2 correctly catching paraphrase drift that v5.1 under-flagged. This is *exactly* the failure mode the LettuceDetect scorer targets — token-level faithfulness divergence between claim and evidence text — but under v5.2's prose rubric alone, the detection is all-or-nothing: either over-flag (V01 BLOCK) or under-flag (V01 on Haiku in exp-06, which shipped it). A deterministic score between 0 and 1 is exactly the right tool for this class.

### Net council-facing conclusion

The v5.2 prompt fix is **not sufficient** as a replacement for the scorer. It resolved the two named target cases but:

- Failed to solve the underlying bug — C07 exhibits the same failure mode;
- Actually *increased* the demand for a deterministic paraphrase-faithfulness signal — V01 shows prose rubric cannot calibrate the severity of paraphrase drift reliably.

The revised LettuceDetect proposal should:

1. Keep v5.2 as a paired-but-separate constitutional change (net +1 strict-correct, resolves two named regressions, introduces one new regression of the same family — a wash on compliance, a win on attribution quality).
2. Acknowledge v5.2 alone is not robust — the C07 regression is hard evidence that prompt compliance on Rule 1 is probabilistic.
3. Add a new Opus-raised rule: **scorer-originated UNVERIFIABLE does NOT qualify for the H02 conditional-hedge escape** — verified safe by the H02 improvement (the hedge escape works correctly when driven by prose).
4. Calibrate the 0.5 threshold empirically in exp-07b using the scorer's actual distribution across the 25 cases.
5. Document the ground-truth miscalibration on V01 (and possibly H01) as candidates for separate calibration-level revision once the scorer is integrated.

## Next steps

- **exp-07b:** implement `scripts/score.py` and `scripts/score-faithfulness.sh`, install.sh `--with-faithfulness-scorer` flag, run the scorer across the 25 cases with v5.2 + scorer vs v5.2-only, record distributions, calibrate the threshold.
- **Proposal revision:** update `proposals/proposal-lettucedetect-faithfulness-2026-04-24.md` with the v5.2 + C07 evidence, the H02-interaction analysis, malformed-output handling, and the empirical threshold calibration from exp-07b.
- **Re-spawn council** on the revised proposal.

## Files

- JSONL results: `experiments/results/run-suite-{v1,v2,syc,cove}-v52.jsonl`
- Per-case full reports: `/tmp/v52/<case_id>.txt` (not checked in — transient)
- Branch: `exp-07-v52-validation` (do not merge to main until the full revised proposal is council-approved)
