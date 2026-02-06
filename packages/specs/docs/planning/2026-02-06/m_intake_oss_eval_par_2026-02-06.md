# M_Intake OSS Eval — PAR DPIA (v2026-02-06)

## Task 3 — OSS candidate analysis: PAR DPIA (intake UX adapter)

### Objective
Treat PAR export as an input, map it to intake_bundle_v0_1, and flag EUPL constraints without implementing M_Intake.

### Inputs (code-grounded)
- Constitution: `packages/specs/docs/planning/2026-02-06/m_intake_constitution_2026-02-06.md`.
- Runbook: `packages/specs/docs/planning/2026-02-06/m_intake_codex_runbook_2026-02-06.md`.
- Codebase map: `packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md`.
- PAR OSS notes + license caution: `packages/specs/docs/artifacts/2026-02-05_OSS_EU_Opportunities.md`.

### Fit matrix status
- Fit matrix: Present — `packages/specs/docs/planning/2026-02-06/m_intake_monorepo_fit_matrix_2026-02-06.md`

### Outputs (artifacts + paths)
- `packages/specs/docs/planning/2026-02-06/m_intake_oss_eval_par_2026-02-06.md`

### Allowed commands
- Read-only enumeration only (no implementation).

### Stop conditions
- If PAR licensing scope or export schema cannot be verified, mark the integration plan as conditional and defer adoption until verified.

### Risks/notes
- PAR DPIA Form is EUPL-1.2; EUPL treats SaaS delivery as distribution, which can trigger source-sharing obligations if modified and offered as a service.

---

## License + isolation plan (EUPL)
- **License:** MinBZK PAR DPIA Form is **EUPL-1.2** (per OSS opportunities artifact).
- **Isolation plan (required by constitution):**
  - Treat PAR as **optional, external intake UI** that exports a JSON file.
  - Keep PAR code **out of** `packages/ep` and `packages/pe` (no code copy into core).
  - Use a **clean adapter boundary**: `par_export.json → intake_bundle_v0_1.json`.
  - If PAR is deployed in SaaS form, prefer **unmodified** deployment or publish modifications as required by EUPL; otherwise keep it as a **reference UI** and implement a native AiGov intake UI later.

---

## Concrete mapping plan: PAR export → AiGov artifacts (names only)
> Note: PAR export schema is not present in this repo. The field names below are placeholders aligned to common DPIA export sections; replace with exact PAR keys once the PAR JSON schema is ingested.

**Target AiGov artifacts (names only):**
- `intake_bundle_v0_1`
- `context_profile`
- `policy_profile`
- `target_profile`
- `evidence_index`
- `unknowns[]`
- `conflicts[]`
- `clarification_questions[]`

**Mapping plan (PAR export fields → AiGov artifact names):**
- `par.controller_identity` → `intake_bundle_v0_1` (organization metadata)
- `par.processing_purposes[]` → `policy_profile`
- `par.data_categories[]` → `intake_bundle_v0_1` (data inventory)
- `par.data_subjects[]` → `intake_bundle_v0_1`
- `par.processing_legal_basis[]` → `policy_profile`
- `par.retention_periods[]` → `policy_profile`
- `par.security_measures[]` → `policy_profile`
- `par.processors[]` → `target_profile`
- `par.transfers[]` → `context_profile`
- `par.risk_assessment[]` → `intake_bundle_v0_1` (risk section)
- `par.mitigation_measures[]` → `intake_bundle_v0_1`
- `par.dpia_outcome` → `intake_bundle_v0_1` (decision/summary)
- `par.evidence_attachments[]` → `evidence_index` + `evidence_refs`
- `par.unknowns[]` → `unknowns[]`
- `par.open_questions[]` → `clarification_questions[]`

**AiGov touchpoints (from codebase map; verify against fit matrix):**
- Contract + schema locations: `packages/specs/docs/contracts/`, `packages/specs/schemas/`.
- Runtime validation: `packages/ep/aigov_ep/` (intake validation + fail-closed checks).
- PE gates + fixtures: `packages/pe/tests/`, `tools/fixtures/validators/`.

---

## Determinism risks
- **Unordered collections:** PAR export arrays may be unordered; must be normalized (sorted) before producing AiGov artifacts.
- **Timestamp fields:** PAR exports may include creation timestamps; must be excluded from deterministic artifacts or recorded only in non-canonical logs.
- **Free-text variability:** narrative fields (risk/mitigation text) must be captured as evidence-backed strings with stable normalization rules (no auto-summarization in the adapter).
- **External references:** attachments/URLs must be content-addressed (hash) and stored in `evidence_index` to prevent nondeterministic links.

---

## Recommendation
**Defer** adoption as a runtime dependency; **adopt as a reference UX + optional adapter** once the intake_bundle_v0_1 contract and fixtures exist.
- Rationale: EUPL obligations + missing in-repo PAR schema mean integration should be gated by a documented adapter + eval-first fixtures.

---

## Summary
- PAR DPIA Form is EUPL-1.2 and should be isolated behind a JSON export adapter to protect AiGov’s core contracts.
- A mapping plan is defined from PAR export fields to AiGov artifact names, pending verification of the PAR schema.
- Determinism risks are identified and must be mitigated via normalization, hashing, and evidence indexing.

## Work performed
- Read constitution + runbook + codebase map to preserve determinism and fail-closed invariants.
- Reviewed OSS opportunities artifact for PAR licensing and integration cautions.
- Drafted a mapping plan and adapter boundary consistent with intake_bundle_v0_1.

## Findings
- PAR is best treated as an **optional intake UI** with a strict adapter boundary.
- Adoption should be deferred until the intake_bundle_v0_1 schema and fixtures exist and PAR export fields are verified.

## Checkpoint
- Files changed:
  - `packages/specs/docs/planning/2026-02-06/m_intake_oss_eval_par_2026-02-06.md`
- Commands run:
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_task_pack_2026-02-06.md`
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_constitution_2026-02-06.md`
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_codex_runbook_2026-02-06.md`
  - `sed -n '1,220p' packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md`
  - `rg -n "PAR" packages/specs/docs -S`
  - `rg -n "intake_bundle" packages/specs -S`
  - `sed -n '5410,5710p' packages/specs/docs/artifacts/2026-02-05_OSS_EU_Opportunities.md`
  - `find packages/specs/docs/planning -name "*fit_matrix*" -print`
- Results:
  - Fit matrix file present; mapping references both fit matrix and codebase map.
- Risks/unknowns:
  - PAR export schema not in repo; field mapping is placeholder pending schema verification.
- Next task:
  - Confirm fit-matrix touchpoints against PAR export schema once that schema is available.
  - Acquire a PAR export schema/sample and replace placeholder field names in the mapping.
