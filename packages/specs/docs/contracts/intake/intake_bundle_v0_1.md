# Intake Bundle v0.1

GDPR-only scope.

## Purpose
Define the canonical, deterministic intake artifact consumed by readiness and downstream scenario generation gates.

## Top-Level Contract
`intake_bundle_v0_1` requires these top-level keys:
- `schema_version` (`"intake_bundle_v0_1"`)
- `bundle_id` (non-empty string)
- `intake` (normalized intake payload)
- `evidence_index` (Evidence Model B index)
- `evidence_refs` (Evidence Model B references)

Canonical schema:
- `packages/specs/schemas/intake_bundle_v0_1.schema.json`

Evidence model contract:
- `packages/specs/docs/contracts/intake/evidence_model_b_v0_1.md`

Workflow-stage artifact contract:
- `packages/specs/docs/contracts/intake/intake_bundle_stage_artifacts_v0_1.md`

Upstream deterministic ingestion/extract contracts:
- `packages/specs/docs/contracts/intake/intake_source_snapshot_v0_1.md`
- `packages/specs/docs/contracts/intake/intake_bundle_extract_v0_1.md`

## Relationship to Legacy Intake Output
Legacy intake output contracts remain supported for intake collection flows.
`intake_bundle_v0_1` is the canonical artifact for deterministic readiness/gating.

## Taxonomy Requirements
Allowlists are contract-first and external to schema:
- `packages/specs/docs/contracts/taxonomy/jurisdictions_v0.json`
- `packages/specs/docs/contracts/taxonomy/sectors_v0.json`
- `packages/specs/docs/contracts/taxonomy/policy_packs_v0.json`

Validator policy enforces:
- `intake.context_profile.jurisdiction` is allowlisted.
- `intake.context_profile.sector` is allowlisted.
- `intake.context_profile.policy_pack_stack` equals `[
  "GDPR_EU", jurisdiction, sector, "client"
]` and each element is allowlisted.

## Determinism and Hashing
Canonicalization and hashing rules are pinned to:
- `packages/specs/docs/contracts/reporting/hash_canonicalization_v0_1.md`

## Fail-Closed Expectations
- Any schema mismatch fails validation.
- Any unknown taxonomy value fails validation.
- Any dangling evidence reference fails validation.
- Empty `evidence_index` or empty `evidence_refs` fails validation.
- Any unsafe `source_path` (absolute or traversal) fails validation.
- Forbidden root-level nondeterministic fields (`generated_at`, `processed_at`) fail validation.

## Schema Vs Policy
- Schema-enforced:
  - Required keys and object shapes.
  - `additionalProperties: false` at root and nested objects.
  - `sha256` pattern and non-empty identifiers.
- Validator-enforced policy:
  - Taxonomy allowlists and policy stack equality rule.
  - Referential integrity (`evidence_refs` -> `evidence_index`).
  - Path traversal and absolute-path rejection.
  - Forbidden root-level nondeterministic field names.
