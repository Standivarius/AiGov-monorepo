# AiGov Factory Method v1

Date: `2026-02-20`  
Status: `Proposed-for-use`  
Type: `Method + gates only (no build kickoff)`

## 1) Source-of-Truth Order

1. Spine flow (6 stages)
2. Pre-PRD Discovery artifacts
3. PRDs (`PRD-P`, `PRD-M`, `PRD-E`)
4. Code and tests

If code conflicts with (1)-(3), code is wrong.

## 2) Stage Model (Method Stages)

### S0 Contract Reset
Goal:
- Lock working rules and workflow boundaries.

Exit evidence:
- Method memo accepted.
- Gate checklist accepted.

### S1 Pre-PRD Discovery Pack
Goal:
- Define expected behavior as concrete examples and scenarios.

Required artifacts:
- Story Map (backbone + SLICE v0.1 walking skeleton)
- Example Maps (rules/examples/questions) for walking-skeleton stories
- Scenario Pack spec (fixtures, expected artifacts, comparison rules)
- Holdout policy draft

Exit evidence:
- No unresolved red-card questions on walking skeleton.
- Discovery checklist passed.

### S2 PRD Compilation
Goal:
- Compile Discovery Pack into PRDs.

Required artifacts:
- `PRD-P` v0
- `PRD-M` v0 for all 6 spine modules

Exit evidence:
- PRD checklists passed.
- Open decisions isolated in ADR stubs only.

### S3 Engineering Truth Pack
Goal:
- Convert PRD claims into enforceable contracts and gates.

Required artifacts:
- Schema/contract index + validators
- ADR set for contested decisions
- Test/eval registry with gate tags

Exit evidence:
- Validation commands defined and passing for baseline.
- No silent ambiguity in critical enums/contracts.

### S4 Build Readiness Gate
Goal:
- Explicitly decide whether build can start.

Required:
- S0-S3 signed off.
- First implementation slice selected and bounded.

Only after S4 passes can implementation milestones begin.

## 3) Required Human Involvement (Marius)

Mandatory approval points:
1. Method selection (S0)
2. Discovery Pack freeze (S1)
3. PRD-P + PRD-M acceptance (S2)
4. Engineering Truth Pack gate rules (S3)
5. Build readiness decision (S4)

## 4) PM/EX Operating Rule

- Default: `PM`
- `EX` only when explicitly requested for a defined scope.
- In PM: no hidden implementation starts.
- In EX: implementation must trace to approved PRD/contract IDs.

## 5) Gate Checklist Summary

### Gate G0 (Method)
- [ ] Method selected and recorded
- [ ] Workflow rules recorded

### Gate G1 (Pre-PRD)
- [ ] Story Map complete
- [ ] Example Maps complete for walking skeleton
- [ ] Scenario Pack spec complete
- [ ] No unresolved blocker questions

### Gate G2 (PRDs)
- [ ] PRD-P accepted
- [ ] PRD-M accepted for all 6 modules
- [ ] Open decisions moved to ADR stubs

### Gate G3 (Truth Pack)
- [ ] Contracts/schemas indexed
- [ ] Validators defined
- [ ] Eval/test gate tags defined

### Gate G4 (Build readiness)
- [ ] First build slice chosen
- [ ] Acceptance and proof commands locked
- [ ] Approval to enter implementation

## 6) Module Naming Note

Current repo registry still uses legacy operational IDs (`M_Bundle`, `M_LiveRun`, `M_Report`) in several tools/docs.  
Canonical migration to spine-aligned IDs is tracked via:
- `packages/specs/docs/decisions/ADR-006-module-id-canonical-migration-v0.1.md`

Method usage rule until ADR-006 is resolved:
- Use existing registry IDs in enforcement artifacts.
- Include friendly spine labels in parentheses for clarity.

