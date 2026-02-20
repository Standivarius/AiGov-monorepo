# Taxonomy Dictionary v0 (Proposed Lock)

Snapshot SHA: `11e3072cfa8a429fb809c02c58ed56d0551184cb`  
Date: `2026-02-20`

Purpose: provide one code-facing vocabulary for planning, PRDs, and PRs.

## 1) Module dictionary (code-facing)

Use module IDs in code/spec commits; use friendly names only as secondary labels.

| Module ID | Friendly label | Spine stage |
|---|---|---|
| `M_Library` | Scenario Library | 1 |
| `M_Intake` | Client Intake | 2 |
| `M_Bundle` | Bespoke Scenario Preparation (legacy naming) | 3 |
| `M_LiveRun` | Testing Target (legacy naming) | 4 |
| `M_Judge` | Judge | 5 |
| `M_Report` | Reporting (legacy naming) | 6 |
| `M_Dashboard` | Dashboard (non-spine support module) | N/A |

Naming rule:

- In commit titles, PR scopes, task IDs, and acceptance criteria use `M_*` IDs first.
- Friendly labels are allowed after ID, example: `M_Intake (Client Intake)`.

Planned alias migration (pending ADR-006 stub):
- `M_Bundle -> M_BespokePrep`
- `M_LiveRun -> M_TestTarget`
- `M_Report -> M_Reporting`

## 2) Verdict dictionary

### 2.1 Canonical (contract-first)

ADR-005 is accepted. Contract authority is:

- `INFRINGEMENT`
- `COMPLIANT`
- `UNDECIDED`

### 2.2 Legacy-to-canonical map (must be explicit)

| Legacy value | Canonical value |
|---|---|
| `VIOLATED` | `INFRINGEMENT` |
| `VIOLATION` | `INFRINGEMENT` |
| `NO_VIOLATION` | `COMPLIANT` |
| `PASS` | `COMPLIANT` |
| `UNCLEAR` | `UNDECIDED` |

Rule:

- Producers should emit canonical values.
- Legacy values are accepted only at ingress and must be normalized before artifact persistence.

## 3) Signal dictionary

Source of truth:

- `packages/specs/docs/contracts/taxonomy/signals.json`

Rule:

- Scenario files, judge outputs, and reports must use only IDs from this file.
- Any new signal ID requires taxonomy changelog update and contract review.

## 4) Stage A artifact dictionary (v0.1)

Allowed Stage A artifacts:

- `scenario.json`
- `transcript.json`
- `run_meta.json`
- `run_manifest.json`
- `checksums.sha256`

Disallowed in Stage A:

- `scores.json`
- `evidence_pack.json`

## 5) EP/PE dictionary

| Term | Meaning in this project |
|---|---|
| `EP` | Client-run product pipeline (execution, judge, reporting) |
| `PE` | Product evaluations/regression harness validating EP |

Monorepo location rule (this workspace):

- EP implementation: `packages/ep`
- PE implementation: `packages/pe`

## 6) Human-to-code translation table

| Friendly phrase | Use this in specs/PRs |
|---|---|
| Scenario Library | `M_Library` |
| Client Intake | `M_Intake` |
| Bespoke Prep | `M_Bundle` (until ADR-006 migration) |
| Testing Target | `M_LiveRun` (until ADR-006 migration) |
| Judge | `M_Judge` |
| Reporting | `M_Report` (until ADR-006 migration) |
| violation / violated | `INFRINGEMENT` (after normalization) |
| no violation / pass | `COMPLIANT` (after normalization) |
| unclear | `UNDECIDED` (after normalization) |

## 7) Enforcement hooks (next step)

1. Run taxonomy validator (strict):
   `python tools/validate_taxonomy_contracts.py`
2. Module-card/registry consistency gate is now wired through taxonomy validator.
3. Keep legacy verdict aliases only for backward compatibility input normalization, not for persisted schema outputs.
