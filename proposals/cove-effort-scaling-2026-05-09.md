# Constitutional change proposal — CoVe effort-scaling

**Date:** 2026-05-09
**Author:** main session (Claude Opus 4.7), at user request
**Classification:** **Constitutional** (modifies the CoVe stage rules)
**Threshold:** 3 of 3 judge-council tiers must APPROVE + human approval
**Status:** **REJECTED 3/3 by council on 2026-05-09 — change NOT applied.**

## Council outcome (2026-05-09)

All three tiers rejected.

- **Opus tier — REJECT.** Integrity, Evidence, Scope all REJECT. Cited: zero case evidence (n=0, below the n≥10 the project requires even for calibration), the proposal's own "possible no-op" admission, and the fact that low-effort sessions are exactly when high-stakes claims still need verification. Suggested a shadow-run instrumentation period before resubmitting, or a per-invocation `--quick` UX flag instead of a rubric change.
- **Sonnet tier — REJECT.** Same three stances REJECT. Cited: integrity argument fails on its own terms (no-op if low-effort means no tokens; harmful if low-effort still has substantive claims), zero empirical basis, and an unspecified failure mode if `${CLAUDE_EFFORT}` is unset/empty/unknown.
- **Haiku tier — REJECT.** Same three stances REJECT. Cited: CoVe is the validator's strongest token-level signal and degrading Groundedness for a speculative gain is not justified. Suggested optimizing Phase 0 itself (batch token extraction, skip "safe" tokens) instead of conditionally gating it.

Constitutional threshold is 3/3 APPROVE. With 0/3 APPROVE, the change is rejected.

**Common recommendation:** instrument low-effort audits first (log a `would_have_skipped` flag for ~30 cases), measure whether Phase 0 ever returns non-trivial CONFIRMED/REFUTED/NOT-FOUND results in that population, and resubmit only if the data shows a real cost without integrity loss. Or implement as a per-invocation user flag rather than a constitutional CoVe change.

---

## Proposed change

Add an effort-scaled execution path to Phase 0 of the bias-validator subagent.

- When the caller's spawn prompt contains the literal string `skip-cove: low-effort`, the subagent skips Phase 0 (per-token verification) and proceeds directly to the five checks.
- The validator output records `COVE-VERIFICATION: skipped — low-effort mode` instead of the verification table.
- The BIAS-VALIDATOR REPORT preamble includes a one-line note that CoVe was skipped, so the human knows the audit was lighter.
- The skill orchestrator (`skills/tvl-tech-bias-validator/SKILL.md`, Step 2) reads the Claude Code `${CLAUDE_EFFORT}` substitution (introduced in v2.1.121) and includes the skip flag only when effort is `low`.
- Default behavior is unchanged — `medium`, `high`, `xhigh`, `max` all run Phase 0 fully.

## Rationale

Phase 0 (token extraction + per-token verification) is the most expensive part of an audit. On a `low`-effort turn, the user has explicitly signaled "good enough, prefer speed." Forcing full CoVe in that mode wastes tokens and time on rapid iteration. The five checks still run; only the verification table is dropped.

## Why this is constitutional, not calibration

Per `CLAUDE.md`:

> **Never auto-applied:** the rubric, the BLOCK/FLAG/PASS criteria, **the CoVe rules**, the verdict calculation.
>
> **Constitutional changes** (new checks, removed checks, changed BLOCK/FLAG/PASS criteria, **CoVe stage changes**): 3 of 3 model tiers APPROVE + human

This proposal adds a conditional skip for the CoVe stage. That is a "CoVe stage change" and goes through the constitutional path.

## Risks the council should weigh

1. **Integrity exploit.** Could a draft self-request `low` effort to bypass token verification on a high-stakes claim? The skip flag is set by the orchestrator (the skill), not by anything inside the draft, and only Claude Code's session effort level controls it. A user who picks low effort accepts this trade-off explicitly.

2. **Override-rate distortion.** Audits without CoVe will likely flag fewer Groundedness issues. If CoVe-skipped and CoVe-full audits pool into the same dashboard stats, drift signals get noisy. Mitigation: the case schema gains `validator.cove_skipped: bool` so the dashboard can separate the two populations.

3. **User confusion.** Users may not realize their low-effort session is also getting a lighter audit. Mitigation: the report preamble notes "CoVe verification skipped (low-effort mode)" so it appears in every output.

4. **Possible no-op.** If `low` effort tends to mean trivial conversational turns, those turns usually have no project-specific tokens anyway and Phase 0 self-skips already (`COVE-VERIFICATION: no project-specific tokens — skipped.`). The change may be a no-op in practice — and a constitutional change with little measurable effect is hard to justify.

## Exact text to add

### File: `agents/tvl-tech-bias-validator.md`, Phase 0 section

Insert after the existing first paragraph of "Phase 0 — CoVe Verification":

```
**Effort-scaled execution.** If the caller's input contains the literal string
`skip-cove: low-effort`, do not run Steps 1–4. Output
`COVE-VERIFICATION: skipped — low-effort mode` and proceed directly to the five
checks. Add a one-line note at the top of the BIAS-VALIDATOR REPORT so the
human knows the audit was lighter (e.g. `Note: CoVe verification skipped
(low-effort mode).`). Otherwise run Phase 0 fully — that is the default.
```

### File: `skills/tvl-tech-bias-validator/SKILL.md`, Step 2

Insert after "Do not audit inline — same-context self-audit inherits the same biases.":

```
**Effort-scaled CoVe.** Read `${CLAUDE_EFFORT}` and decide whether the subagent
should run Phase 0:
- `low` → include the literal string `skip-cove: low-effort` in the spawn
  prompt. The subagent skips Phase 0 (per-token verification) and runs the
  five checks directly.
- `medium`, `high`, `xhigh`, `max` (default) → run Phase 0 fully.

Skipping CoVe on low effort trades verification rigor for speed. The five
checks still run; only the per-token verification table is dropped. Note
this in the case log under `validator.cove_skipped: true` so the dashboard
can separate audited-with-CoVe from audited-without.
```

## Evidence base

This is a **forward-looking** proposal driven by a Claude Code platform change (`${CLAUDE_EFFORT}` substitution shipped in v2.1.121, confirmed via `https://code.claude.com/docs/en/changelog.md`). No accumulated case data motivates it. The council should weigh whether speculative-feature gating is justified without case-driven evidence.

## What APPROVE means

If the council and the human approve, the two text inserts above are applied verbatim to the rubric files, plus a corresponding `validator.cove_skipped` field is added to `cases/case-schema.json`. No other rubric changes.
