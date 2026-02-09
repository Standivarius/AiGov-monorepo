# Deterministic Bundle Manifest v0.1.0 Contract

GDPR-only scope.

## Purpose
Define the canonical shape for deterministic execution bundle `manifest.json` consumed by EP execution.

## Canonical Schema
- `packages/specs/schemas/deterministic_bundle_manifest_v0_1_0.schema.json`

## Required Shape
- Root:
  - `schema_version` MUST equal `"0.1.0"`.
  - `scenarios` MUST be a non-empty array.
- Each `scenarios[]` item MUST include:
  - `scenario_id`
  - `scenario_instance_id`
  - `path`
  - `sha256` (lowercase 64-char hex)

## Optional Root Fields
- `bundle_hash` is optional; if present it MUST be lowercase 64-char hex.
- `bundle_dir` is optional; if present it MUST be a non-empty string.

## Schema vs Policy Boundary
- Schema enforces shape/required keys/field formats/strictness (`additionalProperties: false`).
- Runtime policy validators enforce filesystem and integrity checks:
  - path traversal rejection
  - symlink rejection
  - file existence under bundle root
  - `sha256` content verification against on-disk files

## Non-Goals
- No OPA/PAR/LLM runtime semantics.
- No non-GDPR execution expansion.
