# M_Intake Phase 2 Open Items Report (2026-02-08)

## Update (2026-02-08)
- PR `#154` scope drift is resolved; it is now planning-only with 4 changed files.
- Review-pack artifacts were moved to PR `#160` (`pr6-phase2-reviews`).
- MUST count is `0`.
- SHOULD polish items are addressed by PR `pr7-phase2-polish` (this docs/tracking slice).

## 1) Current State Summary
- Branch inspected: `pr5-phase2-planning`
- HEAD: `851b06a3357df57eedb4a1ce96a3369cb3a8d130`
- Snapshot time (UTC): `2026-02-08T21:28:46Z`

Recent commits:
- `851b06a` Merge pull request #159 from Standivarius/pr10-phase2-review-pack-v1
- `e9b2812` Planning: add Claude review pack v1 for Phase 2 PR stack
- `60341c0` Merge pull request #155 from Standivarius/pr6-phase2-followup-schemas
- `29edc42` Follow-up: relax stage ID caps and bound readiness notes
- `bac0fbb` Merge branch 'pr4-phase2-docs' into pr5-phase2-planning

Local proof commands:
- `python3 tools/validate_planning_pack.py`: PASS
- `bash tools/run_pr_gate_validators.sh`: PASS
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`: PASS
- Latest migration-smoke log: `docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260208_212654.log`

PR stack status (#150-#154):
1. `#150` https://github.com/Standivarius/AiGov-monorepo/pull/150
   - mergeable: `MERGEABLE`
   - checks: all PASS
   - reviews/comments: no requested changes, no comments
   - changed files: 6
2. `#151` https://github.com/Standivarius/AiGov-monorepo/pull/151
   - mergeable: `MERGEABLE`
   - checks: all PASS
   - reviews/comments: no requested changes, no comments
   - changed files: 6
3. `#152` https://github.com/Standivarius/AiGov-monorepo/pull/152
   - mergeable: `MERGEABLE`
   - checks: all PASS
   - reviews/comments: no requested changes, no comments
   - changed files: 6
4. `#153` https://github.com/Standivarius/AiGov-monorepo/pull/153
   - mergeable: `MERGEABLE`
   - checks: all PASS
   - reviews/comments: no requested changes, no comments
   - changed files: 2
5. `#154` https://github.com/Standivarius/AiGov-monorepo/pull/154
   - mergeable: `MERGEABLE`
   - checks: all PASS
   - reviews/comments: no requested changes, no comments
   - changed files currently shown by PR: 10

## 2) MUST FIX (Blocks Merge)
1. PR `#154` scope/size drift
- PR: `#154`
- File paths currently in `gh pr diff --name-only #154` include planning files plus extra review-pack and schema files:
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_codex_roadmap.md`
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_milestone_report.md`
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_review_prompt_claude.md`
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_review_prompt_gemini.md`
  - `packages/specs/docs/planning/2026-02-08/reviews/claude_review_evidence_v1.md`
  - `packages/specs/docs/planning/2026-02-08/reviews/claude_review_pack_v1.md`
  - `packages/specs/docs/planning/2026-02-08/reviews/claude_review_prompt_v1.txt`
  - `packages/specs/schemas/intake_bundle_gap_v0_1.schema.json`
  - `packages/specs/schemas/intake_bundle_readiness_v0_1.schema.json`
  - `packages/specs/schemas/intake_bundle_reconcile_v0_1.schema.json`
- Symptom:
  - PR #154 is no longer the original “planning-only” slice and currently exceeds the milestone reviewability guardrail (`<=6 files/PR`).
- Minimal fix approach:
  - Replace #154 with a clean planning-only PR (4 files) based on `pr4-phase2-docs` + planning commit only, then keep review-pack/schema follow-ups out of milestone stack closure.

## 3) SHOULD FIX (Before Milestone Close)
1. Stage artifacts contract does not explicitly document deferred cross-artifact referential checks
- PR: `#153`
- File: `packages/specs/docs/contracts/intake/intake_bundle_stage_artifacts_v0_1.md`
- Symptom:
  - Contract is deterministic/fail-closed but does not clearly state what evidence-reference checks are deferred to parent-bundle composition.
- Minimal fix approach:
  - Add explicit boundary language in stage-artifact contract doc (docs-only).

2. Roadmap tracking metadata is stale (`PR #: TBD`, legacy branch names)
- PR: `#154`
- File: `packages/specs/docs/planning/2026-02-08/m_intake_phase2_codex_roadmap.md`
- Symptom:
  - Completion-tracking section still has placeholder PR numbers and old branch identifiers.
- Minimal fix approach:
  - Update completion-tracking entries with actual PR numbers/branches/proof references.

## 4) COULD
1. Schema strictness tradeoff review (non-blocking)
- PRs: `#150-#152`
- Files:
  - `packages/specs/schemas/intake_bundle_reconcile_v0_1.schema.json`
  - `packages/specs/schemas/intake_bundle_gap_v0_1.schema.json`
  - `packages/specs/schemas/intake_bundle_readiness_v0_1.schema.json`
- Symptom:
  - Current constraints may be stricter than some future payload shapes (for example: reconcile `left_value/right_value` as strings only; gap requires at least one clarification question).
- Minimal fix approach:
  - Keep as accepted risk for milestone, or document rationale explicitly in contracts.

## 5) Merge Plan
- Safe to merge `#150` now: **YES**.
- Does stack need rebase: **Not for #150-#153**; **#154 should be replaced/cleaned** due scope drift.
- Recommended merge order for milestone stack: `#150 -> #151 -> #152 -> #153 -> (cleaned #154)`.

## 6) Smallest Fix PR Slices (<=6 files each)
Because MUST/SHOULD are non-empty, use minimal follow-up slices:

### Slice A (MUST): Replace/clean PR #154 as planning-only
- Max files: 4
- Files:
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_codex_roadmap.md`
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_milestone_report.md`
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_review_prompt_claude.md`
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_review_prompt_gemini.md`
- Acceptance criteria:
  - PR contains only planning artifacts intended for milestone closeout.
  - File count <= 6.
  - No schema/review-pack additions in this PR.
- Proof commands:
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`

### Slice B (SHOULD): Stage-artifact contract boundary clarification
- Max files: 1
- File:
  - `packages/specs/docs/contracts/intake/intake_bundle_stage_artifacts_v0_1.md`
- Acceptance criteria:
  - Explicitly states stage-level enforcement vs deferred composition checks.
- Proof commands:
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`

### Slice C (SHOULD): Roadmap tracking metadata refresh
- Max files: 1
- File:
  - `packages/specs/docs/planning/2026-02-08/m_intake_phase2_codex_roadmap.md`
- Acceptance criteria:
  - PR numbers/branch names/proof references are current and complete.
- Proof commands:
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`
