# Retrieval Conflicts v1

Date: `2026-02-20`  
Scope: `M_Intake`, `M_Judge`  
Resolution policy applied:
1. contract/ADR over planning/chat artifacts  
2. newer dated source over older  
3. merged PR/runtime source over draft notes  
4. planning over chat artifact when both are non-contract

## Conflict C1: Intake runtime implementation state

- Conflict key: `intake_runtime_state`
- Claim A:
  - Intake validator is still `NotImplementedError`.
  - Source: `packages/specs/docs/artifacts/2026-02-20/taxonomy_conflicts_v0.md`
  - Source kind/date: planning, 2026-02-20
- Claim B:
  - Intake validator is implemented with fail-closed rules.
  - Source: `packages/ep/aigov_ep/intake/validate.py`
  - Source kind/date: contract/runtime, undated
- Resolution:
  - **Resolved in favor of Claim B** (runtime source + newer merged behavior).
- Impact:
  - Taxonomy conflict doc is stale on this point and should be updated in a later cleanup pass.

## Conflict C2: Canonical judge output contract

- Conflict key: `judge_canonical_output_contract`
- Claim A:
  - Judge output contract is `behaviour_json_v1` narrative with specific field expectations (confidence, reasoning string, UUID formats).
  - Source: `packages/specs/docs/specs/data-contracts-v0.1.md`
  - Source kind/date: contract, 2025-12-14
- Claim B:
  - Runtime currently persists `behaviour_json_v0_phase0.json` and `judgments.json` with canonical verdict mapping.
  - Sources:
    - `packages/ep/aigov_ep/judge/judge.py`
    - `packages/specs/docs/contracts/judgements/judgments_v0.schema.json`
  - Source kind/date: runtime + contract, current
- Resolution:
  - **Unresolved** (contested design choice; requires ADR).
- Impact:
  - Risk of drift in PRD-M for Judge and in downstream reporting contract assumptions.

## Conflict C3: Judge test maturity statement

- Conflict key: `judge_test_maturity_status`
- Claim A:
  - Judge J01/J02/J03 tests are pending.
  - Source: `packages/pe/tests/judge/README.md`
  - Source kind/date: contract doc, undated
- Claim B:
  - J02 schema test and offline runner are implemented and runnable; J03 remains scaffold with `NotImplementedError`.
  - Sources:
    - `packages/pe/tests/judge/test_j02_schema.py`
    - `packages/pe/aigov_eval/offline_judge_runner.py`
    - `packages/pe/tests/judge/test_j03_accuracy.py`
  - Source kind/date: runtime/tests
- Resolution:
  - **Partially resolved**:
    - J02 implemented,
    - J03 not implemented.
- Impact:
  - PRD/test registry should track Judge as partial maturity, not binary pending/done.
  - Escalated to `ADR-014` in `open_decisions_for_adr_v1.md` for explicit gate policy.

## Conflict C4: Intake locale boundary long-term policy

- Conflict key: `intake_locale_deprecation_policy`
- Claim A:
  - Legacy `locale_context` remains in contract and runtime behavior.
  - Sources:
    - `packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md`
    - `packages/ep/aigov_ep/intake/validate.py`
- Claim B:
  - Planning discussions propose eventual context_profile-first simplification and possible locale deprecation.
  - Source: `packages/specs/docs/artifacts/2026-02-05_GDPR_Execution_Planning.md`
- Resolution:
  - **Unresolved by design** (future-policy decision, no current runtime contradiction).
- Impact:
  - Requires explicit ADR to avoid future accidental breakage of deterministic legacy path.
