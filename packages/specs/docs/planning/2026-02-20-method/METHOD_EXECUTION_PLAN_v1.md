# Method Execution Plan v1

Date: `2026-02-20`  
Objective: run method-first setup to completion before PRD drafting or implementation.

## Canonical board

- GitHub Project: `AiGov_Factory_Execution_Board`
- URL: `https://github.com/users/Standivarius/projects/5`
- Gate issue chain: `#194` -> `#195` -> `#196` -> `#197` -> `#198`

## Phase A - Method lock

Deliverables:
- `METHOD_SELECTION_MEMO_v1.md`
- `AIGOV_FACTORY_METHOD_v1.md`

Exit criteria:
- method option explicitly selected,
- stage gates accepted.

## Phase B - Pre-PRD Discovery completion

Deliverables:
- `PRE_PRD_DISCOVERY_PACK_v0.md`
- `PRE_PRD_CHECKLIST_v0.md`
- Example map files from template
- first Scenario Pack instance aligned to spec
- Retrieval outputs from issues `#199`, `#200`, and `#201`:
  - `packages/specs/docs/artifacts/2026-02-20/retrieval_index_v1.json`
  - `packages/specs/docs/artifacts/2026-02-20/m_intake_dossier_v1.md`
  - `packages/specs/docs/artifacts/2026-02-20/m_judge_dossier_v1.md`
  - `packages/specs/docs/artifacts/2026-02-20/retrieval_conflicts_v1.md`
  - `packages/specs/docs/artifacts/2026-02-20/open_decisions_for_adr_v1.md`
- GPT Pro output ingestion from issue `#202`

Exit criteria:
- Pre-PRD checklist passes,
- unresolved blocker questions = 0 for walking skeleton (`factory:blocker` issues under `#199`-`#202` are all closed),
- approval recorded.

## Phase C - PRD compilation and authorization gates (still no coding)

Action:
- produce and approve `PRD-P`, `PRD-M`, and `PRD-E` baseline.

Gate mapping:
- G2: `PRD-P` + all `PRD-M` approved.
- G3: `PRD-E` approved with validator baseline.

Exit criteria:
- explicit gate record that Pre-PRD is complete,
- explicit gate record that `PRD-P`, `PRD-M`, and `PRD-E` are approved.

## Phase D - Build readiness decision (still no coding in this plan)

Action:
- evaluate whether implementation can start, but do not start it in this plan.

Exit criteria:
- approved build-readiness record with first slice and proof commands.

## Out of scope for this plan

- Any implementation milestone kickoff
- Any architecture refactor in code
- Any new runtime features
