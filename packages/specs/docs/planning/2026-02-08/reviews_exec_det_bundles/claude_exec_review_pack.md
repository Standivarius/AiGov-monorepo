# Claude Review Pack: M_Execution Deterministic Bundle Consumption

Date: 2026-02-09  
Scope: GDPR-only, deterministic bundle consumption boundary.

## PR Stack
1. PR1 `#164` (base `main`)  
   https://github.com/Standivarius/AiGov-monorepo/pull/164
2. PR2 `#165` (base `pr1-mexec-schema`)  
   https://github.com/Standivarius/AiGov-monorepo/pull/165
3. PR3 `#166` (base `pr2-mexec-gates`)  
   https://github.com/Standivarius/AiGov-monorepo/pull/166
4. PR4 `#167` (base `pr3-mexec-ambiguity`)  
   https://github.com/Standivarius/AiGov-monorepo/pull/167

## Invariant Checklist
- Contract-first: schema + contract exist before runtime boundary change.
- Fail-closed: invalid/ambiguous manifests must error, no fallback ambiguity.
- Deterministic: stable error substrings and deterministic gate assertions.
- Backward compatibility: legacy-only `bundle_manifest.json` path still works.
- Scope lock: no OPA/PAR/LLM/non-GDPR expansion.

## Files of Interest
- Schema + contract:
  - `packages/specs/schemas/deterministic_bundle_manifest_v0_1_0.schema.json`
  - `packages/specs/docs/contracts/execution/deterministic_bundle_manifest_v0_1_0.md`
- Runtime boundary:
  - `packages/ep/aigov_ep/cli.py`
  - `packages/ep/aigov_ep/scenario/bundle_manifest_v0_1_0.py`
- Tooling + gates:
  - `tools/validate_ep_deterministic_bundle_manifest.py`
  - `tools/validate_planning_pack.py`
  - `tools/fixtures/validators/scenario_schema_list.json`
- New fixtures:
  - `tools/fixtures/bundles/fail_manifest_bad_schema_version/manifest.json`
  - `tools/fixtures/bundles/fail_dual_manifest/manifest.json`
  - `tools/fixtures/bundles/fail_dual_manifest/bundle_manifest.json`
- Tracking docs:
  - `packages/specs/docs/planning/2026-02-08/m_exec_deterministic_bundles_codex_roadmap.md`
  - `packages/specs/docs/planning/2026-02-08/m_exec_deterministic_bundles_milestone_report.md`

## Required Commands
Run exactly:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

If a command fails:
- paste the last 80 lines of output
- identify smallest impacted PR slice
- propose minimal <=6 file fix

## Required Output Format
1. MUST FIX (blocking)
2. SHOULD FIX (before close)
3. COULD (deferred)
4. Merge readiness per PR (`#164`..`#167`) with ✅/⚠️
5. Top 3 determinism/fail-closed risks
