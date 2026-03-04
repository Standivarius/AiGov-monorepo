# AiGov Reset Plan v2 (Consistency-Corrected, Task-List Anchored)

## Summary
This plan is explicitly anchored to the original task list:

- Source baseline: `C:\Users\User\OneDrive - DMR Ergonomics\CODEX_TASK_LIST_2026-03-04_1.md`

It keeps the original Stage 1-5 structure and task numbering, then applies only approved corrections from your latest decisions and Claude’s final adjustments.

## Consistency fixes applied
1. Added explicit source reference to original task list as the base authority.
2. Resolved Task 1.1 vs 1.2 conflict with sequential semantics:
- Task 1.1 can leave empties.
- Task 1.2 fills empties via semantic fallback.
3. Updated Task 2.2 model to `google/gemini-3-flash-preview`.
4. Updated Task 3.1 to include principles + human-readable rationale.
5. Replaced L1/L2/L3 naming with P0/P1/P2.
6. Added mandatory holdout as Stage 2.4 (your decision).
7. Kept old method docs active where valid, with explicit supersession notes for changed parts.

## Locked decisions (final)
1. Execution base: `origin/main`.
2. Canonical task list location: `packages/specs/docs/planning/2026-03-04-method/`.
3. Canonical model for Task 2.2: `google/gemini-3-flash-preview`.
4. Judge context packs naming:
- P0 Principles Pack
- P1 Domain Requirement Pack
- P2 Case Procedure Pack
5. Holdout gate is mandatory at Stage 2.4.
6. AGENTS strategy: Lean Router with progressive disclosure packs.

## Stage 0 (new, before original Stage 1)
1. Workspace reset.
- Record base commit from `origin/main`.
- Mark stale branch as non-authoritative for new execution.
2. Canonical task authority reset.
- Create `CODEX_TASK_LIST_v2.md` in `packages/specs/docs/planning/2026-03-04-method/`.
- Preserve original Stage/Task IDs and numbering.
3. AGENTS router reset.
- Keep PM/EX, source-of-truth order, triage rules, lean evidence policy.
- Add references to:
- `PM_GDPR_AUDITOR_PLAYBOOK_v1.md`
- `JUDGE_CONTEXT_PACKS_v1.md`
- `SKILL_ORCHESTRATION_CONTRACT_v1.md`
4. Method supersession note.
- Keep 2026-02-22 docs.
- Add one “active vs superseded” map to eliminate conflicts.

## Stage 1 (original Stage 1, corrected)
1. Task 1.1 EDPB relevance filter.
- Keep as v0.1 stopgap.
- Output filtered map with cap policy.
2. Task 1.2 empty mappings semantic fallback.
- Scope explicitly limited to the 12 calibration cases.
- After this task, all 12 should have at least one mapping.
3. Task 1.3 runner default source.
- Runner uses filtered mapping by default.
- Optional unfiltered switch remains for comparison.

## Stage 2 (original Stage 2, corrected + one added gate)
1. Task 2.1 full 12-case A/B on Mistral Large (filtered context).
2. Task 2.2 full 12-case A/B on Gemini 3 Flash preview (filtered context).
3. Task 2.3 model comparison summary.
4. Task 2.4 holdout gate (new, mandatory).
- Run same prompt variants on unseen holdout set.
- No baseline quality claim if holdout gate fails.

## Stage 3 (original Stage 3, corrected)
1. Gate to enter Stage 3 remains:
- Proceed only if enriched is non-inferior or better under Stage 2 criteria.
2. Task 3.1 prompt extraction/refactor.
- Externalize prompt templates.
- Add P0 always-loaded principles.
- Add requirement for human-readable rationale tied to evidence.
3. Task 3.2 enrich flag integration into runner/CLI.
- Backward-compatible generic mode.
- Enriched mode injects P0/P1/P2 packs.
4. Task 3.3 rerun TEST-J03 in both modes and compare.

## Stage 4 (original Stage 4)
1. Keep micro-PR split hygiene.
2. Keep scripts-only policy where already defined.
3. Keep ordered merge discipline and independent reviewability targets.

## Stage 5 (original Stage 5)
1. Keep current parked items parked.
2. Add one explicit note:
- P0/P1/P2 semantic selection scaling for 200+ golden sets is parked for Bespoke-phase design, not solved by Stage 1 stopgaps.

## AGENTS.md reset specification (explicit)
1. Keep:
- source-of-truth hierarchy
- PM/EX switch rule
- method lock references
- triage requirement
- lean logging constraints
2. Add:
- “Canonical task authority file” path
- “Execution base branch rule” (`origin/main`)
- “Context pack router” section with progressive disclosure order:
- P0 always
- P1 by scenario family
- P2 by case
- “Claim policy” section:
- calibration-only = engineering signal
- calibration + holdout = quality claim
3. Do not add:
- bulky legal rule dumps
- full auditor methodology inline in AGENTS

## Public interfaces/types/contracts impacted
1. Judge prompt contract:
- P0/P1/P2 fields and rationale requirements.
2. Runner CLI contract:
- `--enrich` behavior stays explicit and backward-compatible.
3. Evaluation contract:
- Add holdout report artifact requirement before quality claims.
4. Task governance contract:
- Every task must include input paths, output paths, acceptance gate, dependency IDs.

## Test scenarios and acceptance
1. Governance acceptance.
- Task list v2 exists and is referenced by AGENTS.
- Supersession map exists and removes method conflicts.
2. Mapping acceptance.
- Stage 1.1 outputs filtered mappings.
- Stage 1.2 resolves previously empty mappings for the 12-case set.
3. Runner acceptance.
- Generic and enriched modes both pass schema checks.
4. Quality acceptance.
- Stage 2 comparison report produced.
- Stage 2.4 holdout gate report produced.
- No quality claim if holdout fails.

## Assumptions/defaults
1. `origin/main` is the execution truth for next cycle.
2. Rule-cap remains a v0.1 anti-flooding guardrail, not final semantics.
3. Semantic scalable rule selection belongs to Bespoke-phase evolution.
4. GitHub Project remains tracking surface; canonical sequencing remains in repo task list v2.
