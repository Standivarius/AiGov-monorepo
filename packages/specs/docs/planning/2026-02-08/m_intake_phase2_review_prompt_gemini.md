# Gemini Adversarial Review Prompt — M_Intake Phase 2

Perform an adversarial review of M_Intake Phase 2 stage-boundary artifacts. Try to find deterministic/fail-closed bypasses.

## MUST Checks
- Validate that all stage schemas are strict and reject unexpected keys.
- Validate that stage ordering invariants are enforced in validator logic (not only in fixture shape).
- Validate readiness fail-closed logic:
  - critical unknowns cannot produce `ready`.
  - unresolved conflicts cannot produce `ready`.
  - blocked readiness cannot set `allow_downstream=true`.
- Validate planning-pack gate includes all reserved stage fixtures.
- Validate stage changes do not weaken evidence referential integrity guarantees from intake spine.

## SHOULD Checks
- Check that stage fixtures are deterministic and not accidentally order-insensitive.
- Check for dual-mode or ambiguous failures where a fixture can fail for multiple unrelated reasons.
- Check for hidden acceptance of null/empty values not intended by contract.
- Check output messages for deterministic, stable text useful for CI triage.

## Specific Invariants to Inspect
- Determinism:
  - sort order enforcement in reconcile/gap/readiness lists.
  - uniqueness checks where applicable.
- Fail-closed:
  - blocked status requirements tied to blockers.
  - no path where blockers exist and downstream stays allowed.
- Evidence referential integrity:
  - verify stage layer did not introduce bypass around existing bundle-level evidence checks.

## Exact Commands
- `python3 tools/validate_intake_bundle_v0_1.py --mode reconcile --fixture tools/fixtures/validators/intake_bundle_reconcile_conflict.json`
- `python3 tools/validate_intake_bundle_v0_1.py --mode gap --fixture tools/fixtures/validators/intake_bundle_gap_questions_order.json`
- `python3 tools/validate_intake_bundle_v0_1.py --mode readiness --fixture tools/fixtures/validators/intake_bundle_readiness_blocked_unknown.json`
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

## Likely Bug Locations
- `tools/validate_intake_bundle_v0_1.py`
  - schema walker coverage and stage policy guards
  - readiness branching (`must_block`, blockers, allow_downstream coupling)
- `packages/specs/schemas/intake_bundle_reconcile_v0_1.schema.json`
- `packages/specs/schemas/intake_bundle_gap_v0_1.schema.json`
- `packages/specs/schemas/intake_bundle_readiness_v0_1.schema.json`
- `tools/validate_planning_pack.py`
  - fixture registration and fail-closed behavior on stage validation errors
