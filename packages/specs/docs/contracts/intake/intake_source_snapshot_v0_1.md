# Intake Source Snapshot v0.1

GDPR-only scope.

## Purpose
Define the deterministic ingestion boundary artifact for export/file sources consumed by Extract-stage processing.

## Adapter Linkage
- Produced by `tools/run_intake_export_file_adapter_v0_1.py` from a local export directory.
- Canonical adapter contract:
  - `packages/specs/docs/contracts/intake/intake_export_file_adapter_v0_1.md`
- `snapshot_id` is the canonical provenance handle and is consumed by:
  - `intake_bundle_extract_v0_1.source_snapshot_id`

## Canonical Schema
- `packages/specs/schemas/intake_source_snapshot_v0_1.schema.json`

## Required Shape
- Root required keys:
  - `schema_version` (must be `"intake_source_snapshot_v0_1"`)
  - `snapshot_id`
  - `source_type` (`"file_export"` or `"github_export_pack"`)
  - `source_files[]`
- Each `source_files[]` entry requires:
  - `source_path`
  - `sha256`

## Deterministic Rules
- `source_files[]` MUST be sorted by `source_path` (ascending lexical order).
- `source_path` values MUST be unique.
- Adapter output serialization is canonical JSON bytes (sorted keys, compact separators, trailing newline).
- `snapshot_id` MUST be deterministic from canonical source inventory:
  - only `source_path` and `sha256` contribute to snapshot digest
  - `content_type` does not affect snapshot digest

## Fail-Closed Rules
- Unknown keys are rejected (`additionalProperties: false`).
- Missing required keys reject the artifact.
- Absolute source paths reject the artifact.
- Traversal paths (`..`) reject the artifact.
- For `github_export_pack` sources, adapter rejects unsupported top-level paths and non-JSON recognized files before snapshot emission.

## Schema vs Policy Boundary
- Schema enforces shape and field formats.
- Validator policy enforces path safety and ordering constraints.

## Non-Goals
- No PAR runtime adapter implementation.
- No OPA execution runtime.
- No LLM extraction logic.
