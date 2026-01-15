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
