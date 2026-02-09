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

## Scenario Determinism Rules
- `scenarios` MUST be sorted by `scenario_instance_id` (ascending lexical order).
- `scenario_id`, `scenario_instance_id`, and `path` MUST each be unique across `scenarios[]`.

## Validator Scope Boundary
- `tools/validate_ep_deterministic_bundle_manifest.py` validates deterministic manifests only.
- Legacy-only bundles (`bundle_manifest.json` without `manifest.json`) are out of scope for this validator.
- Legacy-only fallback behavior is handled in EP CLI (`packages/ep/aigov_ep/cli.py`).

## Schema vs Policy Boundary
- Schema enforces shape/required keys/field formats/strictness (`additionalProperties: false`).
- Schema-level checks also include exact duplicate scenario-object rejection (`uniqueItems: true`).
- Runtime policy validators enforce filesystem and integrity checks:
  - scenario ordering and uniqueness policy checks
  - path traversal rejection
  - symlink rejection
  - file existence under bundle root
  - `sha256` content verification against on-disk files

## Non-Goals
- No OPA/PAR/LLM runtime semantics.
- No non-GDPR execution expansion.
