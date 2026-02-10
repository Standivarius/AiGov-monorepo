# M_Intake Phase 6: Jira Export Pack v0.1 — Milestone Report (Skeleton)

Date: YYYY-MM-DD  
Milestone: M_Intake Phase 6 (Jira export pack, file-based deterministic ingestion, GDPR-only)

## 1) Objective and Scope
- Objective:
- Scope confirmation (GDPR-only):
- Non-goals confirmation (no live Jira connector/auth, no EP runtime integration, no OPA/PAR/LLM runtime):

## 2) Delivered Artifacts
- Jira export pack contract delivered:
- Snapshot schema `source_type` expansion delivered:
- Adapter Jira-pack runtime updates delivered:
- Adapter validator Jira pass/fail coverage delivered:
- Planning-pack wiring for Jira pass/fail fixtures delivered:

## 3) PR Ledger (Merged Order)
- PR# / branch:
- Title:
- Files changed:
- Merge commit:

## 4) Deterministic / Fail-Closed Invariants
- Jira pack layout contract (allowed top-level dirs and required files):
- Directory/file ordering rule:
- Snapshot provenance rule (`snapshot_id`, `source_path`, `sha256`, `source_type`, `content_type`):
- Unsupported extension fail rule:
- Malformed/wrong-shape JSON fail rule:
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
- Fixed findings:
- Deferred non-blocking findings:

## 8) Residual Risks
- Risk:
- Why acceptable now:
- Follow-up milestone/action:

## 9) OSS Stitching Note
- Adapter boundary used:
- Confirmation no live Jira connector/auth coupling introduced:
- Future connector expansion boundary:

## 10) Closure Checklist
- [ ] Jira export pack contract is implemented and enforced.
- [ ] Adapter emits deterministic snapshot/extract from Jira pass fixture.
- [ ] Unsupported extension and bad-shape fail fixtures are enforced.
- [ ] Planning-pack pass/fail checks are deterministic and stable.
- [ ] All slices stayed `<=6 files/PR`.
- [ ] All allowed proof commands pass on final stack head.
