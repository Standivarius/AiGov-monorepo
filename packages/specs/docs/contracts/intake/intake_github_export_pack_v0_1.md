# Intake GitHub Export Pack v0.1

GDPR-only scope.

## Purpose
Define a deterministic, file-based GitHub export pack layout that can be consumed by the tools-only intake export adapter to produce:
- `intake_source_snapshot_v0_1`
- `intake_bundle_extract_v0_1`

## Required Layout (v0.1)
Top-level directories must be exactly:
- `repo/`
- `issues/`
- `pull_requests/`
- `comments/`

Required file:
- `repo/metadata.json`

Allowed files in recognized directories:
- `.json` files only

## Fail-Closed Rules
- Any top-level entry outside `repo/`, `issues/`, `pull_requests/`, `comments/` is rejected.
- Any non-`.json` file in recognized pack directories is rejected.
- Malformed JSON in recognized pack files is rejected.
- Wrong top-level JSON shape in recognized pack files is rejected.
- No silent skipping is allowed for recognized GitHub pack paths.

## Determinism Rules
- Directory traversal must be lexical and stable.
- Relative paths must be normalized to POSIX style.
- Snapshot output uses canonical serialization (sorted keys, stable separators, trailing newline).
- Extract output ordering remains deterministic (`field_path`, `evidence_refs`).

## Non-Goals
- No live GitHub connector/authentication.
- No EP runtime integration in this milestone.
- No OPA/PAR/LLM runtime behavior.
