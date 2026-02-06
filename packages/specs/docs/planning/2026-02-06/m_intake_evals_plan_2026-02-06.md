# M_Intake Evals-First Plan (v2026-02-06)

## Objective
Define fixtures and tests that gate M_Intake safely before any implementation (eval-first), including readiness gate and legacy intake output boundary regressions.

## Inputs (code-grounded)
- Constitution: `packages/specs/docs/planning/2026-02-06/m_intake_constitution_2026-02-06.md`.
- Runbook: `packages/specs/docs/planning/2026-02-06/m_intake_codex_runbook_2026-02-06.md`.
- Codebase map: `packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md`.
- Task pack: `packages/specs/docs/planning/2026-02-06/m_intake_task_pack_2026-02-06.md`.
- Intake + taxonomy anchors:
  - `packages/specs/schemas/client_intake_v0_2.schema.json`
  - `packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md`
  - `packages/specs/docs/contracts/taxonomy/evidence_schema.md`
  - `tools/fixtures/validators/intake_output_context_fail_locale_context_null.json`

## Fit matrix status
- **Missing**: `packages/specs/docs/planning/2026-02-06/m_intake_monorepo_fit_matrix_2026-02-06.md` was not present in the repo at the provided path. Touchpoint paths below are grounded in the codebase map and must be verified against the fit matrix once available.

---

## 1) Fixtures to add (names + locations)

### 1.1 intake_bundle_v0_1 pass fixture
- `tools/fixtures/validators/intake_bundle_v0_1_pass.json`
  - Minimal valid bundle with evidence_index + evidence_refs.

### 1.2 intake_bundle_v0_1 fail fixtures
- `tools/fixtures/validators/intake_bundle_v0_1_fail_unknown_vocab.json`
- `tools/fixtures/validators/intake_bundle_v0_1_fail_nondeterministic_field.json`
- `tools/fixtures/validators/intake_bundle_v0_1_fail_missing_required.json`
- `tools/fixtures/validators/intake_bundle_v0_1_fail_missing_evidence_ref.json`

### 1.3 Reconciliation conflict fixture
- `tools/fixtures/validators/intake_bundle_reconcile_conflict.json`
  - Two drafts disagree on a critical field; `conflicts[]` present and ordered.

### 1.4 Gap-analysis output fixture
- `tools/fixtures/validators/intake_bundle_gap_questions_order.json`
  - `clarification_questions[]` ordered deterministically.

### 1.5 Readiness gate fixture
- `tools/fixtures/validators/intake_bundle_readiness_blocked_unknown.json`
  - Critical unknown blocks readiness (fail-closed).

---

## 2) Regression fixtures for intake OUTPUT boundary (explicit)
These protect existing intake output behavior and must fail-closed:
- `tools/fixtures/validators/intake_output_context_fail_locale_context_null.json` (already exists).
- `tools/fixtures/validators/intake_output_context_fail_unknown_jurisdiction.json` (exists per codebase map).
- `tools/fixtures/validators/intake_output_context_fail_unknown_sector.json` (exists per codebase map).
- `tools/fixtures/validators/intake_output_context_fail_pack_order.json` (exists per codebase map).
- **Add new:** `tools/fixtures/validators/intake_output_context_fail_missing_locale_and_context.json` (both locale_context and context_profile missing).

---

## 3) Test files to extend (paths only; no edits)
- **New tests for intake bundle validation:**
  - `packages/pe/tests/intake/test_intake_bundle_validation.py`
- **Extend existing intake validation tests:**
  - `packages/pe/tests/intake/test_intake_validation.py` (add regression cases for locale_context null and policy_pack_stack ordering).
- **Readiness gate tests (if split):**
  - `packages/pe/tests/intake/test_intake_readiness_gate.py`

---

## 4) Pass rules + evidence artifacts (eval-first)
- **Pass rules:**
  - `intake_bundle_v0_1_pass.json` validates schema + evidence refs resolve.
  - Any `intake_bundle_v0_1_fail_*.json` fails with deterministic error messages.
  - Readiness gate fixture blocks when critical unknowns remain.
- **Evidence artifacts:**
  - Each test outputs a deterministic validation report (error list) suitable for PE gate evidence.

---

## 5) Determinism expectations in tests
- Sort order of `clarification_questions[]`, `conflicts[]`, and `evidence_index` must be deterministic.
- Any nondeterministic fields (timestamps, random IDs) must cause failures.
- No network dependencies in tests.

---

## Summary
- Defined exact fixtures for intake_bundle_v0_1 validation, reconciliation conflicts, gap analysis, and readiness gating.
- Listed explicit regression fixtures for the legacy intake output boundary, including a new missing-locale/context failure case.
- Identified test files to add/extend under `packages/pe/tests/` without implementation changes.

## Work performed
- Reviewed constitution/runbook and intake/taxonomy anchors for fail-closed requirements.
- Anchored fixture plan to existing validator fixture paths.

## Findings
- Evals-first coverage can be implemented entirely via fixtures + PE tests before any runtime code changes.

## Checkpoint
- Files changed:
  - `packages/specs/docs/planning/2026-02-06/m_intake_evals_plan_2026-02-06.md`
- Commands run:
  - `ls packages/specs/docs/planning/2026-02-06`
  - `find packages/specs/docs -name "m_intake_oss_eval_cnil_patterns_2026-02-06.md" -print`
  - `find packages/specs/docs -name "*fit_matrix*" -print`
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_constitution_2026-02-06.md`
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_codex_runbook_2026-02-06.md`
  - `sed -n '1,220p' packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md`
  - `sed -n '1,220p' packages/specs/docs/planning/2026-02-06/m_intake_task_pack_2026-02-06.md`
  - `sed -n '1,200p' packages/specs/schemas/client_intake_v0_2.schema.json`
  - `sed -n '1,200p' packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md`
  - `sed -n '1,200p' packages/specs/docs/contracts/taxonomy/evidence_schema.md`
  - `cat tools/fixtures/validators/intake_output_context_fail_locale_context_null.json`
- Results:
  - Docs-only; no proofs executed.
- Risks/unknowns:
  - CNIL patterns doc missing (UNCONFIRMED PATH).
  - Fit matrix file missing at specified path; touchpoints derived from codebase map pending confirmation.
- Next task:
  - Add missing CNIL patterns doc and align evals to its question taxonomy.
  - Draft intake_bundle_v0_1 schema + contract before implementing fixtures.
