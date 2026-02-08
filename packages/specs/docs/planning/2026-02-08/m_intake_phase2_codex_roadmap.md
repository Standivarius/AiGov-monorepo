# M_Intake Phase 2 Codex Roadmap (2026-02-08)

## Milestone Objectives
- Build deterministic, fail-closed workflow-stage artifacts around the existing `intake_bundle_v0_1` spine.
- Add stage contracts/schemas, stdlib validator coverage, fixtures, and planning-pack gate wiring.
- Unblock reserved Phase 2 stage fixtures:
  - `tools/fixtures/validators/intake_bundle_reconcile_conflict.json`
  - `tools/fixtures/validators/intake_bundle_gap_questions_order.json`
  - `tools/fixtures/validators/intake_bundle_readiness_blocked_unknown.json`

## Non-Goals
- No OPA execution runtime.
- No PAR adapter implementation beyond stubs/docs.
- No LLM council / multi-agent extraction.
- No new repo structure; reuse existing paths/patterns.

## Guardrails
- Stdlib-only Python validators.
- Fail-closed behavior for unknown vocab, missing required keys, unresolved references, and ordering violations.
- Deterministic ordering checks for stage lists (`conflicts`, `clarification_questions`, readiness blockers).
- Keep PR slices reviewable: **<= 6 files changed per PR**.
- Extend existing intake bundle artifacts; do not duplicate spine contracts/validators.
- Every PR updates this roadmap with status and proof results.

## Research Summary
- Found and reviewed:
  - `packages/specs/schemas/intake_bundle_v0_1.schema.json`
  - `tools/validate_intake_bundle_v0_1.py`
  - `tools/validate_planning_pack.py`
  - `packages/specs/docs/planning/2026-02-06/m_intake_evals_plan_2026-02-06.md`
  - `packages/specs/docs/planning/2026-02-06/m_intake_architecture_plan_2026-02-06.md`
- Existing patterns:
  - Schemas are strict with `additionalProperties: false` and explicit `required`.
  - Validators are stdlib-only and return deterministic sorted error lists.
  - Planning-pack wiring uses explicit pass/expected-fail fixture checks with substring assertions.
- Reserved Phase 2 stage fixtures are listed in plan docs and currently missing on disk.

## PR Roadmap (3-5 PRs)

### PR1 — Stage Contracts and Schemas
- **Effort:** M
- **Status:** Done
- **Title:** Define deterministic stage artifact contracts around `intake_bundle_v0_1`.
- **Exact file list:**
  - `packages/specs/docs/contracts/intake/intake_bundle_v0_1.md`
  - `packages/specs/docs/contracts/intake/intake_bundle_stage_artifacts_v0_1.md`
  - `packages/specs/schemas/intake_bundle_reconcile_v0_1.schema.json`
  - `packages/specs/schemas/intake_bundle_gap_v0_1.schema.json`
  - `packages/specs/schemas/intake_bundle_readiness_v0_1.schema.json`
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_codex_roadmap.md`
- **Fixtures:** none (schema/contract slice)
- **Expected substrings:**
  - `PASS: scenario schema strictness validated.`
- **Acceptance criteria:**
  - New stage schemas are strict (`additionalProperties: false` everywhere).
  - Stage contract doc defines deterministic ordering + fail-closed semantics.
  - Existing intake bundle contract links to stage artifact contract.
- **Proof commands:**
  - `python3 tools/validate_schema_strictness.py --schema-list tools/fixtures/validators/scenario_schema_list.json`

### PR2 — Validator Stage Modes + Reserved Stage Fixtures
- **Effort:** M
- **Status:** Done
- **Title:** Extend intake bundle validator for reconcile/gap/readiness and add reserved fixtures.
- **Exact file list:**
  - `tools/validate_intake_bundle_v0_1.py`
  - `tools/fixtures/validators/intake_bundle_reconcile_conflict.json`
  - `tools/fixtures/validators/intake_bundle_gap_questions_order.json`
  - `tools/fixtures/validators/intake_bundle_readiness_blocked_unknown.json`
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_codex_roadmap.md`
- **Fixtures:**
  - `intake_bundle_reconcile_conflict.json`
  - `intake_bundle_gap_questions_order.json`
  - `intake_bundle_readiness_blocked_unknown.json`
- **Expected substrings:**
  - `PASS: intake bundle reconcile fixture validated.`
  - `PASS: intake bundle gap fixture validated.`
  - `PASS: intake bundle readiness fixture validated.`
- **Acceptance criteria:**
  - Validator supports explicit stage modes with deterministic sorted errors.
  - Reconcile fixture enforces ordered `conflicts`.
  - Gap fixture enforces ordered `clarification_questions`.
  - Readiness fixture enforces blocked status when critical unknowns remain.
- **Proof commands:**
  - `python3 tools/validate_intake_bundle_v0_1.py --mode reconcile --fixture tools/fixtures/validators/intake_bundle_reconcile_conflict.json`
  - `python3 tools/validate_intake_bundle_v0_1.py --mode gap --fixture tools/fixtures/validators/intake_bundle_gap_questions_order.json`
  - `python3 tools/validate_intake_bundle_v0_1.py --mode readiness --fixture tools/fixtures/validators/intake_bundle_readiness_blocked_unknown.json`

### PR3 — Planning-Pack Gate Wiring for Stage Artifacts
- **Effort:** S
- **Status:** Done
- **Title:** Wire stage artifact checks into planning-pack and strictness list.
- **Exact file list:**
  - `tools/validate_planning_pack.py`
  - `tools/fixtures/validators/scenario_schema_list.json`
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_codex_roadmap.md`
- **Fixtures:**
  - All three reserved stage fixtures from PR2.
- **Expected substrings:**
  - `PASS: intake bundle reconcile fixture validated:`
  - `PASS: intake bundle gap fixture validated:`
  - `PASS: intake bundle readiness fixture validated:`
  - `PASS: planning pack validated.`
- **Acceptance criteria:**
  - Planning pack fails closed if any stage fixture fails validation.
  - Stage schemas are included in strictness list validation.
- **Proof commands:**
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`

### PR4 — Milestone Closeout Docs
- **Effort:** S
- **Status:** Done
- **Title:** Publish milestone report and external review prompts.
- **Exact file list:**
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_milestone_report.md`
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_review_prompt_claude.md`
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_review_prompt_gemini.md`
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_codex_roadmap.md`
- **Fixtures:** n/a
- **Expected substrings:**
  - `MUST checks`
  - `SHOULD checks`
  - `evidence referential integrity`
- **Acceptance criteria:**
  - Report summarizes changes, proofs, residual risks, and non-goals.
  - Claude/Gemini prompts include required invariants, exact commands, and likely bug locations.
- **Proof commands:**
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`

## Completion Tracking

### PR1 Tracking
- **Status:** Done
- **Branch:** `phase2-candidate-v0_1`
- **PR #:** TBD
- **Proof checklist:**
  - [x] `python3 tools/validate_schema_strictness.py --schema-list tools/fixtures/validators/scenario_schema_list.json`
- **Proof results:** strictness pass on existing schema list; strictness pass also verified for new stage schemas via `/tmp/m_intake_phase2_stage_schema_list.json`.

### PR2 Tracking
- **Status:** Done
- **Branch:** `phase2-candidate-v0_1`
- **PR #:** TBD
- **Proof checklist:**
  - [x] `python3 tools/validate_intake_bundle_v0_1.py --mode reconcile --fixture tools/fixtures/validators/intake_bundle_reconcile_conflict.json`
  - [x] `python3 tools/validate_intake_bundle_v0_1.py --mode gap --fixture tools/fixtures/validators/intake_bundle_gap_questions_order.json`
  - [x] `python3 tools/validate_intake_bundle_v0_1.py --mode readiness --fixture tools/fixtures/validators/intake_bundle_readiness_blocked_unknown.json`
- **Proof results:** all three reserved stage fixtures validated successfully via explicit stage modes.

### PR3 Tracking
- **Status:** Done
- **Branch:** `phase2-candidate-v0_1`
- **PR #:** TBD
- **Proof checklist:**
  - [x] `python3 tools/validate_planning_pack.py`
  - [x] `bash tools/run_pr_gate_validators.sh`
- **Proof results:** planning-pack and PR-gate validators passed with stage artifact checks wired.

### PR4 Tracking
- **Status:** Done
- **Branch:** `phase2-candidate-v0_1`
- **PR #:** TBD
- **Proof checklist:**
  - [x] `python3 tools/validate_planning_pack.py`
  - [x] `bash tools/run_pr_gate_validators.sh`
  - [x] `NX_DAEMON=false npx nx run evalsets:migration-smoke`
- **Proof results:** all three final proof commands passed; migration-smoke log: `docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260208_071955.log`.
