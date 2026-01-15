#!/usr/bin/env bash
set -euo pipefail

ts(){ date +"%Y-%m-%d %H:%M:%S"; }
step(){ echo; echo "==> [$(ts)] $1"; }

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SPECS="${AIGOV_SPECS_ROOT:-$REPO_ROOT/packages/specs}"
EP="${AIGOV_MVP_ROOT:-$REPO_ROOT/packages/ep}"
PE="${AIGOV_EVAL_ROOT:-$REPO_ROOT/packages/pe}"

LOG="EVALSET-MIGRATION-SMOKE-v1_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$REPO_ROOT/$LOG") 2>&1

fail(){ echo; echo "❌ EVALSET-MIGRATION-SMOKE-v1 FAILED"; echo "$1"; echo "Log saved to: $REPO_ROOT/$LOG"; exit 1; }
pass(){ echo; echo "✅ EVALSET-MIGRATION-SMOKE-v1 PASSED"; echo "Log saved to: $REPO_ROOT/$LOG"; }

assert_dir(){ [[ -d "$1" ]] || fail "Missing directory: $1"; }

assert_clean_diff_path(){
  local label="$1" path="$2"
  local diff
  diff="$(git diff --name-only -- "$path" || true)"
  [[ -n "$diff" ]] && { echo "$diff"; fail "$label: Drift detected under $path"; }
  echo "$label: OK (no drift under $path)."
}

assert_dir "$SPECS"; assert_dir "$EP"; assert_dir "$PE"

step "EP: sync from Specs + drift gate"
cd "$EP"
python3 tools/sync_taxonomy_from_specs.py --specs-root "$SPECS" || fail "EP: sync failed"
cd "$REPO_ROOT"
assert_clean_diff_path "EP" "packages/ep"

step "PE: sync from Specs + drift gate"
cd "$PE"
python3 tools/sync_contracts_from_specs.py --specs-root "$SPECS" || fail "PE: sync failed"
cd "$REPO_ROOT"
assert_clean_diff_path "PE" "packages/pe"

step "PE: run judge smoke"
cd "$PE"
export AIGOV_RUN_EP_SMOKE="1"
PE_VENV_PY="$PE/.venv/bin/python"
PYTHON_BIN="python3"
if [[ -x "$PE_VENV_PY" ]]; then
  PYTHON_BIN="$PE_VENV_PY"
fi
"$PYTHON_BIN" -m pytest tests/minimal_loop/test_ep_cli_judge_smoke.py -q || fail "PE: pytest failed"

pass
