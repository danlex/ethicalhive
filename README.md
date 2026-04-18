# EthicalHive

AI integrity through adversarial self-audit — local-only.

A Claude Code plugin that audits drafts before delivery. Five checks (Groundedness, Sycophancy, Confirmation, Anchoring, Scope creep) with a Chain-of-Verification stage. Every audit is logged locally and feeds a governed learning loop. **No data leaves your machine.**

**Advisory, not blocking.** The validator gives structured feedback. The human decides.
**Self-aware.** The validator knows it has its own confirmation bias. It tracks its own override rate.
**Governed.** Changes to the rubric go through a judge council (3 independent reviewers) + human approval. No auto-updates. No corruption.
**Local-only.** Cases accumulate in `~/.claude/tvl-tech-bias-validator/`. Nothing is shared externally. Community hive submission is intentionally disabled pending hardening.

## Install

One-liner:

```bash
curl -sL https://raw.githubusercontent.com/danlex/ethicalhive/main/install-remote.sh | bash -s /path/to/your/project
```

Or clone and install manually:

```bash
git clone https://github.com/danlex/ethicalhive.git
cd ethicalhive
bash install.sh /path/to/your/project
```

Either path copies the plugin as a self-contained bundle into `/path/to/your/project/.claude/plugins/tvl-tech-bias-validator/`. Start a fresh Claude Code session in the project and invoke via `/tvl-tech-bias-validator`, or ask Claude to "run the bias validator".

### Updating

Re-run the one-liner. The installer is idempotent — it wipes the plugin's managed subdirs (`.claude-plugin/`, `skills/`, `agents/`, `cases/`, `references/`) and re-copies from the latest main. Your local case database (`~/.claude/tvl-tech-bias-validator/cases/`) and calibration (`calibration.md`, `recent-overrides.md`) are never touched.

## How it works

1. **Audit** — Before delivering non-trivial output, Claude spawns the tvl-tech-bias-validator
2. **Verify** — Subagent extracts every claim, runs Read/Grep/Glob to confirm or refute each one
3. **Five checks** — Groundedness, Sycophancy, Confirmation, Anchoring, Scope creep
4. **Negotiate** — Main session evaluates findings, confirms or disputes each flag
5. **Human decides** — Findings presented alongside the response, user has final word
6. **Log** — Case saved locally with all three perspectives (validator, agent, human)
7. **Learn** — Recent overrides feed consultative memory; n≥10 cases with repeat overrides trigger auto-drafted calibration proposals (judge-council + human approval)

## The agents

| Agent | Role | Runs on |
|---|---|---|
| `tvl-tech-bias-validator` | Audits drafts — CoVe verification + 5 checks | Sonnet |
| `tvl-tech-bias-validator-learner` | Processes resolved cases into the learning loop — appends overrides, drafts calibration proposals at threshold | Haiku |
| `judge-council` | Reviews proposed rubric/calibration changes — 3 independent judges | Sonnet |

## The skills

| Skill | Invocation | Role |
|---|---|---|
| `tvl-tech-bias-validator` | `/tvl-tech-bias-validator` | Full audit workflow + learning loop |
| `tvl-tech-bias-validator-dashboard` | `/tvl-tech-bias-validator-dashboard` | Read-only stats: verdict mix, override rates, drift, calibration state |

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
│   ├── tvl-tech-bias-validator-learner.md  # post-audit learning loop (overrides + proposal drafts)
│   └── judge-council.md                    # governance for rubric/calibration changes
├── cases/
│   └── case-schema.json            # JSON schema for logged cases
├── experiments/
│   ├── cases/                      # test suites (25 cases across 4 suites)
│   ├── results/                    # experiment reports (exp-01 through exp-06)
│   └── run-suite.sh                # automated suite runner
├── references/
│   ├── prior-art.md                # vs CoVe, SelfCheckGPT, Semantic Entropy
│   ├── research.md                 # 2023-2026 citations per check
│   ├── glossary.md                 # related-terms taxonomy
│   └── mindmap.md                  # research landscape
├── install.sh                      # local installer
└── install-remote.sh               # curl|bash bootstrap for the one-liner
```

## Learning loop (local)

Every audit is logged to `~/.claude/tvl-tech-bias-validator/cases/`. Two levels of feedback:

- **Fast (consultative):** human overrides append to `recent-overrides.md` (last 20 FIFO). The subagent reads these as hints on next audit. They bias judgment but never suppress a flag. No governance.
- **Slow (governed):** at n≥10 cases with ≥3 overrides on a single check, an auto-drafted calibration proposal is sent to the judge council. Council APPROVE + human approval is required before `calibration.md` updates. The rubric itself never auto-changes.

## Governance

The validator's rubric is its constitution. It does not auto-update.

- **Calibration changes** (sensitivity, project notes): 2/3 judge council approval + human
- **Constitutional changes** (new checks, changed criteria): 3/3 unanimous + human
- **Never auto-applied**: the rubric, the BLOCK/FLAG/PASS criteria, the CoVe rules, the verdict calculation

## Known limitations

- **Not SOTA.** Sampling-based methods and hidden-state probes are stronger. See `references/prior-art.md`.
- **Circularity.** Drafter and auditor share the same model family.
- **The validator has its own confirmation bias.** It's primed to find problems. It tracks its own override rate to stay honest.
- **Learning is pattern-based, not parameter-based.** No model fine-tuning.
- **Local-only.** Cases never leave your machine in the current version. Community sharing was removed pending deterministic redaction, full-preview consent gate, blocklist, and category-refusal hardening.
