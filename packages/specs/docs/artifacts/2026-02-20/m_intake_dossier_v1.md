# M_Intake Dossier v1

Date: `2026-02-20`  
Module: `M_Intake` (Client Intake)  
Status: `Draft for Pre-PRD`

## 1) Module scope

- Canonical module ID: `M_Intake`
- Friendly label: Client Intake
- In-scope responsibilities:
  - Validate intake output payloads against contract and policy rules.
  - Enforce fail-closed allowlists for jurisdiction, sector, and policy packs.
  - Preserve deterministic context resolution (`context_profile` + policy stack).
- Out-of-scope responsibilities:
  - Scenario execution or scoring.
  - Judge verdict generation.

## 2) Contracts

- Input contracts:
  - `packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md`
- Output contracts:
  - validated intake output (same contract boundary)
  - canonical readiness artifact uses `packages/specs/docs/contracts/intake/intake_bundle_v0_1.md`
- Provenance requirements:
  - intake bundle requires `evidence_index` and `evidence_refs`.
  - unsafe paths and nondeterministic root fields fail validation.

## 3) Invariants and fail-closed behavior

- Invariants:
  - `policy_pack_stack` exact order is mandatory.
  - `context_profile` is authoritative when present.
  - locale/context mismatch fails closed.
- Failure modes:
  - missing required keys,
  - unknown allowlist values,
  - missing locale/context key path when context profile absent,
  - invalid stack shape or order.
- Fail-closed rules:
  - reject invalid stack/order,
  - reject unknown taxonomy values,
  - reject ambiguous context.

## 4) Evidence and telemetry

- Evidence emitted:
  - validated intake payload boundary,
  - deterministic bundle contract linkage through `intake_bundle_v0_1`.
- Telemetry emitted:
  - CLI validation error strings and exit code for invalid payloads.
- Privacy constraints:
  - contract uses bounded profile fields and refs rather than raw internal reasoning traces.
- Security considerations:
  - strict allowlists + path-safety constraints at bundle boundary.

## 5) Acceptance and test/eval expectations

- Acceptance criteria:
  - contract-required keys present,
  - deterministic context stack policy enforced,
  - mismatch and unknown-value cases fail.
- Deterministic test/eval expectations:
  - planning-pack fixtures for pass/fail context cases,
  - intake contract and bundle validator gates stay fail-closed.

## 6) Sourced claims

| claim_type | claim_text | source_path | source_date | source_kind | confidence | conflict_key |
|---|---|---|---|---|---|---|
| scope | M_Intake validates GDPR intake output payloads with context_profile authoritative. | packages/specs/docs/contracts/modules/cards/M_Intake.card.json | 2026-02-20 | contract | high | intake_scope_authority |
| input_contract | Input contract for M_Intake is client_intake_output_contract_v0_1.md. | packages/specs/docs/contracts/modules/cards/M_Intake.card.json | 2026-02-20 | contract | high | intake_input_contract_ref |
| output_contract | Output boundary is validated intake output aligned to client_intake_output_contract_v0_1.md. | packages/specs/docs/contracts/modules/cards/M_Intake.card.json | 2026-02-20 | contract | high | intake_output_contract_ref |
| invariant | policy_pack_stack must equal ['GDPR_EU', jurisdiction, sector, 'client'] with strict ordering. | packages/ep/aigov_ep/intake/validate.py | null | contract | high | intake_policy_stack_order |
| invariant | locale_context and context_profile.jurisdiction mismatch fails closed. | packages/ep/aigov_ep/intake/validate.py | null | contract | high | intake_locale_context_mismatch_rule |
| failure_mode | If context_profile is absent and locale_context key is absent, validation fails. | packages/ep/aigov_ep/intake/validate.py | null | contract | high | intake_missing_context_fail_closed |
| security | Jurisdiction/sector/policy packs are allowlist enforced and unknown values fail. | packages/specs/docs/contracts/intake/intake_bundle_v0_1.md | null | contract | high | intake_allowlist_enforcement |
| evidence | Canonical deterministic intake artifact for gating is intake_bundle_v0_1. | packages/specs/docs/contracts/intake/intake_bundle_v0_1.md | null | contract | high | intake_canonical_artifact |
| test_eval | Intake context fixtures cover pass/fail null/mismatch/unknown cases in planning-pack flow. | packages/specs/docs/artifacts/2026-02-05_GDPR_Execution_Planning.md | 2026-02-05 | planning | medium | intake_fixture_gate_coverage |
| telemetry | Runtime intake validator emits deterministic error strings and non-zero exit code for invalid payloads. | packages/ep/aigov_ep/intake/validate.py | null | contract | high | intake_runtime_telemetry_surface |
| privacy | No raw chain-of-thought persistence is a method-level hard rule and intake contracts stay structured/profile-based. | packages/specs/docs/planning/2026-02-20-method/AIGOV_FACTORY_METHOD_v1.md | 2026-02-20 | planning | medium | intake_no_raw_cot_rule |
| open_decision | Locale_context long-term boundary remains open for later milestone policy. | packages/specs/docs/artifacts/2026-02-05_GDPR_Execution_Planning.md | 2026-02-05 | planning | medium | intake_locale_deprecation_policy |

## 7) Open decisions (ADR candidates only)

- Title: `ADR-013 Intake locale_context deprecation boundary`
- Context: Legacy `locale_context` is still enforced and used for deterministic derivation, but planning artifacts discuss future context_profile-first simplification.
- Options:
  - Keep `locale_context` required through v1.0.
  - Make `locale_context` optional when `context_profile` is present.
  - Remove `locale_context` from canonical output and rely only on `context_profile`.
