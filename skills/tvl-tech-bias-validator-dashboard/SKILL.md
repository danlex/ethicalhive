---
name: tvl-tech-bias-validator-dashboard
description: Show the TVL Tech Bias Validator's accumulated case stats — total audits, verdict mix, per-check override rates, drift direction, most-overridden check, and a summary of recent overrides. Invoke when the user asks to "see the dashboard", "show validator stats", "how is the validator doing", or types /tvl-tech-bias-validator-dashboard.
---

# TVL Tech Bias Validator — Dashboard

Reads the accumulated case database and renders a single at-a-glance report. Non-destructive — only reads.

## Data sources

- `~/.claude/tvl-tech-bias-validator/cases/*.json` — every logged case (schema in `cases/case-schema.json`).
- `~/.claude/tvl-tech-bias-validator/calibration.md` — approved patterns.
- `~/.claude/tvl-tech-bias-validator/recent-overrides.md` — consultative memory (last ~20 overrides).

## Procedure

1. **Enumerate cases.** `ls ~/.claude/tvl-tech-bias-validator/cases/*.json`. If empty → report "No cases yet." and stop.

2. **For each case file, extract:**
   - `timestamp`, `validator.verdict`, `validator.checks.*.level`, `resolution.human_decision`, `resolution.agent_assessment.*.agree`, `resolution.final_action`, `tags`.

3. **Compute:**
   - **Total cases:** N.
   - **Verdict distribution:** count SHIP / REVISE / BLOCK.
   - **True catches:** cases where a FLAG/BLOCK was confirmed by the human (`agent_assessment.<check>.agree == true` AND `final_action == revised|blocked`).
   - **False positives:** cases where a FLAG/BLOCK was overridden (`agent_assessment.<check>.agree == false` OR `human_decision == overridden`).
   - **Clean passes:** cases where the validator said SHIP and the human agreed.
   - **Override rate:** `false_positives / (true_catches + false_positives)`. Target window: 10–30%. Under 10% → too lenient. Over 40% → too strict.
   - **Per-check FLAG+BLOCK count** and **per-check override count**. Compute override rate per check.
   - **Most overridden check:** the check with the highest per-check override rate (min n=3 for signal).
   - **Drift direction:** compare override rate in the first half of cases vs the second half. Rising = validator getting stricter relative to user expectations. Falling = validator aligning better (or user tolerance expanding).

4. **Render** the report block below. Keep it compact — 30 lines max.

## Output format

```
TVL TECH BIAS VALIDATOR — DASHBOARD
Generated: <YYYY-MM-DD HH:MM>
Cases: <total>  (oldest: <date>, newest: <date>)

VERDICT MIX
  SHIP   : <n> (<p%>)
  REVISE : <n> (<p%>)
  BLOCK  : <n> (<p%>)

OVERRIDES
  True catches   : <n>
  False positives: <n>
  Override rate  : <p%>   [target 10–30%; <status>]

PER-CHECK  (fires → overrides → override rate)
  Groundedness : <fires> → <overrides> → <p%>
  Sycophancy   : <fires> → <overrides> → <p%>
  Confirmation : <fires> → <overrides> → <p%>
  Anchoring    : <fires> → <overrides> → <p%>
  Scope creep  : <fires> → <overrides> → <p%>

MOST OVERRIDDEN: <check> (<p%>, n=<fires>)  [needs recalibration if sustained]
DRIFT: <rising|falling|stable> (first half <p%> → second half <p%>)

RECENT OVERRIDES (last 5)
  - <date> <check>: <summary>
  - ...

CALIBRATION STATE
  Approved patterns : <n>
  Pending proposals : <n>

NEXT ACTIONS
  <auto-suggested: e.g. "Scope creep overridden 4/5 times — candidate for calibration proposal.">
```

## Rules

- Read-only. Do not modify any file.
- If fewer than 5 cases, omit the DRIFT line (not enough data) and say so.
- If a check has fewer than 3 fires, omit its override rate (insufficient signal).
- The `NEXT ACTIONS` line should flag any check crossing the 40% override threshold at n≥3 — this is a candidate for a calibration proposal (Step 4b of the validator skill).
- Do NOT auto-spawn judge-council here. This is a reporter, not an actor.

## Implementation note

Prefer a single `jq` pass over the cases to compute stats, then compose the report string. Avoid running the validator subagent or case-submitter — this skill only reads.
