# Intake Export File Adapter v0.1

GDPR-only scope.

## Purpose
Define a deterministic, fail-closed adapter contract for converting local export inputs into intake stage artifacts:
- `intake_source_snapshot_v0_1`
- `intake_bundle_extract_v0_1`

This contract is tools-only for `v0.1` and does not integrate EP runtime.

## Input Contract
- Input is a local directory path in one of two deterministic source profiles:
  - `file_export`
  - `github_export_pack`
- Directory traversal is recursive and deterministic:
  - sort directory names lexically
  - sort file names lexically
  - normalize recorded relative paths to POSIX style

### GitHub Export Pack v0.1 Layout
`github_export_pack` mode is enabled when the export root contains all and only:
- `repo/`
- `issues/`
- `pull_requests/`
- `comments/`

Rules:
- `repo/` allows only `metadata.json`
- `issues/`, `pull_requests/`, `comments/` require at least one `*.json` each
- nested paths (deeper than one segment under these folders) are rejected in `v0.1`

## Fail-Closed Safety Rules
- Adapter MUST fail if input path does not exist or is not a directory.
- Adapter MUST fail on any symlink encountered in the export tree.
- Adapter MUST fail if any resolved file path escapes the export root.
- Adapter MUST fail on unreadable files or unsupported payload structure.
- For `github_export_pack`, adapter MUST fail on:
  - unsupported top-level paths
  - non-`.json` files in recognized pack folders
  - malformed JSON
  - recognized pack files that are not JSON objects
- No silent skip is allowed for recognized `github_export_pack` paths.

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
- For `github_export_pack`, first-run deterministic heuristics are limited to:
  - `intake.context_profile.jurisdiction`
  - `intake.context_profile.sector`
  - `intake.policy_profile.retention_days`
- If conflicting values are derived for the same field across multiple source files, adapter MUST fail closed.

## Deterministic Serialization
Adapter outputs use canonical JSON serialization:
- `json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)`
- trailing newline appended

## Non-Goals
- No OPA execution.
- No PAR runtime adapter.
- No LLM extraction.
- No live connector/API ingestion.
