# Claude Architecture Review Prompt — M_Intake Phase 2

Review only M_Intake Phase 2 changes for deterministic, fail-closed stage boundaries around `intake_bundle_v0_1`.

## MUST Checks
- Stage schemas are strict (`additionalProperties: false`) and have explicit required keys.
- Validator remains stdlib-only and returns deterministic sorted errors.
- Reconcile stage enforces deterministic `conflicts` ordering.
- Gap stage enforces deterministic `clarification_questions` ordering.
- Readiness stage blocks when critical unknowns or unresolved conflicts remain.
- Planning-pack wiring executes all three reserved stage fixtures.
- Evidence referential integrity assumptions in stage artifacts are not weakened.

## SHOULD Checks
- Error messages are specific enough to identify exact failing field/path.
- Stage fixture examples are single-purpose and deterministic.
- New contract doc aligns with schema and validator semantics.
- No non-goal behavior (OPA/PAR/LLM runtime) was introduced.

## Specific Invariants to Inspect
- Determinism:
  - `conflicts` sorted by `(field_path, conflict_id)`.
  - `clarification_questions` sorted by `question_id`.
  - `blocking_unknowns` sorted by `(field_path, question_id)`.
- Fail-closed:
  - critical unknowns => blocked readiness + `allow_downstream=false`.
  - unresolved conflicts => blocked readiness + `allow_downstream=false`.
- Evidence referential integrity:
  - ensure stage work did not bypass existing `intake_bundle_v0_1` evidence ref guarantees.

## Exact Commands
- `python3 tools/validate_intake_bundle_v0_1.py --mode reconcile --fixture tools/fixtures/validators/intake_bundle_reconcile_conflict.json`
- `python3 tools/validate_intake_bundle_v0_1.py --mode gap --fixture tools/fixtures/validators/intake_bundle_gap_questions_order.json`
- `python3 tools/validate_intake_bundle_v0_1.py --mode readiness --fixture tools/fixtures/validators/intake_bundle_readiness_blocked_unknown.json`
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

## Likely Bug Locations
- `tools/validate_intake_bundle_v0_1.py`
  - `_validate_schema` type handling (`string/array/object/integer/boolean`)
  - stage policy validators (`_validate_reconcile_policy`, `_validate_gap_policy`, `_validate_readiness_policy`)
  - CLI `--mode` dispatch
- `tools/validate_planning_pack.py`
  - new stage fixture constants/imports
  - stage fixture execution order and fail handling
- `tools/fixtures/validators/intake_bundle_*stage*.json`
  - ordering and blocker semantics encoded in fixture data
