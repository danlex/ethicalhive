#!/usr/bin/env bash
set -euo pipefail

# bias-validator installer
#
# Three installation methods:
#
#   bash install.sh                        # user scope — symlinks to ~/.claude/
#   bash install.sh project /path/to/proj  # project scope — symlinks to project's .claude/
#   bash install.sh plugin /path/to/proj   # plugin mode — copies into project as a plugin
#
# After install, Claude Code auto-discovers the skill and agents.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCOPE="${1:-user}"

case "$SCOPE" in
  user)
    SKILL_DIR="$HOME/.claude/skills"
    AGENT_DIR="$HOME/.claude/agents"

    mkdir -p "$SKILL_DIR" "$AGENT_DIR"

    # Skill
    rm -rf "$SKILL_DIR/bias-validator" 2>/dev/null || true
    ln -s "$SCRIPT_DIR/skills/bias-validator" "$SKILL_DIR/bias-validator"
    echo "Linked skill:    $SKILL_DIR/bias-validator"

    # Agents
    for agent in bias-validator judge-council case-submitter; do
      rm -f "$AGENT_DIR/$agent.md" 2>/dev/null || true
      ln -s "$SCRIPT_DIR/agents/$agent.md" "$AGENT_DIR/$agent.md"
      echo "Linked agent:    $AGENT_DIR/$agent.md"
    done
    ;;

  project)
    if [ -z "${2:-}" ]; then
      echo "Usage: bash install.sh project /path/to/project"
      exit 1
    fi
    PROJECT_ROOT="$2"
    SKILL_DIR="$PROJECT_ROOT/.claude/skills"
    AGENT_DIR="$PROJECT_ROOT/.claude/agents"

    mkdir -p "$SKILL_DIR" "$AGENT_DIR"

    rm -rf "$SKILL_DIR/bias-validator" 2>/dev/null || true
    ln -s "$SCRIPT_DIR/skills/bias-validator" "$SKILL_DIR/bias-validator"
    echo "Linked skill:    $SKILL_DIR/bias-validator"

    for agent in bias-validator judge-council case-submitter; do
      rm -f "$AGENT_DIR/$agent.md" 2>/dev/null || true
      ln -s "$SCRIPT_DIR/agents/$agent.md" "$AGENT_DIR/$agent.md"
      echo "Linked agent:    $AGENT_DIR/$agent.md"
    done
    ;;

  plugin)
    if [ -z "${2:-}" ]; then
      echo "Usage: bash install.sh plugin /path/to/project"
      exit 1
    fi
    PROJECT_ROOT="$2"
    PLUGIN_DIR="$PROJECT_ROOT/.claude/plugins/bias-validator"

    mkdir -p "$PLUGIN_DIR"
    cp -r "$SCRIPT_DIR/.claude-plugin" "$PLUGIN_DIR/"
    cp -r "$SCRIPT_DIR/skills" "$PLUGIN_DIR/"
    cp -r "$SCRIPT_DIR/agents" "$PLUGIN_DIR/"
    cp -r "$SCRIPT_DIR/cases" "$PLUGIN_DIR/"
    cp -r "$SCRIPT_DIR/references" "$PLUGIN_DIR/"
    echo "Installed plugin: $PLUGIN_DIR"
    ;;

  *)
    echo "Usage: bash install.sh [user|project|plugin] [/path/to/project]"
    echo ""
    echo "  user              Symlink to ~/.claude/ (available in all projects)"
    echo "  project <path>    Symlink to a project's .claude/ directory"
    echo "  plugin <path>     Copy into a project as a self-contained plugin"
    exit 1
    ;;
esac

# --- Global case database (always created) ---

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
echo "Invoke via /bias-validator or ask Claude to 'run the bias validator'."
