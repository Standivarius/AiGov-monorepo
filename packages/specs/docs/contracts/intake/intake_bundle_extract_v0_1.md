# Intake Bundle Extract v0.1

GDPR-only scope.

## Purpose
Define the deterministic Extract-stage artifact produced from export/file ingestion before reconcile/gap/readiness stages.

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
