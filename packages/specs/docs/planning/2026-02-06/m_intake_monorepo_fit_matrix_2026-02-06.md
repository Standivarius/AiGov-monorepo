# M_Intake Monorepo Fit Matrix (v2026-02-06)

Scope: GDPR-only. This matrix maps existing repo touchpoints to M_Intake requirements.

| Path | What it is | M_Intake impact | Verified? | Notes |
| --- | --- | --- | --- | --- |
| `packages/specs/schemas/` | Canonical JSON Schemas | Source of truth for intake_bundle_v0_1 and related schema contracts | yes | Phase D will add intake_bundle_v0_1 schema here. |
| `packages/specs/docs/contracts/` | Contract docs | Contract definitions for intake output + new intake bundle artifacts | yes | LiveRun contracts now split into liverun/* docs. |
| `packages/specs/docs/contracts/taxonomy/` | Taxonomy allowlists | Single source of truth for jurisdiction/sector/policy packs | yes | Must remain standalone JSON files. |
| `packages/ep/aigov_ep/intake/validate.py` | Runtime intake validation | Fail-closed enforcement for intake output boundary | yes | Known gap: context_profile absent + locale_context key absent. |
| `tools/fixtures/validators/` | Validator fixtures | Eval-first fixtures for intake output + future intake bundle | yes | Naming convention: *_pass.json, *_fail_<reason>.json. |
| `packages/pe/tests/intake/` | PE intake tests | Regression + deterministic behavior tests | yes | Extend for intake_bundle_v0_1 and readiness gate. |
