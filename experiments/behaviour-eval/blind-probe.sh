#!/usr/bin/env bash
# blind-probe.sh - run a factual probe through a fresh headless Claude (claude -p)
# from a neutral temp directory, so the model gets NO repo or session context
# (no project CLAUDE.md, no project memory). This removes the "never invent"
# priming confound of running the probe as an in-session subagent.
#
# Usage: blind-probe.sh <model-alias> <prompt-file>
#   model-alias: opus | sonnet | haiku
set -euo pipefail
model="${1:?model alias required}"
prompt_file="${2:?prompt file required}"
prompt="$(cat "$prompt_file")"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
cd "$work"   # neutral cwd: no CLAUDE.md, no project memory in scope
claude -p "$prompt" --model "$model" --allowed-tools "" 2>/dev/null
