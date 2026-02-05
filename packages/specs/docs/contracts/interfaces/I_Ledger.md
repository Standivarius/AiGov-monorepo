# Interface Ledger v0 (GDPR-only)

Scope: GDPR-only execution surfaces. Non-GDPR frameworks are out of scope unless later requested.
Determinism: interfaces must fail closed on invalid or ambiguous inputs; no silent fallbacks.

| Module | Inputs | Outputs | Guarantees | Unknowns | Tests |
| --- | --- | --- | --- | --- | --- |
| Intake | Intake output payload (client_intake_output_contract_v0_1.md) | validated intake output | context_profile is authoritative; legacy locale_context allowed; allowlisted jurisdiction/sector/policy packs; deterministic policy_pack_stack ordering | TBD: non-GDPR context extensions | aigov_ep.intake.validate.validate_intake_payload (planning-pack fixtures) |
| AIGov bundle | Deterministic scenario bundle (manifest.json v0.1.0 + sha256) | Scenario JSON files + manifest | Paths and hashes are verified; fails closed on mismatch or ambiguity | TBD: multi-scenario execution policy | tools/validate_bundle_integrity.py |
| Exporter | Bundle directory + manifest.json v0.1.0 | seed_instructions JSON list | Deterministic ordering; fails closed on invalid manifest or schema drift | TBD: future non-GDPR export formats | tools/validate_export_bundle_to_petri_seed_instructions_alpha.py |
| Inspect | seed_instructions + task args | inspect_logs | Deterministic command printing; fail closed on invalid args | TBD: CLI surface changes | tools/validate_print_inspect_petri_run_command.py |
| LiveRun (M_LiveRun) | seed_instructions + inspect_task_args | inspect_logs + petri_transcripts | Coordinates Inspect + Petri runs; no additional validation beyond component validators | TBD: runtime orchestration invariants | TBD (dedicated validator pending) |
| Petri | seed_instructions + audit runtime | petri_transcripts | Transcript outputs are required; missing outputs fail closed | TBD: transcript schema evolution | TBD (dedicated validator pending) |
| Scout | runtime logs + transcripts | findings report | Fail closed on missing required inputs; deterministic evaluation order | TBD: report schema and scoring policy | TBD (dedicated validator pending) |

## Validation Policy
- tools/validate_interface_ledger.py enforces: file exists, table header columns, required module rows, and minimum column count.
- It does NOT enforce: semantic correctness, referenced tool existence, or I/O contract reality.
