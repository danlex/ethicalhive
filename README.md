# EthicalHive

Collective AI integrity through adversarial self-audit.

Every Claude Code instance running EthicalHive is a sensor. When the validator catches a fabrication, flags a false positive, or encounters an edge case — it asks the user one question: "share anonymously?" The cases flow to the hive. The validator evolves from real-world usage, not from one person's test suite.

**Advisory, not blocking.** The validator gives structured feedback. The human decides.
**Self-aware.** The validator knows it has its own confirmation bias. It tracks its own error rate.
**Governed.** Changes to the rubric go through a judge council (3 independent reviewers) + human approval. No auto-updates. No corruption.
**Open source.** Anyone can install it. Every user contributes to the collective intelligence just by saying "yes" when asked.

## Install

Three modes — pick one.

**User scope** (recommended — available in every project on the machine):

```bash
git clone https://github.com/danlex/ethicalhive.git
cd ethicalhive
bash install.sh
```

Symlinks to `~/.claude/skills/` and `~/.claude/agents/`. `git pull` to update.

**Project scope** (one project only, via symlink):

```bash
bash install.sh project /path/to/your/project
```

**Plugin mode** (self-contained copy inside the project — no external repo dependency):

```bash
bash install.sh plugin /path/to/your/project
```

Copies the full plugin into `/path/to/your/project/.claude/plugins/bias-validator/`. Good for teammates who won't clone EthicalHive separately.

After install, start a fresh Claude Code session in the target project. Invoke via `/bias-validator` or ask Claude to "run the bias validator".

## How it works

1. **Audit** — Before delivering non-trivial output, Claude spawns the bias-validator
2. **Verify** — Subagent extracts every claim, runs Read/Grep/Glob to confirm or refute each one
3. **Five checks** — Groundedness, Sycophancy, Confirmation, Anchoring, Scope creep
4. **Negotiate** — Main session evaluates findings, confirms or disputes each flag
5. **Human decides** — Findings presented alongside the response, user has final word
6. **Log** — Case saved locally with all three perspectives (validator, agent, human)
7. **Share** — If interesting: "Share anonymously?" → one word → case flows to the hive
8. **Evolve** — Accumulated cases inform rubric changes (through judge council governance)

## The agents

| Agent | Role | Runs on |
|---|---|---|
| `bias-validator` | Audits drafts — CoVe verification + 5 checks | Sonnet |
| `case-submitter` | Anonymizes + submits interesting cases to the hive | Haiku (fast, cheap) |
| `judge-council` | Reviews proposed rubric changes — 3 independent judges | Sonnet |

## Plugin structure

```
ethicalhive/
├── .claude-plugin/
│   └── plugin.json                 # plugin manifest
├── skills/
│   └── bias-validator/
│       └── SKILL.md                # the skill: full audit workflow + learning loop
├── agents/
│   ├── bias-validator.md           # the auditor (CoVe + 5 checks)
│   ├── case-submitter.md           # anonymize + share with hive
│   └── judge-council.md            # governance for rubric changes
├── cases/
│   ├── case-schema.json            # JSON schema for logged cases
│   └── community/                  # cases from the hive (submitted via PRs)
├── experiments/
│   ├── cases/                      # test suites (25 cases across 4 suites)
│   ├── results/                    # experiment reports (exp-01 through exp-06)
│   └── run-suite.sh                # automated suite runner
├── references/
│   ├── prior-art.md                # vs CoVe, SelfCheckGPT, Semantic Entropy
│   ├── research.md                 # 2023-2026 citations per check
│   ├── glossary.md                 # related-terms taxonomy
│   └── mindmap.md                  # research landscape
└── install.sh                      # installer (user/project/plugin scope)
```

## How the hive works

What you see:

```
You: Fix the auth bug

Claude: [runs audit internally]
        [catches that it fabricated a file path]
        [fixes itself, delivers correct response]

        Fixed the auth validation in src/middleware/auth.ts...

        The validator caught a fabricated path in my first draft
        and I corrected it before showing you.

        Share anonymously with the community? This helps the
        validator get smarter for everyone. (yes/no)

You: yes

Claude: Shared. ✓
```

That's it. No JSON to review. No PR to understand. No programming. One word: "yes."

Behind the scenes, the case-submitter (running on Haiku, fast and cheap) anonymizes the case, strips your project details, preserves the failure pattern ("fabricated file path, caught by CoVe NOT-FOUND"), and submits a PR to `danlex/ethicalhive`. A maintainer reviews it later. When enough cases accumulate showing the same pattern, the rubric evolves — through the judge council, with human approval.

Every Claude Code instance running this plugin is a worker bee. The repo is the hive. The cases are the honey. The judge council is the immune system that keeps the rubric from being corrupted.

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
- **The hive needs scale.** At n=19 internal cases, the rubric tied a baseline. At n=500+ community cases, patterns become statistically meaningful.
