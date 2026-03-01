# Method Selection Memo v1

Date: `2026-02-20`  
Owner: `Marius + Codex`  
Scope: method selection only (no implementation kickoff)

## Decision

Selected method for current phase: **Option A — Factory-Lite (Method only)**.

This means:
- We treat **scenarios and validation artifacts as truth**.
- We enforce **explicit stage gates** and a strict definition of done.
- We do **not** build a new orchestration runner now.
- We complete **Pre-PRD Discovery Pack first**, then PRDs, then code.

## Why this is the best fit now

1. Solo-founder compatible:
- Lowest operational overhead.
- Strong structure without introducing platform complexity.

2. Agent-compatible:
- Produces concrete, testable artifacts agents can execute against.
- Reduces interpretation drift from prose-only planning.

3. Audit-compatible:
- Gate evidence and scenario contracts are explicit and reviewable.
- Avoids premature coding before scope/contracts are stable.

## Explicitly not selected now

- **Option B (DOT as method source):** deferred; can be added after Factory-Lite is stable.
- **Option C (full orchestration + digital twin):** deferred; too heavy for current stage.

## Non-negotiable rules (locked)

1. No PRD authoring from imagination.  
2. No coding milestone starts before:
- Pre-PRD Discovery Pack approved,
- PRD-P approved,
- PRD-M approved,
- PRD-E baseline approved.
3. No raw chain-of-thought persistence.
4. Validation evidence is required at each gate.

## Immediate output set

This memo adopts the companion playbook and Pre-PRD artifacts:
- `AIGOV_FACTORY_METHOD_v1.md`
- `PRE_PRD_DISCOVERY_PACK_v0.md`
- `PRE_PRD_CHECKLIST_v0.md`
- `PRE_PRD_SCENARIO_PACK_SPEC_v0.md`
- `PRE_PRD_EXAMPLE_MAP_TEMPLATE_v0.md`

