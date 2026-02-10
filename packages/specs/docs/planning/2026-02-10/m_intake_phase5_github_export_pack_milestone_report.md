# M_Intake Phase 5: GitHub Export Pack v0.1 — Milestone Report

Date: 2026-02-10  
Milestone: M_Intake Phase 5 (GitHub export pack, file-based deterministic ingestion, GDPR-only)  
Status: In progress (stack split pending)

## 1) Objective and Scope
- Objective: extend tools-only deterministic intake export adapter coverage to a strict `github_export_pack` layout and deterministic extract heuristics.
- Scope confirmation (GDPR-only): maintained.
- Non-goals confirmation: no live connector/auth, no OPA/PAR runtime execution, no LLM extraction.

## 2) Delivered Artifacts (Current Progress)
- GitHub export pack contract delivered:
  - `packages/specs/docs/contracts/intake/intake_github_export_pack_v0_1.md`
- Snapshot schema source_type expansion delivered:
  - `packages/specs/schemas/intake_source_snapshot_v0_1.schema.json` includes `github_export_pack`
- Adapter GitHub-pack runtime updates delivered:
  - `tools/run_intake_export_file_adapter_v0_1.py`
- Adapter validator GitHub pass/fail coverage delivered:
  - `tools/validate_intake_export_file_adapter_v0_1.py`
- Planning-pack wiring for GitHub pass/fail fixtures delivered:
  - `tools/validate_planning_pack.py`
- Contract linkage updates in progress:
  - `intake_export_file_adapter_v0_1.md`
  - `intake_source_snapshot_v0_1.md`
  - `intake_bundle_extract_v0_1.md`
  - `intake_bundle_stage_artifacts_v0_1.md`

## 3) PR Ledger (Planned Stack)
- PR1 / `pr1-mintake5-contract`: contract + schema enum + GitHub pass fixture seed (`42c1a10`)
- PR2 / `pr2-mintake5-snapshot`: snapshot runtime/validator/gates (`5469cd9`)
- PR3 / `pr3-mintake5-extract`: extract runtime/validator/gates (`b7574eb`)
- PR4 / `pr4-mintake5-closeout`: contract linkage + roadmap/report closeout (current slice)

## 4) Deterministic / Fail-Closed Invariants
- GitHub pack layout: root entries must be exactly `repo/`, `issues/`, `pull_requests/`, `comments/`.
- Directory/file ordering: lexical traversal and lexical file ordering.
- Snapshot provenance: each source file carries deterministic `source_path` + `sha256`; `snapshot_id` is content-addressed from canonical inventory.
- Unsupported extension fail rule: recognized GitHub pack folders reject non-JSON files.
- Malformed recognized JSON shape fail rule: recognized GitHub pack files must parse and be JSON objects.
- Extract ordering/linkage: `extracted_fields` sorted; `evidence_refs` sorted unique; `source_snapshot_id == snapshot_id`.

## 5) Fixture and Gate Coverage
- PASS export fixture dir:
  - `tools/fixtures/exports/github_export_pack_pass_minimal/`
- FAIL export fixture dirs:
  - `tools/fixtures/exports/github_export_pack_fail_bad_shape/` (shape fail)
- Snapshot gate fixtures:
  - pass: `tools/fixtures/validators/intake_export_adapter_snapshot_pass_github_pack.json`
  - fail: `tools/fixtures/validators/intake_export_adapter_snapshot_fail_github_unsupported_ext.json`
- Extract gate fixtures:
  - pass: `tools/fixtures/validators/intake_export_adapter_extract_pass_github_pack.json`
  - fail: `tools/fixtures/validators/intake_export_adapter_extract_fail_github_bad_shape.json`

## 6) Proofs (Allowed Commands Only)
- `python3 tools/validate_planning_pack.py`: PASS on integration after PR1/PR2/PR3
- `bash tools/run_pr_gate_validators.sh`: PASS on integration after PR1/PR2/PR3
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`: PASS on integration after PR1/PR2/PR3
- smoke logs:
  - `docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260210_074115.log`
  - `docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260210_074337.log`
  - `docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260210_074620.log`

## 7) Review Loop Results (Claude)
- Pending after stacked PRs are opened.

## 8) Residual Risks (Current)
- Merge-order conflict risk on shared planning-pack fixture wiring blocks.
- Potential merge conflict risk on shared validator fixture registries across concurrent milestones.

## 9) OSS Stitching Note
- Adapter boundary remains tools-only and file-based.
- No live GitHub API coupling/auth introduced.
- Future connector work remains explicitly out of scope for v0.1.

## 10) Closure Checklist
- [ ] Stacked PRs opened and each `<=6` files.
- [ ] Proof commands pass per PR branch.
- [ ] Claude architecture + adversarial loops converge to MUST=0/SHOULD=0.
- [ ] Final PR links and residual risks stamped.
