# M_Intake Phase 4: Export Adapters + First Extract Run (Tool-Agnostic, Deterministic) — Codex Roadmap

Date: 2026-02-10  
Status: In execution  
Overall Effort: high

## 1) Why This Milestone Now
Phase 3 established deterministic artifact contracts and validators for `intake_source_snapshot_v0_1` and `intake_bundle_extract_v0_1`, but artifact production is still fixture/manual. This milestone closes that gap by adding a deterministic file-export adapter that consumes a local export directory and emits both artifacts in a fail-closed way, with fixture-gated proofs and no live connector coupling.

## 2) Verified Repo Truth (Research)
- Existing validators already enforce stage-local deterministic policy:
  - `tools/validate_intake_bundle_extract_v0_1.py`
  - `tools/validate_intake_source_snapshot_v0_1.py`
- Existing fixture pattern for stage artifacts exists under:
  - `tools/fixtures/validators/intake_bundle_extract_*`
  - `tools/fixtures/validators/intake_source_snapshot_*`
- Planning-pack already wires these validators deterministically:
  - `tools/validate_planning_pack.py`
- Existing deterministic export pattern to reuse:
  - producer: `tools/export_bundle_to_petri_seed_instructions_alpha.py`
  - determinism validator: `tools/validate_export_bundle_to_petri_seed_instructions_alpha.py`
- Stage boundary contract already defines deterministic/fail-closed invariants and deferred composition checks:
  - `packages/specs/docs/contracts/intake/intake_bundle_stage_artifacts_v0_1.md`

## 3) Milestone Objective
Given an input `file_export` directory, deterministically produce:
- A) `intake_source_snapshot_v0_1` JSON (content-addressed, sorted, traversal-safe)
- B) `intake_bundle_extract_v0_1` JSON (deterministic candidate extraction, sorted, references snapshot id)

No questionnaires, no LLM, no live connector calls.

## 4) Non-Goals
- No OPA runtime execution.
- No PAR runtime adapter.
- No LLM-assisted extraction.
- No external API connectors.
- No non-GDPR scope expansion.

## 5) Guardrails
- Contract-first + fail-closed.
- Deterministic ordering and stable error messages.
- Stdlib-only validators/tools where possible.
- OSS stitching only behind export/file adapter boundaries.
- PR hygiene: `<=6 files changed per PR`.
- Required proof commands in every slice:
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`

## 6) Deterministic Adapter Decisions (Locked for v0.1)
- Adapter implementation location: `tools/` (no EP runtime integration in this milestone).
- Input mode: local directory (`file_export`) only.
- File inventory:
  - walk recursively in lexical order (sorted dirs, sorted files)
  - normalize to POSIX relative paths
  - reject symlink entries (fail-closed)
  - reject any resolved path escaping export root (fail-closed)
- Provenance:
  - each source file includes `source_path` (relative, normalized) + `sha256`
  - `snapshot_id` is deterministic from canonical source inventory hash
  - extract payload `source_snapshot_id` MUST equal generated `snapshot_id`
- Extract ordering:
  - extracted candidates sorted by `field_path`
  - `evidence_refs` sorted and unique
- Content handling (first run): deterministic manual heuristics from JSON files only; unsupported shapes fail closed.

## 7) PR Slices (Execution Plan)

### PR1 — Export Adapter Contract + Tiny Export Fixtures
Effort: medium

Exact file list (`<=6`):
1. `packages/specs/docs/contracts/intake/intake_export_file_adapter_v0_1.md` (new)
2. `tools/fixtures/exports/file_export_pass_minimal/context_profile.json` (new)
3. `tools/fixtures/exports/file_export_fail_symlink/context_profile.json` (new symlink fixture seed)
4. `tools/fixtures/exports/file_export_fail_symlink/README.md` (new fixture note)
5. `packages/specs/docs/planning/2026-02-10/m_intake_phase4_export_adapters_codex_roadmap.md` (status stamping)
6. `packages/specs/docs/planning/2026-02-10/m_intake_phase4_export_adapters_milestone_report_skeleton.md` (new, tracked skeleton)

PASS + FAIL fixtures (minimum):
- PASS: `tools/fixtures/exports/file_export_pass_minimal/`
- FAIL: `tools/fixtures/exports/file_export_fail_symlink/`

Validators/hooks location:
- Contract and fixture-only slice (no runtime hook yet).

Acceptance criteria:
- Adapter contract explicitly defines traversal/symlink fail-closed rules.
- Tiny export fixture directory exists and is consumable by planned adapter.
- Fail fixture semantics are explicit and deterministic.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

---

### PR2 — Snapshot Producer + Snapshot Determinism Validator + Gate Wiring
Effort: high

Exact file list (`<=6`):
1. `tools/run_intake_export_file_adapter_v0_1.py` (new; snapshot emission)
2. `tools/validate_intake_export_file_adapter_v0_1.py` (new; repeated-run determinism check)
3. `tools/fixtures/validators/intake_export_adapter_snapshot_pass.json` (new expected snapshot fixture)
4. `tools/fixtures/validators/intake_export_adapter_snapshot_fail_symlink.json` (new expected-fail fixture metadata)
5. `tools/validate_planning_pack.py` (snapshot pass/fail gate wiring)
6. `packages/specs/docs/planning/2026-02-10/m_intake_phase4_export_adapters_codex_roadmap.md` (status stamping)

PASS + FAIL fixtures (minimum):
- PASS: `intake_export_adapter_snapshot_pass.json`
- FAIL: `intake_export_adapter_snapshot_fail_symlink.json`

Validators/hooks location:
- Tools-only:
  - producer hook in `tools/run_intake_export_file_adapter_v0_1.py`
  - determinism validator hook in `tools/validate_intake_export_file_adapter_v0_1.py`
  - planning-pack hook in `tools/validate_planning_pack.py`

Acceptance criteria:
- Adapter emits valid `intake_source_snapshot_v0_1` JSON.
- Repeated runs over same export dir produce byte-identical snapshot output.
- Symlink fixture fails with deterministic expected substring.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

---

### PR3 — Extract Producer Extension + Extract Gates
Effort: high

Exact file list (`<=6`):
1. `tools/run_intake_export_file_adapter_v0_1.py` (update; add extract emission)
2. `tools/validate_intake_export_file_adapter_v0_1.py` (update; validate extract output + snapshot linkage)
3. `tools/fixtures/exports/file_export_fail_empty_payload/context_profile.json` (new fail export fixture)
4. `tools/fixtures/validators/intake_export_adapter_extract_pass.json` (new expected extract fixture)
5. `tools/fixtures/validators/intake_export_adapter_extract_fail_empty.json` (new expected-fail metadata)
6. `tools/validate_planning_pack.py` (extract pass/fail gate wiring)

PASS + FAIL fixtures (minimum):
- PASS: `intake_export_adapter_extract_pass.json`
- FAIL: `intake_export_adapter_extract_fail_empty.json`

Validators/hooks location:
- Tools-only producer + validator + planning-pack checks.

Acceptance criteria:
- Adapter emits valid `intake_bundle_extract_v0_1` JSON.
- `source_snapshot_id` in extract equals generated snapshot `snapshot_id`.
- Extract ordering and evidence refs deterministic constraints are enforced.
- Empty payload fail fixture triggers deterministic expected substring.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

---

### PR4 — Contract Linkage + Stage Boundary Clarifications + Closeout
Effort: medium

Exact file list (`<=6`):
1. `packages/specs/docs/contracts/intake/intake_source_snapshot_v0_1.md` (update provenance semantics)
2. `packages/specs/docs/contracts/intake/intake_bundle_extract_v0_1.md` (update snapshot-link and extraction semantics)
3. `packages/specs/docs/contracts/intake/intake_bundle_stage_artifacts_v0_1.md` (update adapter boundary notes)
4. `packages/specs/docs/contracts/intake/intake_bundle_v0_1.md` (link adapter-produced upstream artifacts)
5. `packages/specs/docs/planning/2026-02-10/m_intake_phase4_export_adapters_milestone_report.md` (new closeout report)
6. `packages/specs/docs/planning/2026-02-10/m_intake_phase4_export_adapters_codex_roadmap.md` (final stamping)

PASS + FAIL fixtures (minimum):
- PASS: reuse `intake_export_adapter_snapshot_pass.json`, `intake_export_adapter_extract_pass.json`
- FAIL: reuse `intake_export_adapter_snapshot_fail_symlink.json`, `intake_export_adapter_extract_fail_empty.json`

Validators/hooks location:
- Docs-only slice; no new runtime hooks.

Acceptance criteria:
- Contracts exactly match delivered producer/validator behavior.
- Stage-boundary documentation explicitly states enforced vs deferred checks.
- Milestone report contains PR links, proofs, residual risks.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

## 8) Definition of Done
- [ ] Deterministic file-export adapter exists in `tools/` and is fail-closed.
- [ ] Adapter emits both `intake_source_snapshot_v0_1` and `intake_bundle_extract_v0_1`.
- [ ] Snapshot provenance includes deterministic `snapshot_id`, sorted `source_files`, and `sha256` values.
- [ ] Traversal/symlink unsafe inputs are rejected deterministically.
- [ ] Extract output ordering (`field_path`, `evidence_refs`) is deterministic and validated.
- [ ] Planning-pack enforces adapter PASS/FAIL fixtures with expected substring assertions.
- [ ] Every PR slice stays `<=6 files` and passes allowed proofs.

## 9) Stop / Rescope Conditions
- If deterministic extraction heuristics require probabilistic parsing, stop and split into separate milestone.
- If symlink fixture portability blocks deterministic CI behavior, replace with generated temp symlink inside validator while preserving fail-closed semantics.
- If EP runtime integration is requested, split to a separate milestone after tool-level proofs stabilize.
- If fixture count pressure breaks `<=6 files/PR`, split further rather than widening slices.

## 10) Blockers
- None identified for planning.

## 11) Execution Tracking
- PR1 (`pr1-mintake4-contract`) — Status: In progress
  - PR: TBD
  - Proofs:
    - [ ] `python3 tools/validate_planning_pack.py`
    - [ ] `bash tools/run_pr_gate_validators.sh`
    - [ ] `NX_DAEMON=false npx nx run evalsets:migration-smoke`
- PR2 (`pr2-mintake4-snapshot`) — Status: Planned
  - PR: TBD
  - Proofs:
    - [ ] `python3 tools/validate_planning_pack.py`
    - [ ] `bash tools/run_pr_gate_validators.sh`
    - [ ] `NX_DAEMON=false npx nx run evalsets:migration-smoke`
- PR3 (`pr3-mintake4-extract`) — Status: Planned
  - PR: TBD
  - Proofs:
    - [ ] `python3 tools/validate_planning_pack.py`
    - [ ] `bash tools/run_pr_gate_validators.sh`
    - [ ] `NX_DAEMON=false npx nx run evalsets:migration-smoke`
- PR4 (`pr4-mintake4-closeout`) — Status: Planned
  - PR: TBD
  - Proofs:
    - [ ] `python3 tools/validate_planning_pack.py`
    - [ ] `bash tools/run_pr_gate_validators.sh`
    - [ ] `NX_DAEMON=false npx nx run evalsets:migration-smoke`
