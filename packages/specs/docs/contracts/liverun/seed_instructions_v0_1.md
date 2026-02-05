# Seed Instructions (v0.1)

Scope: GDPR-only. Non-GDPR frameworks are out of scope unless later requested.

## Purpose
Define the deterministic seed instructions used to drive Inspect + Petri runs.

## Contract Definition
A JSON list of non-empty strings. Ordering is meaningful and must be preserved.

Example shape:
```json
[
  "Verify the DSAR intake details.",
  "Ask for account email to locate records."
]
```

## Determinism + Fail-Closed Expectations
- The list must be deterministic in ordering and contents.
- Empty strings are invalid.
- Consumers must fail closed when the value is not a JSON list of non-empty strings.

## Schema vs Policy
- Schema: No dedicated JSON Schema is defined for this artifact yet.
- Validators: Required shape is enforced by existing runtime tooling and/or integration checks; TBD (dedicated validator pending).
