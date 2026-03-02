# Checkpoint: UAVG/AP + AutoGen + Judge Context-Engineering Work
**Date:** 2026-03-02  
**Author:** Codex  
**Purpose:** Durable summary of completed work since the prompt beginning with Dutch UAVG/AP research request, plus branch de-risking proposal.

## Completed Work (Corrected)

### 1) Dutch UAVG + AP mapping for chatbot testing (healthcare + municipal)
Completed a structured legal mapping that translates Dutch national specifications and AP guidance into concrete chatbot-testing implications and evidence expectations. The output covers healthcare and municipal citizen-services contexts, and includes control themes, test objectives, expected behavior, and evidence types to be consumed by AiGov scenario design and intake assumptions.
- Artifact: `packages/specs/docs/artifacts/2026-03-02__nl-uavg-ap__chatbot-testing-mapping_v1.md`

### 2) AutoGen courtroom spike scaffold (repo structure + runnable orchestrator)
Implemented the AutoGen debate spike baseline with separated knowledge folders (`docs_auditor_manual` vs `docs_client_evidence`), a runtime orchestrator, deterministic turn-taking logic, and strict judge JSON validation behavior. This established an executable prototype for the prosecutor/defender/judge interaction pattern requested.
- Artifacts: `experiments/spikes/autogen-debate-s0/main.py`, `experiments/spikes/autogen-debate-s0/README.md`, `experiments/spikes/autogen-debate-s0/requirements.txt`

### 3) Master audit schema models for extraction + runtime injection
Implemented strict schema objects for extracted EDPB rules and judge verdict structures so extracted methodology can be loaded deterministically at runtime. This is the bridge between raw policy text and executable audit behavior.
- Artifact: `experiments/spikes/autogen-debate-s0/schemas.py`

### 4) EDPB D2 extraction pipeline (parse -> map -> structured outputs)
Implemented and executed the extraction script that ingests the EDPB D2 PDF, parses testcase-like units, maps GDPR article references, and outputs both JSON and YAML catalogs. The pipeline uses deterministic fallback behavior and flags unresolved extraction points for manual review.
- Artifact: `experiments/spikes/autogen-debate-s0/extract_edpb_rules.py`
- Outputs: `experiments/spikes/autogen-debate-s0/data/master_audit_rules.json`, `experiments/spikes/autogen-debate-s0/data/master_audit_rules.yaml`

### 5) Calibration-to-EDPB rule mapper
Implemented mapping logic from calibration fixtures to EDPB rules via article-number intersection, producing the first machine-readable linkage file for case-to-rule injection.
- Artifact: `experiments/spikes/autogen-debate-s0/map_calibration_to_edpb_rules.py`
- Output: `experiments/spikes/autogen-debate-s0/data/calibration_to_edpb_rules.json`

### 6) Mapping diagnostics + inspector helpers
Added helper scripts to inspect catalog/rule coverage and case mappings quickly, including diagnostics for empty mapping cases and likely near-match candidates under different article references.
- Artifacts:  
  - `experiments/spikes/autogen-debate-s0/inspect_catalog.py`  
  - `experiments/spikes/autogen-debate-s0/inspect_case_rule_mapping.py`  
  - `experiments/spikes/autogen-debate-s0/check_empty_mapping_cases.py`

### 7) Empty-case root-cause analysis (cal_003, cal_008, cal_012)
Confirmed empty mappings were not caused by missing case citations, but by extraction/mapping coverage gaps: current extracted EDPB catalog has no rules mapped to Articles 5/13/14, so strict article-intersection mapping returns zero even when semantically relevant controls exist under other articles (notably 12/17/25).
- Supporting artifact: `experiments/spikes/autogen-debate-s0/check_empty_mapping_cases.py`

### 8) Judge accuracy test implementation (TEST-J03)
Replaced placeholder logic in TEST-J03 with real offline judge execution over all 12 calibration fixtures, verdict+signal comparison against expected outcomes, and computed baseline metrics (precision/recall/F1 + verdict accuracy). This produced an executable baseline gate before judge improvements.
- Artifact: `packages/pe/tests/judge/test_j03_accuracy.py`

### 9) One-case context-engineering A/B runner
Implemented reusable A/B runner comparing generic vs enriched judge prompts using EDPB rules + GDPR criteria + Dutch locale context, with deterministic scoring and report emission (JSON + MD).
- Artifact: `experiments/spikes/judge-context-ab/run_cal001_context_ab.py`

### 10) Model/case parameterization for A/B runner
Extended the one-case runner to support `--case-id` and explicit model overrides (`--openrouter-model`, `--openai-model`) to avoid shell-env ambiguity and make reruns reproducible.
- Artifact: `experiments/spikes/judge-context-ab/run_cal001_context_ab.py`

### 11) Single-case A/B experiments executed
Executed A/B on `cal_001_lack_of_consent` and `cal_011_unclear_consent` with model variants, capturing where enrichment helps and where it saturates. This established practical evidence about context engineering value by case difficulty/model capacity.
- Artifacts under: `experiments/spikes/judge-context-ab/work/`

### 12) Full 12-case A/B batch run on Mistral Large
Implemented and ran full batch A/B on all 12 calibration cases using `mistralai/mistral-large-2512`, producing per-case and aggregate summary tables. This is the current whole-set baseline for generic vs enriched prompting.
- Runner: `experiments/spikes/judge-context-ab/run_all_cases_ab.py`
- Summary: `experiments/spikes/judge-context-ab/work/full12_ab_summary__mistralai_mistral-large-2512.md`

## PR De-risk Proposal (for oversized branch)

Current branch carries far more than one reviewable change set. Recommended action is to preserve current state as parking baseline, then promote work as small thematic PRs:

1. **PR-A Legal research pack**
   - Include: `packages/specs/docs/artifacts/2026-03-02__nl-uavg-ap__chatbot-testing-mapping_v1.md`

2. **PR-B Judge A/B spike tooling**
   - Include: `experiments/spikes/judge-context-ab/*.py`
   - Include only essential output artifacts (or regenerate in CI/local)

3. **PR-C AutoGen + EDPB extraction spike**
   - Include: `experiments/spikes/autogen-debate-s0/*.py`, `README.md`, `requirements.txt`
   - Include generated catalogs only if intentionally versioned

4. **PR-D Judge baseline test wiring**
   - Include: `packages/pe/tests/judge/test_j03_accuracy.py`

5. **Do not PR now**
   - Temporary caches (`__pycache__`)
   - Large incidental local artifacts not tied to approved scope

This preserves value while restoring auditability and review quality.

