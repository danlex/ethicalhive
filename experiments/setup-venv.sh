#!/usr/bin/env bash
set -euo pipefail

# Create or refresh the experiments Python venv and install dependencies.
#
# Reusable setup primitive required by `contracts/paper-writing-contract.md`
# PAP-WORK-06: environment setup, venv creation, and dependency installation
# MUST be a named, committed script. Inline `python3 -m venv ... && pip install`
# chains in Bash tool calls are Breaches.
#
# Idempotent: safe to re-run. Creates .venv at the repo root if missing,
# upgrades pip, installs everything in experiments/requirements.txt.
#
# Usage:
#   bash experiments/setup-venv.sh           # create + install
#   bash experiments/setup-venv.sh --check   # just verify the venv resolves the deps
#
# Activate in subsequent shell sessions with:
#   source .venv/bin/activate

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$REPO_ROOT/.venv"
REQ_FILE="$REPO_ROOT/experiments/requirements.txt"

MODE="install"
if [ "${1:-}" = "--check" ]; then
  MODE="check"
fi

if [ ! -f "$REQ_FILE" ]; then
  echo "Error: $REQ_FILE not found." >&2
  exit 1
fi

if [ "$MODE" = "check" ]; then
  if [ ! -d "$VENV_DIR" ]; then
    echo "venv missing at $VENV_DIR. Run: bash experiments/setup-venv.sh"
    exit 1
  fi
  "$VENV_DIR/bin/python" -c "
import sys, importlib
ok = True
for line in open('$REQ_FILE'):
    pkg = line.strip().split('=')[0].split('>')[0].split('<')[0]
    if not pkg or pkg.startswith('#'):
        continue
    try:
        importlib.import_module(pkg)
        print(f'ok    {pkg}')
    except ImportError as e:
        print(f'MISS  {pkg}: {e}')
        ok = False
sys.exit(0 if ok else 1)
"
  exit $?
fi

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating venv at $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --quiet --upgrade pip
"$VENV_DIR/bin/python" -m pip install --quiet --requirement "$REQ_FILE"

echo "venv ready: $VENV_DIR"
echo "activate with: source .venv/bin/activate"
"$VENV_DIR/bin/python" - <<'PY'
import sys
print(f"python: {sys.version.split()[0]} at {sys.executable}")
PY
