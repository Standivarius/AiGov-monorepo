# M_Intake Architecture Plan (v2026-02-06)

## Objective
Define the M_Intake architecture (ingest → extract → reconcile → gap → readiness gate) with deterministic, fail-closed contracts and OSS adapter boundaries only. No implementation.

## Inputs (code-grounded)
- Constitution: `packages/specs/docs/planning/2026-02-06/m_intake_constitution_2026-02-06.md`.
- Runbook: `packages/specs/docs/planning/2026-02-06/m_intake_codex_runbook_2026-02-06.md`.
- Codebase map: `packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md`.
- Task pack: `packages/specs/docs/planning/2026-02-06/m_intake_task_pack_2026-02-06.md`.
- OPA eval: `packages/specs/docs/planning/2026-02-06/m_intake_oss_eval_opa_2026-02-06.md`.
- PAR eval: `packages/specs/docs/planning/2026-02-06/m_intake_oss_eval_par_2026-02-06.md`.
- CNIL patterns (missing): `UNCONFIRMED PATH` (file not found; verify when available).
- Intake + taxonomy anchors:
  - `packages/specs/schemas/client_intake_v0_2.schema.json`
  - `packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md`
  - `packages/specs/docs/contracts/taxonomy/evidence_schema.md`
  - `tools/fixtures/validators/intake_output_context_fail_locale_context_null.json`

## Fit matrix status
- **Missing**: `packages/specs/docs/planning/2026-02-06/m_intake_monorepo_fit_matrix_2026-02-06.md` was not present in the repo at the provided path. Touchpoints below are grounded in the codebase map and must be verified against the fit matrix once available.

---

## 1) Canonical module boundary (M_Intake output)
- **Canonical output artifact:** `intake_bundle_v0_1` (schema + contract to be defined under `packages/specs/schemas/` and `packages/specs/docs/contracts/`).
- **Evidence Model B:** global `evidence_index` with field → `evidence_refs` pointers (per constitution).
- **M_Intake scope:** produce a deterministic, schema-valid intake bundle that downstream EP runtime validation (`packages/ep/aigov_ep/`) and PE gates (`packages/pe/tests/`, `tools/fixtures/validators/`) can consume.

---

## 2) Pipeline architecture (ingest → extract → reconcile → gap → readiness gate)

### 2.1 Ingest (input capture)
- **Inputs:** PAR export JSON, internal form JSON, or manual fixtures.
- **Outputs:** `intake_bundle_draft_i` (draft artifacts, not canonical).
- **Determinism rule:** drafts are treated as evidence sources only; no nondeterministic fields in canonical output.

### 2.2 Extract (structure + evidence)
- **Purpose:** convert inputs into structured fields + attach evidence refs.
- **Evidence discipline:** every non-trivial claim must map to `evidence_index` entries; unknowns are explicit.

### 2.3 Reconcile (conflict resolution)
- **Inputs:** multiple drafts.
- **Outputs:** `intake_bundle_candidate` + `conflicts[]` + `unknowns[]`.
- **Determinism rule:** conflict ordering is stable and reproducible (sorted by field path).

### 2.4 Gap analysis (clarification)
- **Outputs:** `clarification_questions[]` in deterministic order.
- **Fail-closed:** readiness gate must block if required fields remain unknown.

### 2.5 Readiness gate (policy + validation)
- **Purpose:** validate schema + enforce policy readiness before downstream use.
- **Gate inputs:** `intake_bundle_v0_1`, `policy_profile`, `context_profile`.
- **Fail-closed:** any unknown taxonomy, missing required section, or nondeterministic field → block.

---

## 3) Deterministic rules (explicit)
- **Stable ordering:**
  - Lists are sorted lexicographically by stable key (e.g., field path or ID).
  - `evidence_index` keys sorted by evidence ID.
- **Hashing rules:**
  - Evidence artifacts are content-addressed (hash of canonical JSON serialization).
  - `input_digest` computed from normalized `intake_bundle_v0_1` (ordered keys).
- **Fail-closed validation:**
  - Unknown vocab (jurisdiction/sector/policy pack) is rejected.
  - Schema mismatch rejects the bundle.
  - **Locale edge:** `locale_context: null` must fail closed (regression fixture enforced).

---

## 4) OSS seams (adapter boundaries only; no code)
- **OPA readiness gate (optional):**
  - Embedded CLI, pinned bundle digest, offline evaluation only.
  - Forbid nondeterministic builtins (time, uuid, rand, external HTTP).
- **PAR DPIA (optional UI):**
  - External UI → adapter boundary: `par_export.json → intake_bundle_v0_1`.
  - EUPL isolation required; no code copied into core `packages/ep` or `packages/pe`.
- **CNIL PIA patterns (reference only):**
  - Use as question-pattern library; **no GPL code import** into core packages.

---

## 5) Explicitly deferred
- LLM extractors / council / model voting.
- Advanced policy reasoning engine beyond OPA-like readiness gate.
- UI buildout (native AiGov intake UI).

---

## 6) Migration plan (client_intake_v0_2 → intake_bundle_v0_1)
- **Current intake output** (`client_intake_output_contract_v0_1`) remains valid for legacy EP flows.
- **M_Intake adds** `intake_bundle_v0_1` as a **new canonical intake artifact** feeding readiness + scenario generation.
- **Bridging strategy:**
  - Keep `client_intake_v0_2` inputs as supported sources (ingest) while the canonical output moves to `intake_bundle_v0_1`.
  - Preserve existing output boundary rules (context_profile precedence; locale_context mismatch fails).
  - Do not change existing EP validation behavior; introduce M_Intake outputs in parallel with explicit fixtures first.

---

## 7) Concrete AiGov touchpoint paths (verify against fit matrix)
- **Contracts + schemas:** `packages/specs/docs/contracts/`, `packages/specs/schemas/`.
- **Taxonomy allowlists:** `packages/specs/docs/contracts/taxonomy/`.
- **Runtime validation:** `packages/ep/aigov_ep/`.
- **PE gates + fixtures:** `packages/pe/tests/`, `tools/fixtures/validators/`.

---

## Summary
- M_Intake outputs a canonical `intake_bundle_v0_1` with Evidence Model B; drafts and reconciliation remain internal.
- Deterministic ordering, hashing, and fail-closed rules are explicit (including locale_context null regression).
- OSS seams are adapter-only (OPA, PAR, CNIL) with strict license isolation and offline determinism.

## Work performed
- Reviewed constitution, runbook, codebase map, and intake/taxonomy anchors.
- Anchored architecture to existing intake output rules and fixtures.
- Documented deterministic rules, seams, deferred scope, and migration strategy.

## Findings
- A parallel canonical bundle path avoids breaking legacy intake output while enabling readiness gating.
- The missing CNIL patterns doc is a blocker for detailed question-pattern mapping.

## Checkpoint
- Files changed:
  - `packages/specs/docs/planning/2026-02-06/m_intake_architecture_plan_2026-02-06.md`
- Commands run:
  - `ls packages/specs/docs/planning/2026-02-06`
  - `find packages/specs/docs -name "m_intake_oss_eval_cnil_patterns_2026-02-06.md" -print`
  - `find packages/specs/docs -name "*fit_matrix*" -print`
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_constitution_2026-02-06.md`
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_codex_runbook_2026-02-06.md`
  - `sed -n '1,220p' packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md`
  - `sed -n '1,220p' packages/specs/docs/planning/2026-02-06/m_intake_task_pack_2026-02-06.md`
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_oss_eval_opa_2026-02-06.md`
  - `sed -n '1,220p' packages/specs/docs/planning/2026-02-06/m_intake_oss_eval_par_2026-02-06.md`
  - `sed -n '1,200p' packages/specs/schemas/client_intake_v0_2.schema.json`
  - `sed -n '1,200p' packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md`
  - `sed -n '1,200p' packages/specs/docs/contracts/taxonomy/evidence_schema.md`
  - `cat tools/fixtures/validators/intake_output_context_fail_locale_context_null.json`
- Results:
  - Docs-only; no proofs executed.
- Risks/unknowns:
  - CNIL patterns doc missing (UNCONFIRMED PATH).
  - Fit matrix file missing at specified path; touchpoints derived from codebase map pending confirmation.
- Next task:
  - Add CNIL patterns doc and update OSS seam references.
  - Define intake_bundle_v0_1 schema + contract docs (Phase D evals-first prep).
