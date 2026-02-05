# Inspect Task Args (v0.1)

Scope: GDPR-only. Non-GDPR frameworks are out of scope unless later requested.

## Purpose
Define the minimal deterministic argument envelope needed to construct an Inspect/Petri run command.

## Contract Definition
An envelope describing the minimal run arguments needed to construct a deterministic Inspect/Petri command. At minimum, this includes:
- model roles or identifiers
- limit
- max_turns
- log_dir
- transcript_dir

This document defines the envelope only; individual fields and schemas are not yet formalized.

## Determinism + Fail-Closed Expectations
- All argument values must be deterministic and explicitly specified.
- Missing required fields should fail closed in the consuming tooling.

## Schema vs Policy
- Schema: No dedicated JSON Schema is defined for this artifact yet.
- Validators: TBD (dedicated validator pending).
