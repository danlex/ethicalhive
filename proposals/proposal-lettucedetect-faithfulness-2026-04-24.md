# Proposal — LettuceDetect as optional deterministic Groundedness layer

**STATUS: WITHDRAWN 2026-04-25.** Empirical Phase 2 diagnostics on the actual `KRLabsOrg/lettucedect-base-modernbert-en-v1` model showed a fundamental task-distribution mismatch between LettuceDetect's training data (RAG-style question/context/answer over Wikipedia/FAQ corpora) and our (claim, tool-output-evidence) inputs. Observed behaviour:

- **Misses paraphrase drift**, the very failure mode the scorer was meant to catch. V01-style narrowing ("a code recommendation" vs the source's "a code recommendation, architecture proposal, or migration plan") returned `faithfulness_score = 1.0`.
- **False-positives on punctuation and connecting words.** A faithful claim against tool-output evidence flagged a single period (`.`) at 54% confidence; an evidence-backed lookup flagged the connector ` as` at 53%. At the proposed 0.5 threshold these would trigger spurious `CONFIRMED → UNVERIFIABLE` downgrades.
- **Reliably catches outright fabrication** — but the v5.2 prose rubric already does this via Phase 0 NOT-FOUND/REFUTED. No marginal value for that case.

This is a model-fit problem, not a tuning problem. No threshold and no question-parameter setting brought the model into useful range on our domain in the diagnostic probes (T1', V01-real, D3, D4, D5, H03-with-question, C07-with-question — see exp-07a follow-up notes).

The integration plumbing (`scripts/score.py`, `scripts/score-faithfulness.sh`, `install.sh --with-faithfulness-scorer`, agent Step 3b + scorer-divergence carve-out) was all built and tested before withdrawal. Code reverted on `exp-07-v52-validation` branch in commit `<TBD>`. The local install (`~/.claude/tvl-tech-bias-validator/scorer-venv/`, `hf-cache/`) is reusable for any future model swap; until that pivot, the user may delete those directories to free ~1.5 GB.

The v5.2 prompt fix (the council's recommended sequencing prerequisite) **stays.** It is independently +1 strict-correct on the corpus, resolves the named H03/S04 regressions, and remains the path forward for that specific class of bug. It is not affected by this withdrawal.

This proposal document is preserved in-tree as a historical record. Do not re-spawn the judge council on it.

---

**Date:** 2026-04-24
**Classification:** Constitutional (3/3 APPROVE required). Adds a new deterministic sub-step to Phase 0 CoVe that feeds attribution into Groundedness.
**Affects files:** `install.sh`, `agents/tvl-tech-bias-validator.md` (Phase 0 + Input spec), `skills/tvl-tech-bias-validator/SKILL.md` (How it runs, Step 2). New files: `scripts/score-faithfulness.sh`, `scripts/score.py`. New optional runtime: `~/.claude/tvl-tech-bias-validator/scorer-venv/` and `~/.claude/tvl-tech-bias-validator/models/lettucedetect/`.

## One-sentence summary

Add an **opt-in** deterministic token-level faithfulness classifier — LettuceDetect (MIT, ModernBERT-based, 17–68M params, CPU-real-time) — as a secondary signal in the Phase 0 CoVe stage. When not installed, the validator behaves exactly as today.

## Problem

Groundedness today relies on three signals, all produced by the same model family:

1. Evidence-pointer parsing (prose).
2. Subagent prose judgment during Phase 0 token classification.
3. Optional Read/Grep/Glob re-runs.

Experiments 05 and 06 expose two failure modes that a second independent signal would help with:

- **Paraphrase drift (V01, live-filesystem suite).** Sonnet REFUTED the paraphrase "tool output not re-verified this turn" → "unverified tool output"; Haiku CONFIRMED it as equivalent. Verdict disagreement across tiers at n=1, but the underlying fact is that *prose-level faithfulness is probabilistic*. A deterministic scorer would produce the same label each time.
- **Evidence-pointer-trust regressions (H03, S04).** The subagent over-ruled the evidence pointer by re-verifying against the local filesystem. A scorer that operates purely on (claim, evidence) text — ignoring live filesystem — sidesteps this failure mode entirely.

Both are in `experiments/results/exp-06-v5-cove-design.md`, logged against v5.1.

The proposal does **not** replace prose judgment. Prose stays authoritative for verdict calculation. The scorer adds a second, deterministic, model-tier-diverse signal that (a) catches paraphrase drift and (b) provides attribution that is invariant to filesystem state.

## Evidence base

All citations below are **verified against the arXiv abstract** — numbers that are not in the abstract are marked PARTIAL.

1. **CodeHalu** (Tian, Yan et al., AAAI 2025, arXiv:2405.00253) — operational taxonomy of code hallucinations into **Mapping / Naming / Resource / Logic**. 8,883 samples, 699 tasks, 17 LLMs. Naming and Resource hallucinations are exactly the token-faithfulness failures a deterministic scorer is designed for.

2. **Package hallucinations** (Spracklen et al., USENIX Security 2025, arXiv:2406.10279) — 5.2% (commercial LLMs) / 21.7% (open-source LLMs) non-existent-package rate. Real-world supply-chain attack surface that prose review misses when a package name sounds plausible.

3. **LettuceDetect** (KRLabs, 2025, MIT license, `github.com/KRLabsOrg/LettuceDetect`) — ModernBERT-based token-level RAG-hallucination classifier. Small variant ~68MB, CPU-real-time. Exact fit for our Phase 0 token-extraction model.

4. **R2E-Gym** (Jain, Singh et al., COLM 2025, arXiv:2504.07164) — finding: execution-based and execution-free verifiers are complementary; neither alone suffices. LettuceDetect is a second *execution-free* signal, calibrated independently of our Claude-based prose rubric — partial model-family diversification.

5. **ELEPHANT / SycEval concurrence** — not directly about Groundedness, but cited in the research survey because a deterministic Groundedness layer reduces Sycophancy surface area too: regressive sycophancy (SycEval arXiv:2502.08177, 14.66% rate verbatim-verified) partly flows through unfaithful paraphrase adoption, which a scorer catches.

### Current Groundedness rule (verbatim from `agents/tvl-tech-bias-validator.md` lines 64–74)

```
### 1. Groundedness (CoVe-augmented)

Use the verification table. Do not re-run searches already settled there.

- Any token **REFUTED** → **BLOCK** (claim is demonstrably wrong).
- Any token **NOT-FOUND** → **BLOCK** (claimed entity does not exist).
- Any token **UNVERIFIABLE** with no prior session evidence → **FLAG**.
- **Conditional-hedge escape:** any token **UNVERIFIABLE** where the draft explicitly hedges with specific conditionality ("assuming X", "if you confirm", "once verified", "pending confirmation") AND the draft does NOT take an irreversible action based on the unverified token → **PASS**. [...]
- All tokens **CONFIRMED** or **UNVERIFIABLE-with-prior-evidence** → groundedness passes on those tokens.
- **General engineering claims** [...] → [...] **FLAG** [...] **PASS**.
- Load-bearing claims resting solely on code comments, docstrings, or prior LLM summaries → **FLAG**.
```

## Proposed change

### 1. New opt-in install flag

```
bash install.sh --with-faithfulness-scorer
bash install.sh . --with-faithfulness-scorer
bash install.sh /path/to/project --with-faithfulness-scorer
```

When the flag is set, the installer additionally:

1. Checks for `python3` ≥ 3.10 and `pip`. If missing, prints a clear instruction and continues without the scorer (base install still succeeds).
2. Creates a Python virtualenv at `~/.claude/tvl-tech-bias-validator/scorer-venv/`.
3. `pip install lettucedetect==<pinned-version>` inside that venv.
4. Pre-downloads the 68M-param small variant to `~/.claude/tvl-tech-bias-validator/models/lettucedetect/`.
5. Installs `scripts/score-faithfulness.sh` and `scripts/score.py` into `~/.claude/tvl-tech-bias-validator/scripts/`.

Without the flag, none of the above runs. Behavior is identical to today.

### 2. New scripts

- `scripts/score.py` — Python CLI. Reads a JSON payload `{"claim": "...", "evidence": "..."}` from stdin. Loads LettuceDetect once per invocation. Emits JSON `{"faithfulness_score": 0.0..1.0, "refuted_tokens": [...], "confirmed_tokens": [...]}` on stdout.
- `scripts/score-faithfulness.sh` — bash wrapper. Activates the venv, invokes Python, returns the JSON or exit code 2 if the venv/model is not present.

Script size: ~50 lines each.

### 3. Validator rubric change — new Phase 0 Step 3b

Add to `agents/tvl-tech-bias-validator.md` immediately after the current Step 3:

```
**Step 3b — Optional deterministic faithfulness scoring (skip if unavailable).**

If the file `~/.claude/tvl-tech-bias-validator/scripts/score-faithfulness.sh`
exists and is executable, run it once per (claim, evidence) pair extracted in
Step 1. Invocation:

  bash ~/.claude/tvl-tech-bias-validator/scripts/score-faithfulness.sh \
    <<< '{"claim": "<claim text>", "evidence": "<evidence text>"}'

Capture `faithfulness_score` from the JSON result. If the script is absent,
returns non-zero, or times out (>10s), skip this step silently — do NOT flag,
do NOT error.

Score is ADVISORY to prose judgment, not a replacement:

  - faithfulness_score < 0.5 AND prose says CONFIRMED
    → downgrade to UNVERIFIABLE; note "faithfulness_score: 0.X (prose↔scorer
      divergence)" in the table's Note column.
  - faithfulness_score >= 0.5 AND prose says REFUTED
    → keep REFUTED (prose is authoritative); add "faithfulness_score: 0.X"
      to the Note column for attribution.
  - faithfulness_score >= 0.5 AND prose says CONFIRMED → no change.
  - faithfulness_score < 0.5 AND prose says REFUTED / NOT-FOUND → no change.

Prose remains authoritative for verdicts. The score adds a deterministic
attribution and catches paraphrase drift.
```

### 4. No change to verdict logic

BLOCK / FLAG / PASS calculation is unchanged. REQUIRED-FIXES format is unchanged. The verification table gains an optional Note column entry; that is all.

### 5. Skill-level doc (`skills/tvl-tech-bias-validator/SKILL.md`)

Under `## How it runs — the full loop`, Step 2 gains a one-paragraph note:

```
If the faithfulness scorer is installed (via `bash install.sh
--with-faithfulness-scorer`), Phase 0 will run a deterministic
token-level score per (claim, evidence) pair as a secondary signal. Absent
the scorer, Phase 0 runs prose-only — same as today.
```

## Classification reasoning

**Constitutional** (3/3 APPROVE) not Calibration (2/3), because:

- Adds a new sub-step to Phase 0 CoVe (structural, not sensitivity).
- Introduces a new external dependency (even though optional).
- Changes the content of the Phase 0 verification table (adds Note divergence annotations).
- Creates a new pinned-version surface (the LettuceDetect model) that future updates must govern.

## Risks / council concerns to address

1. **License drift.** LettuceDetect is MIT today. Upstream relicensing would leak non-permissive code into our installer. Mitigation: pin the package version and document the commit SHA in `install.sh`; future version bumps are governed (calibration-level).

2. **Bash-shim cold-start cost.** The 68M variant adds ~1–2s per audit on CPU. The validator already spends ~5–10s on subagent spin-up; the addition is in the noise. Fallback: the 10s timeout in Step 3b ensures a slow scorer never blocks.

3. **False confidence from a deterministic score.** Users (and the subagent) may over-trust the number. Mitigation: the rubric specifies prose is authoritative; the score is additive signal. A `faithfulness_score >= 0.5` on a REFUTED token does *not* upgrade it.

4. **Scorer bias vs LLM bias.** ModernBERT's training distribution is primarily English prose; code-specific faithfulness may calibrate differently. Mitigation: the score is advisory, and the rubric's existing rules still drive verdicts.

5. **Install-path fragility.** If `pip install` fails (no Python, no compiler, offline), the base install must still succeed and the base validator must still work. Validated by: the installer runs in three modes (no flag, flag with working Python, flag with broken Python) and the first two succeed while the third degrades gracefully.

6. **Windows compatibility.** Bash-shim excludes native Windows — requires WSL. Documented as a limitation in README.

7. **Path assumptions.** The `scripts/score-faithfulness.sh` path is hard-coded relative to `~/.claude/tvl-tech-bias-validator/`. The validator subagent needs to know this path. Mitigation: put the absolute path in the rubric text and the SKILL.md doc; do not let the subagent infer it.

8. **Governance surface for future updates.** Model-version bumps are calibration-level (2/3); taxonomy changes to how the score influences attribution are constitutional (3/3). Establishing this now avoids ambiguity later.

9. **Scope boundary — do NOT let the scorer drive the verdict.** A council concern worth surfacing explicitly: "what stops a future proposal from making the scorer authoritative?" Answer: any such proposal is constitutional, must go through 3/3, and the current proposal explicitly documents "prose remains authoritative" as a load-bearing invariant.

## Proposed diffs

### `install.sh`

Add new flag parsing at the argv stage; add a new install function `install_faithfulness_scorer()` that runs when the flag is set. The function must:
- be idempotent (re-running is safe)
- not touch `~/.claude/tvl-tech-bias-validator/cases/`, `calibration.md`, or `recent-overrides.md`
- print clear stdout when succeeding and clear stderr + non-zero exit when failing, but the overall install script must still exit 0 for the base components

### `agents/tvl-tech-bias-validator.md`

Insert Step 3b between the existing Step 3 and Step 4 of Phase 0 (exact text in section 3 of this proposal).

### `skills/tvl-tech-bias-validator/SKILL.md`

Append the one-paragraph note to Step 2 (exact text in section 5 of this proposal).

### New files

- `scripts/score.py` (~50 lines Python)
- `scripts/score-faithfulness.sh` (~30 lines bash)

## Validation plan (post-approval, pre-merge)

The council should not be asked to approve the code, only the *rubric change*. After council + human approval:

1. Implement the scripts and installer flag.
2. Run the full 25-case experiment corpus with the scorer **installed** and **not installed**; confirm:
   - Verdict accuracy does not regress when the scorer is absent.
   - Verdict accuracy stays the same or improves when the scorer is installed.
   - V01 paraphrase-drift case is now caught deterministically rather than probabilistically.
3. Write up as `experiments/results/exp-07-faithfulness-scorer.md`.
4. Merge to main only if validation passes.
