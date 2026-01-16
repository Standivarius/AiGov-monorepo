Phase: Hardening the monorepo proof so it runs the same everywhere.

## PR-E: STATUS guard + status-pr-update skill
- STATUS guard added: PRs touching core areas must update STATUS.md.
- Codex skill added: status-pr-update produces a paste-ready STATUS snippet + conflict check.
- Dashboard: (link)


## PR-C: AGENTS + Claude handoff
- Added AGENTS.md and the Claude handoff protocol to the codex-rules skill.

## PR-B: Devcontainer + reproducible migration smoke
- Added devcontainer config for Node + Python to make Codespaces/local devcontainer setup predictable.
- Migration smoke now writes logs under `docs/logs/` and ensures a PE venv exists with required deps (no global pip).
- WSL proof: `npm install`; `npx nx run evalsets:migration-smoke` (1 skipped). Log: docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260116_004744.log.
- Next: PR-D (CI wiring + Windows parity).

## PR-0: Monorepo skeleton + migration smoke runner
- Added minimal Nx workspace files and evalsets migration-smoke target to run `node tools/run-migration-smoke.cjs`.
- Added WSL-first smoke runners with drift gates scoped to packages/ep and packages/pe plus venv-aware pytest.
- Imported specs, ep, pe as git subtrees under packages/ to preserve history and keep specs canonical.
- If pytest deps are missing: `python3 -m venv packages/pe/.venv` then `packages/pe/.venv/bin/python -m pip install -r packages/pe/requirements.txt -r packages/pe/requirements-dev.txt` and `packages/pe/.venv/bin/python -m pip install -e packages/ep`; if jsonschema import fails, also install `jsonschema` in the venv.
- WSL proof: `npm install`; `npx nx run evalsets:migration-smoke` (1 skipped). Log: EVALSET-MIGRATION-SMOKE-v1_20260115_185556.log.
- Next: PR-B (Codespaces/devcontainer parity).

## PR-A: Codex operating scaffolding
- Added repo-scoped Codex skills under `.codex/skills` (new-chat, end-chat, codex-rules).
- Established STATUS discipline: record what changed, why, and what's next.
- Ignored local smoke logs and workspace artifacts (EVALSET-MIGRATION-SMOKE-v1_*.log, node_modules/, .nx/, packages/**/.venv).
- Next: PR-0/PR-B to land monorepo structure + cross-platform smoke runners.
