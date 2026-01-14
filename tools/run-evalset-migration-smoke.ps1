<# 
run-evalset-migration-smoke.ps1

Single-command runner for EVALSET-MIGRATION-SMOKE-v1 (multi-repo workspace or monorepo).

Usage:
  cd "C:\Users\User\OneDrive - DMR Ergonomics\aigov-workspace\aigov-nx"
  powershell -ExecutionPolicy Bypass -File .\tools\run-evalset-migration-smoke.ps1

Optional overrides:
  $env:AIGOV_SPECS_ROOT = "..."
  $env:AIGOV_MVP_ROOT   = "..."
  $env:AIGOV_EVAL_ROOT  = "..."
#>

$ErrorActionPreference = "Stop"

# --- Roots (defaults match EVALSETS.yaml) ---
$RepoRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
$MonorepoSpecs = Join-Path $RepoRoot "packages\specs"
$MonorepoMvp   = Join-Path $RepoRoot "packages\ep"
$MonorepoEval  = Join-Path $RepoRoot "packages\pe"
$HasMonorepoLayout = (Test-Path -LiteralPath $MonorepoSpecs) -and (Test-Path -LiteralPath $MonorepoMvp) -and (Test-Path -LiteralPath $MonorepoEval)

$SPECS = if ($env:AIGOV_SPECS_ROOT) { $env:AIGOV_SPECS_ROOT } elseif ($HasMonorepoLayout) { $MonorepoSpecs } else { "C:\Users\User\OneDrive - DMR Ergonomics\aigov-workspace\AiGov-specs" }
$MVP   = if ($env:AIGOV_MVP_ROOT)   { $env:AIGOV_MVP_ROOT }   elseif ($HasMonorepoLayout) { $MonorepoMvp }   else { "C:\Users\User\OneDrive - DMR Ergonomics\aigov-workspace\AiGov-mvp" }
$EVAL  = if ($env:AIGOV_EVAL_ROOT)  { $env:AIGOV_EVAL_ROOT }  elseif ($HasMonorepoLayout) { $MonorepoEval }  else { "C:\Users\User\OneDrive - DMR Ergonomics\aigov-workspace\Aigov-eval" }

function Assert-Dir($Path, $Name) {
  if (-not (Test-Path -LiteralPath $Path)) { throw "Missing $Name directory: $Path" }
}

function Invoke-Step($Name, [scriptblock]$Block) {
  $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
  Write-Host ""
  Write-Host "==> [$ts] $Name" -ForegroundColor Cyan
  & $Block
  if ($LASTEXITCODE -ne 0) { throw "$Name failed with exit code $LASTEXITCODE" }
}

function Assert-Clean-GitDiff($RepoLabel) {
  $diff = git diff --name-only
  if ($LASTEXITCODE -ne 0) { throw "${RepoLabel}: git diff failed with exit code $LASTEXITCODE" }

  if ($diff) {
    Write-Host $diff
    throw "${RepoLabel}: Drift detected after sync (git diff not empty)."
  }

  Write-Host "${RepoLabel}: OK (no drift after sync)."
}

# --- Preflight ---
Assert-Dir $SPECS "AiGov-specs"
Assert-Dir $MVP   "AiGov-mvp"
Assert-Dir $EVAL  "Aigov-eval"

# Transcript
$log = "EVALSET-MIGRATION-SMOKE-v1_{0}.log" -f (Get-Date -Format "yyyyMMdd_HHmmss")
Start-Transcript -Path $log | Out-Null

try {
  Invoke-Step "Specs: checkout main + pull" {
    Set-Location -LiteralPath $SPECS
    git checkout main
    git pull
  }

  Invoke-Step "MVP: checkout main + pull + sync from Specs + drift gate" {
    Set-Location -LiteralPath $MVP
    git checkout main
    git pull

    python tools/sync_taxonomy_from_specs.py --specs-root "$SPECS"
    if ($LASTEXITCODE -ne 0) { throw "MVP: sync_taxonomy_from_specs.py failed with exit code $LASTEXITCODE" }

    Assert-Clean-GitDiff "MVP"
  }

  Invoke-Step "Eval: checkout main + pull + sync from Specs + drift gate" {
    Set-Location -LiteralPath $EVAL
    git checkout main
    git pull

    python tools/sync_contracts_from_specs.py --specs-root "$SPECS"
    if ($LASTEXITCODE -ne 0) { throw "Eval: sync_contracts_from_specs.py failed with exit code $LASTEXITCODE" }

    Assert-Clean-GitDiff "Eval"
  }

  Invoke-Step "Eval: PATH sanity (where.exe aigov-ep)" {
    Set-Location -LiteralPath $EVAL
    where.exe aigov-ep
    Write-Host "NOTE: Ensure aigov-ep points to your expected install (often editable install from AiGov-mvp)."
  }

  Invoke-Step "Eval: run EP judge smoke (pytest minimal_loop)" {
    Set-Location -LiteralPath $EVAL
    $env:AIGOV_RUN_EP_SMOKE = "1"
    python -m pytest tests/minimal_loop/test_ep_cli_judge_smoke.py -q
  }

  Write-Host ""
  Write-Host "✅ EVALSET-MIGRATION-SMOKE-v1 PASSED" -ForegroundColor Green
  Write-Host "Log saved to: $log"
}
catch {
  Write-Host ""
  Write-Host "❌ EVALSET-MIGRATION-SMOKE-v1 FAILED" -ForegroundColor Red
  Write-Host $_.Exception.Message -ForegroundColor Red
  Write-Host "Log saved to: $log"
  exit 1
}
finally {
  Stop-Transcript | Out-Null
}
