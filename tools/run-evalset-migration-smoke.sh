#!/usr/bin/env bash
set -euo pipefail

ts(){ date +"%Y-%m-%d %H:%M:%S"; }
step(){ echo; echo "==> [$(ts)] $1"; }

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SPECS="${AIGOV_SPECS_ROOT:-$REPO_ROOT/packages/specs}"
EP="${AIGOV_MVP_ROOT:-$REPO_ROOT/packages/ep}"
PE="${AIGOV_EVAL_ROOT:-$REPO_ROOT/packages/pe}"

LOG="EVALSET-MIGRATION-SMOKE-v1_$(date +%Y%m%d_%H%M%S).log"
LOG_DIR="$REPO_ROOT/docs/logs"
mkdir -p "$LOG_DIR"
LOG_PATH="$LOG_DIR/$LOG"
exec > >(tee -a "$LOG_PATH") 2>&1

fail(){ echo; echo "❌ EVALSET-MIGRATION-SMOKE-v1 FAILED"; echo "$1"; echo "Log saved to: $LOG_PATH"; exit 1; }
pass(){ echo; echo "✅ EVALSET-MIGRATION-SMOKE-v1 PASSED"; echo "Log saved to: $LOG_PATH"; }

assert_dir(){ [[ -d "$1" ]] || fail "Missing directory: $1"; }

ensure_pe_venv(){
  local venv_dir="$PE/.venv"
  local venv_py="$venv_dir/bin/python"
  if [[ ! -x "$venv_py" ]]; then
    echo "PE: creating venv at $venv_dir"
    python3 -m venv "$venv_dir" || fail "PE: failed to create venv. Run: python3 -m venv $venv_dir"
  fi
  PE_VENV_PY="$venv_py"
}

ensure_pe_deps(){
  if "$PE_VENV_PY" - <<'PY'
import importlib.util
missing = [name for name in ("pytest", "jsonschema", "aigov_ep") if importlib.util.find_spec(name) is None]
raise SystemExit(1 if missing else 0)
PY
  then
    return 0
  fi
  echo "PE: installing venv dependencies"
  "$PE_VENV_PY" -m pip install -r "$PE/requirements.txt" -r "$PE/requirements-dev.txt" || fail "PE: pip install requirements failed"
  "$PE_VENV_PY" -m pip install -e "$EP" || fail "PE: pip install -e packages/ep failed"
  "$PE_VENV_PY" -m pip install jsonschema || fail "PE: pip install jsonschema failed"
}

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
ensure_pe_venv
ensure_pe_deps
"$PE_VENV_PY" -m pytest tests/minimal_loop/test_ep_cli_judge_smoke.py -q || fail "PE: pytest failed"

pass
