# Intake Export File Adapter v0.1

GDPR-only scope.

## Purpose
Define a deterministic, fail-closed adapter contract for converting local `file_export` inputs into intake stage artifacts:
- `intake_source_snapshot_v0_1`
- `intake_bundle_extract_v0_1`

This contract is tools-only for `v0.1` and does not integrate EP runtime.

## Input Contract
- Input is a local directory path (`file_export`).
- Directory traversal is recursive and deterministic:
  - sort directory names lexically
  - sort file names lexically
  - normalize recorded relative paths to POSIX style

## Fail-Closed Safety Rules
- Adapter MUST fail if input path does not exist or is not a directory.
- Adapter MUST fail on any symlink encountered in the export tree.
- Adapter MUST fail if any resolved file path escapes the export root.
- Adapter MUST fail on unreadable files or unsupported payload structure.

## Snapshot Output Rules (`intake_source_snapshot_v0_1`)
- Output MUST conform to `packages/specs/schemas/intake_source_snapshot_v0_1.schema.json`.
- `source_files[]` MUST be sorted by `source_path`.
- Each item includes deterministic provenance:
  - `source_path` (relative POSIX path)
  - `sha256` (lowercase 64-char hex)
- `snapshot_id` is deterministic from canonical source inventory.

## Extract Output Rules (`intake_bundle_extract_v0_1`)
- Output MUST conform to `packages/specs/schemas/intake_bundle_extract_v0_1.schema.json`.
- `source_snapshot_id` MUST equal generated snapshot `snapshot_id`.
- `extracted_fields[]` MUST be sorted by `field_path`.
- Each `evidence_refs[]` MUST be sorted and unique.
- First-run extraction logic is deterministic, heuristics-based, and local-file only.

## Deterministic Serialization
Adapter outputs use canonical JSON serialization:
- `json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)`
- trailing newline appended

## Non-Goals
- No OPA execution.
- No PAR runtime adapter.
- No LLM extraction.
- No live connector/API ingestion.
