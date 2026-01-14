# AiGov monorepo

This repository is the monorepo form of the AiGov program, preserving the original repo boundaries:

- packages/specs — canonical contracts, schemas, eval definitions (formerly AiGov-specs)
- packages/ep    — EP / Stage A execution (formerly AiGov-mvp)
- packages/pe    — PE / Stage B judge + evaluation harness (formerly Aigov-eval)

## Canonical proof (single command)

From the repo root:

    npx nx run evalsets:migration-smoke

What it proves (EVALSET-MIGRATION-SMOKE-v1):
- Specs are the canonical source of truth
- EP and PE vendor contracts/schemas from Specs via sync scripts
- Drift gate: sync must produce an empty git diff --name-only
- PE minimal_loop judge smoke passes (including behaviour_json schema validation)

Outputs:
- Creates a timestamped log file: EVALSET-MIGRATION-SMOKE-v1_YYYYMMDD_HHMMSS.log

## Notes
- The runner performs an igov-ep PATH sanity check. If it points to an unexpected install, fix your Python/editable install before trusting results.
- Git pulls may be skipped when no upstream is configured (common before the monorepo has a remote).
