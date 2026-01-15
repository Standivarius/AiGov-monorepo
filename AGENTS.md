# AiGov Monorepo — Codex Operating Contract

Codex must treat Git as the durable memory. Chat is not a source of truth.

## Source of truth
- /STATUS.md is canonical for: current phase, what is green, next steps.
- Canonical proof spec:
  - /packages/specs/docs/program/EVALSETS.yaml

## Definition of Done for any PR
- Update /STATUS.md (what changed + why + what’s next).
- If repo plumbing / migration invariants are touched: run
  - npx nx run evalsets:migration-smoke
- Prefer small PRs; no drive-by refactors.

## Guardrails
- Never hand-edit vendored contracts; use sync scripts + drift gate.
- Keep verification repeatable (“one command proves it”).
