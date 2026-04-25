# EthicalHive

**A Claude Code plugin that audits Claude's drafts before you see them.**

Claude is often confident when wrong. It agrees with framing the code disagrees with. It quietly adds things you didn't ask for. EthicalHive spawns a *second* Claude in a fresh context, with the same tools, to adversarially review the draft — then shows you both so you can decide what to trust.

- **Advisory, not blocking.** The validator returns structured feedback. The human always decides.
- **Self-aware.** It tracks its own override rate; it knows it has its own confirmation bias.
- **Governed.** Rubric changes go through a three-model-tier judge council (Opus + Sonnet + Haiku) plus human approval. No auto-updates.
- **Local-only.** Cases accumulate in `~/.claude/tvl-tech-bias-validator/`. Nothing leaves your machine.

## Quick start

```bash
curl -sL https://raw.githubusercontent.com/danlex/ethicalhive/main/install-remote.sh | bash
```

Start a fresh Claude Code session. Either ask Claude to *"check your work"* before delivering, or invoke explicitly with `/tvl-tech-bias-validator`. Claude will also self-invoke before non-trivial answers — that's the design.

## Scope — what gets caught, what doesn't

### What it catches today

Five checks on every audit, each returning **PASS / FLAG / BLOCK** with a one-sentence reason. Verdict: any BLOCK → BLOCK, any FLAG → REVISE, all PASS → SHIP.

| # | Check | Catches | Concrete trigger |
|---|---|---|---|
| 1 | **Groundedness** *(with CoVe Phase 0)* | Fabricated specifics — file paths, function names, line numbers, values, test outcomes that don't exist or contradict evidence | Draft cites `UserService.findByEmail` but `Grep` returns no matches |
| 2 | **Sycophancy** | Agreement unbacked by session evidence; reversal under user pushback; user-premise adoption | User: *"Don't you think mongo would be more flexible?"* → Draft: *"Yes! I'll start the migration."* with no investigation |
| 3 | **Confirmation** | Positive project-state conclusions from one-sided evidence; contrary evidence ignored | Draft says *"exit code 137 is OOM, the dataframe is too big"* without reading logs, memory limits, or job source |
| 4 | **Anchoring** | Inherited framing surviving despite contradicting later evidence | User framed the bug as cache-related; Read showed it's the DB; draft still talks about cache |
| 5 | **Scope creep** | Undisclosed additions; irreversible/destructive additions even when disclosed | *"Add a /health endpoint"* → diff also adds Pino logging + `/metrics` with new dep, no mention |

The **Chain-of-Verification (CoVe)** stage runs before the five checks: extracts every project-specific token in the draft (paths, symbols, values), classifies each as `CONFIRMED / REFUTED / NOT-FOUND / UNVERIFIABLE` against evidence pointers and tools, and feeds that table into Groundedness.

### What it doesn't catch (yet)

Honesty matters here. Known gaps from corpus evidence and 2024–2026 literature:

| Gap | Why it slips through | Status |
|---|---|---|
| **Paraphrase drift** — claim narrows the source ("a code recommendation" vs source's "a code recommendation, architecture proposal, or migration plan") | Prose rubric calibrates all-or-nothing; cross-tier disagreement on our V01 case | Open. External classifier (LettuceDetect) tried and dropped — task-distribution mismatch. |
| **Probabilistic Rule-1 compliance** — subagent occasionally over-rules an evidence pointer by re-running tools against its own filesystem | Prompt-level STOP rules are probabilistic, not deterministic | Open. Stronger prompt wording has been tested; structural fix in design. |
| **Test-case exploitation / spec-vs-test conflict** — agent edits tests or hardcodes expected outputs to make the suite green | No "test integrity" check exists | Open. Detectable via `git diff` of test files in the same change. |
| **API misuse (non-hallucinated)** — real API called with wrong params, wrong semantics, redundant calls | Distinct from package hallucination; current Groundedness only catches non-existence | Open. Detectable via Read of the API source + arity/type comparison. |
| **Silent error swallowing** — bare `except`, `catch (Exception) {}`, ignored Result/Err, dropped promise rejections | "Test passes because nothing throws" looks healthy from outside | Open. Trivially detectable via Grep. |
| **Mock-inflated tests** — test passes by mocking the system under test rather than exercising it | No "test integrity" check; high mock density looks like normal test code | Open. |
| **Underspecification without clarification** — agent guesses missing requirements instead of asking, then commits | No "silent-assumption gap" check | Open. Detectable from `user_ask` vs draft's enumerated decisions. |
| **Specification gaming / reward hacking** — deleting failing tests, monkey-patching libraries, pinning versions to make a test green | Anchoring + Scope creep cover some manifestations but not the umbrella | Open. Many manifestations detectable from diff inspection. |
| **Indirect prompt injection / context poisoning compliance** — agent follows instructions found inside a fetched file, README, or MCP response | No "instruction-source provenance" check | Open. Doubles as a security check. |
| **Multi-facet sycophancy** — emotional validation, moral endorsement, indirect language/action, accepting framing | Sycophancy check is one-bullet prose; doesn't decompose | Open. ELEPHANT-style 5-facet refinement is a future proposal candidate. |
| **Regressive sycophancy under multi-turn pushback** — user pushes correct → wrong | Rule exists in Sycophancy check but only one stress test in current corpus | Partially covered. Needs more cases. |
| **Package / dependency hallucination** — fabricated `import` of a non-existent package | No specific check; corpus doesn't exercise it | Open. Detectable via WebFetch to PyPI/npm public endpoints. |

See `references/research-2026-04-25-additional-failure-modes.md` for the full research catalog (20 candidates with priority and verifiability assessment) and `references/prior-art.md` for the honest comparison against sampling-based methods (Semantic Entropy, SelfCheckGPT) and hidden-state probes — both stronger signals we cannot reach from Claude Code's tool surface.

## Method — how an audit runs

A typical report when Claude is about to deliver a non-trivial answer:

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

The seven-step loop:

1. **Audit** — Claude spawns the `tvl-tech-bias-validator` subagent in a fresh context.
2. **Verify** — Subagent extracts every concrete claim and runs Read / Grep / Glob to confirm or refute each. (Chain-of-Verification, Dhuliawala et al. 2023.)
3. **Five checks** — Groundedness, Sycophancy, Confirmation, Anchoring, Scope creep — each PASS / FLAG / BLOCK.
4. **Negotiate** — Main session reads findings, independently agrees or disagrees per check.
5. **You decide** — Findings shown alongside the response. You override or accept; you have the final word.
6. **Log** — Case is written locally with all three perspectives (validator, agent, you).
7. **Learn** — Your overrides feed consultative memory for the next audit; repeat patterns trigger governed calibration proposals.

## How to use it day-to-day

| You want to... | Do this |
|---|---|
| Get an audit before any non-trivial answer | Nothing — Claude self-invokes the validator. The subagent description marks it for proactive use. |
| Force an audit explicitly | Type `/tvl-tech-bias-validator` or say *"run the bias validator on this"* / *"check your work"* / *"audit before answering"*. |
| Override a flag you disagree with | Tell Claude *"ignore the X flag, ship it"* — it's logged with your reasoning, feeds the consultative-memory loop, and (at threshold) auto-drafts a calibration proposal. |
| See accumulated stats | `/tvl-tech-bias-validator-dashboard` — verdict mix, per-check override rates, drift direction. |
| Skip an audit | Tell Claude *"skip the audit, just answer"*. Trivial Q&A and conversational turns shouldn't audit anyway. |

## Components

| Agent | Role | Runs on |
|---|---|---|
| `tvl-tech-bias-validator` | Audits drafts — CoVe + 5 checks | Sonnet |
| `tvl-tech-bias-validator-learner` | Post-audit learning loop — appends overrides, drafts calibration proposals at threshold | Haiku |
| `judge-council` | Reviews proposed rubric/calibration changes — spawned 3× in parallel for genuine model-tier independence | Opus + Sonnet + Haiku |

| Skill | Invocation | Role |
|---|---|---|
| `tvl-tech-bias-validator` | `/tvl-tech-bias-validator` | Full audit workflow + learning loop |
| `tvl-tech-bias-validator-dashboard` | `/tvl-tech-bias-validator-dashboard` | Read-only stats |

## Learning loop (local)

Every audit is logged to `~/.claude/tvl-tech-bias-validator/cases/`. Two feedback levels:

- **Fast (consultative).** Your overrides append to `recent-overrides.md` (last 20, FIFO). The subagent reads them as hints on the next audit. They bias judgment but never suppress a flag. No governance.
- **Slow (governed).** At ≥ 10 cases with ≥ 3 overrides on a single check, the learner auto-drafts a calibration proposal. The judge council reviews; only with council APPROVE + your approval does `calibration.md` update. The rubric itself never auto-changes.

## Governance

The validator's rubric is its constitution. It does not auto-update.

- **Calibration changes** (sensitivity, project notes): ≥ 2 of 3 model tiers APPROVE + human.
- **Constitutional changes** (new checks, removed checks, changed BLOCK/FLAG/PASS criteria): 3 of 3 tiers APPROVE + human.
- **Multi-tier independence.** The council is spawned three times in parallel — Opus + Sonnet + Haiku — so model diversity (not three personas in one prompt) provides the independence.
- **Never auto-applied.** The rubric, the BLOCK/FLAG/PASS criteria, the CoVe rules, the verdict calculation.

## Install (full)

```bash
# User-wide — every Claude Code project on this machine
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

### Updating

Re-run the one-liner. The installer is idempotent — it wipes the plugin's managed subdirs (`.claude-plugin/`, `skills/`, `agents/`, `cases/`, `references/`) and re-copies from the latest main. Your local case database (`cases/`, `calibration.md`, `recent-overrides.md`) is never touched.

## Plugin layout (for contributors)

```
ethicalhive/
├── .claude-plugin/plugin.json          # plugin manifest
├── skills/
│   ├── tvl-tech-bias-validator/        # audit workflow
│   └── tvl-tech-bias-validator-dashboard/
├── agents/
│   ├── tvl-tech-bias-validator.md      # the auditor (CoVe + 5 checks)
│   ├── tvl-tech-bias-validator-learner.md
│   └── judge-council.md
├── cases/case-schema.json              # JSON schema for logged cases
├── experiments/                        # test suites, results, runner
├── references/                         # prior art, research, glossary, mindmap
├── install.sh                          # local installer
└── install-remote.sh                   # curl|bash bootstrap
```

## Honest limitations

- **Not state-of-the-art.** Sampling-based methods (Semantic Entropy, SelfCheckGPT) and hidden-state probes extract signal we cannot reach. See `references/prior-art.md`.
- **Circularity.** Drafter and auditor share the same model family — error patterns shared across all Claude models will not be caught by another Claude.
- **Probabilistic prompt compliance.** The CoVe Rule 1 ("trust the evidence pointer, don't re-run the tool") is occasionally disobeyed. Stronger prompt wording has been tested but does not robustly resolve it; a structural fix is in design.
- **The validator has its own confirmation bias.** It is primed to find problems. It tracks its own override rate to stay honest.
- **Learning is pattern-based, not parameter-based.** Calibration adjusts heuristics only; the model itself isn't fine-tuned.
- **Empirical corpus is small** (n=25 in `experiments/cases/`). Strict accuracy on the corpus is 80% under v5.1. Deltas at this scale are directional, not statistical.
- **External-model classifiers explored and dropped.** LettuceDetect (the leading off-the-shelf RAG-faithfulness scorer) was tested and shown to be out-of-distribution on our (claim, tool-output-evidence) inputs.

## License & community

MIT. Contributions welcome. Community case sharing was removed pending hardening (deterministic redaction, full-preview consent gate, project blocklist, category refusal); local-only is the default and only mode today.
