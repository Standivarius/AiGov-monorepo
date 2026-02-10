# M_Intake Phase 5: GitHub Export Pack v0.1 (File-Based, Deterministic) — Codex Roadmap

Date: 2026-02-10  
Status: In progress (execution in-flight on integration branch)  
Overall Effort: high

## 1) Why This Milestone Now
Phase 4 delivered a deterministic, fail-closed file export adapter (`file_export`) that emits `intake_source_snapshot_v0_1` and `intake_bundle_extract_v0_1`. The next highest-leverage step is a deterministic **GitHub export pack** format and extraction profile that broadens evidence capture while keeping ingestion tools-only, offline, and fixture-gated.

## 2) Verified Repo Truth (Research)
- Adapter runtime and determinism hooks already exist:
  - `tools/run_intake_export_file_adapter_v0_1.py`
  - `tools/validate_intake_export_file_adapter_v0_1.py`
- Shared strict schema helper exists and already enforces `additionalProperties` and `uniqueItems`:
  - `tools/_schema_helpers.py`
- Snapshot schema currently constrains `source_type` to only `"file_export"`:
  - `packages/specs/schemas/intake_source_snapshot_v0_1.schema.json`
- Extract validation and existing extract fixture patterns are already in place:
  - `tools/validate_intake_bundle_extract_v0_1.py`
  - `tools/fixtures/validators/intake_bundle_extract_*`
- Planning-pack already has adapter pass/fail wiring blocks to extend:
  - `tools/validate_planning_pack.py`
- Reusable deterministic exporter pattern exists:
  - `tools/export_bundle_to_petri_seed_instructions_alpha.py`
  - `tools/validate_export_bundle_to_petri_seed_instructions_alpha.py`

## 3) Milestone Objective
Define and support a deterministic `github_export_pack_v0_1` directory layout that the existing file adapter can consume to emit:
- `intake_source_snapshot_v0_1` (with deterministic provenance and strict fail-closed behavior)
- `intake_bundle_extract_v0_1` (expanded GDPR-relevant evidence candidates, deterministic ordering)

Target pack layout (v0.1):
- `repo/metadata.json`
- `issues/*.json`
- `pull_requests/*.json`
- `comments/*.json`

Fail-closed rule for this milestone:
- Unsupported file types/shapes in the GitHub pack must raise explicit errors (no silent skip for those pack paths).

## 4) Non-Goals
- No live GitHub connector/authentication.
- No OPA runtime execution.
- No PAR runtime adapter.
- No LLM extraction/council.
- No non-GDPR scope expansion.

## 5) Guardrails
- Contract-first + fail-closed.
- Deterministic ordering and stable error strings.
- Stdlib-only in tools where possible.
- Tools-only ingestion boundary (offline exported files only).
- PR hygiene: `<=6 files changed per PR`.
- Allowed proof commands for every PR slice:
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`

## 6) Deterministic Decisions (Locked for v0.1)
- Reuse `tools/run_intake_export_file_adapter_v0_1.py`; do not create a second adapter namespace.
- Add a new `source_type` enum value for snapshot artifacts:
  - `github_export_pack`
- Deterministic path traversal and inventory ordering stay unchanged:
  - sorted dirs/files, POSIX relative paths, symlink reject, root escape reject
- GitHub pack parsing is explicit and fail-closed:
  - only `.json` files under recognized pack folders are allowed
  - malformed JSON or wrong top-level shape in recognized files is a hard error
  - unknown file extension in recognized folders is a hard error
- Extraction ordering rules remain unchanged:
  - `extracted_fields` sorted by `field_path`
  - `evidence_refs` sorted; uniqueness via schema-level `uniqueItems`

## 7) PR Slices (Execution Plan)

### PR1 — Contract + Snapshot Source-Type Expansion + GitHub Pack Seed Fixture
Effort: medium

Exact file list (`<=6`):
1. `packages/specs/docs/contracts/intake/intake_github_export_pack_v0_1.md` (new)
2. `packages/specs/schemas/intake_source_snapshot_v0_1.schema.json` (update: allow `github_export_pack`)
3. `tools/fixtures/exports/github_export_pack_pass_minimal/repo/metadata.json` (new)
4. `tools/fixtures/exports/github_export_pack_pass_minimal/issues/ISSUE-001.json` (new)
5. `tools/fixtures/exports/github_export_pack_pass_minimal/pull_requests/PR-001.json` (new)
6. `tools/fixtures/exports/github_export_pack_pass_minimal/comments/COMMENT-001.json` (new)

PASS + FAIL fixtures:
- PASS: `tools/fixtures/exports/github_export_pack_pass_minimal/`
- FAIL (reuse in this slice): `tools/fixtures/exports/file_export_fail_symlink/` for fail-closed baseline

Gate wiring locations:
- None in this slice (contract/schema/fixture seed only).

Acceptance criteria:
- GitHub pack v0.1 layout contract is explicit and deterministic.
- Snapshot schema accepts `source_type == "github_export_pack"` without breaking existing `file_export`.
- Seed fixture includes all required layout sections: repo/issues/pull_requests/comments.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

---

### PR2 — Snapshot Adapter Support for GitHub Pack + Unsupported-File Fail Gate
Effort: high

Exact file list (`<=6`):
1. `tools/run_intake_export_file_adapter_v0_1.py` (update: recognize GitHub pack profile + explicit unsupported-type errors)
2. `tools/validate_intake_export_file_adapter_v0_1.py` (update: GitHub-pack snapshot pass/fail checks)
3. `tools/fixtures/exports/github_export_pack_fail_unsupported_ext/repo/metadata.yaml` (new fail fixture)
4. `tools/fixtures/validators/intake_export_adapter_snapshot_pass_github_pack.json` (new pass fixture)
5. `tools/fixtures/validators/intake_export_adapter_snapshot_fail_github_unsupported_ext.json` (new fail fixture metadata)
6. `tools/validate_planning_pack.py` (wire snapshot GitHub pass/fail assertions)

PASS + FAIL fixtures:
- PASS: `intake_export_adapter_snapshot_pass_github_pack.json` against `github_export_pack_pass_minimal`
- FAIL: `intake_export_adapter_snapshot_fail_github_unsupported_ext.json`

Gate wiring locations:
- `tools/validate_intake_export_file_adapter_v0_1.py`
- `tools/validate_planning_pack.py`

Acceptance criteria:
- Adapter emits deterministic snapshot for GitHub pass fixture with `source_type="github_export_pack"`.
- Unsupported extension in recognized GitHub pack path fails with deterministic expected substring.
- Existing file_export snapshot checks remain green.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

---

### PR3 — GitHub Pack Extract Heuristics + Malformed-Shape Fail Gate
Effort: high

Exact file list (`<=6`):
1. `tools/run_intake_export_file_adapter_v0_1.py` (update: deterministic GitHub extract candidates)
2. `tools/validate_intake_export_file_adapter_v0_1.py` (update: extract pass/fail checks for GitHub pack)
3. `tools/fixtures/exports/github_export_pack_fail_bad_shape/issues/ISSUE-001.json` (new fail fixture)
4. `tools/fixtures/validators/intake_export_adapter_extract_pass_github_pack.json` (new pass fixture)
5. `tools/fixtures/validators/intake_export_adapter_extract_fail_github_bad_shape.json` (new fail fixture metadata)
6. `tools/validate_planning_pack.py` (wire extract GitHub pass/fail assertions)

PASS + FAIL fixtures:
- PASS: `intake_export_adapter_extract_pass_github_pack.json`
- FAIL: `intake_export_adapter_extract_fail_github_bad_shape.json`

Gate wiring locations:
- `tools/validate_intake_export_file_adapter_v0_1.py`
- `tools/validate_planning_pack.py`

Acceptance criteria:
- Extract output is deterministic and byte-stable across repeated runs.
- Extract includes deterministic evidence candidates derived from repo/issues/prs/comments pack inputs.
- Malformed recognized JSON shape fails closed with deterministic expected substring.
- `source_snapshot_id == snapshot_id` linkage preserved.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

---

### PR4 — Contract Linkage + Roadmap/Milestone Closeout
Effort: medium

Exact file list (`<=6`):
1. `packages/specs/docs/contracts/intake/intake_export_file_adapter_v0_1.md` (update: GitHub pack mode details)
2. `packages/specs/docs/contracts/intake/intake_source_snapshot_v0_1.md` (update: `github_export_pack` provenance semantics)
3. `packages/specs/docs/contracts/intake/intake_bundle_extract_v0_1.md` (update: GitHub-derived extraction semantics)
4. `packages/specs/docs/contracts/intake/intake_bundle_stage_artifacts_v0_1.md` (update: enforced vs deferred boundary for GitHub pack)
5. `packages/specs/docs/planning/2026-02-10/m_intake_phase5_github_export_pack_milestone_report.md` (new closeout report)
6. `packages/specs/docs/planning/2026-02-10/m_intake_phase5_github_export_pack_codex_roadmap.md` (status/proof stamping)

PASS + FAIL fixtures:
- PASS: reuse GitHub snapshot/extract pass fixtures from PR2/PR3
- FAIL: reuse unsupported-ext and bad-shape fail fixtures from PR2/PR3

Gate wiring locations:
- No new runtime wiring (docs + planning closeout only).

Acceptance criteria:
- Contracts match delivered behavior and explicitly describe fail-closed policy.
- Roadmap/milestone report includes PR links, proof evidence, residual risks.
- All Phase 5 checks remain deterministic and green.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

## 8) Definition of Done
- [ ] GitHub export pack v0.1 layout contract exists and is deterministic.
- [ ] Snapshot schema supports both `file_export` and `github_export_pack`.
- [ ] Adapter rejects unsupported GitHub pack file types/shapes with explicit errors.
- [ ] Deterministic snapshot and extract pass fixtures for GitHub pack are gated in planning-pack.
- [ ] Deterministic fail fixtures for unsupported extension and malformed JSON shape are gated with expected substrings.
- [ ] Snapshot/extract linkage and repeated-run byte equality are preserved.
- [ ] Every PR slice stays `<=6 files` and uses only allowed proof commands.

## 9) Stop / Rescope Conditions
- If GitHub pack export variability requires connector/auth logic, stop and split to a new milestone.
- If robust candidate extraction requires probabilistic NLP/LLM interpretation, stop and split extraction expansion to later milestone.
- If deterministic gating cannot stay within `<=6 files/PR`, split further instead of widening slices.

## 10) Blockers
- No blockers identified for planning.

## 11) Execution Tracking (In Progress)
### Slice Status
| Slice | Title | Branch (planned) | Status |
| --- | --- | --- | --- |
| PR1 | Contract + snapshot source-type + GitHub pack seed | `pr1-mintake5-contract` | Done on integration commit `42c1a10` |
| PR2 | Snapshot adapter support + unsupported-extension gate | `pr2-mintake5-snapshot` | Done on integration commit `5469cd9` |
| PR3 | GitHub extract heuristics + bad-shape gate | `pr3-mintake5-extract` | Done on integration commit `b7574eb` |
| PR4 | Contract linkage + closeout docs | `pr4-mintake5-closeout` | In progress |

### Proof Log Stamps
- PR1 local proof run:
  - `python3 tools/validate_planning_pack.py` PASS
  - `bash tools/run_pr_gate_validators.sh` PASS
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke` PASS
  - log: `docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260210_074115.log`
- PR2 local proof run:
  - `python3 tools/validate_planning_pack.py` PASS
  - `bash tools/run_pr_gate_validators.sh` PASS
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke` PASS
  - log: `docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260210_074337.log`
- PR3 local proof run:
  - `python3 tools/validate_planning_pack.py` PASS
  - `bash tools/run_pr_gate_validators.sh` PASS
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke` PASS
  - log: `docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260210_074620.log`
