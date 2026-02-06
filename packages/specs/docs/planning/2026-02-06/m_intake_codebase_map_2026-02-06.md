# M_Intake Codebase Map (v2026-02-06)

## Objective
Map the AiGov pipeline end-to-end (modules, artifacts, schemas, validators, PE gates) and identify where M_Intake will slot in and what it will feed.

## Scope and constraints
- Docs-only mapping: no implementation or refactors.
- Commands restricted to read-only enumeration (`ls`, `find`, `rg`, `sed -n`, `cat`, `python -c`).
- Every claim includes concrete file paths.

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

## File-level inventory
### Schemas (packages/specs/schemas) matching intake/bundle/context
- `packages/specs/schemas/client_intake_v0_2.schema.json`
- `packages/specs/schemas/gdpr_bundle_scenario_v0.schema.json`

### Contract docs (packages/specs/docs/contracts) for intake/context/taxonomy
- `packages/specs/docs/contracts/intake/README.md`
- `packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md`
- `packages/specs/docs/contracts/taxonomy/README.md`
- `packages/specs/docs/contracts/taxonomy/CHANGELOG.md`
- `packages/specs/docs/contracts/taxonomy/client_constraints_v0.json`
- `packages/specs/docs/contracts/taxonomy/dsar_channels_v0.json`
- `packages/specs/docs/contracts/taxonomy/evidence_schema.md`
- `packages/specs/docs/contracts/taxonomy/jurisdictions_v0.json`
- `packages/specs/docs/contracts/taxonomy/policy_packs_v0.json`
- `packages/specs/docs/contracts/taxonomy/pre2.2/Pre2.2-TAXONOMY-Pro-Run.md`
- `packages/specs/docs/contracts/taxonomy/pre2.2/README.md`
- `packages/specs/docs/contracts/taxonomy/sectors_v0.json`
- `packages/specs/docs/contracts/taxonomy/signals.json`
- `packages/specs/docs/contracts/taxonomy/signals.meta.json`
- `packages/specs/docs/contracts/taxonomy/verdicts.json`
- `packages/specs/docs/contracts/modules/cards/M_Intake.card.json`

### EP runtime validation (packages/ep/aigov_ep/intake + intake validator entrypoints)
- `packages/ep/aigov_ep/intake/__init__.py`
- `packages/ep/aigov_ep/intake/validate.py`
- `packages/ep/aigov_ep/cli.py` (CLI entrypoint wiring `validate_intake`)

### PE gates + fixtures (intake-related)
- `packages/pe/tests/intake/test_intake_validation.py`
- `tools/fixtures/validators/client_intake_v0_2_fail.json`
- `tools/fixtures/validators/client_intake_v0_2_fail_channel_mismatch.json`
- `tools/fixtures/validators/client_intake_v0_2_fail_empty_supported.json`
- `tools/fixtures/validators/client_intake_v0_2_pass.json`
- `tools/fixtures/validators/intake_output_context_fail_locale_context_null.json`
- `tools/fixtures/validators/intake_output_context_fail_pack_order.json`
- `tools/fixtures/validators/intake_output_context_fail_unknown_jurisdiction.json`
- `tools/fixtures/validators/intake_output_context_fail_unknown_sector.json`
- `tools/fixtures/validators/intake_output_context_pass_legacy_locale_only_nl.json`
- `tools/fixtures/validators/intake_output_context_pass_nl_healthcare.json`
- `tools/fixtures/validators/intake_output_context_pass_nl_public.json`

## Deterministic ordering + fail-closed enforcement points (expected locations)
- Determinism must be enforced at schema validation and runtime artifact serialization layers; candidate enforcement locations are within `packages/ep/aigov_ep/` and schema definitions under `packages/specs/schemas/`.
- Fail-closed behavior is expected at runtime validation sites in `packages/ep/aigov_ep/`, with schema strictness defined in `packages/specs/schemas/`.

## Uncertainties / stop conditions
- Inventory is limited to filename matching and known intake taxonomy files; deeper semantic coupling requires content review.
- If additional intake-related schemas or contracts exist without intake/bundle/context naming, they may need a follow-on pass.

## Checkpoint
- Files changed: `packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md`
- Commands run:
  - `ls`
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_constitution_2026-02-06.md`
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_codex_runbook_2026-02-06.md`
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_task_pack_2026-02-06.md`
  - `find packages/specs/schemas -type f | rg -i 'intake|bundle|context'`
  - `find packages/specs/docs/contracts -type f | rg -i 'intake|context|taxonomy'`
  - `find packages/ep/aigov_ep/intake -type f`
  - `rg -n "intake" packages/ep/aigov_ep`
  - `find packages/pe/tests -type f | rg -i "intake"`
  - `find tools/fixtures/validators -type f | rg -i '^(.*\\/)?(intake_|client_intake_)'`
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md`
  - `cat <<'EOF' > packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md` (this update)
- Results: N/A (docs-only mapping; no proofs executed)
- Risks/unknowns:
  - Inventory is based on filename matches; may miss intake-related artifacts not labeled with intake/bundle/context.
- Next task:
  - Validate whether additional intake-adjacent schemas/contracts exist outside naming match criteria.
  - Proceed to Task 2 (OPA OSS candidate analysis) if inventory is sufficient.
