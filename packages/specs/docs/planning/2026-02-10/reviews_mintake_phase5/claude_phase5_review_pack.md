# Claude Review Pack — M_Intake Phase 5 (GitHub Export Pack v0.1)

Date: 2026-02-10
Scope: PR stack #182 -> #185
Mode: independent review only (no implementation)

## Milestone intent
Phase 5 adds deterministic, fail-closed tools-only ingestion for a file-based `github_export_pack` profile (no live connector/auth, no EP runtime integration, no OPA/PAR/LLM runtime scope).

## PR stack map
- PR1: #182 (base: `main`, head: `pr1-mintake5-contract`)
  - contract for GitHub export pack v0.1
  - snapshot schema enum includes `github_export_pack`
  - minimal pass fixture seed
- PR2: #183 (base: `pr1-mintake5-contract`, head: `pr2-mintake5-snapshot`)
  - adapter snapshot support for GitHub pack
  - unsupported-extension fail behavior and gate wiring
- PR3: #184 (base: `pr2-mintake5-snapshot`, head: `pr3-mintake5-extract`)
  - deterministic GitHub extract heuristics
  - malformed-shape fail behavior and gate wiring
- PR4: #185 (base: `pr3-mintake5-extract`, head: `pr4-mintake5-closeout`)
  - contract linkage updates and closeout docs

## Files of interest
- Adapter runtime: `tools/run_intake_export_file_adapter_v0_1.py`
- Adapter validator/gate helpers: `tools/validate_intake_export_file_adapter_v0_1.py`
- Gate wiring: `tools/validate_planning_pack.py`
- Snapshot schema: `packages/specs/schemas/intake_source_snapshot_v0_1.schema.json`
- Contract docs:
  - `packages/specs/docs/contracts/intake/intake_github_export_pack_v0_1.md`
  - `packages/specs/docs/contracts/intake/intake_export_file_adapter_v0_1.md`
  - `packages/specs/docs/contracts/intake/intake_source_snapshot_v0_1.md`
  - `packages/specs/docs/contracts/intake/intake_bundle_extract_v0_1.md`
  - `packages/specs/docs/contracts/intake/intake_bundle_stage_artifacts_v0_1.md`
- Fixtures:
  - `tools/fixtures/exports/github_export_pack_pass_minimal/`
  - `tools/fixtures/exports/github_export_pack_fail_bad_shape/issues/ISSUE-001.json`
  - `tools/fixtures/validators/intake_export_adapter_snapshot_pass_github_pack.json`
  - `tools/fixtures/validators/intake_export_adapter_snapshot_fail_github_unsupported_ext.json`
  - `tools/fixtures/validators/intake_export_adapter_extract_pass_github_pack.json`
  - `tools/fixtures/validators/intake_export_adapter_extract_fail_github_bad_shape.json`

## Review invariants
- Fail-closed:
  - GitHub pack top-level must be exactly `repo/`, `issues/`, `pull_requests/`, `comments/`
  - recognized pack paths reject non-JSON and malformed/wrong-shape JSON
  - no silent skip for recognized pack paths
- Determinism:
  - lexical traversal order
  - canonical JSON bytes (`sort_keys`, compact separators, trailing newline)
  - repeated adapter runs produce byte-identical outputs
- Contract-first:
  - behavior aligns to schema+contract docs
  - schema strictness remains fail-closed (`additionalProperties: false`)
- Scope control:
  - no live connector/auth
  - no EP runtime integration added

## Required local commands
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

If any command fails, include last 80 lines and classify the likely root cause file(s).

## Critical reviewer role constraint
Claude must not implement or edit files.
Claude only reports findings and recommended minimal fix slices for Codex to implement.

## Required output format
1. MUST FIX (blocking)
2. SHOULD FIX (pre-close)
3. COULD (deferred)
4. Merge readiness per PR (#182-#185): ✅/⚠️
5. Top 3 determinism/fail-closed risks
6. Proof command result summary
7. Codex handoff plan with smallest file-scoped fix slices
