# EthicalHive

A Claude Code plugin that checks Claude's own work before you see it.

Claude is often confident when wrong. It agrees with your framing even when the code disagrees. It quietly adds things you didn't ask for. EthicalHive spawns a second Claude — fresh context, same tools — to adversarially review the draft before delivery, then shows you both so you can decide what to trust.

**Advisory, not blocking.** The validator gives structured feedback. The human decides.
**Self-aware.** It knows it has its own confirmation bias. It tracks its own override rate to stay honest.
**Governed.** Changes to its rubric go through a three-model-tier judge council + human approval. No auto-updates.
**Local-only.** Nothing leaves your machine. Cases accumulate in `~/.claude/tvl-tech-bias-validator/`. Community hive submission is intentionally disabled pending hardening.

## Why you'd want this

Claude Code is powerful enough to cause real damage when confidently wrong. The failure mode is rarely "Claude refuses to try" — it is "Claude ships an answer that *sounds* right." EthicalHive targets the specific ways these answers go wrong:

| You ask Claude... | Without this, Claude might... | EthicalHive flags it as |
|---|---|---|
| "Is this bug fixed?" | Claim yes and cite a function that doesn't exist, or a line that says something different | **Groundedness** — refuted / missing tokens |
| "I think the issue is in the cache" | Agree and start rewriting the cache even though the logs point at the DB | **Sycophancy** — premise adopted without evidence |
| "Does this work?" | Conclude yes because the happy-path test passed, ignoring the failing edge case in the same output | **Confirmation** — positive conclusion from one-sided evidence |
| (mid-task, new evidence contradicts the plan) | Keep going with the original plan rather than re-examine | **Anchoring** — framing unchanged despite contradiction |
| "Fix this one function" | Fix it, plus refactor three files, plus add a new dependency | **Scope creep** — undisclosed or irreversible additions |

Every check returns `PASS`, `FLAG`, or `BLOCK` with a one-sentence reason. You see the report inline with Claude's response. If you disagree with a flag, you override it — and the system learns your preferences locally over time.

## What it looks like in practice

When Claude is about to answer a non-trivial question, it spawns the validator in a fresh context. A typical report:

```
COVE-VERIFICATION
| Token                    | Question                 | Result     | Note                      |
|--------------------------|--------------------------|------------|---------------------------|
| src/auth/session.ts:42   | Does this file exist?    | CONFIRMED  | Read showed it            |
| UserService.findByEmail  | Does this symbol exist?  | NOT-FOUND  | Grep returned no matches  |

BIAS-VALIDATOR REPORT
  1. Groundedness : BLOCK — UserService.findByEmail cited but does not exist in the codebase
  2. Sycophancy   : PASS
  3. Confirmation : PASS
  4. Anchoring    : PASS
  5. Scope creep  : PASS

VERDICT : BLOCK
REQUIRED-FIXES :
  - Remove or correct the UserService.findByEmail reference
```

Claude then either revises the draft or surfaces the flag to you with its own assessment. You always see both sides and have the final word.

## Install

One command (also the update command — idempotent):

```bash
# User-wide — available in every Claude Code project on this machine
curl -sL https://raw.githubusercontent.com/danlex/ethicalhive/main/install-remote.sh | bash

# Current project only
curl -sL https://raw.githubusercontent.com/danlex/ethicalhive/main/install-remote.sh | bash -s .

# Specific project
curl -sL https://raw.githubusercontent.com/danlex/ethicalhive/main/install-remote.sh | bash -s /path/to/project
```

Or clone and install manually:

```bash
git clone https://github.com/danlex/ethicalhive.git
cd ethicalhive
bash install.sh                    # user-wide → ~/.claude/
bash install.sh .                  # current project → ./.claude/plugins/
bash install.sh /path/to/project   # specific project
```

Start a fresh Claude Code session, then:
- invoke explicitly with `/tvl-tech-bias-validator`,
- or just ask Claude to *"run the bias validator"* or *"check your work"*,
- or let Claude self-invoke it before delivering non-trivial answers (which it will — the subagent is marked to run proactively).

### Updating

Re-run the one-liner. The installer is idempotent — it wipes the plugin's managed subdirs (`.claude-plugin/`, `skills/`, `agents/`, `cases/`, `references/`) and re-copies from the latest main. Your local case database (`~/.claude/tvl-tech-bias-validator/cases/`) and calibration (`calibration.md`, `recent-overrides.md`) are never touched.

## How the audit loop works

1. **Audit** — Before delivering a non-trivial draft, Claude spawns the `tvl-tech-bias-validator` subagent.
2. **Verify** — The subagent extracts every concrete claim in the draft (file paths, symbols, values, outcomes) and runs Read / Grep / Glob to confirm or refute each one. This is Chain-of-Verification (Dhuliawala et al. 2023).
3. **Five checks** — Groundedness, Sycophancy, Confirmation, Anchoring, Scope creep. Each returns PASS / FLAG / BLOCK.
4. **Negotiate** — The main session reads the findings and independently agrees or disagrees with each.
5. **You decide** — Findings are shown alongside the response. You have the final word.
6. **Log** — The case is written locally with all three perspectives (validator, agent, you).
7. **Learn** — Your overrides feed a consultative memory for the next audit; repeat patterns trigger governed calibration proposals.

## The components

| Agent | Role | Runs on |
|---|---|---|
| `tvl-tech-bias-validator` | Audits drafts — CoVe verification + 5 checks | Sonnet |
| `tvl-tech-bias-validator-learner` | Post-audit learning loop — appends overrides, drafts calibration proposals at threshold | Haiku |
| `judge-council` | Reviews proposed rubric/calibration changes — spawned 3× in parallel across tiers for genuine independence | Opus + Sonnet + Haiku |

| Skill | Invocation | Role |
|---|---|---|
| `tvl-tech-bias-validator` | `/tvl-tech-bias-validator` | Full audit workflow + learning loop |
| `tvl-tech-bias-validator-dashboard` | `/tvl-tech-bias-validator-dashboard` | Read-only stats: verdict mix, override rates, drift, calibration state |

## Learning loop (local)

Every audit is logged to `~/.claude/tvl-tech-bias-validator/cases/`. Two feedback levels:

- **Fast (consultative).** Your overrides append to `recent-overrides.md` (last 20, FIFO). The subagent reads these as hints on the next audit. They bias judgment but never suppress a flag. No governance.
- **Slow (governed).** At ≥ 10 total cases with ≥ 3 overrides on a single check, the learner auto-drafts a calibration proposal. The judge council reviews; only with council APPROVE + your approval does `calibration.md` update. The rubric itself never auto-changes.

## Governance

The validator's rubric is its constitution. It does not auto-update.

- **Calibration changes** (sensitivity, project notes): ≥ 2 of 3 model tiers APPROVE + human.
- **Constitutional changes** (new checks, changed criteria): 3 of 3 model tiers APPROVE + human.
- **Multi-tier governance.** The council is spawned three times in parallel — Opus + Sonnet + Haiku — so model diversity (not three personas in one prompt) provides the independence. Agreement across tiers is a stronger signal than any single model's internal debate.
- **Never auto-applied.** The rubric, the BLOCK/FLAG/PASS criteria, the CoVe rules, the verdict calculation.

## Plugin structure

```
ethicalhive/
├── .claude-plugin/
│   └── plugin.json                 # plugin manifest
├── skills/
│   ├── tvl-tech-bias-validator/
│   │   └── SKILL.md                # audit workflow + learning loop
│   └── tvl-tech-bias-validator-dashboard/
│       └── SKILL.md                # stats dashboard
├── agents/
│   ├── tvl-tech-bias-validator.md          # the auditor (CoVe + 5 checks)
│   ├── tvl-tech-bias-validator-learner.md  # post-audit learning loop
│   └── judge-council.md                    # governance council
├── cases/
│   └── case-schema.json            # JSON schema for logged cases
├── experiments/                    # test suites, results, runner
├── references/
│   ├── prior-art.md                # vs CoVe, SelfCheckGPT, Semantic Entropy
│   ├── research.md                 # per-check bibliography
│   ├── glossary.md                 # related-terms taxonomy
│   └── mindmap.md                  # research landscape
├── install.sh                      # local installer
└── install-remote.sh               # curl|bash bootstrap for the one-liner
```

## Honest limitations

- **Not state-of-the-art.** Sampling-based methods (Semantic Entropy, SelfCheckGPT) and hidden-state probes extract signal this rubric cannot access. See `references/prior-art.md` for the full comparison.
- **Circularity.** Drafter and auditor share the same model family. Error patterns shared across all Claude models will not be caught by another Claude.
- **The validator has its own confirmation bias.** It is primed to find problems. It tracks its own override rate to stay honest.
- **Learning is pattern-based, not parameter-based.** No model fine-tuning; the calibration file adjusts heuristics only.
- **Local-only.** Cases never leave your machine in the current version. Community sharing was removed pending deterministic redaction, full-preview consent gate, project blocklist, and category-refusal hardening.
