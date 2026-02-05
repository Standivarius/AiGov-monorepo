# M_Intake Task Pack (v2026-02-06)

## Task template (every task must follow)
- Objective:
- Inputs:
- Outputs (artifacts + paths):
- Allowed commands:
- Stop conditions:
- Risks/notes:
- Checkpoint (must include files changed + commands run + results):

## Task 0 — Baseline proof (already done)
Objective: Ensure cloud env can run repo proof commands.
Outputs: Pass/fail logs.

## Task 1 — Codebase map: pipeline + artifact graph
Objective:
- Map the AiGov pipeline end-to-end: modules, artifacts, schemas, validators, PE gates.
- Identify precisely where M_Intake will slot in and what it will feed.

Outputs:
- packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md
Content requirements:
- List modules and artifact boundaries (with file paths)
- Schema inventory under packages/specs/schemas/
- Contract docs inventory under packages/specs/docs/contracts/
- Runtime validation locations under packages/ep/aigov_ep/
- PE gates under packages/pe/tests/ and tools/fixtures/validators/
- Notes on deterministic ordering + fail-closed enforcement points

Allowed commands: proof commands only.

Stop conditions:
- If any part is uncertain, note it explicitly and provide candidate paths to verify.

## Task 2 — OSS candidate analysis: OPA (policy gating)
Objective:
- Determine how OPA would plug into policy_profile/readiness gate deterministically.
Outputs:
- m_intake_oss_eval_opa_2026-02-06.md
Include: license, adapter boundary, input/output contracts, determinism implications.

## Task 3 — OSS candidate analysis: PAR DPIA (intake UX adapter)
Objective:
- Treat PAR export as an input; map to intake_bundle_v0_1; flag EUPL constraints.
Outputs:
- m_intake_oss_eval_par_2026-02-06.md
Include: license constraints and isolation plan.

## Task 4 — OSS candidate analysis: CNIL PIA patterns (workflow/questions)
Objective:
- Extract methodology patterns without importing GPL code.
Outputs:
- m_intake_oss_eval_cnil_patterns_2026-02-06.md

## Task 5 — OSS candidate analysis: Fides (taxonomy alignment)
Objective:
- Evaluate taxonomy mapping value; keep AiGov allowlists canonical.
Outputs:
- m_intake_oss_eval_fides_taxonomy_2026-02-06.md

## Task 6 — Architecture plan (no implementation)
Objective:
- Propose M_Intake architecture: ingest/extract/reconcile/gap/gate with seams and artifacts.
Outputs:
- m_intake_architecture_plan_2026-02-06.md
Must include:
- new/updated contracts
- adapter boundaries for OSS options
- migration and risk plan
- deterministic rules

## Task 7 — Evals-first plan (no implementation)
Objective:
- Define fixtures/tests required to gate M_Intake safely.
Outputs:
- m_intake_evals_plan_2026-02-06.md
Must include:
- new fixtures for intake_bundle_v0_1 (valid/invalid)
- regression fixtures for Intake OUTPUT boundary (locale_context:null etc.)
- readiness gate fixtures
