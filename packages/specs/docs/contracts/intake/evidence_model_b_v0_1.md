# Evidence Model B v0.1

GDPR-only scope.

## Purpose
Define deterministic, fail-closed evidence linkage for intake bundles.

## Contract Definition
Evidence Model B is a pair of structures inside `intake_bundle_v0_1`:

1. `evidence_index`: object mapping `evidence_id` to an evidence entry.
2. `evidence_refs`: object mapping canonical `field_path` to a non-empty array of `evidence_id` values.

Evidence entry shape (exact):

```json
{
  "source_path": "string",
  "sha256": "^[a-f0-9]{64}$"
}
```

## Referential Integrity
Every `evidence_id` listed in any `evidence_refs[field_path]` array MUST exist as a key in `evidence_index`.

## Path Semantics
`source_path` is interpreted relative to the bundle root.

Validator policy (fail-closed):
- Reject absolute paths.
- Reject traversal segments such as `..`.

## Determinism
- `sha256` must be lowercase hex (`^[a-f0-9]{64}$`).
- Hash canonicalization for JSON artifacts follows `packages/specs/docs/contracts/reporting/hash_canonicalization_v0_1.md`.

## Schema Vs Policy
- Schema-enforced:
  - Entry keys and types.
  - `sha256` pattern.
  - `evidence_refs` arrays are non-empty.
- Validator-enforced policy:
  - `source_path` safety checks (absolute/traversal rejection).
  - `evidence_refs` referential integrity against `evidence_index` keys.
