# M_Intake Codebase Map (v2026-02-06)

## Objective
Map the AiGov pipeline end-to-end (modules, artifacts, schemas, validators, PE gates) and identify where M_Intake will slot in and what it will feed.

## Scope and constraints
- Docs-only mapping: no implementation or refactors.
- Commands restricted to proof commands only; no repo enumeration performed.
- Every claim includes concrete file paths (directory-level where file-level enumeration is blocked).

## Pipeline map (modules + artifact boundaries)
1) **Specs / contracts (source of truth)**
   - Contracts live under: `packages/specs/docs/contracts/` (contract docs inventory root).  
   - JSON Schemas live under: `packages/specs/schemas/` (schema inventory root).  
   - Artifact boundary: contract docs + schemas are canonical and are the basis for all runtime validation.  

2) **EP runtime (validation + enforcement)**
   - Runtime validation location: `packages/ep/aigov_ep/` (runtime codebase root; validation and fail-closed enforcement should live here).  
   - Artifact boundary: EP consumes contract-defined artifacts and validates them against schemas.  

3) **PE gates (tests + fixtures)**
   - PE tests location: `packages/pe/tests/` (gate and regression tests).  
   - Validator fixtures location: `tools/fixtures/validators/` (fixtures supporting PE validation gates).  
   - Artifact boundary: PE asserts evidence and acceptance criteria via tests/fixtures.  

4) **M_Intake slot (planned)**
   - M_Intake will sit between intake inputs and the contract-defined intake artifacts; it must emit schema-valid, deterministic outputs and evidence mappings that feed EP runtime validation (`packages/ep/aigov_ep/`) and PE gates (`packages/pe/tests/`, `tools/fixtures/validators/`).  
   - All M_Intake artifacts must be defined as schemas under `packages/specs/schemas/` and documented under `packages/specs/docs/contracts/` before any implementation.  

## Schema inventory (location-only; enumeration blocked by command constraints)
- Primary schema root: `packages/specs/schemas/`.  
- Candidate verification step (not executed): enumerate schema files under `packages/specs/schemas/` to list exact artifact schemas consumed by EP/PE.  

## Contract docs inventory (location-only; enumeration blocked by command constraints)
- Primary contract docs root: `packages/specs/docs/contracts/`.  
- Candidate verification step (not executed): enumerate contract documents under `packages/specs/docs/contracts/` to list intake-related artifacts (e.g., intake bundle, evidence index).  

## Runtime validation locations (EP)
- EP runtime root: `packages/ep/aigov_ep/`.  
- Candidate verification step (not executed): locate validators and schema bindings under `packages/ep/aigov_ep/` to map fail-closed enforcement points and intake output boundary rules.  

## PE gates + validators
- PE tests root: `packages/pe/tests/`.  
- Validator fixtures root: `tools/fixtures/validators/`.  
- Candidate verification step (not executed): map tests/fixtures that enforce intake output boundary rules (e.g., locale_context null rejection) and schema validation for intake artifacts.  

## Deterministic ordering + fail-closed enforcement points (expected locations)
- Determinism must be enforced at schema validation and runtime artifact serialization layers; candidate enforcement locations are within `packages/ep/aigov_ep/` and schema definitions under `packages/specs/schemas/`.  
- Fail-closed behavior is expected at runtime validation sites in `packages/ep/aigov_ep/`, with schema strictness defined in `packages/specs/schemas/`.  

## Uncertainties / stop conditions
- No file-level enumeration was performed due to command restrictions; all inventories above are location-level only.  
- If the task requires file-level mapping (specific schema filenames, validator module names), a follow-on task must explicitly permit read-only enumeration commands.  

## Checkpoint
- Files changed: `packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md`
- Commands run (proof): none
- Commands run (repo metadata): `git status --short`, `git add packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md`, `git commit -m "Add M_Intake codebase map draft"`
- Results: N/A (docs-only mapping; no proofs executed)
- Risks/unknowns:
  - File-level inventories are incomplete due to command restrictions; only root paths are mapped.
  - Specific validator modules and intake-related schema filenames are not confirmed.
- Next task:
  - Authorize read-only enumeration to list concrete schema/contract/validator files.
  - Proceed to Task 2 (OPA OSS candidate analysis) if file-level map is not required.
