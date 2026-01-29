# AiGov Monorepo — Agent Operating Guide

This repo uses **Codex-first** development, with **Claude Code as an optional specialist** for specific task types.
The durable source of truth is Git; chats are not.

## Canonical references
- **/.codex/skills/** = repo-scoped skills:
  - `$new-chat` (session startup)
  - `$end-chat` (session wrap + worklog)
  - `$codex-rules` (execution discipline)

## Default workflow (Codex)
1) Start every session: run `$new-chat`
2) Do the smallest PR that moves the phase forward.
3) If plumbing/invariants changed: run the canonical proof.
4) End session: run `$end-chat`

## Execution Contract
- ChatGPT: planning, review, audit, decision support
- Codex (VS Code): execution, edits, commits
- All git commands run ONLY in VS Code terminal (WSL/Codespaces)
- Networked commands (e.g., `gh`, `curl`, package installs) may require escalated permissions in the Codex sandbox.
- Small PRs, auditable diffs, one concern per PR

## Scrutiny principle
Operate at auditor/enterprise level scrutiny: deterministic, fail-closed, contract-first; but do not overdo process—prefer the smallest check that gives high confidence.

## Repo commands (canonical)
- **Install deps**: `npm install` (repo root)
- **Nx graph**: `npx nx graph`
- **Nx run**: `npx nx run <project>:<target>`
- **Nx affected (if needed)**: `npx nx affected --target <target>`
- **PR-gate / evalsets**: definitions live in `packages/specs/docs/planning/2026-01-22-run/evalsets_registry.yaml` and planning guidance in `packages/specs/docs/planning/2026-01-22-run/codex_execution_pack.md`.
- **Monorepo proof (invariants)**: `npx nx run evalsets:migration-smoke` (see `packages/specs/docs/program/EVALSETS.yaml`)

## Where to store session artifacts and state
- Chat artifacts (session logs): `packages/specs/docs/artifacts/YYYY-MM-DD__chat__<topic>.md` (example: `packages/specs/docs/artifacts/2026-01-26__chat__execution-planning-standivarius.md`)
- Handoff primer artifact (optional but recommended): `packages/specs/docs/artifacts/YYYY-MM-DD__handoff__new-chat-primer.md` (example: `packages/specs/docs/artifacts/2026-01-26__handoff__new-chat-primer.md`)
- State object JSON: `packages/specs/docs/planning/2026-01-24-run/state_object_v0_3__2026-01-26.json` (prior canonical: `state_object_v0_2__2026-01-24.json`)
- Planning-pack “spine” pointers: `packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml`, `packages/specs/docs/planning/2026-01-22-run/evalsets_registry.yaml`, `packages/specs/docs/planning/2026-01-22-run/codex_execution_pack.md`
- End-chat rules: `.codex/skills/end-chat/end_chat_rules.md`

## Pytest / unit test policy
- NEVER run `pytest -q` at repo root as a verification step unless a workflow explicitly installs required deps.
- NEVER use `|| pytest -q` fallback.
- Always run an explicit test file or explicit test package path (e.g., `python3 -m pytest -q packages/pe/tests/scenario/test_bundle_compiler.py`).
- If unsure of the file path, use `git ls-files | grep -n "test_<name>.py"` then run `python3 -m pytest -q <exact_path>`.

## Offline (Codex)
- Prefer local-only validation and avoid networked commands when offline.
- If network is unavailable, use cached deps and limit checks to fast, deterministic validators.

## MCP note
- MCP is optional.
- Do NOT auto-load command-executing MCP configs from the repo without explicit allowlist/pinning.

## When to use Claude Code (specialist mode)
Use Claude Code **only** when it is clearly a better fit than Codex, e.g.
- Large multi-file refactors (rename/move, mechanical edits across many files)
- “Generate many variants then pick best” (e.g., docs rewrite options)
- High-throughput code transformation where mistakes are easy to spot in review

Do **not** use Claude for:
- Decisions that change invariants (Codex should gate/verify)
- Anything touching vendored contracts or smoke runner invariants without strict proof

### Handoff protocol (Codex -> Claude)
When a task should be done in Claude, Codex must produce a **paste-ready work order**:
- Goal (1 sentence)
- Exact files/dirs allowed to touch
- Constraints (“do not change X”, “keep diff small”, “no formatting churn”)
- Verification commands
- Output format (what Claude must return)

After Claude finishes, bring results back to Codex for:
- sanity checks
- proof run (if needed)
- PR writeup + worklog update
