# M_Judge Dossier v1

Date: `2026-02-20`  
Module: `M_Judge` (Judge)  
Status: `Draft for Pre-PRD`

## 1) Module scope

- Canonical module ID: `M_Judge`
- Friendly label: Judge
- In-scope responsibilities:
  - Generate judge outputs from transcript/scenario context.
  - Canonicalize verdict and signals before persistence.
  - Emit Stage B artifacts consumed by reporting/evidence flows.
- Out-of-scope responsibilities:
  - Intake contract validation,
  - Reporting layer rendering,
  - Non-GDPR policy logic beyond configured taxonomy/contracts.

## 2) Contracts

- Input contracts:
  - module card points to `packages/specs/docs/specs/data-contracts-v0.1.md`.
  - runtime consumes transcript + scenario + run metadata.
- Output contracts:
  - `scores.json`, `evidence_pack.json`, `evidence_pack_v0.json`, `judgments.json`, `behaviour_json_v0_phase0.json`.
  - schema contract for judgments: `packages/specs/docs/contracts/judgements/judgments_v0.schema.json`.
- Provenance requirements:
  - judgments include `evidence_ids`,
  - deterministic references tie back to transcript/evidence artifacts.

## 3) Invariants and fail-closed behavior

- Invariants:
  - verdicts are normalized to canonical taxonomy values.
  - unknown signals are rejected in canonical signal path.
- Failure modes:
  - live mode requires API key and can fall back to undecided on runtime errors.
  - output contract mismatch risk exists between legacy contract narrative and current artifacts.
- Fail-closed rules:
  - schema enum enforcement for verdict values,
  - explicit normalization before persisted artifacts.

## 4) Evidence and telemetry

- Evidence emitted:
  - `judgments.json` with evidence links and verification labels.
  - Stage B evidence pack artifacts for downstream use.
- Telemetry emitted:
  - judge metadata (`model`, `timestamp_utc`, mock/runtime status).
- Privacy constraints:
  - no raw chain-of-thought persistence surfaced in module contracts.
- Security considerations:
  - live model execution gated by `OPENROUTER_API_KEY`,
  - deterministic mock path reduces nondeterministic dependency risk in v0.1.

## 5) Acceptance and test/eval expectations

- Acceptance criteria:
  - schema-valid behavior output,
  - canonical verdict vocabulary,
  - evidence-linked judgments payload.
- Deterministic test/eval expectations:
  - offline runner + J02 schema tests are implemented.
  - J03 pattern-accuracy test remains scaffold-only and not executable yet.

## 6) Sourced claims

| claim_type | claim_text | source_path | source_date | source_kind | confidence | conflict_key |
|---|---|---|---|---|---|---|
| scope | M_Judge scores audit runs and emits structured outputs used by reporting. | packages/specs/docs/contracts/modules/cards/M_Judge.card.json | 2026-02-20 | contract | high | judge_scope_statement |
| input_contract | Module card points input contract to transcript-oriented data-contracts-v0.1. | packages/specs/docs/contracts/modules/cards/M_Judge.card.json | 2026-02-20 | contract | high | judge_input_contract_ref |
| output_contract | Runtime emits scores, evidence packs, judgments, and behaviour_json_v0_phase0. | packages/ep/aigov_ep/judge/judge.py | null | contract | high | judge_runtime_output_set |
| invariant | Persisted verdict labels are canonicalized to INFRINGEMENT/COMPLIANT/UNDECIDED. | packages/specs/docs/decisions/ADR-005-verdict-label-canonicalization-v0.1.md | 2026-02-20 | decision | high | judge_verdict_canonicalization |
| invariant | Unknown signal IDs are rejected during canonical signal validation for judgments. | packages/ep/aigov_ep/judge/judge.py | null | contract | high | judge_unknown_signal_rejection |
| failure_mode | Live mode depends on OPENROUTER_API_KEY; runtime errors may produce UNDECIDED fallback output. | packages/ep/aigov_ep/judge/judge.py | null | contract | high | judge_live_mode_failure_behavior |
| evidence | judgments schema requires scenario instance, verdict, verification mode/label, and evidence_ids. | packages/specs/docs/contracts/judgements/judgments_v0.schema.json | null | contract | high | judge_evidence_linkage |
| test_eval | Offline schema compliance path is implemented via offline runner + mapper + J02 tests. | packages/pe/tests/judge/test_j02_schema.py | null | contract | high | judge_schema_eval_coverage |
| test_eval | Pattern-accuracy J03 remains non-executable scaffold due NotImplemented runner hook. | packages/pe/tests/judge/test_j03_accuracy.py | null | contract | high | judge_accuracy_eval_status |
| acceptance | EP smoke test requires scores.json, evidence_pack.json, and schema-valid behaviour_json_v0_phase0 output. | packages/pe/tests/minimal_loop/test_ep_cli_judge_smoke.py | null | contract | high | judge_smoke_acceptance_contract |
| privacy | No raw chain-of-thought persistence is a method-level hard rule; judge artifacts remain structured outputs. | packages/specs/docs/planning/2026-02-20-method/AIGOV_FACTORY_METHOD_v1.md | 2026-02-20 | planning | medium | judge_no_raw_cot_rule |
| open_decision | Canonical persisted judge contract is still contested between legacy behaviour_json_v1 narrative and current v0 artifacts. | packages/specs/docs/specs/data-contracts-v0.1.md | 2025-12-14 | contract | medium | judge_canonical_output_contract |

## 7) Open decisions (ADR candidates only)

- Title: `ADR-012 Canonical Judge Output Contract for v0.1`
- Context: Legacy data-contract narrative (`behaviour_json_v1`) diverges from current runtime artifact set (`behaviour_json_v0_phase0` + `judgments_v0`).
- Options:
  - Keep dual-output model and define one canonical persisted contract with adapters.
  - Canonicalize to `behaviour_json_v0_phase0` and deprecate legacy v1 narrative.
  - Canonicalize to `judgments_v0` as source-of-truth and treat behaviour output as derived view.
