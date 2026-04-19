#!/usr/bin/env bash
set -euo pipefail

# Remote bootstrap installer for EthicalHive / tvl-tech-bias-validator.
#
# Usage (one-liner):
#   curl -sL .../install-remote.sh | bash                    # user-wide
#   curl -sL .../install-remote.sh | bash -s .               # current project
#   curl -sL .../install-remote.sh | bash -s /path/to/proj   # specific project
#
# Clones to a temp dir, runs the installer, cleans up.

MODE="${1:-}"

TMPDIR=$(mktemp -d)
trap "rm -rf '$TMPDIR'" EXIT

echo "Cloning ethicalhive to $TMPDIR ..."
git clone --depth 1 --quiet https://github.com/danlex/ethicalhive.git "$TMPDIR/ethicalhive"

echo "Running installer ..."
bash "$TMPDIR/ethicalhive/install.sh" $MODE
