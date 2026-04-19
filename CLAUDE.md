# EthicalHive

AI integrity through adversarial self-audit — local-only.

A Claude Code plugin that audits drafts before delivery. Five checks (Groundedness, Sycophancy, Confirmation, Anchoring, Scope creep) with a Chain-of-Verification stage. Every audit is logged locally and feeds a governed learning loop. **No data leaves your machine.**

**Advisory, not blocking.** The validator gives structured feedback. The human decides.
**Self-aware.** The validator knows it has its own confirmation bias. It tracks its own override rate.
**Governed.** Changes to the rubric go through a judge council (3 model tiers) + human approval. No auto-updates. No corruption.
**Local-only.** Cases accumulate in `~/.claude/tvl-tech-bias-validator/`. Community hive submission is disabled pending hardening.

## Install

One-liner (also the update command — idempotent, wipes and re-copies on re-run):

```bash
# User-wide — available in all Claude Code projects on this machine
curl -sL https://raw.githubusercontent.com/danlex/ethicalhive/main/install-remote.sh | bash

# Current project only
curl -sL https://raw.githubusercontent.com/danlex/ethicalhive/main/install-remote.sh | bash -s .

# Specific project
curl -sL https://raw.githubusercontent.com/danlex/ethicalhive/main/install-remote.sh | bash -s /path/to/project
```

Or clone + install manually:

```bash
git clone https://github.com/danlex/ethicalhive.git
cd ethicalhive
bash install.sh                    # user-wide
bash install.sh .                  # current project
bash install.sh /path/to/project   # specific project
```

Local case database at `~/.claude/tvl-tech-bias-validator/` (cases, calibration, recent-overrides) is never touched by the installer. Start a fresh Claude Code session in the project and invoke via `/tvl-tech-bias-validator`.

## How it works

1. **Audit** — Before delivering non-trivial output, Claude spawns the tvl-tech-bias-validator
2. **Verify** — Subagent extracts every claim, runs Read/Grep/Glob to confirm or refute each one
3. **Five checks** — Groundedness, Sycophancy, Confirmation, Anchoring, Scope creep
4. **Negotiate** — Main session evaluates findings, confirms or disputes each flag
5. **Human decides** — Findings presented alongside the response, user has final word
6. **Log** — Case saved locally with all three perspectives (validator, agent, human)
7. **Learn** — Recent overrides bias next audit; repeat overrides trigger auto-drafted calibration proposals through the judge council

## The agents

| Agent | Role | Runs on |
|---|---|---|
| `tvl-tech-bias-validator` | Audits drafts — CoVe verification + 5 checks | Sonnet |
| `tvl-tech-bias-validator-learner` | Post-audit learning loop (appends overrides, drafts calibration proposals) | Haiku |
| `judge-council` | Reviews proposed rubric/calibration changes — spawned 3× in parallel for true model-tier diversity | Opus + Sonnet + Haiku |

## Skills

- `/tvl-tech-bias-validator` — full audit workflow
- `/tvl-tech-bias-validator-dashboard` — verdict mix, per-check override rates, drift direction

## Learning loop (local)

Every audit is logged to `~/.claude/tvl-tech-bias-validator/cases/`. Two levels:

- **Fast (consultative):** human overrides append to `recent-overrides.md` (last 20 FIFO). The subagent reads these as hints on next audit. They bias judgment but never suppress a flag.
- **Slow (governed):** at n≥10 cases with ≥3 overrides on a single check, an auto-drafted calibration proposal is sent to the judge council. Council APPROVE + human approval is required before `calibration.md` updates. The rubric itself never auto-changes.

## Governance

The validator's rubric is its constitution. It does not auto-update.

- **Calibration changes** (sensitivity, project notes): ≥ 2 of 3 model tiers APPROVE + human
- **Constitutional changes** (new checks, changed criteria): 3 of 3 model tiers APPROVE + human
- **Multi-tier governance:** the council is spawned three times in parallel — Opus + Sonnet + Haiku — so model diversity (not three personas in one prompt) provides the independence. Agreement across tiers is a stronger signal than any single model's internal debate.
- **Never auto-applied:** the rubric, the BLOCK/FLAG/PASS criteria, the CoVe rules, the verdict calculation.

## Why community sharing is off

The case-submitter PR flow was too intrusive. It relied on a single Haiku pass to anonymize and a single yes/no for user consent, with no deterministic redaction and no full-JSON preview. Before re-enabling: add regex redaction, full-preview gate, project blocklist, category refusal (PII/credentials/legal/medical/financial).

## Known limitations

- **Not SOTA.** Sampling-based methods and hidden-state probes are stronger. See `references/prior-art.md`.
- **Circularity.** Drafter and auditor share the same model family.
- **The validator has its own confirmation bias.** It's primed to find problems. It tracks its own override rate to stay honest.
- **Learning is pattern-based, not parameter-based.** No model fine-tuning.
- **Local-only.** Cases never leave your machine in the current version.
