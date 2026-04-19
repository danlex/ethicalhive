#!/usr/bin/env bash
set -euo pipefail

# tvl-tech-bias-validator installer
#
#   bash install.sh                    # user-wide — installs to ~/.claude/, available in all projects
#   bash install.sh .                  # current project — installs to ./.claude/plugins/
#   bash install.sh /path/to/project   # specific project
#
# Idempotent: re-running wipes and re-copies managed files.
# Your local case DB at ~/.claude/tvl-tech-bias-validator/ is never touched.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-}"

install_user_wide() {
  local agents_dir="$HOME/.claude/agents"
  local skills_dir="$HOME/.claude/skills"
  mkdir -p "$agents_dir" "$skills_dir"

  rm -f  "$agents_dir/tvl-tech-bias-validator.md" \
         "$agents_dir/tvl-tech-bias-validator-learner.md" \
         "$agents_dir/judge-council.md"
  rm -rf "$skills_dir/tvl-tech-bias-validator" \
         "$skills_dir/tvl-tech-bias-validator-dashboard"

  cp "$SCRIPT_DIR/agents/tvl-tech-bias-validator.md"         "$agents_dir/"
  cp "$SCRIPT_DIR/agents/tvl-tech-bias-validator-learner.md" "$agents_dir/"
  cp "$SCRIPT_DIR/agents/judge-council.md"                   "$agents_dir/"
  cp -r "$SCRIPT_DIR/skills/tvl-tech-bias-validator"           "$skills_dir/"
  cp -r "$SCRIPT_DIR/skills/tvl-tech-bias-validator-dashboard" "$skills_dir/"

  echo "Installed user-wide: ~/.claude/agents/ + ~/.claude/skills/tvl-tech-bias-validator*"
  echo "Available in every Claude Code session on this machine."
}

install_project() {
  local project_root="$1"
  local plugin_dir="$project_root/.claude/plugins/tvl-tech-bias-validator"
  local action

  if [ -d "$plugin_dir" ]; then
    rm -rf "$plugin_dir"/.claude-plugin "$plugin_dir"/skills "$plugin_dir"/agents "$plugin_dir"/cases "$plugin_dir"/references
    action="Updated"
  else
    mkdir -p "$plugin_dir"
    action="Installed"
  fi

  cp -r "$SCRIPT_DIR/.claude-plugin" "$plugin_dir/"
  cp -r "$SCRIPT_DIR/skills"         "$plugin_dir/"
  cp -r "$SCRIPT_DIR/agents"         "$plugin_dir/"
  cp -r "$SCRIPT_DIR/cases"          "$plugin_dir/"
  cp -r "$SCRIPT_DIR/references"     "$plugin_dir/"
  echo "$action project plugin: $plugin_dir"
}

ensure_case_db() {
  local global_dir="$HOME/.claude/tvl-tech-bias-validator"
  mkdir -p "$global_dir/cases"

  if [ ! -f "$global_dir/calibration.md" ]; then
    cat > "$global_dir/calibration.md" << 'CALIBRATION_EOF'
# TVL Tech Bias Validator Calibration

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
    echo "Created calibration: $global_dir/calibration.md"
  fi
}

case "$MODE" in
  "")
    install_user_wide
    ;;
  ".")
    install_project "$(pwd)"
    ;;
  *)
    if [ -d "$MODE" ]; then
      install_project "$(cd "$MODE" && pwd)"
    else
      echo "Error: target project directory does not exist: $MODE"
      echo ""
      echo "Usage:"
      echo "  bash install.sh                    # user-wide (all projects, to ~/.claude/)"
      echo "  bash install.sh .                  # current project"
      echo "  bash install.sh /path/to/project   # specific project"
      exit 1
    fi
    ;;
esac

ensure_case_db

echo ""
echo "Case DB: $HOME/.claude/tvl-tech-bias-validator/cases/"
echo "Start a fresh Claude Code session. Invoke via /tvl-tech-bias-validator."
