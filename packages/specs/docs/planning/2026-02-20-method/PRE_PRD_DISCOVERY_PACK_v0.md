# Pre-PRD Discovery Pack v0

Date: `2026-02-20`  
Status: `Draft`  
Method: `Factory-Lite`

## 1) Story Map Backbone (6-stage spine)

1. Standard Scenario Library
2. Client Intake
3. Bespoke Scenario Preparation
4. Testing Target
5. Judge
6. Reporting

## 2) Walking Skeleton Definition (SLICE v0.1)

Single deterministic scenario executed end-to-end across all 6 stages with:
- deterministic simulator path (no live LLM call),
- evidence-lane artifact chain,
- repeatable outputs under locked comparison policy.

## 3) Walking Skeleton Stories (one per stage)

### Stage 1 Story
As an auditor, I can load one canonical scenario with stable ID and metadata.

### Stage 2 Story
As an auditor, I can submit minimal intake context required to parameterize that scenario.

### Stage 3 Story
As an auditor, I can generate one bespoke scenario variant with frozen inputs.

### Stage 4 Story
As an auditor, I can run the target interaction and capture Stage A artifacts only.

### Stage 5 Story
As an auditor, I can evaluate the run and receive schema-valid judge output.

### Stage 6 Story
As an auditor, I can receive report outputs (exec/compliance/ciso + structured export).

## 4) Example Mapping Starter (for each walking story)

Use:
- Story (yellow)
- Rules / acceptance criteria (blue)
- Examples (green)
- Questions (red)

Gate rule:
- Walking skeleton cannot pass S1 with unresolved red-card blockers.

## 5) Scenario Pack Requirements (v0.1)

Required components:
- scenario definition
- expected stage artifacts
- expected report outputs
- deterministic comparison policy
- evidence expectations

Holdout rule:
- Keep at least one scenario not used during implementation iterations.

## 6) Open Questions (must be resolved before PRD drafting)

1. Final module-ID canonical set (depends on ADR-006).
2. Minimal holdout policy strictness for v0.1.
3. Exact acceptance wording for Stage 6 structured export in SLICE v0.1.

