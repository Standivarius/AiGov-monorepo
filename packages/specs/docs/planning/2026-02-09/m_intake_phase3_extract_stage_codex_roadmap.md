# M_Intake Phase 3: Extract Stage (Export-Based, Tool-Agnostic) — Codex Roadmap

Date: 2026-02-09  
Status: In execution

## 1) Verified Repo Truth (Research Summary)
- `packages/specs/docs/planning/2026-02-03/state_object_v0_4__2026-02-03.json` and `packages/specs/docs/planning/2026-02-06/planner_state_2026-02-06.json` both pin:
  - GDPR-only scope.
  - Contract-first + fail-closed + deterministic gating.
  - Planner/Codex split (two-brain rule).
  - Allowed proof commands only:
    - `python3 tools/validate_planning_pack.py`
    - `bash tools/run_pr_gate_validators.sh`
    - `NX_DAEMON=false npx nx run evalsets:migration-smoke`
- `packages/specs/docs/planning/2026-02-08/m_intake_phase2_milestone_report.md` confirms Reconcile/Gap/Readiness boundaries are delivered and fixture-gated.
- `packages/specs/docs/planning/2026-02-08/m_intake_phase2_codex_roadmap.md` confirms Phase 2 stack completion and tracking discipline.
- `packages/specs/docs/planning/2026-02-08/m_exec_deterministic_bundles_codex_roadmap.md` confirms deterministic execution-manifest milestone is active with stacked PR plan.
- Existing intake runtime surface is still narrow:
  - `packages/ep/aigov_ep/intake/validate.py` (legacy intake output validation).
  - No dedicated Extract-stage schema or validator exists yet.
- Existing Extract architecture intent exists in planning docs only:
  - `packages/specs/docs/planning/2026-02-06/m_intake_architecture_plan_2026-02-06.md` defines ingest -> extract -> reconcile -> gap -> readiness.
- OSS adapter boundary guidance already exists (no deep coupling) in:
  - `packages/specs/docs/planning/2026-02-06/m_intake_constitution_2026-02-06.md`
  - `packages/specs/docs/planning/2026-02-06/m_intake_oss_eval_par_2026-02-06.md`
  - `packages/specs/docs/planning/2026-02-06/m_intake_architecture_plan_2026-02-06.md`

## 2) Milestone Candidates

### Candidate A (required): M_Intake Phase 3 — Extract Stage (export/file ingestion, tool-agnostic)
- Objective:
  - Define and gate deterministic Extract-stage artifacts between ingest inputs and existing Reconcile/Gap/Readiness stages.
- In scope:
  - Extract-stage schema + contract.
  - Source-snapshot (ingestion boundary) schema + contract.
  - Stdlib validators + PASS/FAIL fixtures + planning-pack wiring.
- Out of scope:
  - OPA runtime, PAR runtime adapter, LLM extraction/council.
- Why now:
  - Reconcile/Gap/Readiness already exist; Extract is the missing deterministic upstream stage.
- Risk: medium  
- Effort: medium

### Candidate B (optional): Process-compliance restack + PR hygiene alignment
- Objective:
  - Normalize branch/stack hygiene where PR slices exceed intended file-count guardrails.
- In scope:
  - Restack/split only; no feature work.
  - Tracking and roadmap consistency cleanup.
- Out of scope:
  - Net-new runtime capabilities.
- Why now:
  - Improves governance quality but does not move MVP intake functionality directly.
- Risk: low  
- Effort: low

### Candidate C (optional): Intake composition integrity gate
- Objective:
  - Add composition-level checks across stage artifacts and canonical `intake_bundle_v0_1` (cross-artifact evidence ref integrity).
- In scope:
  - New composition validator + fixtures + planning-pack checks.
- Out of scope:
  - New extraction logic or OSS integration.
- Why now:
  - Valuable for audit rigor, but lower immediate MVP value than missing Extract stage boundary.
- Risk: medium  
- Effort: medium

## 3) Recommended Next Milestone
- **Recommendation:** Candidate A — `M_Intake Phase 3: Extract Stage (export/file ingestion, tool-agnostic)`.
- Why this is next:
  - Maximizes MVP value by completing the deterministic intake boundary chain.
  - Reuses delivered Reconcile/Gap/Readiness contracts rather than inventing new flow.
  - Keeps coupling risk low by pinning OSS at adapter boundaries only.
  - Fits existing constitution and eval-first repo patterns.

## 4) Objectives (Recommended Milestone)
- Add deterministic Extract-stage artifacts that are contract-first and fail-closed.
- Add deterministic ingestion/source snapshot boundary artifacts for export/file inputs.
- Gate Extract and source-snapshot behavior in planning-pack with explicit PASS/FAIL fixtures.
- Keep implementation slices reviewable (`<=6 files/PR`).

## 5) Non-Goals
- No OPA execution runtime.
- No PAR adapter implementation beyond documented adapter boundaries.
- No LLM extraction/council logic.
- No non-GDPR expansion.
- No repo restructuring.

## 6) Guardrails
- Contract-first + fail-closed.
- Eval-first/TDD via fixtures before complex policy logic.
- Deterministic ordering and stable error messages.
- Stdlib-only validators where possible.
- OSS stitching behind adapters only; isolate license/coupling risk.
- Two-brain rule: planning now, implementation later.
- PR hygiene: `<=6 files changed per PR`.
- Required proof commands in every PR slice:
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`

## 7) Deterministic Contract Boundaries
- New Extract artifact (proposed):
  - `packages/specs/schemas/intake_bundle_extract_v0_1.schema.json`
  - `packages/specs/docs/contracts/intake/intake_bundle_extract_v0_1.md`
- New ingestion/source boundary artifact (proposed):
  - `packages/specs/schemas/intake_source_snapshot_v0_1.schema.json`
  - `packages/specs/docs/contracts/intake/intake_source_snapshot_v0_1.md`
- Existing canonical spine remains unchanged:
  - `intake_bundle_v0_1` remains canonical merge/readiness substrate.
- Existing stage artifacts remain unchanged in role:
  - Extract outputs feed Reconcile input; Reconcile/Gap/Readiness stay deterministic.

## 8) OSS Stitching Note
- OSS tools are optional implementations behind adapters.
- Canonical AiGov artifact shape is source-of-truth and must not drift to match OSS internals.
- Any PAR/OPA/external connector integration remains adapter-boundary-only and explicitly out of this milestone runtime scope.

## 9) PR Slice Plan (Execution Later)

### PR1 — Extract Contract + Schema Baseline
- Effort: medium
- Exact file list (`<=6`):
  - `packages/specs/schemas/intake_bundle_extract_v0_1.schema.json` (new)
  - `packages/specs/docs/contracts/intake/intake_bundle_extract_v0_1.md` (new)
  - `tools/fixtures/validators/scenario_schema_list.json` (register extract schema)
  - `tools/fixtures/validators/intake_bundle_extract_pass_file_export.json` (new)
  - `tools/fixtures/validators/intake_bundle_extract_fail_missing_required.json` (new)
  - `packages/specs/docs/planning/2026-02-09/m_intake_phase3_extract_stage_codex_roadmap.md` (status stamping)
- Fixtures to add:
  - PASS: `tools/fixtures/validators/intake_bundle_extract_pass_file_export.json`
  - FAIL: `tools/fixtures/validators/intake_bundle_extract_fail_missing_required.json`
- Validator/gate wiring locations:
  - Wiring deferred to PR2.
- Acceptance criteria:
  - Schema is strict (`additionalProperties: false`) and contract matches shape.
  - PASS/FAIL fixture JSON aligns with schema intent.
  - Schema strictness list includes new extract schema.
- Proof commands:
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`

### PR2 — Extract Validator Mode + Planning-Pack Gate
- Effort: medium
- Exact file list (`<=6`):
  - `tools/validate_intake_bundle_extract_v0_1.py` (new dedicated extract validator)
  - `tools/validate_planning_pack.py` (extract PASS/FAIL checks + deterministic substrings)
  - `tools/fixtures/validators/intake_bundle_extract_fail_unsorted_field_paths.json` (new)
  - `packages/specs/docs/contracts/intake/intake_bundle_stage_artifacts_v0_1.md` (add Extract stage semantics)
  - `packages/specs/docs/planning/2026-02-09/m_intake_phase3_extract_stage_codex_roadmap.md` (status stamping)
- Fixtures to add:
  - PASS: reuse `intake_bundle_extract_pass_file_export.json`
  - FAIL: `intake_bundle_extract_fail_unsorted_field_paths.json`
- Validator/gate wiring locations:
  - `tools/validate_intake_bundle_extract_v0_1.py`
  - `tools/validate_planning_pack.py`
- Acceptance criteria:
  - Extract mode is explicit/fail-closed.
  - Deterministic ordering failure is asserted by substring check.
  - Planning-pack fails if extract pass fixture fails or fail fixture unexpectedly passes.
- Proof commands:
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`

### PR3 — Source Snapshot Boundary (Contract + Validator + Fixtures)
- Effort: medium
- Exact file list (`<=6`):
  - `packages/specs/schemas/intake_source_snapshot_v0_1.schema.json` (new)
  - `packages/specs/docs/contracts/intake/intake_source_snapshot_v0_1.md` (new)
  - `tools/validate_intake_source_snapshot_v0_1.py` (new, stdlib-only)
  - `tools/fixtures/validators/intake_source_snapshot_v0_1_pass.json` (new)
  - `tools/fixtures/validators/intake_source_snapshot_v0_1_fail_path_traversal.json` (new)
  - `packages/specs/docs/planning/2026-02-09/m_intake_phase3_extract_stage_codex_roadmap.md` (status stamping)
- Fixtures to add:
  - PASS: `intake_source_snapshot_v0_1_pass.json`
  - FAIL: `intake_source_snapshot_v0_1_fail_path_traversal.json`
- Validator/gate wiring locations:
  - Initial validator in `tools/validate_intake_source_snapshot_v0_1.py`
  - planning-pack wiring deferred to PR4.
- Acceptance criteria:
  - Source snapshot schema is strict and fail-closed.
  - Validator rejects traversal/unsafe source path patterns deterministically.
- Proof commands:
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`

### PR4 — Gate Wiring + Canonical Contract Linking + Closeout Docs
- Effort: low
- Exact file list (`<=6`):
  - `tools/validate_planning_pack.py` (source snapshot PASS/FAIL gate + substring assertions)
  - `tools/fixtures/validators/scenario_schema_list.json` (register source snapshot schema)
  - `tools/fixtures/validators/intake_source_snapshot_v0_1_fail_missing_sha256.json` (new)
  - `packages/specs/docs/contracts/intake/intake_bundle_v0_1.md` (link extract/source snapshot contracts)
  - `packages/specs/docs/planning/2026-02-09/m_intake_phase3_extract_stage_milestone_report.md` (new closeout report)
  - `packages/specs/docs/planning/2026-02-09/m_intake_phase3_extract_stage_codex_roadmap.md` (final stamping)
- Fixtures to add:
  - PASS: reuse `intake_source_snapshot_v0_1_pass.json`
  - FAIL: `intake_source_snapshot_v0_1_fail_missing_sha256.json`
- Validator/gate wiring locations:
  - `tools/validate_planning_pack.py`
- Acceptance criteria:
  - planning-pack enforces both extract and source snapshot PASS/FAIL checks.
  - `intake_bundle_v0_1` contract links are coherent with stage boundary docs.
  - Closeout report captures proofs and residual risks.
- Proof commands:
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`

## 10) Definition of Done
- [ ] Extract-stage schema + contract exist and are strict.
- [ ] Source snapshot schema + contract exist and are strict.
- [ ] Extract validator mode is explicit and fail-closed.
- [ ] Source snapshot validator exists and is fail-closed.
- [ ] planning-pack gates both domains with PASS/FAIL fixtures and expected substrings.
- [ ] All PR slices are `<=6` files.
- [ ] All three allowed proof commands pass in every slice.
- [ ] Milestone report is completed with PR links, proof logs, and residual risks.

## 11) Stop / Rescope Conditions
- If proposed extract/source schema fields cannot be derived deterministically from export/file inputs, pause and lock contract semantics first.
- If fixture design requires broad fixture duplication that breaks `<=6` file slices, split into additional small PRs.
- If runtime requirements drift into OPA/PAR/LLM execution, split those into a separate milestone.
- If OSS integration pressure requires changing canonical AiGov artifact shapes, stop and escalate as architecture decision.

## 12) Execution Tracking
- PR1 (`pr1-mintake3-extract-schema`) — Status: Done
  - PR: `#168`
  - Proofs:
    - [x] `python3 tools/validate_planning_pack.py`
    - [x] `bash tools/run_pr_gate_validators.sh`
    - [x] `NX_DAEMON=false npx nx run evalsets:migration-smoke`
- PR2 (`pr2-mintake3-extract-gates`) — Status: Done
  - PR: TBD (push retry pending)
  - Proofs:
    - [x] `python3 tools/validate_planning_pack.py`
    - [x] `bash tools/run_pr_gate_validators.sh`
    - [x] `NX_DAEMON=false npx nx run evalsets:migration-smoke`
- PR3 (`pr3-mintake3-source-snapshot`) — Status: In progress
  - PR: TBD
  - Proofs:
    - [ ] `python3 tools/validate_planning_pack.py`
    - [ ] `bash tools/run_pr_gate_validators.sh`
    - [ ] `NX_DAEMON=false npx nx run evalsets:migration-smoke`
- PR4 (`pr4-mintake3-closeout`) — Status: Planned
  - PR: TBD
  - Proofs:
    - [ ] `python3 tools/validate_planning_pack.py`
    - [ ] `bash tools/run_pr_gate_validators.sh`
    - [ ] `NX_DAEMON=false npx nx run evalsets:migration-smoke`
