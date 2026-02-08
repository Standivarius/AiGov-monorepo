# Intake Bundle Stage Artifacts v0.1

GDPR-only scope.

## Purpose
Define deterministic, fail-closed workflow-stage artifacts around the canonical `intake_bundle_v0_1` spine.

## Artifacts
- `intake_bundle_reconcile_v0_1`
- `intake_bundle_gap_v0_1`
- `intake_bundle_readiness_v0_1`

Canonical schemas:
- `packages/specs/schemas/intake_bundle_reconcile_v0_1.schema.json`
- `packages/specs/schemas/intake_bundle_gap_v0_1.schema.json`
- `packages/specs/schemas/intake_bundle_readiness_v0_1.schema.json`

## Validation Boundary
- Stage artifacts are validated as standalone JSON documents.
- `evidence_refs` in reconcile/gap must reference evidence IDs from the parent `intake_bundle_v0_1.evidence_index`.
- Referential integrity from stage `evidence_refs` to the parent bundle is out of scope for standalone stage validators and must be checked in composition workflows.

## Deterministic Rules
- Reconcile:
  - `conflicts[]` MUST be sorted by `(field_path, conflict_id)`.
  - Each `evidence_refs[]` list MUST be sorted and contain unique IDs.
  - `left_value` and `right_value` MUST be serialized as strings.
- Gap:
  - `clarification_questions[]` MUST be sorted by `question_id`.
  - `evidence_refs[]` is optional per question; unresolved questions may be raised before evidence is fully linked.
- Readiness:
  - `blocking_unknowns[]` MUST be sorted by `(field_path, question_id)`.
  - `unresolved_conflict_ids[]` MUST be sorted and unique.

## Fail-Closed Rules
- Reconcile:
  - At least one conflict is required.
  - Any unknown severity or missing evidence refs fails validation.
- Gap:
  - At least one clarification question is required.
  - Priority must be integer and explicit.
  - If `evidence_refs` is present, it must be non-empty and deterministically ordered.
- Readiness:
  - If any `blocking_unknowns` with `severity == "critical"` exist, `status` MUST be `blocked` and `allow_downstream` MUST be `false`.
  - If `unresolved_conflict_ids` is non-empty, `status` MUST be `blocked` and `allow_downstream` MUST be `false`.
  - If `status == "ready"`, both `blocking_unknowns` and `unresolved_conflict_ids` MUST be empty and `allow_downstream` MUST be `true`.

## Non-Goals
- No OPA runtime execution semantics.
- No PAR adapter implementation.
- No LLM-driven extraction/reconciliation logic.
