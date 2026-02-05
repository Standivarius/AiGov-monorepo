# Petri Transcripts (v0.1)

Scope: GDPR-only. Non-GDPR frameworks are out of scope unless later requested.

## Purpose
Define the deterministic output envelope for Petri transcript artifacts produced by GDPR audit runs.

## Contract Definition
A Petri transcript artifact must exist and be attributable to a specific run. This document is an envelope-level contract only; it does not define a transcript schema yet.

## Determinism + Fail-Closed Expectations
- Transcript artifacts must be deterministically produced for a given run configuration.
- Missing or unreadable transcript outputs should fail closed in downstream tooling.

## Schema vs Policy
- Schema: No dedicated JSON Schema is defined for this artifact yet.
- Validators: TBD (dedicated validator pending).
