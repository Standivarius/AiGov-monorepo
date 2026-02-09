# Intake Bundle Stage Artifacts v0.1

GDPR-only scope.

## Purpose
Define deterministic, fail-closed workflow-stage artifacts around the canonical `intake_bundle_v0_1` spine.

## Artifacts
- `intake_bundle_extract_v0_1`
- `intake_bundle_reconcile_v0_1`
- `intake_bundle_gap_v0_1`
- `intake_bundle_readiness_v0_1`

Canonical schemas:
- `packages/specs/schemas/intake_bundle_extract_v0_1.schema.json`
- `packages/specs/schemas/intake_bundle_reconcile_v0_1.schema.json`
- `packages/specs/schemas/intake_bundle_gap_v0_1.schema.json`
- `packages/specs/schemas/intake_bundle_readiness_v0_1.schema.json`

## Deterministic Rules
- Extract:
  - `extracted_fields[]` MUST be sorted by `field_path`.
  - `field_path` values MUST be unique.
  - Each `evidence_refs[]` list MUST be sorted and contain unique IDs.
- Reconcile:
  - `conflicts[]` MUST be sorted by `(field_path, conflict_id)`.
  - Each `evidence_refs[]` list MUST be sorted and contain unique IDs.
- Gap:
  - `clarification_questions[]` MUST be sorted by `question_id`.
- Readiness:
  - `blocking_unknowns[]` MUST be sorted by `(field_path, question_id)`.
  - `unresolved_conflict_ids[]` MUST be sorted and unique.

## Evidence Boundary (Enforced vs Deferred)
- Stage artifact validators enforce stage-local shape, ordering, and known vocabulary.
- If `evidence_refs[]` is present on a stage item, it MUST be sorted and contain unique IDs.
- Cross-artifact referential integrity (stage `evidence_refs` membership in canonical `intake_bundle_v0_1.evidence_index`) is deferred to composition-level checks.

## Empty-State Semantics
- Stage schemas require non-empty item arrays when the artifact is emitted (`minItems: 1`).
- Empty states are represented by artifact absence (or equivalent upstream "no conflicts/no gaps/no blockers" signal), not by emitting empty artifacts in `v0_1`.

## Conflict Value Representation
- In `intake_bundle_reconcile_v0_1`, `left_value` and `right_value` are strings by design.
- Values MUST use canonical JSON serialization string form of the compared value (scalar/array/object) to keep comparison payloads deterministic.
- A future schema version may allow non-string JSON value types; `v0_1` keeps string-only representation for strictness and deterministic transport.

## Fixture Naming Exception
- Reserved fixtures `intake_bundle_reconcile_conflict.json`, `intake_bundle_gap_questions_order.json`, and `intake_bundle_readiness_blocked_unknown.json` are PASS fixtures by plan reservation.
- They intentionally do not use the usual `_pass.json` suffix convention.
- Canonical fixture naming remains `_pass/_fail` (for example `intake_bundle_v0_1_pass.json` and `intake_bundle_v0_1_fail_missing_required.json`).

## Fail-Closed Rules
- Extract:
  - At least one extracted field is required.
  - Missing required field keys fail validation.
  - Unsorted field paths fail validation.
- Reconcile:
  - At least one conflict is required.
  - Any unknown severity or missing evidence refs fails validation.
- Gap:
  - At least one clarification question is required.
  - Priority must be integer and explicit.
- Readiness:
- If `blocking_unknowns` is non-empty (any severity), `status` MUST be `blocked`.
  - If any `blocking_unknowns` with `severity == "critical"` exist, `status` MUST be `blocked` and `allow_downstream` MUST be `false`.
  - If `unresolved_conflict_ids` is non-empty, `status` MUST be `blocked` and `allow_downstream` MUST be `false`.
  - If `status == "ready"`, both `blocking_unknowns` and `unresolved_conflict_ids` MUST be empty and `allow_downstream` MUST be `true`.

## Non-Goals
- No OPA runtime execution semantics.
- No PAR adapter implementation.
- No LLM-driven extraction/reconciliation logic.
