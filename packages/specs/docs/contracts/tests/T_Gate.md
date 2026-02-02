# T_Gate v0.1 (Tests/Evals)

Purpose: PE/EP dashboard/list.

This document enumerates evalsets and how to run them, based on the canonical
registries in `packages/specs/docs/planning/2026-01-22-run/`.

## Evalsets

| evalset_id | tier | description | command to run |
| --- | --- | --- | --- |
| audit_pack | audit_pack | Audit pack checks for Tier A controls | run-evalset audit_pack |
| pe_nightly | nightly | Nightly pipeline checks (Stage A/B + retrieval + evidence packs) | run-evalset pe_nightly |
| pe_pr_gate_short | pr_gate | PR-gate short checks (schema + determinism + contract drift) | run-evalset pe_pr_gate_short |
| pe_release | release | Release gate checks (exports + citation integrity + Tier A release controls) | run-evalset pe_release |

## Judge performance evalset

This repo does not yet define a dedicated judge performance evalset. When it
exists, add it to `evalsets_registry.yaml` and update the table above.
