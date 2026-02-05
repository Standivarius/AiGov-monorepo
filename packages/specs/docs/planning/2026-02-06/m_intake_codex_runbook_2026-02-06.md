# M_Intake Codex Runbook (v2026-02-06)

## Goal
Enable large, agentic Codex runs safely: explore broadly, harvest selectively, never break invariants.

## Operating modes
1) Docs-only tasks
- May create/modify markdown only.
- No code changes.

2) Mapping/analysis tasks
- No code changes unless explicitly requested.
- Must cite file paths for every claim about the codebase.

3) Architecture/design tasks
- No implementation.
- May add design docs under packages/specs/docs/planning/...

4) Evals-first tasks
- Add fixtures/tests first (PR gates), then stop.
- No implementation of business logic in the same task unless explicitly instructed.

## Checkpoint protocol (required at end of every task)
Every task must end with a "Checkpoint" section containing:
- Files changed (paths)
- Commands run (exact)
- Results (pass/fail + pointers to logs)
- Open risks / unknowns
- Next recommended task (1–3 bullets)

## Command restrictions
- Only run repo-allowed proof commands unless the task explicitly authorizes additional commands.
- Always prefer read-only analysis before running anything.

Allowed proof commands:
- python3 tools/validate_planning_pack.py
- bash tools/run_pr_gate_validators.sh
- NX_DAEMON=false npx nx run evalsets:migration-smoke

## Branch / PR rules
- Cloud tasks may create a branch but MUST NOT merge.
- Prefer small, reviewable diffs even if the exploration is “big” (big ideas, bounded changes).

## License and sourcing rules (enforced)
- Do not paste or port GPL/EUPL code into packages/ep or packages/pe.
- If referencing OSS, record: name, license, what capability it provides, and the proposed adapter boundary.
- Any OSS integration must be behind an adapter and validated with fixtures.

## Determinism rules (enforced)
- No network dependence in runtime paths unless explicitly approved.
- No nondeterministic fields in artifacts unless explicitly listed and then rejected by default in validators.

## “Stop and ask” conditions
Stop and ask for instruction if:
- A change would weaken schema strictness or fail-closed behavior.
- A change would alter existing Intake OUTPUT behavior (context_profile stack rules).
- A license boundary is unclear.
- A task requires enabling broader internet access or new secrets.

## Task reporting format template
### Summary
(1–4 bullets)

### Work performed
- ...

### Findings
- ...

### Checkpoint
- Files changed:
- Commands run:
- Results:
- Risks/unknowns:
- Next task:
