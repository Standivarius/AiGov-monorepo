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
| `packages/specs/schemas/intake_bundle_v0_1.schema.json` | Planned intake bundle schema | Canonical schema for intake_bundle_v0_1 | planned | Phase D deliverable. |
| `packages/specs/docs/contracts/intake/evidence_model_b_v0_1.md` | Planned Evidence Model B contract | Defines evidence_index + evidence_refs contract | planned | Phase D deliverable (new contract). |
| `tools/fixtures/validators/intake_output_context_fail_missing_locale_and_context.json` | Planned regression fixture | Catch fail-open when both context_profile and locale_context key are absent | planned | Requires validator patch to fail. |
| `tools/fixtures/validators/intake_bundle_v0_1_fail_unknown_jurisdiction.json` | Planned bundle fixture | Enforce jurisdiction allowlist split from generic unknown vocab checks | planned | Single-mode failure. |
| `tools/fixtures/validators/intake_bundle_v0_1_fail_unknown_sector.json` | Planned bundle fixture | Enforce sector allowlist split from generic unknown vocab checks | planned | Single-mode failure. |
| `tools/fixtures/validators/intake_bundle_v0_1_fail_sha256_uppercase.json` | Planned bundle fixture | Enforce lowercase sha256 requirement | planned | Single-mode failure. |
| `tools/fixtures/validators/intake_bundle_v0_1_fail_extra_key.json` | Planned bundle fixture | Enforce additionalProperties fail-closed | planned | Single-mode failure. |
| `tools/fixtures/validators/intake_bundle_v0_1_fail_unknown_policy_pack.json` | Planned bundle fixture | Enforce policy pack allowlist | planned | Single-mode failure. |
| `tools/fixtures/validators/intake_bundle_v0_1_fail_empty_bundle_id.json` | Planned bundle fixture | Enforce `bundle_id` minLength 1 | planned | Single-mode failure. |
| `tools/fixtures/validators/intake_bundle_v0_1_fail_source_path_traversal.json` | Planned bundle fixture | Reject `source_path` traversal (`../`) and absolute-path semantics | planned | Single-mode failure. |
| `tools/fixtures/validators/intake_bundle_v0_1_fail_evidence_refs_empty_array.json` | Planned bundle fixture | Enforce required evidence refs are not empty arrays | planned | Distinct from dangling-reference mode. |
| `OPA readiness policy (planned)` | Policy rule set | Forbid nondeterministic builtins including `opa.runtime()` | planned | OPA deny = hard fail when OPA path is enabled. |
| `intake_bundle_v0_1 schema strictness (planned)` | Schema rule set | Require `additionalProperties: false` at root and nested objects | planned | Fail-closed schema baseline. |
| `sha256 format rule (planned)` | Validator/schema rule set | Enforce lowercase hex pattern `^[a-f0-9]{64}$` | planned | Applies to Evidence Model B entries. |
| `tools/validate_intake_bundle_v0_1.py` | Planned validator | Fail-closed validator for intake_bundle_v0_1 pass/fail fixtures | planned | Phase D deliverable. |
| `tools/validate_planning_pack.py` (intake_bundle wiring) | Planned PR-gate wiring | Imports + runs intake bundle validator and fixture checks | planned | Moves bundle fixtures into active gating. |
| `packages/pe/tests/intake/test_intake_bundle_validation.py` | Planned PE tests | Unit-level deterministic assertions for intake bundle validation | planned | Complements tools-level validator coverage. |
