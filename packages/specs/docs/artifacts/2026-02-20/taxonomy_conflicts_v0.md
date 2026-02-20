# Taxonomy Conflicts v0

Snapshot SHA: `11e3072cfa8a429fb809c02c58ed56d0551184cb`  
Date: `2026-02-20`

This file lists taxonomy and naming conflicts that can cause drift or broken gates.

## P0 (resolved in this update; retained for traceability)

### C-001 Verdict canonical mismatch across contract, schema, and runtime

- Contract canonical (`packages/specs/docs/contracts/terminology.md`, `packages/specs/docs/contracts/taxonomy/verdicts.json`):
  - `INFRINGEMENT | COMPLIANT | UNDECIDED`
- Behaviour schema (`packages/specs/schemas/behaviour_json_v0_phase0.schema.json`):
  - `VIOLATED | COMPLIANT | UNDECIDED`
- Runtime internals (`packages/ep/aigov_ep/judge/judge.py`, `packages/pe/aigov_eval/judge_output_mapper.py`):
  - internal `VIOLATION | NO_VIOLATION | UNCLEAR` mapped to schema `VIOLATED | COMPLIANT | UNDECIDED`

Impact (before fix):

- Same semantic verdict had three labels across layers.
- High risk for false gate failures, mapper bugs, and audit confusion.

Status:

- Resolved by `ADR-005-verdict-label-canonicalization-v0.1.md` (accepted 2026-02-20).
- Schema enums, producer outputs, mapper outputs, and fixtures now use canonical verdict labels:
  - `INFRINGEMENT | COMPLIANT | UNDECIDED`
- Legacy verdict labels remain only in explicit alias maps for backward-compatible input normalization.
- Validator baseline after fix:
  - `python tools/validate_taxonomy_contracts.py` => pass

## P1 (should resolve in same planning window)

### C-002 Module registry exists but is not yet gate-enforced

- Registry file now exists:
  - `packages/specs/docs/contracts/modules/module_registry_v0.yaml`
- No planning validator/CI check currently enforces use of its `M_*` IDs.

Impact:

- Naming can still drift if contributors skip the registry.

### C-003 Module ID taxonomy migration aliases are not yet normalized in existing docs

- Registry locks canonical IDs, but historical docs still use mixed terms (`Bundle`, `LiveRun`, `Report`) without `M_*` first-token convention.

Impact:

- Traceability queries still miss records unless alias rules are manually applied.

### C-004 Intake terminology includes schema contract, but runtime validator is still skeleton

- Contract and plan assume intake validation as a real gate.
- Runtime file `packages/ep/aigov_ep/intake/validate.py` is currently `NotImplementedError`.

Impact:

- Terminology and gate language imply behavior that is not yet enforceable in code.

## P2 (cleanup to prevent future re-drift)

### C-005 Duplicate behaviour schema copies across specs/EP/PE

Current copies:

- `packages/specs/schemas/behaviour_json_v0_phase0.schema.json`
- `packages/ep/aigov_ep/contracts/behaviour_json_v0_phase0.schema.json`
- `packages/pe/aigov_eval/contracts/behaviour_json_v0_phase0.schema.json`

Impact:

- Multiple copies increase drift probability on enums/fields.

### C-006 EP/PE naming text still includes legacy multi-repo placement

- `terminology.md` is now monorepo-aligned.
- Legacy repo-name placement terms still appear in historical program docs (`packages/specs/docs/program/*` and related planning references).

Impact:

- New contributors can read conflicting location language depending on document entry point.

## Resolution order (recommended)

1. Resolve `C-001` via `ADR-005` and lock one verdict vocabulary path.
2. Enforce module registry usage in validator/CI and normalize legacy naming in docs (`C-002`, `C-003`).
3. Align terminology with actual monorepo structure and reduce schema duplication (`C-005`, `C-006`).
4. Keep intake gate language synchronized with runtime maturity (`C-004`).
