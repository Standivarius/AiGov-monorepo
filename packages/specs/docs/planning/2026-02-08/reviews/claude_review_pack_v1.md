# Claude Review Pack v1 (Gemini-style second pass)

## A) Milestone intent (one-paragraph overview)
Phase D (`intake_bundle_v0_1`) already exists; this Phase 2 stack adds deterministic, fail-closed workflow-stage boundary artifacts around that canonical spine (`reconcile`, `gap`, `readiness`) with strict schemas, stdlib validators, fixtures, and planning-pack gate wiring. Scope is contract/validator/gating only: no runtime workflow engine, no OPA execution runtime, no PAR adapter implementation, and no LLM council/multi-agent extraction.

## B) PR stack map (#150 -> #154)
1. PR #150: https://github.com/Standivarius/AiGov-monorepo/pull/150
   Base/Head: `main` <- `pr1-phase2-reconcile`
   - adds `intake_bundle_reconcile_v0_1` schema
   - adds reconcile fixtures + reconcile-specific policy checks
   - wires reconcile checks into planning-pack gate

2. PR #151: https://github.com/Standivarius/AiGov-monorepo/pull/151
   Base/Head: `pr1-phase2-reconcile` <- `pr2-phase2-gap`
   - adds `intake_bundle_gap_v0_1` schema
   - adds gap fixtures + question-order policy checks
   - wires gap checks into planning-pack gate

3. PR #152: https://github.com/Standivarius/AiGov-monorepo/pull/152
   Base/Head: `pr2-phase2-gap` <- `pr3-phase2-readiness`
   - adds `intake_bundle_readiness_v0_1` schema
   - adds readiness fixtures + blocked/ready policy checks
   - wires readiness checks into planning-pack gate

4. PR #153: https://github.com/Standivarius/AiGov-monorepo/pull/153
   Base/Head: `pr3-phase2-readiness` <- `pr4-phase2-docs`
   - adds stage-artifact contract doc
   - links stage-artifact contract from main intake bundle contract

5. PR #154: https://github.com/Standivarius/AiGov-monorepo/pull/154
   Base/Head: `pr4-phase2-docs` <- `pr5-phase2-planning`
   - adds roadmap, milestone report, and review prompts
   - captures testing/proof trace and reviewer checklists

## C) Files of interest (grouped by risk)
### Highest risk: validator + mode dispatch + deterministic error behavior
- `tools/validate_intake_bundle_v0_1.py`

### High risk: gate wiring (correct fixture/mode routing)
- `tools/validate_planning_pack.py`

### High risk: stage schema strictness and future-proofing
- `packages/specs/schemas/intake_bundle_reconcile_v0_1.schema.json`
- `packages/specs/schemas/intake_bundle_gap_v0_1.schema.json`
- `packages/specs/schemas/intake_bundle_readiness_v0_1.schema.json`

### Medium risk: fixture semantics and policy intent
- `tools/fixtures/validators/intake_bundle_reconcile_conflict.json`
- `tools/fixtures/validators/intake_bundle_gap_questions_order.json`
- `tools/fixtures/validators/intake_bundle_readiness_blocked_unknown.json`

### Medium risk: docs as contract surface
- `packages/specs/docs/contracts/intake/intake_bundle_stage_artifacts_v0_1.md`
- `packages/specs/docs/contracts/intake/intake_bundle_v0_1.md`

### Medium risk: schema registry coverage
- `tools/fixtures/validators/scenario_schema_list.json`

## D) Known concerns to explicitly check
- Does `validate_intake_bundle_v0_1.py` default behavior remain unchanged for canonical `intake_bundle_v0_1` validation?
- Are stage modes explicit and fail-closed (`unknown mode => error`, no fallback)?
- Are error messages deterministic (sorted/stable ordering and reproducible content)?
- Are stage schemas too restrictive (for example: reconcile conflict values forced to string; gap requires `clarification_questions` `minItems=1`)?
- Does gate wiring ensure stage fixtures are validated by the correct stage mode and never by canonical bundle mode?
- Evidence discipline boundary: what is enforced at stage artifacts vs explicitly deferred to parent-bundle composition checks?

## E) Exact commands Claude should run + PASS criteria
Run exactly:
1. `python3 tools/validate_planning_pack.py`
2. `bash tools/run_pr_gate_validators.sh`
3. `NX_DAEMON=false npx nx run evalsets:migration-smoke`

PASS criteria:
- Command 1 exits `0` and includes final `PASS: planning pack validated.`
- Command 2 exits `0` and all listed validators report `PASS`.
- Command 3 exits `0` and prints `EVALSET-MIGRATION-SMOKE-v1 PASSED`.

If any command fails:
- stop merge recommendation for affected PR(s)
- include exact failing command
- paste the last 50 lines of output for that command in the review response

## F) Required output format Claude must use
Claude output MUST include:
- `MUST` findings list
- `SHOULD` findings list
- `COULD` findings list
- Merge readiness per PR `#150`, `#151`, `#152`, `#153`, `#154` with `✅` or `⚠️`
- Top 3 audit/determinism risks

## Local proof status for this review pack (filled by Codex)
- `python3 tools/validate_planning_pack.py`: PASS at 2026-02-08T11:53:39Z
- `bash tools/run_pr_gate_validators.sh`: PASS at 2026-02-08T11:53:39Z
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`: PASS at 2026-02-08T11:53:39Z (log: `docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260208_115313.log`)
