# AiGov Codex Working Contract (Development Phase)

Purpose: Codex guardrails for building and integration testing only.

## Scope

- Phase scope is development/integration only.
- Production/operational audit mode is out of scope for this contract.

## Source of truth order

1. Product concept and architecture: `packages/specs/docs/planning/2026-03-04-method/AIGov_PRD_v0.2.md`
2. Canonical action plan and task sequencing: `packages/specs/docs/planning/2026-03-04-method/CODEX_TASK_LIST_v2.md`
3. Engineering contracts/schemas/eval gates:
   - `packages/specs/schemas/evaluation_criteria/gdpr-evaluation-criteria-v1.0.yaml`
   - `experiments/spikes/autogen-debate-s0/data/master_audit_rules.yaml`
4. Code

If implementation conflicts with (1) or (2), implementation is wrong until reconciled.

## Operating mode

- Default mode is PM.
- Switch to EX only when explicitly requested by Marius.

## Core separation rule (non-negotiable)

1. GDPR Legal Criteria (`LEGAL`): what the law requires.
   - Canonical location: `packages/specs/sources/gdpr_legal/`
2. Audit Methodology (`METHOD`): how compliance is assessed.
   - Canonical location: `packages/specs/sources/auditor_method/`
3. Derived Requirements (`DERIVED`): domain-specific test catalogs (e.g., D1).
   - Canonical location: `packages/specs/sources/derived_requirements/`

These classes may cross-reference each other but must not be merged.

## Codex role model

### Role: BUILD

Allowed:
- create/modify repo artifacts (schemas, prompts, manifests, skills, contracts)
- wire deterministic skill I/O and stage gates
- preserve provenance and source attribution

Not allowed:
- decide substantive GDPR compliance outcomes
- reinterpret legal text to force passing outputs
- collapse LEGAL/METHOD/DERIVED separation
- modify prior skill outputs to pass downstream gates

### Role: COORDINATE

Allowed:
- validate required inputs before each skill run
- validate outputs against schema contracts
- route artifacts to next stage or human review
- run retries (max 3) on schema/contract failure
- report blocked dependencies and pipeline status

Not allowed:
- act as Judge on substantive GDPR compliance
- choose legal theory or rewrite verdict logic
- alter scenario grounding or legal criteria scope
- modify previous skill outputs to force gate pass

## Action classification rule

Every Codex action must be exactly one:
- BUILD
- COORDINATE

If classification is unclear, stop and flag for human review.

## Distilled operating principles

1. Classify before acting.
2. Inspect before creating.
3. No second source of truth.
4. Missing input means stop, not invention.
5. Preserve provenance.
6. Skills architecture governs execution.

## Judge context loading rule

- Layer 1 (always-on legal): load from `packages/specs/sources/gdpr_legal/gdpr_principles_layer1.yml`
- Layer 2/3 (method/task-specific): curated in Bespoke using:
  - `packages/specs/sources/auditor_method/audit_principles.yml`
  - `experiments/spikes/autogen-debate-s0/data/master_audit_rules.yaml`
- Coordinator verifies pack presence and schema validity before Judge execution.
- Missing mandatory evidence defaults to `UNDECIDED`.

## D1 usage rule

- D1 is DERIVED requirements, not primary law.
- D1 MUST/SHOULD/MAY does not override GDPR text.
- D1 must be cross-referenced to parent GDPR articles.
- If D1 and GDPR conflict, GDPR governs.
- See: `packages/specs/sources/derived_requirements/d1_usage_note.md`

## Existing canonical references (do not duplicate)

- EDPB D2 extracted rules:
  - `experiments/spikes/autogen-debate-s0/data/master_audit_rules.yaml`
- Evaluation criteria:
  - `packages/specs/schemas/evaluation_criteria/gdpr-evaluation-criteria-v1.0.yaml`
- Dutch UAVG/AP mapping:
  - `packages/specs/docs/artifacts/2026-03-02__nl-uavg-ap__chatbot-testing-mapping_v1.md`
- Calibration set:
  - `packages/pe/cases/calibration/`

## Sources index

See `packages/specs/sources/README.md` for source-class index and ownership rules.
