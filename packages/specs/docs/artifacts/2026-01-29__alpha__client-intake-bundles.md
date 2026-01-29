# Client intake → overrides → bundle (alpha)

## Scope
- GDPR-only alpha workflow for building scenario overrides and a deterministic bundle from client intake JSON.
- Any tools referenced that do not exist yet are marked as Planned.

## What exists today
- Deterministic compiler entrypoint: `packages/ep/aigov_ep/scenario/compiler.py` (`compile_bundle`).
- Intake validation is defined in `packages/ep/aigov_ep/intake/validate.py` (`validate_intake_payload`).
- Override generation is defined in `packages/ep/aigov_ep/scenario/override.py` (`generate_override`).

## Planned tools (not yet on main)
- `tools/build_client_bundle.py` — Planned (Milestone 2).

## Determinism expectations
- Determinism is defined as: **bundle_hash is stable across runs for the same inputs**.
- Note: `manifest.json` may include output-path fields, so compare `bundle_hash` when checking determinism.

## Failure modes (examples)
- Intake payload fails validation in `validate_intake_payload` (see `packages/ep/aigov_ep/intake/validate.py`).
- Override generation fails for a scenario in `generate_override` (see `packages/ep/aigov_ep/scenario/override.py`).
- Bundle compilation fails in `compile_bundle` (see `packages/ep/aigov_ep/scenario/compiler.py`).

## Inputs and outputs (alpha)
- Input: client intake JSON payload (contracted by `client_intake_output_contract_v0_1.md`).
- Output: per-scenario override JSONs and a compiled bundle with `manifest.json` + `bundle_hash`.
