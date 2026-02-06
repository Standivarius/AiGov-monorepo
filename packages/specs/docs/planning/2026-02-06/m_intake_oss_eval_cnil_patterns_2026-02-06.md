# M_Intake OSS Eval — CNIL PIA Patterns (v2026-02-06)

## Objective
Extract CNIL PIA methodology patterns (workflow + question taxonomy) without importing GPL code, and map them to M_Intake stages and AiGov artifacts for GDPR-only MVP intake.

## Inputs (code-grounded)
- Constitution: `packages/specs/docs/planning/2026-02-06/m_intake_constitution_2026-02-06.md`
- Runbook: `packages/specs/docs/planning/2026-02-06/m_intake_codex_runbook_2026-02-06.md`
- Codebase map: `packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md`
- Intake contracts + schemas:
  - `packages/specs/docs/contracts/intake/README.md`
  - `packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md`
  - `packages/specs/schemas/client_intake_v0_2.schema.json`
- Taxonomy + evidence contracts:
  - `packages/specs/docs/contracts/taxonomy/README.md`
  - `packages/specs/docs/contracts/taxonomy/evidence_schema.md`
  - `packages/specs/docs/contracts/taxonomy/jurisdictions_v0.json`
  - `packages/specs/docs/contracts/taxonomy/sectors_v0.json`
  - `packages/specs/docs/contracts/taxonomy/dsar_channels_v0.json`
  - `packages/specs/docs/contracts/taxonomy/policy_packs_v0.json`
- Runtime + PE touchpoints:
  - `packages/ep/aigov_ep/intake/validate.py`
  - `packages/ep/aigov_ep/cli.py`
  - `packages/pe/tests/intake/test_intake_validation.py`
  - `tools/fixtures/validators/client_intake_v0_2_pass.json`

## Fit matrix status
- Fit matrix: Present — `packages/specs/docs/planning/2026-02-06/m_intake_monorepo_fit_matrix_2026-02-06.md`

---

## A) Workflow step mapping — CNIL steps → M_Intake stages
CNIL PIA guidance emphasizes structured scoping, data flow understanding, risk analysis, and mitigation signoff. Mapping those steps into the M_Intake pipeline keeps intake deterministic and contract-first.

| CNIL PIA step (pattern) | Description (methodology) | M_Intake stage | Deterministic output expectation |
| --- | --- | --- | --- |
| Context & scope definition | Define processing purpose, scope, stakeholders, and boundaries | **Ingest** | Raw intake payload captured verbatim for traceability |
| Data processing description | Identify data categories, sources, flows, storage, and transfers | **Extract** | Normalized fields + structured data flow entries |
| Necessity & proportionality | Assess purpose limitation, data minimization, legal basis | **Reconcile** | Structured mapping to lawful basis and purpose fields |
| Risk assessment | Identify risks to rights/freedoms (likelihood/impact) | **Gap** | Structured risk inventory + missing evidence flags |
| Mitigations & validation | Define measures, assign ownership, and validate controls | **Gate** | Readiness decision + evidence artifact requirements |

---

## B) Question-pattern library proposal (conceptual) mapped to AiGov artifacts
The goal is to capture **question patterns** (not GPL code) and bind each to existing AiGov artifact names, so M_Intake can generate deterministic intake_bundle outputs.

| Question-pattern family | Example prompt intent (conceptual) | AiGov artifact(s) to map | Deterministic constraint |
| --- | --- | --- | --- |
| Processing context & scope | “What is the processing purpose and geographic scope?” | `client_intake_v0_2.schema.json` fields for purpose + scope; `jurisdictions_v0.json` | Jurisdiction must match allowlist; exact string normalization |
| Stakeholders & roles | “Who is the controller, processor, joint controller?” | `client_intake_output_contract_v0_1.md` (intake output roles) | Role labels fixed to contract-defined enums |
| Data categories & sources | “What personal data categories are processed and where do they come from?” | `client_intake_v0_2.schema.json` + taxonomy extensions | Categories must map to approved taxonomy entries |
| Data flow & storage | “Where is data stored, transferred, or accessed?” | `client_intake_output_contract_v0_1.md` (context profile); evidence refs | Flow entries normalized; locations mapped to jurisdiction/sector |
| Legal basis & purpose limitation | “What is the lawful basis and justification?” | `client_intake_output_contract_v0_1.md` + `policy_packs_v0.json` | Basis must map to policy packs; no free-form basis |
| DSAR readiness | “How can data subjects submit requests?” | `dsar_channels_v0.json` + `client_intake_v0_2.schema.json` | Channels must be in allowlist; ordered list required |
| Risk assessment | “What risks to rights and freedoms exist?” | Maps to Evidence Model B (Phase D contract): `packages/specs/docs/contracts/intake/evidence_model_b_v0_1.md` | Risks recorded as evidence artifacts with severity scale |
| Mitigations & controls | “What measures reduce identified risks?” | Maps to Evidence Model B (Phase D contract): `packages/specs/docs/contracts/intake/evidence_model_b_v0_1.md` + `client_intake_output_contract_v0_1.md` | Mitigations must include evidence artifact references |
| Residual risk & approval | “Who approves residual risk and when?” | `client_intake_output_contract_v0_1.md` (approval metadata) | Approval fields required for Gate pass |

---

## C) Concrete AiGov touchpoint paths (from fit matrix → confirm pending)
**Primary intake validation seams:**
- `packages/ep/aigov_ep/intake/validate.py` — deterministic validation of intake payloads; M_Intake should emit schema-valid artifacts before this step.
- `packages/ep/aigov_ep/cli.py` — CLI entrypoint to surface validation failures in a fail-closed manner.

**Contract + schema anchors:**
- `packages/specs/schemas/client_intake_v0_2.schema.json` — canonical schema for intake payloads (Ingest/Extract output).
- `packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md` — required fields for output (Reconcile/Gap/Gate output).
- Maps to Evidence Model B (Phase D contract): `packages/specs/docs/contracts/intake/evidence_model_b_v0_1.md`.
- `packages/specs/docs/contracts/taxonomy/evidence_schema.md` is verdict/signal schema only.

**PE gates + fixtures (evidence + regression):**
- `packages/pe/tests/intake/test_intake_validation.py` — validation gate for schema + determinism.
- `tools/fixtures/validators/client_intake_v0_2_pass.json` — baseline valid intake payload fixture.
- `tools/fixtures/validators/client_intake_v0_2_fail.json` — baseline fail path fixture.
- `tools/fixtures/validators/intake_output_context_fail_pack_order.json` — deterministic policy_pack ordering enforcement.

---

## D) Recommendation
- **Adopt CNIL PIA as a pattern source, not code**: use its workflow structure and question taxonomy to shape deterministic M_Intake intake questions without importing GPL artifacts.
- **Bind every question pattern to a contract-defined artifact** (schema or evidence) so each response becomes a validated intake_bundle field or evidence entry.
- **Fail-closed at Gate**: if any CNIL-derived question maps to a required evidence artifact and it is missing, the Gate stage must block readiness.

---

## Work performed
- Read the task pack and codebase map to align CNIL patterns with existing intake contracts and runtime validation locations.
- Produced a deterministic mapping from CNIL workflow steps to M_Intake stages and a question-pattern library proposal bound to AiGov artifacts.

## Checkpoint
- Files changed:
  - `packages/specs/docs/planning/2026-02-06/m_intake_oss_eval_cnil_patterns_2026-02-06.md`
- Commands run:
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_task_pack_2026-02-06.md`
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md`
  - `rg -n "fit matrix" packages/specs/docs/planning/2026-02-06`
- Results: docs-only; no executable validation required.

Runbook Checkpoint.
