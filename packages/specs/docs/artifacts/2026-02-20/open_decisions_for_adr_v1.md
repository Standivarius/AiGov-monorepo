# Open Decisions For ADR v1

Date: `2026-02-20`

## ADR-012: Canonical Judge Output Contract for v0.1

Context:
- Runtime emits `behaviour_json_v0_phase0.json` and `judgments.json`.
- Legacy narrative contract still describes `behaviour_json_v1` field expectations.
- PRD and reporting layers need one canonical persisted contract to avoid drift.

Options:
1. Keep dual outputs; declare one canonical persisted contract and one derived view.
2. Canonicalize to `behaviour_json_v0_phase0` and deprecate legacy v1 narrative.
3. Canonicalize to `judgments_v0` and generate behaviour output as projection.

## ADR-013: Intake locale_context deprecation boundary

Context:
- Current contract/runtime use `locale_context` with deterministic derivation rules.
- Planning artifacts discuss future simplification toward context_profile-first behavior.
- Premature removal risks breaking deterministic compatibility and existing fixtures.

Options:
1. Keep `locale_context` required through MVP v1.0.
2. Make `locale_context` optional when `context_profile` exists, preserving backward compatibility.
3. Remove `locale_context` from canonical output in v0.x and migrate all fixtures/contracts now.

## ADR-014: Judge evaluation gate maturity rule

Context:
- J02 schema validation path is implemented.
- J03 pattern-accuracy suite is scaffolded but runner hook remains `NotImplemented`.
- Gate policy needs explicit stance on whether J03 is required for method gate closure.

Options:
1. Require J02 only for v0.1 gate; treat J03 as deferred.
2. Require J02 + J03 before G3 closes.
3. Replace J03 with deterministic replay metric for v0.1 and defer pattern-accuracy to v1.0.

