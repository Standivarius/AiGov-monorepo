# M_Intake Phase 4: Export Adapters + First Extract Run — Milestone Report (Skeleton)

Date: YYYY-MM-DD  
Milestone: M_Intake Phase 4 (export/file adapter to snapshot+extract, GDPR-only)

## 1) Objective and Scope
- Objective:
- Scope confirmation (GDPR-only):
- Non-goals confirmation (OPA/PAR/LLM/live connectors out of scope):

## 2) Delivered Artifacts
- Export adapter contract delivered:
- Export adapter producer tool delivered:
- Adapter determinism validator delivered:
- Snapshot + extract fixture/gate coverage delivered:
- Planning-pack wiring delivered:

## 3) PR Ledger (Merged Order)
- PR# / branch:
- Title:
- Files changed:
- Merge commit:

## 4) Deterministic/Fall-Closed Invariants
- Source file inventory order rule:
- Snapshot provenance rule (`snapshot_id`, `source_path`, `sha256`):
- Symlink/traversal fail-closed behavior:
- Extract ordering rule (`field_path`, `evidence_refs`):
- Snapshot->extract linkage rule (`source_snapshot_id`):

## 5) Fixture and Gate Coverage
- Export PASS fixture dir(s):
- Export FAIL fixture dir(s):
- Snapshot PASS/FAIL validator fixtures:
- Extract PASS/FAIL validator fixtures:
- Expected substring assertions:

## 6) Proofs (Allowed Commands Only)
- `python3 tools/validate_planning_pack.py`:
- `bash tools/run_pr_gate_validators.sh`:
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`:
- Log paths:

## 7) Residual Risks
- Risk:
- Why acceptable now:
- Follow-up milestone/action:

## 8) OSS Stitching Note
- Adapter boundary used:
- Confirm no live connector coupling introduced:
- Future adapter expansion boundary:

## 9) Closure Checklist
- [ ] Adapter emits valid snapshot and extract artifacts from export dir.
- [ ] Determinism proven via repeated-run stable outputs.
- [ ] Fail-closed behavior proven for symlink/traversal/invalid payload fixtures.
- [ ] planning-pack PASS/FAIL gating is deterministic.
- [ ] All slices respected `<=6 files/PR`.
- [ ] All allowed proof commands pass on final head.

