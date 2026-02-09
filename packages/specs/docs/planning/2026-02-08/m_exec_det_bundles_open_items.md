# M_Execution Deterministic Bundles — Open Items Tracker

Single source of truth for Claude review loop outcomes.

## Iteration Log

### Iteration 0 (pre-Claude)
- Date: 2026-02-09
- Stack under review:
  - PR1 `#164` https://github.com/Standivarius/AiGov-monorepo/pull/164
  - PR2 `#165` https://github.com/Standivarius/AiGov-monorepo/pull/165
  - PR3 `#166` https://github.com/Standivarius/AiGov-monorepo/pull/166
  - PR4 `#167` https://github.com/Standivarius/AiGov-monorepo/pull/167
- MUST count: TBD
- SHOULD count: TBD
- COULD count: TBD
- Claude architecture summary: Pending
- Claude adversarial summary: Pending
- Impacted PR(s): TBD
- Fixes applied: None yet

### Iteration 1 (local architecture + adversarial review)
- Date: 2026-02-09
- Reviewer mode: Codex local (using prepared Claude review invariants/prompts as checklist)
- MUST count: 0
- SHOULD count: 0
- COULD count: 3
- Architecture summary:
  - Contract-first ordering is preserved (`#164` schema/contract precede runtime hardening).
  - Fail-closed boundaries hold for schema mismatch and dual-manifest ambiguity.
  - Backward compatibility check: legacy-only `bundle_manifest.json` path still routes past manifest selection logic.
- Adversarial summary:
  - Rejected unknown key (`additionalProperties: false`) in manifest root.
  - Rejected missing required scenario fields and invalid `sha256` format.
  - Verified deterministic multi-error ordering (stable output across repeated runs).
  - CLI `execute` dual-manifest fixture exits with code `2` and explicit error.
- Required proof commands in this iteration:
  - `python3 tools/validate_planning_pack.py`: PASS
  - `bash tools/run_pr_gate_validators.sh`: PASS
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`: PASS (`docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260209_080550.log`)
- Impacted PR(s): none
- Fixes applied:
  - Docs-only closeout stamping in PR4 branch (`pr4-mexec-closeout`): roadmap PR metadata, DoD checks, milestone report status.
- Deferred COULD items:
  - Optional future schema policy for scenario ordering/uniqueness.
  - Optional additional fixture coverage for path policy edge-cases at schema-vs-policy boundary.
  - Optional independent external rerun via Claude prompts for extra audit redundancy.

### Iteration 2 (Codex fix pass for SHOULD + COULD closure)
- Date: 2026-02-09
- MUST count: 0
- SHOULD count: 0
- COULD count: 0
- Findings addressed:
  - Shared schema helper introduced to eliminate divergent `_validate_schema` behavior between validators.
  - Deterministic manifest contract now explicitly documents deterministic-validator scope vs legacy CLI fallback.
  - Scenario ordering/uniqueness policy implemented and gated (schema + validator + runtime checks).
  - Added deterministic fail fixtures for duplicate `scenario_instance_id` and unsorted `scenarios`.
- Impacted PR(s): `#165`, `#166`, `#167` (follow-up updates on top of stack)
- Required proof commands:
  - `python3 tools/validate_planning_pack.py`: PASS
  - `bash tools/run_pr_gate_validators.sh`: PASS
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`: PASS (run after committing this fix pass)

## Working Rule
- Iterate until MUST=0 and SHOULD=0.
- Apply fixes at earliest impacted branch, then propagate to downstream stack branches.
