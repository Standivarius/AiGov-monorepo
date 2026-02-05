# Inspect Logs (v0.1)

Scope: GDPR-only. Non-GDPR frameworks are out of scope unless later requested.

## Purpose
Define the deterministic output envelope for Inspect logs produced by GDPR audit runs.

## Contract Definition
An Inspect log artifact must exist and be attributable to a specific run. This document is an envelope-level contract only; it does not define a log schema yet.

## Determinism + Fail-Closed Expectations
- Log artifacts must be deterministically produced for a given run configuration.
- Missing or unreadable log outputs should fail closed in downstream tooling.

## Schema vs Policy
- Schema: No dedicated JSON Schema is defined for this artifact yet.
- Validators: TBD (dedicated validator pending).
