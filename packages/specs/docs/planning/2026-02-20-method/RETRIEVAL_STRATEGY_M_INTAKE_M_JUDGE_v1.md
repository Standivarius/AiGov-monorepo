# Retrieval Strategy (M_Intake + M_Judge) v1

Date: `2026-02-20`  
Scope: Pre-PRD discovery retrieval only (no coding)  
Related issues: `#199`, `#200`, `#201`, `#202`

## Objective

Extract highest-signal historical knowledge for `M_Intake` and `M_Judge` from existing planning/chat artifacts, then normalize it into deterministic dossier artifacts that can be reviewed and approved.

## Retrieval corpus (priority order)

1. `packages/specs/docs/contracts/modules/cards/M_Intake.card.json`
2. `packages/specs/docs/contracts/modules/cards/M_Judge.card.json`
3. `packages/specs/docs/contracts/taxonomy/verdicts.json`
4. `packages/specs/docs/contracts/modules/module_registry_v0.yaml`
5. `packages/specs/docs/decisions/ADR-005-verdict-label-canonicalization-v0.1.md`
6. `packages/specs/docs/decisions/ADR-006-module-id-canonical-migration-v0.1.md`
7. `packages/specs/docs/artifacts/2026-01-29__alpha__client-intake-bundles.md`
8. `packages/specs/docs/artifacts/2026-02-03_GDPR_Execution_Planning.md`
9. `packages/specs/docs/artifacts/2026-02-05_GDPR_Execution_Planning.md`
10. `packages/specs/docs/artifacts/2026-02-20/taxonomy_inventory_v0.md`
11. `packages/specs/docs/artifacts/2026-02-20/taxonomy_conflicts_v0.md`
12. `packages/specs/docs/artifacts/2026-02-20/taxonomy_progress_status_v1.md`
13. `packages/specs/docs/artifacts/2026-02-20__codex_briefing__factory-start.json`

Authoritative input list:
- `packages/specs/docs/artifacts/2026-02-20__gptpro__artifact-manifest_v1.json`

## Extraction schema

Each extracted claim should be stored with:

- `module_id`: `M_Intake` or `M_Judge`
- `claim_type`: one of `scope`, `input_contract`, `output_contract`, `invariant`, `failure_mode`, `evidence`, `telemetry`, `privacy`, `security`, `acceptance`, `test_eval`, `open_decision`
- `claim_text`: normalized one-sentence statement
- `source_path`: repo-relative file path
- `source_date`: parsed from filename/date header if available
- `source_kind`: `contract`, `decision`, `planning`, `chat_artifact`
- `confidence`: `high | medium | low`
- `conflict_key`: deterministic key used to detect contradictory claims

## Conflict policy

When two claims conflict on the same `conflict_key`, resolve using:

1. Contract/ADR source over chat/planning source.
2. Newer dated source over older source.
3. Merged PR source over unmerged draft source.
4. Between `planning` and `chat_artifact`, prefer `planning`.

If still unresolved, keep both competing claims and emit an ADR-stub candidate under `open_decision` and `open_decisions_for_adr_v1.md`.

## Required outputs

- `packages/specs/docs/artifacts/2026-02-20/retrieval_index_v1.json`
- `packages/specs/docs/artifacts/2026-02-20/m_intake_dossier_v1.md`
- `packages/specs/docs/artifacts/2026-02-20/m_judge_dossier_v1.md`
- `packages/specs/docs/artifacts/2026-02-20/retrieval_conflicts_v1.md`
- `packages/specs/docs/artifacts/2026-02-20/open_decisions_for_adr_v1.md`

## Definition of done

1. At least one sourced claim exists for every `claim_type` required by module-card drafting.
2. No unresolved high-severity conflict remains outside ADR-stub candidates.
3. Dossiers only use canonical verdict values: `INFRINGEMENT`, `COMPLIANT`, `UNDECIDED`.
4. Dossiers clearly separate accepted claims vs open decisions.
5. `open_decisions_for_adr_v1.md` exists and every unresolved conflict is listed there.
