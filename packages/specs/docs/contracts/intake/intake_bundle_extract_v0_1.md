# Intake Bundle Extract v0.1

GDPR-only scope.

## Purpose
Define the deterministic Extract-stage artifact produced from export/file ingestion before reconcile/gap/readiness stages.

## Adapter Linkage
- Produced by `tools/run_intake_export_file_adapter_v0_1.py` in tools-only mode.
- Canonical adapter contract:
  - `packages/specs/docs/contracts/intake/intake_export_file_adapter_v0_1.md`
- `source_snapshot_id` MUST reference the exact `snapshot_id` emitted in the paired
  `intake_source_snapshot_v0_1` output from the same adapter run.

## Canonical Schema
- `packages/specs/schemas/intake_bundle_extract_v0_1.schema.json`

## Required Shape
- Root required keys:
  - `schema_version` (must be `"intake_bundle_extract_v0_1"`)
  - `bundle_id`
  - `source_snapshot_id`
  - `extracted_fields`
- Each `extracted_fields[]` item requires:
  - `field_path`
  - `value`
  - `evidence_refs[]`

## Deterministic Rules
- `extracted_fields[]` MUST be sorted by `field_path` in ascending lexical order.
- Each `evidence_refs[]` list MUST be sorted and unique.
- `field_path` values SHOULD be unique per artifact; duplicate field paths are rejected by validator policy.
- Adapter output serialization is canonical JSON bytes (sorted keys, compact separators, trailing newline).

## Fail-Closed Rules
- Unknown keys are rejected (`additionalProperties: false`).
- Missing required keys reject the artifact.
- Empty `extracted_fields` rejects the artifact.
- Invalid `evidence_refs` IDs reject the artifact.

## Schema vs Policy Boundary
- Schema enforces shape, required keys, and strictness.
- Validator policy enforces ordering and deterministic duplicate checks.

## Non-Goals
- No OPA runtime execution.
- No PAR adapter runtime implementation.
- No LLM extraction/council logic.
