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
  - `packages/specs/docs/contracts/taxonomy/evidence_schema.md` (verdict/signal schema only; NOT Evidence Model B)
  - `tools/fixtures/validators/intake_output_context_fail_locale_context_null.json`

## Fit matrix status
- **Present**: `packages/specs/docs/planning/2026-02-06/m_intake_monorepo_fit_matrix_2026-02-06.md` (used to verify touchpoint paths below).

---

## 1) Fixtures to add (names + locations)
**Phase D minimal executable fixture set (Phase 1):** one `*_pass.json` plus single-mode `*_fail_<reason>.json` fixtures listed below.
**Evidence Model B contract (Phase D):** create `packages/specs/docs/contracts/intake/evidence_model_b_v0_1.md` (new contract; not provided by `evidence_schema.md`).

### 1.1 intake_bundle_v0_1 pass fixture
- `tools/fixtures/validators/intake_bundle_v0_1_pass.json`
  - Minimal valid bundle with evidence_index + evidence_refs.
  - **Naming convention:** single `*_pass.json` file per contract version.

### 1.2 intake_bundle_v0_1 fail fixtures
- `tools/fixtures/validators/intake_bundle_v0_1_fail_unknown_vocab.json`
- `tools/fixtures/validators/intake_bundle_v0_1_fail_timestamp_field.json`
- `tools/fixtures/validators/intake_bundle_v0_1_fail_missing_required.json`
- `tools/fixtures/validators/intake_bundle_v0_1_fail_dangling_evidence_ref.json`
- `tools/fixtures/validators/intake_bundle_v0_1_fail_empty_evidence_refs.json`
- `tools/fixtures/validators/intake_bundle_v0_1_fail_sha256_uppercase.json`
- `tools/fixtures/validators/intake_bundle_v0_1_fail_extra_key.json`
- `tools/fixtures/validators/intake_bundle_v0_1_fail_unknown_policy_pack.json`
  - **Naming convention:** `*_fail_<reason>.json` for single-mode failures.

### 1.3 Reconciliation conflict fixture
- `tools/fixtures/validators/intake_bundle_reconcile_conflict.json`
  - Two drafts disagree on a critical field; `conflicts[]` present and ordered.
  - **Phase 2 (blocked)** until a readiness/reconcile validator exists.

### 1.4 Gap-analysis output fixture
- `tools/fixtures/validators/intake_bundle_gap_questions_order.json`
  - `clarification_questions[]` ordered deterministically.
  - **Phase 2 (blocked)** until a gap-analysis validator exists.

### 1.5 Readiness gate fixture
- `tools/fixtures/validators/intake_bundle_readiness_blocked_unknown.json`
  - Critical unknown blocks readiness (fail-closed).
  - **Phase 2 (blocked)** until readiness gate validator exists.

---

## 2) Regression fixtures for intake OUTPUT boundary (explicit)
These protect existing intake output behavior and must fail-closed:
- `tools/fixtures/validators/intake_output_context_fail_locale_context_null.json` (already exists).
- `tools/fixtures/validators/intake_output_context_fail_unknown_jurisdiction.json` (exists per codebase map).
- `tools/fixtures/validators/intake_output_context_fail_unknown_sector.json` (exists per codebase map).
- `tools/fixtures/validators/intake_output_context_fail_pack_order.json` (exists per codebase map).
- **Add new:** `tools/fixtures/validators/intake_output_context_fail_missing_locale_and_context.json` (both locale_context and context_profile missing).
  - **Does not exist yet:** requires Phase D validator patch to make it fail as intended.
- **Live fail-open note:** current validator fails open when both `context_profile` and the `locale_context` key are absent; this requires an explicit validator patch (not covered by existing regression fixtures).

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
- **Enforcement mechanism:** nondeterministic field checks require validator logic (schema alone cannot reliably detect timestamps/random IDs); use a rule that rejects forbidden field names (e.g., `*_timestamp`).

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
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
- Results:
  - `python3 tools/validate_planning_pack.py`:
    - ```
      PASS: evidence_pack_v0 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/evidence_pack_v0_pass.json
      FAIL (as expected): evidence_pack_v0 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/evidence_pack_v0_fail.json
      FAIL (as expected): base scenario fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/base_scenario_empty_signals.json
      PASS: client override validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_override_pass.json
      FAIL (as expected): client override validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_override_fail.json
      FAIL (as expected): client override validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_override_fail_nondeterministic_field.json
      FAIL (as expected): client override validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_override_fail_unknown_vocab.json
      FAIL (as expected): client override validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_override_empty_supported.json
      PASS: client intake v0.2 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_intake_v0_2_pass.json
      FAIL (as expected): client intake v0.2 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_intake_v0_2_fail.json
      FAIL (as expected): client intake v0.2 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_intake_v0_2_fail_channel_mismatch.json
      FAIL (as expected): client intake v0.2 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_intake_v0_2_fail_empty_supported.json
      PASS: intake output context fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_pass_nl_public.json
      PASS: intake output context fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_pass_nl_healthcare.json
      PASS: intake output context fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_pass_legacy_locale_only_nl.json
      FAIL (as expected): intake output context fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_fail_pack_order.json
      FAIL (as expected): intake output context fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_fail_locale_context_null.json
      FAIL (as expected): intake output context fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_fail_unknown_jurisdiction.json
      FAIL (as expected): intake output context fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_fail_unknown_sector.json
      PASS: client intake bundle determinism validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_pass_nl_public.json
      PASS: inspect_task_args v0.1 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/inspect_task_args_v0_1_pass.json
      FAIL (as expected): inspect_task_args v0.1 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/inspect_task_args_v0_1_fail.json
      PASS: LiveRun output artifacts validated: /workspaces/AiGov-monorepo/tools/fixtures/liverun_artifacts_v0_1/pass
      FAIL (as expected): LiveRun output artifacts validated: /workspaces/AiGov-monorepo/tools/fixtures/liverun_artifacts_v0_1/fail
      PASS: bundle integrity validated: /workspaces/AiGov-monorepo/tools/fixtures/bundles/good
      PASS: deterministic bundle manifest validated: /workspaces/AiGov-monorepo/tools/fixtures/bundles/good
      FAIL (as expected): bundle integrity validated: /workspaces/AiGov-monorepo/tools/fixtures/bundles/poison
      PASS: bundle scenario validated: /workspaces/AiGov-monorepo/tools/fixtures/bundles/good/scenarios/GDPR-001__client-001.json
      PASS: bundle scenario validated: /workspaces/AiGov-monorepo/tools/fixtures/bundles/good/scenarios/GDPR-002.json
      FAIL (as expected): bundle scenario validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/gdpr_bundle_scenario_fail_missing_expected.json
      PASS: dataset JSONL validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/dataset_jsonl_v0_1_pass.jsonl
      FAIL (as expected): dataset JSONL validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/dataset_jsonl_v0_1_fail_nondeterministic_field.jsonl
      FAIL (as expected): dataset JSONL validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/dataset_jsonl_v0_1_fail_sha_case.jsonl
      FAIL (as expected): dataset JSONL validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/dataset_jsonl_v0_1_fail_empty_id.jsonl
      PASS: interface ledger validated.
      PASS: seed_instructions export validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/petri_seed_instructions_from_bundle_pass.json
      PASS: runpack command validated: /workspaces/AiGov-monorepo/tools/fixtures/runpack/expected_inspect_command_pass.txt
      PASS: module cards validated: /workspaces/AiGov-monorepo/packages/specs/docs/contracts/modules/cards
      PASS: module dashboard snapshot validated.
      PASS: scenario determinism validated.
      PASS: scenario schema strictness validated.
      PASS: planning pack validated.
      ```
  - `bash tools/run_pr_gate_validators.sh`:
    - ```
      PASS: canonical verdicts only.
      PASS: doc-mode operational evidence requirements satisfied.
      PASS: equivalence labeling requirements satisfied.
      PASS: no golden-set contamination in citations.
      PASS: evidence_id resolution validated.
      PASS: evidence IDs are canonical and registry-backed.
      ```
- Risks/unknowns:
  - Live fail-open when both `context_profile` and `locale_context` key are absent (validator patch required).
- Next task:
  - Draft intake_bundle_v0_1 schema + contract before implementing fixtures.
