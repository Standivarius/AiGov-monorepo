# M_Intake Phase 4: Export Adapters + First Extract Run — Milestone Report

Date: 2026-02-09  
Milestone: M_Intake Phase 4 (export/file adapter to snapshot+extract, GDPR-only)

Status: In review (stack open, proofs passing).

## 1) Objective and Scope
- Objective: deliver a deterministic, fail-closed tools-only adapter that consumes local file exports and emits `intake_source_snapshot_v0_1` plus `intake_bundle_extract_v0_1`.
- Scope confirmation (GDPR-only): confirmed.
- Non-goals confirmation: no OPA runtime, no PAR runtime adapter, no LLM extraction, no live connectors.

## 2) Delivered Artifacts
- Export adapter contract delivered:
  - `packages/specs/docs/contracts/intake/intake_export_file_adapter_v0_1.md`
- Export adapter producer tool delivered:
  - `tools/run_intake_export_file_adapter_v0_1.py`
- Adapter determinism validator delivered:
  - `tools/validate_intake_export_file_adapter_v0_1.py`
- Snapshot + extract fixture/gate coverage delivered:
  - `tools/fixtures/exports/file_export_pass_minimal/context_profile.json`
  - `tools/fixtures/exports/file_export_fail_symlink/context_profile.json`
  - `tools/fixtures/exports/file_export_fail_empty_payload/context_profile.json`
  - `tools/fixtures/validators/intake_export_adapter_snapshot_pass.json`
  - `tools/fixtures/validators/intake_export_adapter_snapshot_fail_symlink.json`
  - `tools/fixtures/validators/intake_export_adapter_extract_pass.json`
  - `tools/fixtures/validators/intake_export_adapter_extract_fail_empty.json`
- Planning-pack wiring delivered:
  - `tools/validate_planning_pack.py`

## 3) PR Ledger (Stack Order)
- PR1 / `pr1-mintake4-contract`: contract + export fixtures seed (PR# TBD)
- PR2 / `pr2-mintake4-snapshot`: snapshot producer + determinism validator + gates (PR# TBD)
- PR3 / `pr3-mintake4-extract`: extract emission + extract gates (PR# TBD)
- PR4 / `pr4-mintake4-closeout`: contract linkage docs + roadmap/milestone closeout (PR# TBD)

## 4) Deterministic / Fail-Closed Invariants
- Source file inventory order: recursive lexical order (`dirnames.sort()`, `filenames.sort()`), then stable `source_path` sort.
- Snapshot provenance: each source file records `source_path` + `sha256`; `snapshot_id` derives from canonical inventory hash.
- Symlink/traversal fail-closed behavior: adapter rejects symlink entries and any path resolving outside export root.
- Extract ordering: `extracted_fields` sorted by `field_path`; `evidence_refs` sorted and unique.
- Snapshot->extract linkage: `extract.source_snapshot_id == snapshot.snapshot_id` enforced in adapter validator.
- Byte-identical determinism: snapshot/extract outputs are compared across repeated runs.

## 5) Fixture and Gate Coverage
- Export PASS fixture dir:
  - `tools/fixtures/exports/file_export_pass_minimal/`
- Export FAIL fixture dirs:
  - `tools/fixtures/exports/file_export_fail_symlink/` (symlink created in temp copy by validator)
  - `tools/fixtures/exports/file_export_fail_empty_payload/`
- Snapshot PASS/FAIL fixtures:
  - `tools/fixtures/validators/intake_export_adapter_snapshot_pass.json`
  - `tools/fixtures/validators/intake_export_adapter_snapshot_fail_symlink.json`
- Extract PASS/FAIL fixtures:
  - `tools/fixtures/validators/intake_export_adapter_extract_pass.json`
  - `tools/fixtures/validators/intake_export_adapter_extract_fail_empty.json`
- Expected substring assertions:
  - snapshot fail: `"symlink entry not allowed"`
  - extract fail: `"no extractable fields found in export payloads"`

## 6) Proofs (Allowed Commands Only)
- `python3 tools/validate_planning_pack.py`: PASS
- `bash tools/run_pr_gate_validators.sh`: PASS
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`: PASS
- Log paths:
  - `docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260209_203931.log`
  - `docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260209_204232.log`
  - `docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260209_204726.log`

## 7) Residual Risks
- Heuristic extraction mapping is intentionally minimal (`context_profile.*`, `policy_profile.retention_days`) for first-run determinism.
- Cross-artifact composition checks remain deferred to later milestones.
- `scenario_schema_list.json` may require merge reconciliation if parallel schema milestones land simultaneously.

## 8) OSS Stitching Note
- Adapter boundary used: local file-export ingestion under `tools/`.
- Confirmed: no live connector coupling introduced.
- Future expansion: additional export adapters remain isolated behind contract+validator boundaries.

## 9) Closure Checklist
- [x] Adapter emits valid snapshot and extract artifacts from export dir.
- [x] Determinism proven via repeated-run stable outputs.
- [x] Fail-closed behavior proven for symlink and empty-payload fixtures.
- [x] planning-pack PASS/FAIL gating is deterministic.
- [x] All slices respect `<=6 files/PR`.
- [x] Allowed proof commands pass on current top-of-stack implementation branch.
