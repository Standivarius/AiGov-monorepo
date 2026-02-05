# M_Intake Constitution (v2026-02-06)

## Purpose
M_Intake is an audit-grade evidence distillation module. Its output must be deterministic, schema-valid, and evidence-backed.

## Non-negotiable invariants (the moat)
1) Contracts are source of truth
- All new artifacts are defined as JSON Schema under packages/specs/schemas/
- Contract docs live under packages/specs/docs/contracts/
- Runtime validation MUST be fail-closed.

2) Determinism
- Same inputs + same policy_pack_stack => byte-identical outputs (stable ordering, stable IDs).
- No time-based or random fields unless explicitly declared nondeterministic (and then rejected by default).

3) Evidence discipline
- All claims must reference evidence via canonical evidence IDs (content-addressed hashes).
- Evidence model is Model B: global evidence_index + field->evidence_refs.
- Unknowns[] and conflicts[] are first-class outputs; do not silently resolve.

4) Fail-closed validation
- Unknown taxonomy/jurisdiction/sector values MUST be rejected.
- Missing required sections MUST be rejected.
- Null where not allowed MUST be rejected (no implicit null acceptance).

5) Legacy boundary (already implemented; must not regress)
- context_profile is the source of truth for intake bundle artifacts.
- locale_context handling and mismatch rules remain at the Intake OUTPUT boundary.
- Known hardening edge: locale_context:null (key present) MUST be rejected; fixtures gate this.

6) OSS stitching rule
- OSS is an input/implementation behind adapters. Canonical AiGov artifacts do not change shape to match OSS.
- No copying code from GPL/EUPL sources into core packages/ep or packages/pe.
- If a GPL/EUPL tool is adopted, it must be isolated as a separate optional component with a clean adapter boundary.

## Definition of done (Phase outcomes)
Phase A (Docs-only)
- Constitution + Runbook + Task Pack exist in repo.

Phase B (Mapping)
- A verified codebase map exists: modules, artifacts, schemas, validators, PE gates, and where M_Intake slots in.

Phase C (Architecture)
- A proposed architecture (no implementation) identifies seams, adapters, artifacts, and pipeline impacts.
- Risks + migration steps are explicit.

Phase D (Evals-first)
- PR-gating fixtures/tests define desired behavior BEFORE implementation/refactors.

## Allowed proof commands (must run & report)
- python3 tools/validate_planning_pack.py
- bash tools/run_pr_gate_validators.sh
- NX_DAEMON=false npx nx run evalsets:migration-smoke
