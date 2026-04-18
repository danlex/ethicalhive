#!/usr/bin/env bash
set -euo pipefail

# Remote bootstrap installer for EthicalHive / tvl-tech-bias-validator.
#
# Usage (one-liner):
#   curl -sL https://raw.githubusercontent.com/danlex/ethicalhive/main/install-remote.sh | bash -s /path/to/project
#
# Equivalent to: git clone, cd, bash install.sh /path/to/project.
# Clones to a temp dir, runs the installer, cleans up.

if [ -z "${1:-}" ]; then
  echo "Usage: curl -sL https://raw.githubusercontent.com/danlex/ethicalhive/main/install-remote.sh | bash -s /path/to/project"
  exit 1
fi

PROJECT_ROOT="$1"

if [ ! -d "$PROJECT_ROOT" ]; then
  echo "Error: target project directory does not exist: $PROJECT_ROOT"
  exit 1
fi

TMPDIR=$(mktemp -d)
trap "rm -rf '$TMPDIR'" EXIT

echo "Cloning ethicalhive to $TMPDIR ..."
git clone --depth 1 --quiet https://github.com/danlex/ethicalhive.git "$TMPDIR/ethicalhive"

echo "Running installer ..."
bash "$TMPDIR/ethicalhive/install.sh" "$PROJECT_ROOT"
