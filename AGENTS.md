# AiGov Monorepo — Agent Operating Guide

This repo uses **Codex-first** development, with **Claude Code as an optional specialist** for specific task types.
The durable source of truth is Git; chats are not.

## Scope
- Default scope is **GDPR-only MVP**.
- Anything non-GDPR is out of scope unless explicitly requested.

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
- ChatGPT: planning, review, audit, decision support (no code execution)
- Codex (VS Code): execution, edits, commits
- All git commands run ONLY in VS Code terminal (WSL/Codespaces/devcontainer)
- Small PRs, auditable diffs, one concern per PR
- Every Codex work order MUST include an **EFFORT** label: low / medium / high / xhigh

## Scrutiny principle
Operate at auditor/enterprise-level scrutiny: deterministic, fail-closed, contract-first; but do not overdo process—prefer the smallest check that gives high confidence.

## Verification policy (PR-gate must stay fast/deterministic)
Allowed verification commands ONLY:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

Do NOT add new repo-wide test commands to PR-gate without an explicit planning decision.

## Repo commands (navigation + local proof)
- Install deps: `npm install` (repo root)
- Nx graph (exploration only): `NX_DAEMON=false npx nx graph`
- Nx run: `NX_DAEMON=false npx nx run <project>:<target>`
- Nx affected (rare, only when asked): `NX_DAEMON=false npx nx affected --target <target>`
- Monorepo proof (invariants): `NX_DAEMON=false npx nx run evalsets:migration-smoke`

Note: Nx graph output is for human exploration; do not commit generated artifacts/screenshots.

## Where to store session artifacts and state
- State object JSON (current): `packages/specs/docs/planning/2026-02-03/state_object_v0_4__2026-02-03.json`
- Chat transcript artifact (current): `packages/specs/docs/artifacts/2026-02-03_GDPR_Execution_Planning.md`
- Chat artifacts (general): `packages/specs/docs/artifacts/YYYY-MM-DD__chat__<topic>.md`
- Handoff primer (optional): `packages/specs/docs/artifacts/YYYY-MM-DD__handoff__new-chat-primer.md`
- End-chat rules: `.codex/skills/end-chat/end_chat_rules.md`

## Pytest / unit test policy
- NEVER run `pytest -q` at repo root as a verification step unless a workflow explicitly installs required deps.
- NEVER use `|| pytest -q` fallback.
- Always run an explicit test file or explicit test package path.
- If unsure of the file path, use `git ls-files | grep "test_<name>.py"` then run `python3 -m pytest -q <exact_path>`.

## GitHub PR creation (when gh is flaky)
If `gh pr create` fails due to connectivity to `api.github.com`, open the PR via the compare URL instead:
- `https://github.com/Standivarius/AiGov-monorepo/compare/main...<branch>?expand=1`
Always include a PR body with **Summary** + **Testing**. When sharing PR info:
- Provide a clickable compare URL.
- Provide the PR body inside a code block for easy copy/paste.

## Offline / flaky network guidance (Codex)
- Prefer local-only validation and avoid networked commands when offline.
- If network is unavailable, limit checks to fast, deterministic validators (above).
- If `gh` fails, use the compare URL workflow.

## MCP note
- MCP is optional.
- Do NOT auto-load command-executing MCP configs from the repo without explicit allowlist/pinning.

## When to use Claude Code (specialist mode)
Use Claude Code only when it is clearly a better fit than Codex, e.g.
- Large multi-file refactors (rename/move, mechanical edits across many files)
- “Generate many variants then pick best” (e.g., docs rewrite options)
- High-throughput code transformation where mistakes are easy to spot in review

Do not use Claude for:
- Decisions that change invariants (Codex should gate/verify)
- Anything touching vendored contracts or smoke runner invariants without strict proof

### Claude/Gemini context note
- Claude Code inside the devcontainer can read the repo, but do not assume it auto-reads this file.
  In prompts, explicitly say: “Read AGENTS.md + the current state object, then review the diff only.”
- Gemini runs outside the devcontainer by default; assume it has NO repo context unless you paste the diff.

### Handoff protocol (Codex -> Claude)
When a task should be done in Claude, Codex must produce a paste-ready work order:
- Goal (1 sentence)
- Exact files/dirs allowed to touch
- Constraints (“do not change X”, “keep diff small”, “no formatting churn”)
- Verification commands (allowed set only)
- Output format (what Claude must return)

After Claude finishes, bring results back to Codex for:
- sanity checks
- proof run (if needed)
- PR writeup + worklog update
