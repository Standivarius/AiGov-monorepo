# GPT Pro Workorder - Factory Discovery (v1)

Date: `2026-02-20`  
Owner: `Marius`  
Prepared by: `Codex`

## Goal

Produce high-confidence discovery dossiers for `M_Intake` and `M_Judge` using the attached repo snapshot, with explicit conflict handling and no silent assumptions.

## Operating constraints

1. Do not propose code changes.
2. Use only repository content from the uploaded snapshot.
3. Preserve canonical verdict vocabulary: `INFRINGEMENT`, `COMPLIANT`, `UNDECIDED`.
4. If a decision is contested, output ADR stub format only:
   - title
   - context
   - options
5. Keep output deterministic and structured.

## Required outputs

1. `packages/specs/docs/artifacts/2026-02-20/retrieval_index_v1.json`
2. `packages/specs/docs/artifacts/2026-02-20/m_intake_dossier_v1.md`
3. `packages/specs/docs/artifacts/2026-02-20/m_judge_dossier_v1.md`
4. `packages/specs/docs/artifacts/2026-02-20/retrieval_conflicts_v1.md`
5. `packages/specs/docs/artifacts/2026-02-20/open_decisions_for_adr_v1.md`

## Pre-run checks

1. Confirm all files in `packages/specs/docs/artifacts/2026-02-20__gptpro__artifact-manifest_v1.json` exist in the uploaded snapshot.
2. If any required file is missing, stop immediately and return a `missing_input_error` list with missing paths.
3. `packages/specs/docs/artifacts/2026-02-20__codex_briefing__factory-start.json` is mandatory and cannot be skipped.

## Extraction format requirements

For every extracted claim include:

- module_id
- claim_type
- claim_text
- source_path
- source_date (if available)
- source_kind
- confidence
- conflict_key

## Claim types (must cover all)

- scope
- input_contract
- output_contract
- invariant
- failure_mode
- evidence
- telemetry
- privacy
- security
- acceptance
- test_eval
- open_decision

## Priority source files

- `packages/specs/docs/contracts/modules/cards/M_Intake.card.json`
- `packages/specs/docs/contracts/modules/cards/M_Judge.card.json`
- `packages/specs/docs/contracts/taxonomy/verdicts.json`
- `packages/specs/docs/contracts/modules/module_registry_v0.yaml`
- `packages/specs/docs/decisions/ADR-005-verdict-label-canonicalization-v0.1.md`
- `packages/specs/docs/decisions/ADR-006-module-id-canonical-migration-v0.1.md`
- `packages/specs/docs/artifacts/2026-01-29__alpha__client-intake-bundles.md`
- `packages/specs/docs/artifacts/2026-02-03_GDPR_Execution_Planning.md`
- `packages/specs/docs/artifacts/2026-02-05_GDPR_Execution_Planning.md`
- `packages/specs/docs/artifacts/2026-02-20/taxonomy_inventory_v0.md`
- `packages/specs/docs/artifacts/2026-02-20/taxonomy_conflicts_v0.md`
- `packages/specs/docs/artifacts/2026-02-20/taxonomy_progress_status_v1.md`

## Conflict resolution policy

When claims conflict:

1. Prefer contract/ADR over chat/planning text.
2. Prefer newer dated source over older.
3. Prefer merged-PR source over unmerged draft source.
4. Between `planning` and `chat_artifact`, prefer `planning`.
5. If unresolved, keep both conflicting claims and put the decision in `packages/specs/docs/artifacts/2026-02-20/open_decisions_for_adr_v1.md`.

## Acceptance checks

1. Every claim in dossiers has a source.
2. Every conflict is either resolved or listed as open decision.
3. No deprecated verdict labels appear in final dossiers.
4. Output is readable by a non-coder founder.
