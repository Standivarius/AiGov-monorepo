# Claude Code Architecture Review & Execution Plan (Snapshot)

- Date: 2026-01-24
- Source: Claude Code
- Purpose: Snapshot artifact (not a living plan)
- Note: May contain stale PR numbering; see `packages/specs/docs/planning/2026-01-22-run/pro_run_2_codex_pr_chain.md` for current sequence.

---

# ARCHITECTURE REVIEW & EXECUTION PLAN — AiGov Monorepo Pro Run 2

**Date:** 2026-01-24
**Branch:** `claude/add-contract-fields-xy9pR`
**Scope:** End-to-end MVP readiness assessment + minimal next PR chain

---

## 1. REPO-GROUNDED ARCHITECTURE INVENTORY

### A. SCENARIO LIBRARY + LOADERS

**What Exists:**
- **Scenario Card Schema v1.2** (`packages/specs/schemas/scenario_card/scenario-card-schema-v1.2.md`) - Complete markdown spec with validation pseudocode
- **GDPR Evaluation Criteria v1.0** (`packages/specs/schemas/evaluation_criteria/gdpr-evaluation-criteria-v1.0.yaml`) - 348-line production rubric
- **Scenario Loaders** (`packages/pe/aigov_eval/loader.py`, `packages/ep/aigov_ep/loader.py`) - 62 lines each, YAML/JSON support, duplicated across packages
- **Bundle Compiler** (`packages/ep/aigov_ep/bundle/compiler.py`) - Bundles scenarios with SHA256 checksums + manifests
- **Example Scenarios** (`packages/pe/examples/scenarios/`) - 4 YAML scenarios (old schema, pre-v1.2)
- **Calibration Fixtures** (`packages/pe/cases/calibration/`) - 12 JSON calibration cases for judge testing

**What is Stubbed:**
- **Expansion Rules** (`packages/specs/docs/contracts/scenarios/scenario_instance_expansion_rules_v0_1.md`) - Contract written, **zero implementation code**
- **Bespoke Scenario Spec** (`packages/specs/docs/contracts/scenarios/bespoke_scenario_spec_v0_1.md`) - Contract written, **zero implementation code**
- **Instance Contract Validator** - No validation code for scenario instances
- **Scenario Library** (`packages/specs/scenarios/library/`) - Empty directory, no v1.2 scenarios authored

**Paths:**
```
packages/specs/schemas/scenario_card/scenario-card-schema-v1.2.md
packages/specs/schemas/evaluation_criteria/gdpr-evaluation-criteria-v1.0.yaml
packages/pe/aigov_eval/loader.py
packages/ep/aigov_ep/loader.py
packages/ep/aigov_ep/bundle/compiler.py
packages/pe/examples/scenarios/{pii_disclosure,special_category_leak}.yaml
packages/pe/cases/calibration/cal_*.json
```

---

### B. INTAKE CONTRACTS + VALIDATORS

**What Exists:**
- **Client Intake Contract Spec** (`packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md`) - Complete markdown contract with JSON validation block
- **Intake Validator Tool** (`tools/validate_pre2_5_intake_contracts.py`) - Validates contract spec JSON blocks + mock target fields
- **Mock Target Adapters** (`packages/ep/aigov_ep/targets/mock_llm.py`, `http_target.py`, `scripted.py`) - 3 fully implemented adapters
- **Bundle Manifest Generator** (`packages/ep/aigov_ep/bundle/compiler.py`) - Creates bundle_manifest.json + checksums
- **Run Manifest Generator** (`packages/ep/aigov_ep/artifacts/manifests.py`) - Creates run_manifest.json + checksums.sha256

**What is Stubbed:**
- **Intake Runtime Validator** (`packages/ep/aigov_ep/intake/validate.py`) - Single function raises `NotImplementedError`
- **Client Intake Output Generation** - No code to create client_intake_output objects
- **Client ID/Profile Mapping** - No code to generate policy/target profiles

**Paths:**
```
packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md
tools/validate_pre2_5_intake_contracts.py
packages/ep/aigov_ep/intake/validate.py (STUB)
packages/ep/aigov_ep/targets/{mock_llm,http_target,scripted}.py
packages/ep/aigov_ep/bundle/compiler.py
packages/ep/aigov_ep/artifacts/manifests.py
```

---

### C. STAGE A RUNNER + TARGETS

**What Exists:**
- **EP Runner** (`packages/ep/aigov_ep/execute/runner.py`) - Fully implemented orchestration: loads scenario → instantiates target → executes turns → captures transcript
- **PE Runner** (`packages/pe/aigov_eval/runner.py`) - Parallel implementation (older, couples Stage A+B)
- **CLI Entry Points** (`packages/ep/aigov_ep/cli.py`) - `execute`, `bundle`, `judge` subcommands
- **Target Adapters:**
  - `MockTargetAdapter` (mock_llm.py) - OpenRouter LLM backend + leak simulation
  - `HttpTargetAdapter` (http_target.py) - External HTTP endpoint integration
  - `ScriptedMockTargetAdapter` (scripted.py) - Deterministic script-based responses
- **Artifact Generation:** transcript.json, run_meta.json, scenario.json, run_manifest.json, checksums.sha256
- **Smoke Tests:** `test_ep_bundle_execute_smoke.py`, `test_ep_cli_execute_smoke.py` - Validate Stage A-only execution (no Stage B leakage)

**What is Stubbed:**
- None. Stage A is **production-ready**.

**Paths:**
```
packages/ep/aigov_ep/execute/runner.py
packages/pe/aigov_eval/runner.py
packages/ep/aigov_ep/cli.py
packages/ep/aigov_ep/targets/{mock_llm,http_target,scripted}.py
packages/ep/aigov_ep/artifacts/manifests.py
packages/pe/tests/minimal_loop/test_ep_*_smoke.py
```

---

### D. EVIDENCE PACK BUILDER + MANIFEST/HASHING

**What Exists:**
- **Evidence Pack Assembly** (`packages/ep/aigov_ep/evidence.py`) - `build_evidence_pack()`, `write_evidence_pack()` with LIMITATIONS field
- **Manifest & Hashing Utilities** (`packages/ep/aigov_ep/artifacts/manifests.py`):
  - `write_run_manifest()` - Generates canonical run manifest v0.1
  - `sha256_file()` - Streaming SHA256 hash (8KB chunks)
  - `write_checksums()` - Creates checksums.sha256 file
  - `_sanitize_config()` - Redacts sensitive keys (api_key, token, secret, etc.)
- **Evidence Pack Schema v0** (`packages/specs/docs/contracts/evidence_pack/evidence_pack_v0.schema.json`) - JSON Schema with signals[], items[]
- **Evidence Pack Manifest v1** (`packages/specs/schemas/evidence_pack_manifest_v1.json`) - Schema defined but not runtime-integrated
- **Judge Integration** (`packages/ep/aigov_ep/judge/judge.py`) - `judge_run()` orchestrates evidence pack building

**What is Stubbed:**
- **Evidence/Telemetry Separation** - Designed but not enforced; telemetry fields (http_audit, mock_audit) packaged alongside evidence
- **Schema Validation** - No JSON schema validators against v0/v1 schemas
- **Checksum Verification** - No post-load integrity check function
- **Reporting Generator** (`packages/ep/aigov_ep/reporting/generate.py`) - Single function raises `NotImplementedError`

**Paths:**
```
packages/ep/aigov_ep/evidence.py
packages/ep/aigov_ep/artifacts/manifests.py
packages/specs/docs/contracts/evidence_pack/evidence_pack_v0.schema.json
packages/specs/schemas/evidence_pack_manifest_v1.json
packages/ep/aigov_ep/judge/judge.py
packages/ep/aigov_ep/reporting/generate.py (STUB)
```

---

### E. STAGE B JUDGE HARNESS + JUDGMENTS OUTPUTS

**What Exists:**
- **Judge Adapter** (`packages/pe/aigov_eval/judge.py`) - OpenRouter LLM backend + mock deterministic mode
  - `run_judge()` - Main orchestration supporting live & mock
  - `_run_mock_judge()` - Deterministic mock (reads expected_outcome from fixture)
  - `_run_openrouter_judge()` - Live judge via OpenRouter with taxonomy validation
  - Temperature=0.0, top_p=1.0 for determinism
- **Verdict Normalization** (`packages/pe/aigov_eval/judge_output_mapper.py`):
  - `_map_verdict_to_rating()` - VIOLATION→VIOLATED, NO_VIOLATION→COMPLIANT, UNCLEAR→UNDECIDED
  - `map_judge_output_to_behaviour_json()` - Full schema-compliant transformation
  - `map_and_validate()` - Combined mapping + jsonschema validation
- **Judgments Schema** (`packages/specs/docs/contracts/judgements/judgments_v0.schema.json`) - Canonical specs schema
- **Behaviour JSON Schema v0 Phase 0** (`packages/pe/aigov_eval/contracts/behaviour_json_v0_phase0.schema.json`) - Working eval harness schema
- **Golden Set Fixtures:**
  - 12 calibration cases (`packages/pe/cases/calibration/cal_*.json`)
  - 1 golden set item (`packages/pe/golden_set/gs_001.json`)
- **Schema Compliance Tests** (`packages/pe/tests/judge/test_j02_schema.py`) - All 12 scenarios validated ✅

**What is Stubbed:**
- **Replay/Versioning** - Mock determinism works; judgement_id versioning + material change detection not implemented
- **Evidence ID Mapping** - Schema expects evidence_ids array, not wired in mapper
- **Accuracy Tests** (`test_j03_accuracy.py`) - Requires external MOCK_LOG ground-truth files (not in repo)

**Paths:**
```
packages/pe/aigov_eval/judge.py
packages/pe/aigov_eval/judge_output_mapper.py
packages/specs/docs/contracts/judgements/judgments_v0.schema.json
packages/pe/aigov_eval/contracts/behaviour_json_v0_phase0.schema.json
packages/pe/cases/calibration/cal_*.json
packages/pe/golden_set/gs_001.json
packages/pe/tests/judge/test_j02_schema.py
```

---

### F. STAGE C REPORTING GENERATOR + CROSSWALK/AGGREGATION/LINK INTEGRITY

**What Exists (Specifications):**
- **Report Layers** (`packages/specs/docs/contracts/reporting/report_layers.md`) - Canonical L1/L2/L3 definitions
- **Report Fields v0.1** (`packages/specs/docs/contracts/reporting/report_fields_v0_1.md`) - Minimum required fields per layer
- **Report Fields Crosswalk v0.1** (`packages/specs/docs/contracts/reporting/report_fields_crosswalk_v0_1.md`) - 18 field entries mapping L1/L2/L3/GDPR-GR to evidence artifacts
- **Report Aggregation v0.1** (`packages/specs/docs/contracts/reporting/report_aggregation_v0_1.md`) - Fail-closed aggregation rules
- **Phase 2 Exports Spec** (`packages/specs/docs/specs/phase2-reporting-exports-v0.1.md`) - L2 structure + L3 JSON schema + annex definitions
- **Hash Canonicalization** (`packages/specs/docs/contracts/reporting/hash_canonicalization_v0_1.md`) - JCS/RFC8785 specification

**What Exists (Validators):**
- **Crosswalk Validator** (`tools/validate_pre2_3_contracts.py`) - Validates report fields crosswalk against signals.json
- **Report Layer Drift Checker** (`tools/check_report_layer_drift.py`) - Prevents forbidden L-layer audience mappings
- **Schema Files:**
  - `limitations_log_v0.schema.json` - Complete schema
  - `evidence_pack_v0.schema.json` - Complete schema
  - `judgments_v0.schema.json` - Complete schema

**What Exists (Research):**
- **GRC Export Schemas** (`packages/specs/research/aigov-analysis/03-exports/grc_exports/`):
  - OneTrust CSV schema
  - Vanta JSON schema
  - VeriifyWise API schema
- **Report-Gen Project** (`packages/specs/projects/report-gen/`) - README, TASKS, RESEARCH (all planning phase)

**What is Stubbed:**
- **Report Generator** (`packages/ep/aigov_ep/reporting/generate.py`) - Single function raises `NotImplementedError`
- **JCS Canonicalization Code** - Specification exists, no implementation
- **Link Integrity Validator** - No artifact chain integrity checker
- **Export Generators** - No OneTrust/Vanta/VeriifyWise export code

**Paths:**
```
packages/specs/docs/contracts/reporting/{report_layers,report_fields_v0_1,report_fields_crosswalk_v0_1,report_aggregation_v0_1,hash_canonicalization_v0_1}.md
packages/specs/docs/contracts/reporting/limitations_log_v0.schema.json
packages/specs/docs/specs/phase2-reporting-exports-v0.1.md
tools/validate_pre2_3_contracts.py
tools/check_report_layer_drift.py
packages/ep/aigov_ep/reporting/generate.py (STUB)
packages/specs/research/aigov-analysis/03-exports/grc_exports/*.json
packages/specs/projects/report-gen/
```

---

### G. RAG/AKG INTEGRATION POINTS

**What Exists:**
- **TargetLab RAG Service** (`packages/ep/services/targetlab_rag/`) - FastAPI service with:
  - Deterministic offline mode (keyword retrieval over synthetic corpus)
  - Optional OpenRouter LLM mode
  - Leak simulation (PII/special category)
  - Docker Compose deployment
  - Validation artifacts (5 test cases)
- **HTTP Target Adapter** (`packages/ep/aigov_ep/targets/http_target.py`) - Integrates with TargetLab RAG endpoint
- **RAG Validation Reports** (`packages/ep/docs/reports/2025-12-19_targetlab-rag_*.md`) - 3 validation reports (v0.1, local, OpenRouter)

**What is Stubbed:**
- **AKG Retrieval Precision Eval** (EVAL-012 in eval_registry.yaml) - Defined but no implementation
- **RAG Retrieval Relevance Eval** (EVAL-013) - Defined but no implementation

**Paths:**
```
packages/ep/services/targetlab_rag/{app.py,README.md,docker-compose.yml}
packages/ep/aigov_ep/targets/http_target.py
packages/ep/docs/reports/2025-12-19_targetlab-rag_*.md
```

---

## 2. BLOCKERS/IMPORTANT GAPS (End-to-End MVP)

### **BLOCKER-1: Intake validation not runtime-integrated**
- **Location:** `packages/ep/aigov_ep/intake/validate.py`
- **Gap:** Single function stub raises `NotImplementedError`
- **Impact:** Cannot validate client intake outputs in EP pipeline
- **Contract exists:** Yes (`client_intake_output_contract_v0_1.md`)
- **Validator exists:** Yes (tool: `validate_pre2_5_intake_contracts.py`)
- **Fix:** Port tool logic into EP runtime validator

### **BLOCKER-2: Reporting generator not implemented**
- **Location:** `packages/ep/aigov_ep/reporting/generate.py`
- **Gap:** Single function stub raises `NotImplementedError`
- **Impact:** Cannot generate L1/L2/L3 reports or GDPR-GR exports
- **Contracts exist:** Yes (report_fields_v0_1, crosswalk, aggregation)
- **Fix:** Implement report generator using contracts + crosswalk

### **BLOCKER-3: Scenario expansion rules not implemented**
- **Location:** No code exists; contract at `scenario_instance_expansion_rules_v0_1.md`
- **Gap:** Cannot expand scenario cards into bespoke instances with variants
- **Impact:** Cannot generate multi-channel instances or policy-based variants
- **Contract exists:** Yes
- **Fix:** Implement expansion engine

### **IMPORTANT-1: Evidence/telemetry separation not enforced**
- **Location:** `packages/ep/aigov_ep/evidence.py`
- **Gap:** Telemetry fields (http_audit, mock_audit) packaged alongside evidence; no filtering layer
- **Impact:** Evidence packs not portable/admissible per specification
- **Contract exists:** Yes (PRD.md lines 73-75)
- **Fix:** Add separation filter in evidence pack builder

### **IMPORTANT-2: JCS canonicalization not implemented**
- **Location:** No code exists; contract at `hash_canonicalization_v0_1.md`
- **Gap:** Cannot perform deterministic hash comparisons for replay validation
- **Impact:** Determinism validation relies on string comparison, not canonical hashing
- **Contract exists:** Yes (RFC8785 reference)
- **Fix:** Implement JCS canonicalization + hash comparison utility

### **IMPORTANT-3: Link integrity validator missing**
- **Location:** No code exists
- **Gap:** No validator to check evidence_ids resolve to evidence pack artifact IDs
- **Impact:** Reports may contain broken evidence links
- **Contract exists:** Yes (EVAL-015 citation accuracy requirement)
- **Fix:** Implement link integrity checker for reports

### **IMPORTANT-4: Judge material change detection not implemented**
- **Location:** `packages/pe/aigov_eval/judge.py`, `judge_output_mapper.py`
- **Gap:** No versioning for judgement_id; no tracking of model_id, prompt_hash, etc.
- **Impact:** Cannot detect when judge outputs should be re-baselined
- **Contract exists:** Yes (`stage_b_determinism_v0_1.md`)
- **Fix:** Add judge manifest with material change fields

---

## 3. MINIMAL NEXT PR CHAIN (3-6 PRs)

### **PR #44: Intake validation runtime integration**
**EFFORT:** low–medium

**TODOs (required):**
1. Port `tools/validate_pre2_5_intake_contracts.py` logic into `packages/ep/aigov_ep/intake/validate.py`
2. Add `validate_intake(client_intake_output)` function with contract field checks
3. Add minimal fixture test (`test_intake_validation.py`)
4. Wire into CLI intake command (currently stubbed)

**Suggestions (optional):**
- Add `generate_intake_output()` helper to create intake objects from client config

**Good looks like:**
- `validate_intake()` enforces all required fields per contract
- PR-gate test validates fixture intake succeeds
- Invalid intake fails with clear error message

**Bad looks like:**
- Validation only checks field presence, not allowed values
- No test coverage for invalid inputs

**How to decide:**
- If validation adds heavy runtime, keep it structural-only in PR-gate; move deep checks to nightly

**File touch list:**
- `packages/ep/aigov_ep/intake/validate.py` (replace stub)
- `packages/pe/tests/intake/test_intake_validation.py` (new)
- `packages/ep/aigov_ep/cli.py` (wire validation into intake command)

**Verification commands:**
- **PR-gate:**
  ```bash
  pytest packages/pe/tests/intake/test_intake_validation.py -v
  python3 -m packages.ep.aigov_ep.cli intake --help
  ```
- **Nightly:** None (fast validation only)

**Stop conditions:**
- Cannot find contract field names (then update contract first)
- Validation requires LLM calls or external API (too slow for PR-gate)
- Touching more than 5 files

**Evidence artifacts:**
- EVID-011 (PE test reports)

**Mapping updates:**
- EVAL-003 (intake schema validation) - Add intake validation test to pass rule

---

### **PR #45: Evidence/telemetry separation filter**
**EFFORT:** low

**TODOs (required):**
1. Add `separate_evidence_from_telemetry()` function in `packages/ep/aigov_ep/evidence.py`
2. Define telemetry field list: `http_audit`, `http_raw_response`, `mock_audit`, `usage`
3. Create `build_admissible_evidence_pack()` that calls separation filter
4. Add test: evidence pack contains no telemetry fields
5. Update evidence pack schema docs to clarify admissible vs debug variants

**Suggestions (optional):**
- Add `build_debug_pack()` that includes telemetry for development use

**Good looks like:**
- Admissible evidence pack contains only evidence fields
- Telemetry available separately for debugging
- Schema validation passes for admissible pack

**Bad looks like:**
- Separation logic hardcoded in multiple places
- No clear documentation of which fields are evidence vs telemetry

**How to decide:**
- If telemetry field list grows beyond 5-6 items, extract to config file
- If separation requires deep recursion, add explicit allow-list instead of block-list

**File touch list:**
- `packages/ep/aigov_ep/evidence.py` (add separation function)
- `packages/pe/tests/evidence/test_separation.py` (new)
- `packages/specs/docs/contracts/evidence_pack/evidence_pack_v0.schema.json` (add comment clarifying admissible variant)

**Verification commands:**
- **PR-gate:**
  ```bash
  pytest packages/pe/tests/evidence/test_separation.py -v
  python3 -c "from packages.ep.aigov_ep.evidence import build_admissible_evidence_pack; print('Separation function exists')"
  ```
- **Nightly:** None

**Stop conditions:**
- Cannot determine telemetry field list without ambiguity
- Separation breaks existing evidence pack consumers (requires coordination PR)

**Evidence artifacts:**
- EVID-005 (evidence pack + manifest)
- EVID-011 (PE test reports)

**Mapping updates:**
- EVAL-018 (evidence pack validation) - Update pass rule to require telemetry absence

---

### **PR #46: High-ROI integrity validators (from PR #43 prompt)**
**EFFORT:** medium–high

**TODOs (required):**
1. Add validators (tools/*.py):
   - `mock_freshness_check.py` - Verify challenge_nonce presence (structural, PR-gate)
   - `equivalence_evidence_auditor.py` - Verify policy_ref required for equivalence assertions (PR-gate)
   - `verdict_strictness_check.py` - No legacy aliases in final outputs (PR-gate)
   - `fail_closed_aggregation_validator.py` - Instance INFRINGEMENT/EXECUTION_ERROR → parent INFRINGEMENT (nightly)
   - `link_integrity_validator.py` - Content hash vs manifest (nightly)
   - `golden_contamination_validator.py` - RAG citations cannot point to golden set ids/paths (release)
2. Add minimal fixtures for each validator (seconds runtime for PR-gate validators)
3. Wire fast validators into `.github/workflows/pr-gate.yml`
4. Wire heavy validators into `.github/workflows/nightly.yml` and `.github/workflows/release.yml`

**Suggestions (optional):**
- `undecided_cap_check.py` - Enforce cap per eval pass rules (nightly)
- `doc_mode_evidence_auditor.py` - timeline/change_log_ref required (release)
- `out_of_scope_cap_validator.py` - For release checks

**Good looks like:**
- PR-gate validators run in <5 seconds total
- Each validator has clear pass/fail output
- Validators reference contract field names explicitly

**Bad looks like:**
- PR-gate validators scan large artifacts (move to nightly)
- Validators guess field names instead of using contracts

**How to decide:**
- If validator requires artifact scanning: nightly or release
- If validator is structural field presence: PR-gate
- If validator requires cross-referencing golden set: release only

**File touch list:**
- `tools/mock_freshness_check.py` (new)
- `tools/equivalence_evidence_auditor.py` (new)
- `tools/verdict_strictness_check.py` (new)
- `tools/fail_closed_aggregation_validator.py` (new)
- `tools/link_integrity_validator.py` (new)
- `tools/golden_contamination_validator.py` (new)
- `.github/workflows/pr-gate.yml` (wire fast validators)
- `.github/workflows/nightly.yml` (wire artifact validators)
- `.github/workflows/release.yml` (wire golden contamination validator)
- `packages/pe/tests/validators/test_*.py` (fixtures for each)

**Verification commands:**
- **PR-gate:**
  ```bash
  python3 tools/mock_freshness_check.py
  python3 tools/equivalence_evidence_auditor.py
  python3 tools/verdict_strictness_check.py
  pytest packages/pe/tests/validators/test_mock_freshness.py -v
  ```
- **Nightly:**
  ```bash
  python3 tools/fail_closed_aggregation_validator.py --artifacts-dir <path>
  python3 tools/link_integrity_validator.py --report <path>
  ```
- **Release:**
  ```bash
  python3 tools/golden_contamination_validator.py --evidence-pack <path> --golden-set-dir packages/pe/golden_set/
  ```

**Stop conditions:**
- Cannot find contract field names (update contracts first)
- PR-gate runtime exceeds 10 seconds
- Touching more than 12 files

**Evidence artifacts:**
- EVID-011 (PE test reports)
- EVID-002 (contract provenance)

**Mapping updates:**
- EVAL-002 (contract sync + drift check) - Add validator checks to pass rule
- EVAL-006 (verdict enum conformance) - Wire verdict_strictness_check
- EVAL-015 (citation accuracy) - Wire link_integrity_validator

---

### **PR #47: JCS canonicalization + determinism validation**
**EFFORT:** medium

**TODOs (required):**
1. Add `packages/ep/aigov_ep/hashing/jcs.py` - JCS/RFC8785 canonicalization implementation
2. Add `canonicalize_json(obj)` function (sorted keys, minimal number representation)
3. Add `canonical_hash(obj)` = SHA256(canonicalize_json(obj))
4. Update `judge_output_mapper.py` to use canonical_hash for deterministic IDs
5. Add determinism validation test: identical inputs → identical canonical hash
6. Add test fixtures: JSON with different key orders → same canonical hash

**Suggestions (optional):**
- Add `compare_canonical()` helper for replay validation
- Add CLI command: `aigov-ep hash --canonical <file>`

**Good looks like:**
- JCS canonicalization matches RFC8785 test vectors
- Identical semantic JSON → identical hash regardless of key order
- Fast (< 1ms for typical judgments.json)

**Bad looks like:**
- Canonicalization doesn't handle edge cases (null, empty arrays, floats)
- Implementation uses external library without vendoring (supply chain risk)

**How to decide:**
- If RFC8785 implementation is complex, vendor a tested library (e.g., canonicaljson-rs Python bindings)
- If performance is slow, profile and optimize number serialization

**File touch list:**
- `packages/ep/aigov_ep/hashing/jcs.py` (new)
- `packages/ep/aigov_ep/hashing/__init__.py` (new)
- `packages/pe/tests/hashing/test_jcs.py` (new)
- `packages/pe/aigov_eval/judge_output_mapper.py` (update ID generation to use canonical_hash)

**Verification commands:**
- **PR-gate:**
  ```bash
  pytest packages/pe/tests/hashing/test_jcs.py -v
  python3 -c "from packages.ep.aigov_ep.hashing.jcs import canonical_hash; import json; print(canonical_hash({'b':1,'a':2}))"
  ```
- **Nightly:**
  ```bash
  pytest packages/pe/tests/judge/test_j01_consistency.py -v  # Uses canonical_hash for determinism checks
  ```

**Stop conditions:**
- JCS implementation doesn't pass RFC8785 test vectors
- Performance degrades PR-gate runtime
- Touching more than 6 files

**Evidence artifacts:**
- EVID-002 (contract provenance with hash)
- EVID-011 (PE test reports)

**Mapping updates:**
- EVAL-009 (determinism + replayability) - Update pass rule to use canonical hashing

---

### **PR #48: Judge material change detection + manifest**
**EFFORT:** medium

**TODOs (required):**
1. Add `packages/ep/aigov_ep/judge/manifest.py` - Judge manifest generation
2. Add `write_judge_manifest(output_dir, judge_config, model_id, prompt_hash, ...)` function
3. Add fields per `stage_b_determinism_v0_1.md`:
   - `model_id`, `base_model_version`, `system_prompt_hash`, `tools_schema_hash`
   - `retrieval_corpus_hash`, `verdicts_version`, `signals_version`
   - `judge_instructions_template_ref`
4. Update `judge_run()` to generate and write judge manifest alongside judgments.json
5. Add `detect_material_change(old_manifest, new_manifest)` function
6. Add test: material change detection triggers new judgement_id

**Suggestions (optional):**
- Add `judgement_id` auto-increment logic based on material changes
- Add CLI command: `aigov-ep judge diff --old <manifest1> --new <manifest2>`

**Good looks like:**
- Judge manifest captures all material change fields
- Material change detection is deterministic
- Judgement IDs increment only when material changes occur

**Bad looks like:**
- Manifest missing fields from contract
- Silent judge config changes don't trigger new judgement_id

**How to decide:**
- If prompt hash computation is expensive, cache it
- If versioning logic is complex, defer auto-increment to separate PR; this PR only generates manifests

**File touch list:**
- `packages/ep/aigov_ep/judge/manifest.py` (new)
- `packages/ep/aigov_ep/judge/judge.py` (call write_judge_manifest)
- `packages/pe/tests/judge/test_manifest.py` (new)
- `packages/specs/docs/contracts/judgements/judge_manifest_v0.schema.json` (new)

**Verification commands:**
- **PR-gate:**
  ```bash
  pytest packages/pe/tests/judge/test_manifest.py -v
  python3 -c "from packages.ep.aigov_ep.judge.manifest import write_judge_manifest; print('Manifest generator exists')"
  ```
- **Nightly:**
  ```bash
  # Run full judge pipeline and verify judge_manifest.json created
  AIGOV_RUN_JUDGE_TESTS=1 pytest packages/pe/tests/judge/ -v
  ```

**Stop conditions:**
- Cannot compute prompt_hash deterministically
- Manifest schema conflicts with existing judgments_v0.schema.json
- Touching more than 6 files

**Evidence artifacts:**
- EVID-006 (Stage B judgments JSON)
- EVID-011 (PE test reports)

**Mapping updates:**
- EVAL-009 (determinism + replayability) - Add judge manifest to pass rule

---

### **PR #49: L1 report generator (minimal viable)**
**EFFORT:** high

**TODOs (required):**
1. Implement `packages/ep/aigov_ep/reporting/generate.py`:
   - `generate_l1_report(evidence_pack, judgments, run_manifest)` → L1 JSON
   - Use `report_fields_crosswalk_v0_1.md` to map:
     - scope_snapshot, overall_status, risk_summary, key_findings, recommendations
2. Add fail-closed aggregation per `report_aggregation_v0_1.md`:
   - If field cannot be verified → omit field, emit limitations_log entry
3. Add `limitations_log` generation for omitted fields
4. Add test: L1 report validates against schema + crosswalk
5. Add CLI command: `aigov-ep report --level L1 --evidence-pack <dir> --out <file>`

**Suggestions (optional):**
- Add L2/L3 generators in follow-up PRs (keep this PR focused on L1 only)
- Add PDF rendering (use weasyprint or similar)

**Good looks like:**
- L1 report contains only fields from crosswalk
- Missing evidence → limitations_log entry, not silent omission
- Report regenerates without rerunning Stage A

**Bad looks like:**
- Report includes fields not in crosswalk (drift risk)
- Missing evidence causes crash instead of limitations_log
- Report embeds raw telemetry

**How to decide:**
- If crosswalk mapping is ambiguous, stop and update crosswalk contract first
- If PDF rendering adds heavy dependencies, keep JSON-only in this PR

**File touch list:**
- `packages/ep/aigov_ep/reporting/generate.py` (replace stub)
- `packages/ep/aigov_ep/reporting/limitations.py` (new - limitations_log generation)
- `packages/pe/tests/reporting/test_l1_generation.py` (new)
- `packages/ep/aigov_ep/cli.py` (add report command)

**Verification commands:**
- **PR-gate:** None (too slow)
- **Nightly:**
  ```bash
  pytest packages/pe/tests/reporting/test_l1_generation.py -v
  python3 -m packages.ep.aigov_ep.cli report --level L1 --evidence-pack <fixture> --out /tmp/l1_report.json
  python3 -c "import json; json.load(open('/tmp/l1_report.json')); print('L1 report valid JSON')"
  ```
- **Release:**
  ```bash
  # Full end-to-end: Stage A → B → L1 report
  # Validate against report_fields_v0_1.md
  ```

**Stop conditions:**
- Crosswalk references missing evidence artifact fields
- Report generation requires guessing field semantics
- Touching more than 8 files

**Evidence artifacts:**
- EVID-007 (L1 report)
- EVID-011 (PE test reports)

**Mapping updates:**
- EVAL-007 (report generation + link integrity) - Add L1 generation to pass rule

---

## 4. PR-GATE VS NIGHTLY/RELEASE SPLIT

### **PR-Gate Evalset (`pe_pr_gate_short`)**
**Max Runtime:** 600 seconds (10 minutes)

**Eval IDs:**
- EVAL-001 (boundary enforcement)
- EVAL-002 (contract sync + drift)
- EVAL-003 (intake schema validation)
- EVAL-006 (verdict enum conformance)
- EVAL-014 (scenario validity)
- EVAL-017 (CI gate required checks)

**New Validators (from PR #46):**
- `mock_freshness_check.py` - Structural field presence
- `equivalence_evidence_auditor.py` - Policy_ref presence
- `verdict_strictness_check.py` - No legacy aliases

**What MUST stay in PR-gate:**
- Schema validation (fast, catches drift early)
- Contract sync checks (prevents taxonomy drift)
- Boundary enforcement (module dependency checks)

**What MUST NOT go in PR-gate:**
- Stage A/B execution (too slow, network calls)
- Artifact scanning (file I/O heavy)
- Golden set comparison (large fixture set)

---

### **Nightly Evalset (`pe_nightly`)**
**Max Runtime:** 7200 seconds (2 hours)

**Eval IDs:**
- EVAL-004 (Stage A smoke run)
- EVAL-005 (Stage B golden cases)
- EVAL-009 (determinism + replayability)
- EVAL-012 (AKG retrieval precision)
- EVAL-013 (RAG retrieval relevance)
- EVAL-016 (golden set importer)
- EVAL-018 (evidence pack validation)

**New Validators (from PR #46):**
- `fail_closed_aggregation_validator.py` - Artifact scanning
- `link_integrity_validator.py` - Report link resolution

**What belongs in nightly:**
- Full Stage A → Stage B pipeline
- Evidence pack generation + validation
- Determinism checks (requires multiple runs)
- RAG/AKG retrieval metrics

---

### **Release Evalset (`pe_release`)**
**Max Runtime:** 7200 seconds (2 hours)

**Eval IDs:**
- EVAL-008 (export schema validation)
- EVAL-010 (translation fidelity)
- EVAL-011 (edge-case handling)
- EVAL-015 (citation accuracy + traceability)
- EVAL-205 (Tier A model/prompt change management)
- EVAL-207 (Tier A privacy notice disclosure)
- EVAL-210 (Tier A audit-ready reporting)

**New Validators (from PR #46):**
- `golden_contamination_validator.py` - RAG citation checks
- `out_of_scope_cap_validator.py` - Final compliance check

**What belongs in release:**
- Full export generation (GDPR-GR, OneTrust, Vanta)
- Citation integrity (all evidence links resolve)
- Tier A control evidence
- Translation fidelity (if multilingual enabled)

---

## 5. GEMINI-STYLE MITIGATIONS - RECONCILIATION

### **Mitigation: run_manifest strict schema**
**Status:** ✅ ALREADY DONE (PR #42)
- **Path:** `packages/specs/docs/contracts/execution/run_manifest_v0.schema.json`
- **Fields:** `schema_version`, `run_id`, `generated_at_utc`, `challenge_nonce`, `artifacts[]` with `captured_at_utc`
- **Enforcement:** JSON Schema v2020-12, `additionalProperties: false`

### **Mitigation: limitations_log strict schema**
**Status:** ✅ ALREADY DONE (PR #42)
- **Path:** `packages/specs/docs/contracts/reporting/limitations_log_v0.schema.json`
- **Fields:** `schema_version`, `run_id`, `generated_at`, `timeline_refs`, `limitations`, `assumptions`
- **Enforcement:** JSON Schema v2020-12, `additionalProperties: false`

### **Mitigation: equivalence abuse guardrail**
**Status:** ✅ ALREADY DONE (PR #42)
- **Path:** `packages/specs/docs/contracts/scenarios/scenario_instance_expansion_rules_v0_1.md:26`
- **Rule:** "Equivalence assertions: any explicit equivalence must include a non-empty `policy_ref` and MUST be labeled deputy-verified (not VERIFIED_RUNTIME)."
- **Enforcement:** Contract written; **validator needed** (PR #46: `equivalence_evidence_auditor.py`)

### **Mitigation: judge manifest verification mode**
**Status:** ⚠️ PARTIAL - Contract exists, implementation missing
- **Path:** `packages/specs/docs/contracts/judgements/stage_b_determinism_v0_1.md`
- **Contract:** Material change fields defined (model_id, prompt_hash, etc.)
- **Missing:** Judge manifest generation code
- **Fix:** PR #48 (judge material change detection + manifest)

### **Mitigation: playback challenge injection**
**Status:** ⚠️ PARTIAL - Schema exists, runtime enforcement missing
- **Path:** `packages/specs/docs/contracts/execution/run_manifest_v0.schema.json`
- **Schema Field:** `challenge_nonce` (required)
- **Missing:** Runtime validator to ensure challenge_nonce is fresh + verified
- **Fix:** PR #46 (`mock_freshness_check.py` - structural presence check)
- **Future:** Add nonce freshness validator (cryptographic verification)

---

## OPEN MITIGATIONS LIST (Priority Order)

### **OPEN-1: Equivalence abuse validator (HIGH)**
**Fix:** PR #46 - `equivalence_evidence_auditor.py`
- Validate policy_ref required for equivalence assertions
- Validate labeling is deputy-verified (not VERIFIED_RUNTIME)
- **Smallest change:** Add tool validator + wire into PR-gate workflow

### **OPEN-2: Judge manifest generation (MEDIUM)**
**Fix:** PR #48 - Judge manifest + material change detection
- Generate judge_manifest.json with material change fields
- Add `detect_material_change()` function
- **Smallest change:** Add manifest.py module + wire into judge_run()

### **OPEN-3: Challenge nonce freshness (LOW - crypto verification deferred)**
**Fix:** PR #46 - `mock_freshness_check.py` (structural presence only)
- Validate challenge_nonce field exists in run_manifest
- **Future:** Add cryptographic freshness verification (separate PR)
- **Smallest change:** Structural field check in PR-gate

### **OPEN-4: Fail-closed aggregation enforcement (MEDIUM)**
**Fix:** PR #46 - `fail_closed_aggregation_validator.py`
- Validate instance INFRINGEMENT/EXECUTION_ERROR → parent INFRINGEMENT
- **Smallest change:** Add nightly validator scanning aggregation outputs

### **OPEN-5: Link integrity validation (MEDIUM)**
**Fix:** PR #46 - `link_integrity_validator.py`
- Validate all evidence_ids in reports resolve to evidence pack artifacts
- **Smallest change:** Add nightly validator checking report citations

---

## SUMMARY: EXECUTION READINESS

**Ready for End-to-End MVP:**
- ✅ Stage A (runner + targets + manifests)
- ✅ Stage B (judge + verdict normalization + schema validation)
- ⚠️ Stage C (contracts complete, implementation stubbed)

**Blockers Removed by Proposed PRs:**
- PR #44: Intake validation (BLOCKER-1)
- PR #49: L1 report generator (BLOCKER-2)
- *Scenario expansion (BLOCKER-3) deferred - not required for fixed-scenario MVP*

**Integrity Validators Added:**
- PR #46: 6 validators (mock freshness, equivalence, verdict strictness, fail-closed, link integrity, golden contamination)
- PR #47: JCS canonicalization for determinism
- PR #48: Judge manifest for material change detection

**Eval-First Discipline Maintained:**
- All PRs map to existing eval_registry.yaml entries
- PR-gate stays fast (<10 minutes)
- Heavy validation in nightly/release tiers

**Next Session Handoff:**
- PRs #44-49 are copy/paste ready for Codex execution
- Each PR includes: TODOs, file paths, verification commands, stop conditions
- Contracts remain source of truth; no new product concepts introduced
