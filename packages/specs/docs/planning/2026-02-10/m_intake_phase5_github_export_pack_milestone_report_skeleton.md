# M_Intake Phase 5: GitHub Export Pack v0.1 — Milestone Report (Skeleton)

Date: YYYY-MM-DD  
Milestone: M_Intake Phase 5 (GitHub export pack, file-based deterministic ingestion, GDPR-only)

## 1) Objective and Scope
- Objective:
- Scope confirmation (GDPR-only):
- Non-goals confirmation (no live connectors/auth, no OPA/PAR/LLM runtime):

## 2) Delivered Artifacts
- GitHub export pack contract delivered:
- Snapshot schema source_type expansion delivered:
- Adapter GitHub-pack runtime updates delivered:
- Adapter validator GitHub-pass/fail coverage delivered:
- Planning-pack wiring for GitHub pass/fail fixtures delivered:

## 3) PR Ledger (Merged Order)
- PR# / branch:
- Title:
- Files changed:
- Merge commit:

## 4) Deterministic / Fail-Closed Invariants
- GitHub pack layout contract:
- Directory/file ordering rule:
- Snapshot provenance rule (`snapshot_id`, `source_path`, `sha256`, `source_type`):
- Unsupported extension fail rule:
- Malformed recognized JSON shape fail rule:
- Extract ordering and linkage rule (`field_path`, `evidence_refs`, `source_snapshot_id`):

## 5) Fixture and Gate Coverage
- PASS export fixture dir(s):
- FAIL export fixture dir(s):
- Snapshot pass/fail fixtures:
- Extract pass/fail fixtures:
- Expected substring assertions:

## 6) Proofs (Allowed Commands Only)
- `python3 tools/validate_planning_pack.py`:
- `bash tools/run_pr_gate_validators.sh`:
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`:
- Log paths:

## 7) Review Loop Results (Claude)
- Iterations run:
- Final counts:
  - MUST:
  - SHOULD:
  - COULD:
- Any fixed findings:
- Deferred non-blocking findings:

## 8) Residual Risks
- Risk:
- Why acceptable now:
- Follow-up milestone/action:

## 9) OSS Stitching Note
- Adapter boundary used:
- Confirmation no live GitHub connector/auth coupling introduced:
- Future connector expansion boundary:

## 10) Closure Checklist
- [ ] GitHub export pack contract is implemented and enforced.
- [ ] Adapter emits deterministic snapshot/extract from GitHub pack fixture.
- [ ] Unsupported file type and malformed-shape fail fixtures are enforced.
- [ ] planning-pack pass/fail checks are deterministic and stable.
- [ ] All slices stayed `<=6 files/PR`.
- [ ] All allowed proof commands pass on final stack head.
