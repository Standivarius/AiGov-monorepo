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
- CNIL patterns: `packages/specs/docs/planning/2026-02-06/m_intake_oss_eval_cnil_patterns_2026-02-06.md`.
- Intake + taxonomy anchors:
  - `packages/specs/schemas/client_intake_v0_2.schema.json`
  - `packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md`
  - `packages/specs/docs/contracts/taxonomy/evidence_schema.md` (verdict/signal schema only; NOT Evidence Model B)
  - `tools/fixtures/validators/intake_output_context_fail_locale_context_null.json`

## Fit matrix status
- **Present**: `packages/specs/docs/planning/2026-02-06/m_intake_monorepo_fit_matrix_2026-02-06.md` (used as the anchor for touchpoint verification below).

---

## 1) Canonical module boundary (M_Intake output)
- **Canonical output artifact:** `intake_bundle_v0_1` (schema + contract to be defined under `packages/specs/schemas/` and `packages/specs/docs/contracts/`).
- **Phase D contract skeleton (intake_bundle_v0_1):**
  - **Required top-level keys:** `schema_version`, `bundle_id`, `intake`, `evidence_index`, `evidence_refs`.
  - **Minimum shapes:**
    - `schema_version`: `"intake_bundle_v0_1"`.
    - `bundle_id`: non-empty string.
    - `intake`: object (normalized intake output content, deterministic ordering).
    - `evidence_index`: object mapping `evidence_id` → `{ "source_path": string, "sha256": string }`.
    - `evidence_refs`: object mapping `field_path` → list of `evidence_id`.
- **Evidence Model B:** global `evidence_index` with field → `evidence_refs` pointers (per constitution).
  - Evidence Model B is a **new** Phase D contract; it is **not** defined by `evidence_schema.md`.
  - **Entry shape:** each `evidence_index` entry is `{source_path, sha256}` only (no timestamps or nondeterministic fields).
  - **Pointer rules:** every `evidence_refs` entry must reference existing `evidence_index` keys.
- **M_Intake scope:** produce a deterministic, schema-valid intake bundle that downstream EP runtime validation (`packages/ep/aigov_ep/`) and PE gates (`packages/pe/tests/`, `tools/fixtures/validators/`) can consume.
- **Taxonomy allowlists:** single source of truth is `packages/specs/docs/contracts/taxonomy/*.json` (jurisdictions, sectors, policy packs, constraints).
  - Schema lives in `packages/specs/schemas/`; validators load allowlists from taxonomy JSON files (separate locations).

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
- **Determinism rule:** conflict ordering is stable and reproducible, sorted by `(field_path, source_priority, evidence_id)`.

### 2.4 Gap analysis (clarification)
- **Outputs:** `clarification_questions[]` in deterministic order.
- **Fail-closed:** readiness gate must block if required fields remain unknown.

### 2.5 Readiness gate (policy + validation)
- **Purpose:** validate schema + enforce policy readiness before downstream use.
- **Gate inputs:** consumes `intake_bundle_v0_1` directly (fail-closed on derivation or reference resolution).
- **Fail-closed:** any unknown taxonomy, missing required section, unresolved evidence ref, or nondeterministic field → block.
  - **OPA semantics:** OPA deny = HARD FAIL (readiness gate fails; pipeline blocked).
  - OPA is optional; default readiness gate uses non-OPA deterministic checks.

---

## 3) Deterministic rules (explicit)
- **Stable ordering:**
  - Lists are sorted lexicographically by stable key (field path or ID).
  - `evidence_index` keys sorted by evidence ID.
  - `evidence_refs[field_path]` lists sorted lexicographically by evidence ID.
  - `conflicts[]` sorted by `(field_path, source_priority, evidence_id)`.
  - `clarification_questions[]` sorted by stable question ID.
- **Hashing rules:**
  - Canonicalization: JSON must be normalized using JCS/RFC8785 before hashing, per `packages/specs/docs/contracts/reporting/hash_canonicalization_v0_1.md` (no new deps in this PR).
  - Evidence artifacts are content-addressed (sha256 of canonical JSON serialization).
  - `input_digest` computed from normalized `intake_bundle_v0_1` (ordered keys, deterministic list order).
- **Fail-closed validation:**
  - Unknown vocab (jurisdiction/sector/policy pack) is rejected.
  - Schema mismatch rejects the bundle.
  - **Locale edge:** `locale_context: null` must fail closed (regression fixture enforced).
- **Known live fail-open gap:** if **both** `context_profile` is absent **and** the `locale_context` key is absent, current intake output validation fails open; this requires a validator patch (do not treat as covered).

---

## Phase D deliverables (required for fail-closed invariants)
- Define `intake_bundle_v0_1.schema.json` under `packages/specs/schemas/`.
- Create Evidence Model B contract doc: `packages/specs/docs/contracts/intake/evidence_model_b_v0_1.md`
  - (Alternative: include the full Evidence Model B spec inside the intake_bundle_v0_1 contract doc; if so, be explicit in that doc.)
- Patch `packages/ep/aigov_ep/intake/validate.py` to fail closed when **both** `context_profile` is absent **and** the `locale_context` key is absent. **Required** to satisfy fail-closed invariant.

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
- The readiness gate boundary must consume `intake_bundle_v0_1` directly to keep derivation and evidence refs fail-closed.

## Checkpoint
- Files changed:
  - `packages/specs/docs/planning/2026-02-06/m_intake_architecture_plan_2026-02-06.md`
- Commands run:
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
- Results:
  - `python3 tools/validate_planning_pack.py`:
    - ```
      PASS: evidence_pack_v0 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/evidence_pack_v0_pass.json
      FAIL (as expected): evidence_pack_v0 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/evidence_pack_v0_fail.json
      FAIL (as expected): base scenario fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/base_scenario_empty_signals.json
      PASS: client override validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_override_pass.json
      FAIL (as expected): client override validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_override_fail.json
      FAIL (as expected): client override validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_override_fail_nondeterministic_field.json
      FAIL (as expected): client override validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_override_fail_unknown_vocab.json
      FAIL (as expected): client override validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_override_empty_supported.json
      PASS: client intake v0.2 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_intake_v0_2_pass.json
      FAIL (as expected): client intake v0.2 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_intake_v0_2_fail.json
      FAIL (as expected): client intake v0.2 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_intake_v0_2_fail_channel_mismatch.json
      FAIL (as expected): client intake v0.2 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/client_intake_v0_2_fail_empty_supported.json
      PASS: intake output context fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_pass_nl_public.json
      PASS: intake output context fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_pass_nl_healthcare.json
      PASS: intake output context fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_pass_legacy_locale_only_nl.json
      FAIL (as expected): intake output context fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_fail_pack_order.json
      FAIL (as expected): intake output context fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_fail_locale_context_null.json
      FAIL (as expected): intake output context fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_fail_unknown_jurisdiction.json
      FAIL (as expected): intake output context fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_fail_unknown_sector.json
      PASS: client intake bundle determinism validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/intake_output_context_pass_nl_public.json
      PASS: inspect_task_args v0.1 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/inspect_task_args_v0_1_pass.json
      FAIL (as expected): inspect_task_args v0.1 fixture validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/inspect_task_args_v0_1_fail.json
      PASS: LiveRun output artifacts validated: /workspaces/AiGov-monorepo/tools/fixtures/liverun_artifacts_v0_1/pass
      FAIL (as expected): LiveRun output artifacts validated: /workspaces/AiGov-monorepo/tools/fixtures/liverun_artifacts_v0_1/fail
      PASS: bundle integrity validated: /workspaces/AiGov-monorepo/tools/fixtures/bundles/good
      PASS: deterministic bundle manifest validated: /workspaces/AiGov-monorepo/tools/fixtures/bundles/good
      FAIL (as expected): bundle integrity validated: /workspaces/AiGov-monorepo/tools/fixtures/bundles/poison
      PASS: bundle scenario validated: /workspaces/AiGov-monorepo/tools/fixtures/bundles/good/scenarios/GDPR-001__client-001.json
      PASS: bundle scenario validated: /workspaces/AiGov-monorepo/tools/fixtures/bundles/good/scenarios/GDPR-002.json
      FAIL (as expected): bundle scenario validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/gdpr_bundle_scenario_fail_missing_expected.json
      PASS: dataset JSONL validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/dataset_jsonl_v0_1_pass.jsonl
      FAIL (as expected): dataset JSONL validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/dataset_jsonl_v0_1_fail_nondeterministic_field.jsonl
      FAIL (as expected): dataset JSONL validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/dataset_jsonl_v0_1_fail_sha_case.jsonl
      FAIL (as expected): dataset JSONL validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/dataset_jsonl_v0_1_fail_empty_id.jsonl
      PASS: interface ledger validated.
      PASS: seed_instructions export validated: /workspaces/AiGov-monorepo/tools/fixtures/validators/petri_seed_instructions_from_bundle_pass.json
      PASS: runpack command validated: /workspaces/AiGov-monorepo/tools/fixtures/runpack/expected_inspect_command_pass.txt
      PASS: module cards validated: /workspaces/AiGov-monorepo/packages/specs/docs/contracts/modules/cards
      PASS: module dashboard snapshot validated.
      PASS: scenario determinism validated.
      PASS: scenario schema strictness validated.
      PASS: planning pack validated.
      ```
  - `bash tools/run_pr_gate_validators.sh`:
    - ```
      PASS: canonical verdicts only.
      PASS: doc-mode operational evidence requirements satisfied.
      PASS: equivalence labeling requirements satisfied.
      PASS: no golden-set contamination in citations.
      PASS: evidence_id resolution validated.
      PASS: evidence IDs are canonical and registry-backed.
      ```
- Risks/unknowns:
  - Known live fail-open gap if both context_profile and locale_context key are absent (validator patch required).
- Next task:
  - Define intake_bundle_v0_1 schema + contract docs (Phase D evals-first prep).
