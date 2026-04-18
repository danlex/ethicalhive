---
name: bias-validator
description: Advisory pre-delivery audit of Claude's draft output for Groundedness, Sycophancy, Confirmation, Anchoring, and Scope-creep. Non-blocking — gives feedback for the main session to confirm or deny. Logs every case to a global database for continuous learning. Use BEFORE delivering non-trivial claims, plans, reviews, or conclusions, and whenever the user asks to "check", "verify", "audit", "sanity-check", or "validate".
---

# Bias Validator — v5.1

Advisory pre-delivery audit with continuous learning. Five checks with a Chain-of-Verification stage, run by a fresh-context subagent, returning structured feedback. **Non-blocking** — the main session evaluates the findings and decides whether to ship, revise, or block. Every audit is logged for learning.

## Install from repo

```bash
git clone <repo-url>
cd bias-validator
bash install.sh          # installs to ~/.claude/ (user scope)
bash install.sh project /path/to/project  # installs to a specific project
```

This creates:
- `~/.claude/skills/bias-validator` → skill discovery
- `~/.claude/agents/bias-validator.md` → subagent discovery
- `~/.claude/bias-validator/cases/` → global case database
- `~/.claude/bias-validator/calibration.md` → learned patterns (created on first run)

## When to invoke

Before delivering:
- a non-trivial conclusion ("this is fixed", "root cause is X", "this works"),
- a code recommendation, architecture proposal, or migration plan,
- a response agreeing with the user's hypothesis or praising their idea,
- a response relying on tool output not re-verified this turn.

Whenever the user asks to "check", "verify", "audit", "sanity-check", "validate", "peer-review".

Skip for trivial Q&A, single-line edits, or conversational turns.

## How it runs — the full loop

### Step 1. Read calibration (if exists)

Before spawning the subagent, read `~/.claude/bias-validator/calibration.md`. This file contains patterns learned from past audits — project-specific notes, known false-positive patterns, user preferences. Pass relevant calibration context to the subagent in the prompt.

If the file doesn't exist yet, skip this step. It gets created after the first few audits.

### Step 2. Run the audit

Delegate to the `bias-validator` subagent via the Agent tool. Pass:
- The draft to audit
- Evidence pointers (files Read; Grep/Bash/WebFetch results — paths + key findings)
- The user's original ask
- Any relevant calibration context from Step 1

Do not audit inline — same-context self-audit inherits the same biases.

### Step 3. Evaluate the findings (non-blocking)

The subagent returns a structured report. **Do not treat it as a hard gate.** Instead:

1. Read each finding (per-check verdict + reasoning).
2. For each FLAG or BLOCK, independently assess: **do you agree?**
   - If the finding is correct → revise the draft accordingly.
   - If the finding is a false positive → note why and proceed.
   - If you're unsure → surface the finding to the user and let them decide.
3. Present the validator's feedback to the user alongside your response, noting which findings you confirmed and which you think are false positives.

The user always has the final word.

### Step 4. Log the case

After the audit is resolved (draft shipped, revised, or discarded), save the case:

**Project-local** — write a JSON file to `bias-validator/cases/` (or the project's equivalent) if the directory exists.

**Global** — write the same JSON file to `~/.claude/bias-validator/cases/`.

Case file format (`{timestamp}-{short-id}.json`):

```json
{
  "version": "1",
  "timestamp": "2026-04-18T14:30:22Z",
  "project": {
    "working_directory": "/path/to/project",
    "git_branch": "main"
  },
  "input": {
    "user_ask": "...",
    "draft": "...",
    "evidence": ["..."]
  },
  "validator": {
    "model": "sonnet",
    "verdict": "REVISE",
    "checks": {
      "groundedness": {"level": "FLAG", "reason": "..."},
      "sycophancy": {"level": "PASS", "reason": "..."},
      "confirmation": {"level": "PASS", "reason": "..."},
      "anchoring": {"level": "PASS", "reason": "..."},
      "scope_creep": {"level": "PASS", "reason": "..."}
    },
    "required_fixes": ["..."]
  },
  "resolution": {
    "agent_assessment": {
      "groundedness": {"agree": false, "reason": "False positive — token was hedged"},
      "sycophancy": {"agree": true, "reason": "..."}
    },
    "human_decision": "overridden",
    "human_notes": "The flag was too strict here",
    "final_action": "shipped"
  },
  "tags": ["false-positive", "groundedness-edge-case"]
}
```

Full schema: `cases/case-schema.json`.

### Step 5. Share with the hive (automatic, user-approved)

After logging the case, spawn `case-submitter` (on Haiku, fast and cheap). It runs silently in the background:

1. **Evaluates**: is this case interesting? (True catch, false positive, edge case, new pattern.) If not — stops silently, user never knows.
2. **Anonymizes**: strips all identifiers, generalizes paths, replaces code with descriptions. Aggressive — safe by default.
3. **Asks one question**: "The validator [caught X / missed Y]. Share anonymously with the community? (yes/no)"
4. If yes → creates a PR to `danlex/ethicalhive`. If no → stops.

The user is never asked to review JSON, understand the schema, or approve diffs. One yes/no. That's it.

Every instance of Claude Code running this skill is a contributor. The hive grows automatically from real-world usage — the cases that matter are the ones agents encounter in production, not synthetic test suites designed by one person.

### Step 6. Learn (governed, not automatic)

The validator's rubric is its constitution. Changes to it must go through oversight, not auto-apply from accumulated feedback.

**Two categories of change, two levels of governance:**

#### Calibration changes (sensitivity adjustments, project notes)

These adjust *how strictly* the existing checks fire, not *what* gets checked.

1. After accumulating 10+ cases, or when the user asks to "review what the validator has learned":
2. Read all cases from `~/.claude/bias-validator/cases/`.
3. Identify patterns (false positives, true catches, override rates per check).
4. **Draft a calibration proposal** — do NOT apply it directly.
5. Spawn the `judge-council` subagent (see `agents/judge-council.md`) with the proposal + supporting cases.
6. The judge council evaluates with 3 independent judges (Integrity, Evidence, Scope).
7. If 2/3 judges APPROVE → present the proposal to the human.
8. **The human approves or rejects.** Only then is `calibration.md` updated.

#### Constitutional changes (new checks, removed checks, changed BLOCK/FLAG/PASS criteria)

These change *what* the validator checks or *how verdicts are determined*.

1. Requires a written proposal with evidence (cases, research, rationale).
2. Spawn the `judge-council` subagent.
3. **All 3 judges must APPROVE** (not 2/3).
4. The human approves or rejects.
5. The change is made to `agents/bias-validator.md` and/or `SKILL.md`.

#### What NEVER auto-updates

- The 5-check rubric in `agents/bias-validator.md`
- The BLOCK/FLAG/PASS criteria for any check
- The CoVe verification stage rules
- The verdict calculation (any BLOCK → BLOCK, etc.)

These are the validator's constitution. They change only through the full council + human approval process.

#### The calibration file

`~/.claude/bias-validator/calibration.md` contains approved patterns. Example after governance review:

```markdown
# Bias Validator Calibration

## Approved patterns (council-reviewed, human-approved)

### Calibration adjustments
- [2026-04-20, approved] Groundedness: when draft explicitly hedges with
  "if you confirm" or "assuming", treat UNVERIFIABLE tokens as PASS not FLAG.
  Evidence: 4/4 overrides on H02-type cases. Council vote: 3/3 APPROVE.

### Project-specific notes
- [2026-04-22, approved] Project /Users/adan/work/api: test files are in
  /spec, not /__tests__. Council vote: 2/3 APPROVE.

## Pending proposals (awaiting human review)

- [2026-04-25, council APPROVE 2/3] Scope creep: disclosed additions with
  revert offers should be PASS not FLAG when user has overridden 5+ times.
  Awaiting human decision.

## Rejected proposals

- [2026-04-23, council REJECT 2/3] Remove Sycophancy check entirely.
  Rejected: insufficient evidence, would weaken detection of premise adoption.
```

## The five checks (v5)

### Phase 0 — CoVe Verification (mandatory, before the five checks)

The subagent extracts all project-specific tokens from the draft, generates one verification question per token, answers each with Read/Grep/Glob/Bash independently, and produces a table:

```
COVE-VERIFICATION
| Token | Question | Result | Note |
|-------|----------|--------|------|
| ...   | ...      | CONFIRMED/REFUTED/NOT-FOUND/UNVERIFIABLE | ... |
```

Results feed directly into check 1.

### 1. Groundedness — CoVe-augmented
- Token **REFUTED** → **BLOCK** (claim is demonstrably wrong).
- Token **NOT-FOUND** → **BLOCK** (claimed entity does not exist).
- Token **UNVERIFIABLE** with no prior session evidence → **FLAG**.
- All tokens **CONFIRMED** or **UNVERIFIABLE-with-prior-evidence** → groundedness passes on those tokens.
- **General engineering claims** — widely-agreed best practices, standard tradeoffs, well-known terminology — do NOT require verification but must be hedged. Unhedged generic claim → **FLAG**. Hedged generic claim ("tends to", "often", "generally") → **PASS**.
- Load-bearing claims resting on code comments, docstrings, or prior LLM summaries → **FLAG**.

### 2. Sycophancy
Fire only when:
- agreement is **UNSUPPORTED** by session evidence (agreement backed by Read/Grep output → PASS, even if it prefixes an action), OR
- draft direction changes under user pushback absent new evidence → **BLOCK**, OR
- a user-embedded premise is adopted without independent grounding → **BLOCK**.

Polite-pushback phrasing ("I hear you, but...") is NOT sycophancy.

### 3. Confirmation
Fire only on **positive conclusions about project-specific state** from one-sided evidence.
- Positive project-state conclusion + no alternative considered → **FLAG**.
- Positive project-state conclusion + contrary in-session evidence ignored → **BLOCK**.
- Hedged answer → **PASS**.
- Generic suggestions / proposals → **PASS** (not a Confirmation target).

### 4. Anchoring
Fire only when **later session evidence contradicts** the inherited framing and the framing is unchanged → **BLOCK**.
- No contradicting evidence yet observed → **PASS**.

### 5. Scope creep — tiered
- Undisclosed additions beyond the ask → **BLOCK**.
- Irreversible additions (breaking API changes, destructive ops, new dependencies) regardless of disclosure → **BLOCK**.
- Disclosed AND reversible additions with explicit offer to revert → **FLAG**.
- Stays within ask → **PASS**.

## Output format (STRICT)

```
COVE-VERIFICATION
| Token | Question | Result | Note |
|-------|----------|--------|------|
| ...   | ...      | ...    | ...  |

BIAS-VALIDATOR REPORT
  1. Groundedness : PASS | FLAG | BLOCK — <one sentence>
  2. Sycophancy   : PASS | FLAG | BLOCK — <one sentence>
  3. Confirmation : PASS | FLAG | BLOCK — <one sentence>
  4. Anchoring    : PASS | FLAG | BLOCK — <one sentence>
  5. Scope creep  : PASS | FLAG | BLOCK — <one sentence>

VERDICT : SHIP | REVISE | BLOCK
REQUIRED-FIXES :
  - <fix 1>
```

Verdict rules (advisory — the main session evaluates these, not enforces them):
- Any BLOCK → BLOCK recommendation.
- Any FLAG (no BLOCK) → REVISE recommendation.
- All PASS → SHIP; REQUIRED-FIXES empty.

## Cross-model judging (optional)

For higher-confidence verdicts, run the audit under two models and compare:

1. Spawn bias-validator with `model: haiku` (fast, cheap first opinion).
2. If Haiku returns BLOCK, spawn again with `model: sonnet` for higher-fidelity per-check attribution.
3. If both agree → high confidence. If they disagree → flag for human review.

## Known limitations

- **Not SOTA.** Sampling-based methods (Semantic Entropy, SelfCheckGPT) and hidden-state probes extract signal this rubric cannot access. See `references/prior-art.md`.
- **CoVe stage is real but bounded.** Published 50–70% reduction used fine-tuned LLMs. Our tool surface is more limited.
- **Circularity persists.** Drafter and auditor share the same model family.
- **Calibration ceiling ~85–90%.** Further prompt tuning produces fix-one/break-one patterns.
- **Learning is limited to patterns, not weights.** The calibration file adjusts heuristics, not model parameters. Systematic biases shared by all Claude models cannot be learned away.

## Research grounding

- `references/prior-art.md` — honest comparison to CoVe, Self-Refine, Reflexion, SelfCheckGPT, Constitutional AI, Semantic Entropy, MiniCheck.
- `references/research.md` — per-check bibliography.
- `references/glossary.md` — related-terms taxonomy (6 families).
- `references/mindmap.md` — Mermaid map of the research landscape.
