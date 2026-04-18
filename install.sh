#!/usr/bin/env bash
set -euo pipefail

# bias-validator installer — plugin mode only
#
#   bash install.sh /path/to/project
#
# Copies the plugin into the target project as a self-contained
# bundle at .claude/plugins/bias-validator/. Claude Code auto-discovers
# the skill and agents on the next session start.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "${1:-}" ]; then
  echo "Usage: bash install.sh /path/to/project"
  exit 1
fi

PROJECT_ROOT="$1"
PLUGIN_DIR="$PROJECT_ROOT/.claude/plugins/bias-validator"

mkdir -p "$PLUGIN_DIR"
cp -r "$SCRIPT_DIR/.claude-plugin" "$PLUGIN_DIR/"
cp -r "$SCRIPT_DIR/skills" "$PLUGIN_DIR/"
cp -r "$SCRIPT_DIR/agents" "$PLUGIN_DIR/"
cp -r "$SCRIPT_DIR/cases" "$PLUGIN_DIR/"
cp -r "$SCRIPT_DIR/references" "$PLUGIN_DIR/"
echo "Installed plugin: $PLUGIN_DIR"

# Global case database — shared across all projects, written by case-submitter

GLOBAL_DIR="$HOME/.claude/bias-validator"
mkdir -p "$GLOBAL_DIR/cases"

if [ ! -f "$GLOBAL_DIR/calibration.md" ]; then
  cat > "$GLOBAL_DIR/calibration.md" << 'CALIBRATION_EOF'
# Bias Validator Calibration

This file is updated through the judge council governance process.
Changes require council review + human approval.

**The validator has its own confirmation bias.** It is primed to find problems.
When reading these patterns, weight override data (human said "no, ship it")
as strongly as catch data (human said "yes, good catch").

## Approved patterns

(none yet — patterns appear after cases are reviewed by the judge council)

## Pending proposals

(none yet)

## Validator self-assessment

- Override rate target: 10-30%
- Below 10%: validator may be too lenient
- Above 40%: validator is too strict

## Stats

- Total cases: 0
- True catches: 0
- False positives: 0
- Clean passes: 0
- Override rate: n/a
CALIBRATION_EOF
  echo "Created calibration: $GLOBAL_DIR/calibration.md"
fi

echo ""
echo "Done. Global case database: $GLOBAL_DIR/cases/"
echo "Start a fresh Claude Code session in the project. Invoke via /bias-validator."
