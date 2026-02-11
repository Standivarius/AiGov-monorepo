# M_Intake Phase 6: Jira Export Pack v0.1 (File-Based, Deterministic) — Codex Roadmap

Date: 2026-02-10  
Status: Proposed (planning-only)  
Overall Effort: high

## 1) Why This Milestone Now
Phase 5 established the reusable pattern for deterministic pack ingestion (`source_type`, strict layout checks, pass/fail fixture wiring, and adapter determinism assertions). The next highest-value step is a Jira-focused file-export profile that broadens GDPR intake coverage while preserving fail-closed behavior and tools-only boundaries.

## 2) Verified Repo Truth (Research)
- Adapter runtime and determinism validator already exist and are reusable:
  - `tools/run_intake_export_file_adapter_v0_1.py`
  - `tools/validate_intake_export_file_adapter_v0_1.py`
- Snapshot/extract schemas already enforce strict shape and deterministic constraints:
  - `packages/specs/schemas/intake_source_snapshot_v0_1.schema.json`
  - `packages/specs/schemas/intake_bundle_extract_v0_1.schema.json`
- Current branch already contains `github_export_pack` support; however `origin/main` still has `source_type` enum limited to `file_export`.
  - Dependency risk: Phase 6 must either stack after Phase 5 merge or include merge-safe enum update that preserves both `github_export_pack` and `jira_export_pack`.
- Phase 5 established fixture/gate pattern to reuse:
  - pass fixture dir under `tools/fixtures/exports/*_pass_minimal/`
  - fail fixture metadata under `tools/fixtures/validators/intake_export_adapter_*_fail_*.json`
  - planning-pack constants + pass/fail call blocks in `tools/validate_planning_pack.py`

## 3) Milestone Objective
Define and support deterministic `jira_export_pack_v0_1` ingestion in the existing tools adapter so it can emit:
- `intake_source_snapshot_v0_1` with `source_type="jira_export_pack"`
- `intake_bundle_extract_v0_1` with deterministic ordering and stable `evidence_refs`

### Jira pack layout v0.1 (locked)
Top-level directories must be exactly:
- `jira_meta/`
- `jira_projects/`
- `jira_issues/`

Required files:
- `jira_meta/metadata.json`
- `jira_projects/projects.json`
- `jira_issues/issues.json`

Design intent: use 3 JSON files total for minimal fixture size and PR-size control.

## 4) Non-Goals
- No live Jira connector/authentication.
- No EP runtime integration.
- No OPA execution.
- No PAR runtime adapter.
- No LLM extraction/council behavior.
- No non-GDPR scope expansion.

## 5) Guardrails
- Contract-first + fail-closed + deterministic.
- Reuse existing adapter namespace and validator surfaces; no parallel runtime path.
- Stdlib-only in tools validators where possible.
- No committed symlinks in fixtures; symlink fail tests use temp symlink generation in validator.
- PR hygiene: `<=6 files changed per PR`.
- Allowed proof commands per PR slice:
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`

## 6) Deterministic Decisions (Locked for v0.1)
- Canonical JSON serialization remains:
  - `json.dumps(..., sort_keys=True, separators=(",", ":"), ensure_ascii=False)` + trailing newline.
- Traversal order remains lexical for dirs/files.
- For recognized Jira pack paths, no silent skipping:
  - unexpected top-level entries => hard error
  - non-`.json` in recognized directories => hard error
  - malformed JSON => hard error
  - wrong top-level JSON shape => hard error
- Extract ordering rules unchanged:
  - `extracted_fields` sorted by `field_path`
  - `evidence_refs` sorted and unique
  - conflicting values for same `field_path` => hard error

## 7) PR Slices (Execution Plan)

### PR1 — Jira Contract + Snapshot Enum Expansion + Pass Fixture Seed
Effort: medium

Exact file list (`<=6`):
1. `packages/specs/docs/contracts/intake/intake_jira_export_pack_v0_1.md` (new)
2. `packages/specs/schemas/intake_source_snapshot_v0_1.schema.json` (update enum to include `jira_export_pack`; preserve `github_export_pack` if present)
3. `tools/fixtures/exports/jira_export_pack_pass_minimal/jira_meta/metadata.json` (new)
4. `tools/fixtures/exports/jira_export_pack_pass_minimal/jira_projects/projects.json` (new)
5. `tools/fixtures/exports/jira_export_pack_pass_minimal/jira_issues/issues.json` (new)
6. `packages/specs/docs/planning/2026-02-10/m_intake_phase6_jira_export_pack_codex_roadmap.md` (status stamp after execution starts)

PASS + FAIL fixtures:
- PASS: `tools/fixtures/exports/jira_export_pack_pass_minimal/`
- FAIL (baseline reuse): existing symlink fail fixture metadata path for adapter safety regression check

Gates touched:
- None in this slice (contract/schema/fixture seed only).

Acceptance criteria:
- Jira pack v0.1 layout contract is explicit.
- Snapshot schema supports `jira_export_pack` without dropping existing source types.
- Pass fixture includes exactly three deterministic JSON files in required locations.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

---

### PR2 — Jira Snapshot Adapter + Unsupported-Extension Fail Gate
Effort: high

Exact file list (`<=6`):
1. `tools/run_intake_export_file_adapter_v0_1.py` (update: Jira pack detect + snapshot validation)
2. `tools/validate_intake_export_file_adapter_v0_1.py` (update: Jira snapshot pass/fail helper)
3. `tools/fixtures/exports/jira_export_pack_fail_unsupported_ext/jira_meta/metadata.yaml` (new fail fixture directory/file)
4. `tools/fixtures/validators/intake_export_adapter_snapshot_pass_jira_pack.json` (new)
5. `tools/fixtures/validators/intake_export_adapter_snapshot_fail_jira_unsupported_ext.json` (new)
6. `tools/validate_planning_pack.py` (wire Jira snapshot pass/fail checks)

PASS + FAIL fixtures:
- PASS: `intake_export_adapter_snapshot_pass_jira_pack.json`
- FAIL: `intake_export_adapter_snapshot_fail_jira_unsupported_ext.json`

Gates touched:
- `tools/validate_intake_export_file_adapter_v0_1.py`
- `tools/validate_planning_pack.py`

Acceptance criteria:
- Adapter emits deterministic snapshot with `source_type="jira_export_pack"`.
- Unsupported extension in recognized Jira path fails with stable expected substring.
- Existing `file_export` and `github_export_pack` snapshot checks remain green.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

---

### PR3 — Jira Extract Heuristics + Bad-Shape Fail Gate
Effort: high

Exact file list (`<=6`):
1. `tools/run_intake_export_file_adapter_v0_1.py` (update: Jira extract heuristics)
2. `tools/validate_intake_export_file_adapter_v0_1.py` (update: Jira extract pass/fail helper)
3. `tools/fixtures/exports/jira_export_pack_fail_bad_shape/jira_issues/issues.json` (new fail fixture directory/file)
4. `tools/fixtures/validators/intake_export_adapter_extract_pass_jira_pack.json` (new)
5. `tools/fixtures/validators/intake_export_adapter_extract_fail_jira_bad_shape.json` (new)
6. `tools/validate_planning_pack.py` (wire Jira extract pass/fail checks)

PASS + FAIL fixtures:
- PASS: `intake_export_adapter_extract_pass_jira_pack.json`
- FAIL: `intake_export_adapter_extract_fail_jira_bad_shape.json`

Gates touched:
- `tools/validate_intake_export_file_adapter_v0_1.py`
- `tools/validate_planning_pack.py`

Acceptance criteria:
- Extract output is byte-stable across repeated runs.
- Extract output is sorted deterministically by `field_path` with stable `evidence_refs`.
- Wrong JSON shape in recognized Jira pack file fails closed with deterministic substring.
- `source_snapshot_id == snapshot_id` linkage is enforced.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

---

### PR4 — Contract Linkage + Milestone Closeout
Effort: medium

Exact file list (`<=6`):
1. `packages/specs/docs/contracts/intake/intake_export_file_adapter_v0_1.md` (update: Jira mode details)
2. `packages/specs/docs/contracts/intake/intake_source_snapshot_v0_1.md` (update: `jira_export_pack` semantics)
3. `packages/specs/docs/contracts/intake/intake_bundle_extract_v0_1.md` (update: Jira-derived extraction semantics)
4. `packages/specs/docs/contracts/intake/intake_bundle_stage_artifacts_v0_1.md` (update: adapter boundary note for Jira)
5. `packages/specs/docs/planning/2026-02-10/m_intake_phase6_jira_export_pack_milestone_report.md` (new closeout report)
6. `packages/specs/docs/planning/2026-02-10/m_intake_phase6_jira_export_pack_codex_roadmap.md` (status/proof stamping)

PASS + FAIL fixtures:
- PASS: reuse Jira snapshot/extract pass fixtures from PR2/PR3.
- FAIL: reuse Jira unsupported-ext and bad-shape fixtures from PR2/PR3.

Gates touched:
- No new runtime gating in this slice (docs and closeout only).

Acceptance criteria:
- Contract docs reflect delivered Jira fail-closed and deterministic behavior.
- Roadmap/milestone report include PR links, proof logs, and residual risks.
- No runtime behavior drift in closeout slice.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

## 8) Definition of Done
- [ ] Jira pack v0.1 contract exists and is deterministic.
- [ ] Snapshot schema supports `jira_export_pack` (without regressing existing source types).
- [ ] Adapter rejects unsupported Jira pack paths/extensions/shapes with explicit deterministic errors.
- [ ] Jira snapshot and extract pass fixtures are wired and deterministic.
- [ ] Jira fail fixtures (unsupported extension + bad shape) are wired with expected substrings.
- [ ] Every PR slice stays `<=6 files` and all allowed proof commands pass.

## 9) Stop / Rescope Conditions
- If Jira export variability requires live API/auth behavior, stop and split to a separate connector milestone.
- If deterministic extraction cannot remain heuristic/fixture-gated without NLP/LLM inference, stop and split extraction expansion.
- If merge conflicts with Phase 5 make schema enum preservation ambiguous, stop and stack after final Phase 5 merge.

## 10) Blockers
- No hard blockers.
- Dependency/risk note: `origin/main` currently does not include `github_export_pack`; Phase 6 must preserve both enum values when merged.
