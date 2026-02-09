# Intake Source Snapshot v0.1

GDPR-only scope.

## Purpose
Define the deterministic ingestion boundary artifact for export/file sources consumed by Extract-stage processing.

## Canonical Schema
- `packages/specs/schemas/intake_source_snapshot_v0_1.schema.json`

## Required Shape
- Root required keys:
  - `schema_version` (must be `"intake_source_snapshot_v0_1"`)
  - `snapshot_id`
  - `source_type` (currently `"file_export"`)
  - `source_files[]`
- Each `source_files[]` entry requires:
  - `source_path`
  - `sha256`

## Deterministic Rules
- `source_files[]` MUST be sorted by `source_path` (ascending lexical order).
- `source_path` values MUST be unique.

## Fail-Closed Rules
- Unknown keys are rejected (`additionalProperties: false`).
- Missing required keys reject the artifact.
- Absolute source paths reject the artifact.
- Traversal paths (`..`) reject the artifact.

## Schema vs Policy Boundary
- Schema enforces shape and field formats.
- Validator policy enforces path safety and ordering constraints.

## Non-Goals
- No PAR runtime adapter implementation.
- No OPA execution runtime.
- No LLM extraction logic.
