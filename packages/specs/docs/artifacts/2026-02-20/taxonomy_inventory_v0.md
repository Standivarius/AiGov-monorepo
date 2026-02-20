# Taxonomy Inventory v0

Snapshot SHA: `11e3072cfa8a429fb809c02c58ed56d0551184cb`  
Date: `2026-02-20`

## Scope

This inventory captures the current vocabulary used across:

- contracts and schemas (`packages/specs`)
- EP runtime (`packages/ep`)
- PE harness and cases (`packages/pe`)
- planning playbook (`packages/specs/docs/planning/2026-02-17/PLAN_OF_RECORD_v1.md`)

## Source files used

- `packages/specs/docs/contracts/terminology.md`
- `packages/specs/docs/contracts/taxonomy/verdicts.json`
- `packages/specs/docs/contracts/taxonomy/signals.json`
- `packages/specs/schemas/behaviour_json_v0_phase0.schema.json`
- `packages/ep/aigov_ep/contracts/behaviour_json_v0_phase0.schema.json`
- `packages/pe/aigov_eval/contracts/behaviour_json_v0_phase0.schema.json`
- `packages/ep/aigov_ep/judge/judge.py`
- `packages/pe/aigov_eval/judge_output_mapper.py`
- `packages/pe/cases/calibration/*.json`
- `packages/specs/docs/planning/2026-02-17/PLAN_OF_RECORD_v1.md`

## Inventory

### 1) Spine stage language

- Canonical stage labels in plan:
  - `Scenario Library`
  - `Client Intake`
  - `Bespoke Prep` (also written as `Bespoke Scenario Preparation`)
  - `Testing Target`
  - `Judge`
  - `Reporting`
- Milestone vocabulary in plan:
  - `M1` through `M5` (milestones, not module IDs)

### 2) Module ID language

- Existing requested code-style format from founder direction: `M_*` (example: `M_Intake`).
- Current repo state:
  - module registry is now tracked at `packages/specs/docs/contracts/modules/module_registry_v0.yaml`
  - canonical IDs in registry: `M_Library`, `M_Intake`, `M_BespokePrep`, `M_TestTarget`, `M_Judge`, `M_Reporting`
  - enforcement in validators/CI is not yet wired

### 3) Verdict vocabulary

- Canonical set (`terminology.md`, `verdicts.json`, resolved by ADR-005):
  - `INFRINGEMENT`
  - `COMPLIANT`
  - `UNDECIDED`
- Legacy aliases (contract mapping, accepted at input boundaries only):
  - `VIOLATED -> INFRINGEMENT`
  - `VIOLATION -> INFRINGEMENT`
  - `NO_VIOLATION -> COMPLIANT`
  - `PASS -> COMPLIANT`
  - `UNCLEAR -> UNDECIDED`
- Schema enum in all three behaviour schema copies:
  - `INFRINGEMENT | COMPLIANT | UNDECIDED`
- Runtime behavior:
  - producers and persisted artifacts now use canonical verdict labels
  - legacy labels are normalized before persistence

### 4) Signal vocabulary

- Canonical signal IDs come from `packages/specs/docs/contracts/taxonomy/signals.json` (20 IDs).
- Calibration scenarios in `packages/pe/cases/calibration/` use IDs aligned to the same naming family (examples):
  - `lack_of_consent`
  - `special_category_violation`
  - `rights_violation`
  - `data_minimization_breach`
  - `retention_violation`

### 5) EP/PE boundary language

- `terminology.md` defines:
  - `EP`: client-run evaluation product pipeline
  - `PE`: product evaluation/regression harness
- `terminology.md` now uses monorepo placement (`packages/ep`, `packages/pe`).
- Legacy repo-name vocabulary (`aigov-mvp`, `aigov-evals`, `AiGov-specs`) remains in historical program docs and requires staged cleanup.

### 6) Evidence/telemetry language

- Locked vocabulary present in contracts/plan:
  - `evidence lane` (persistent audit artifacts)
  - `telemetry lane` (ephemeral operational data)
  - hard rule: no raw CoT persistence

### 7) Stage A artifact language

- Plan v1 defines Stage A artifact set as:
  - `scenario.json`
  - `transcript.json`
  - `run_meta.json`
  - `run_manifest.json`
  - `checksums.sha256`
- Explicit negative boundary:
  - `scores.json` and `evidence_pack.json` must not be present in Stage A output.
