# Pre-PRD Scenario Pack Spec v0

## Purpose

Define the minimal executable validation contract for SLICE v0.1 before PRDs.

## Required structure

### 1) Scenario metadata
- `scenario_id`
- `title`
- `scope`
- `version`

### 2) Input payload
- canonical scenario input
- intake/context input
- deterministic knobs/config

### 3) Expected outputs by stage
- Stage 1 expected output summary
- Stage 2 expected output summary
- Stage 3 expected output summary
- Stage 4 artifact set expectations
- Stage 5 judge output expectations
- Stage 6 report/export expectations

### 4) Comparison policy
- strict fields
- excluded volatile fields
- normalization rules
- pass/fail rule

### 5) Evidence and telemetry expectations
- evidence-lane outputs (persisted)
- telemetry-lane outputs (ephemeral)
- privacy constraints (no raw CoT)

## Holdout policy (minimum)

- Keep at least one holdout scenario outside build-loop prompts.
- Holdout scenarios are used only at gate checks.

## Acceptance for Pre-PRD gate

- Scenario Pack spec exists and is complete.
- At least one concrete scenario instance is drafted against this schema.

