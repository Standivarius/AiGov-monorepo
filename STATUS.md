# STATUS — AiGov Program (Monorepo)

## Current phase
- Codex-first transition: repo operating artifacts (AGENTS + skills + worklog)
- Monorepo bring-up: Nx wrapper + subtree imports (packages/specs|ep|pe)

## Canonical proof
- npx nx run evalsets:migration-smoke
- Logs: EVALSET-MIGRATION-SMOKE-v1_*.log (repo root)

## Active invariants
- Specs is canonical for contracts/schemas/evals.
- EP/PE vendor from Specs via sync scripts with drift gates.
- Migration smoke must stay green before/after structural changes.

## Next actions
- PR-A: add AGENTS + skills + STATUS + worklog (this change)
- PR-B: devcontainer + Codespaces parity
