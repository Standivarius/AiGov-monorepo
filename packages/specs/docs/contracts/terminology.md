# Terminology Lock (EP vs PE) — Canonical Definitions and Boundary Rules

**Canonical file:** `packages/specs/docs/contracts/terminology.md`  
**Applies to:** this monorepo (`packages/specs`, `packages/ep`, `packages/pe`)

---

## EP vs PE (locked)

### EP — Evals-as-Product / Evaluation Product
**Definition:** Client-run product pipeline for audit delivery. EP performs: intake -> bespoke preparation -> target execution -> judgement -> reporting/exports.

**Is**
- Runtime pipeline executed for a client audit engagement.
- Stage A + Stage B + Stage C flow (execution, judgement, reporting).
- Includes target adapters, judge orchestration, manifests, and report generation.

**Is not**
- Internal regression harness validating EP correctness and repeatability.

**Monorepo placement**
- EP implementation lives under `packages/ep`.

---

### PE — Product Evaluations
**Definition:** Evaluation suites and infrastructure that test/regress EP runtime behavior. PE measures correctness, repeatability, stability, and contract compliance.

**Is**
- Calibration case sets, regression suites, CI eval runs, and analysis support used to validate EP behavior.
- Examples in this workspace:
  - `packages/pe/cases/calibration/*.json`
  - `packages/pe/tests/**`

**Is not**
- The client-deliverable runtime pipeline or client report generator.

**Monorepo placement**
- PE implementation lives under `packages/pe`.

---

### Target System (customer system under audit)
**Definition:** The external chatbot/agent system being evaluated.  
**Naming rule:** Do **not** call the customer system "PE". Use **Target System** or **Customer Target**.

---

## Boundary rule (system-of-record)

- **`packages/specs`**: canonical definitions, schemas, taxonomy, traceability contracts.
- **`packages/ep`**: EP runtime product implementation.
- **`packages/pe`**: PE regression and evaluation harness.

**Rule:** "Required for a client run?" => EP (`packages/ep`); otherwise => PE (`packages/pe`).

---

## Module ID terms (locked)

Canonical module IDs are defined in:

- `packages/specs/docs/contracts/modules/module_registry_v0.yaml`

Use `M_*` IDs as first token in planning and PR language (example: `M_Intake`).

---

## Pipeline terms (locked)

### Stage A — Execution / Transcript capture
- Runs scenarios against target adapters and captures run artifacts.
- No scoring and no judge artifacts in Stage A output contract.

### Stage B — Offline judgement
- Consumes Stage A artifacts and produces schema-valid findings.
- Fail-closed: schema invalid -> judgement fails.

### Stage C — Aggregation / Reporting / Exports
- Produces L1/L2/L3 outputs and structured exports from validated inputs.

---

## Verdict labels (canonical + mapping)

### Canonical verdict enum (contract authority)
`INFRINGEMENT | COMPLIANT | UNDECIDED`

### Required migration map
- `VIOLATION` or `VIOLATED` -> `INFRINGEMENT`
- `NO_VIOLATION` or `PASS` -> `COMPLIANT`
- `UNCLEAR` -> `UNDECIDED`

### Schema versioning requirement
If behaviour schema enum differs from canonical verdict labels, migration must be explicit:
- update enum and bump schema version, or
- introduce a new schema version and deprecate prior enum.

---

## Stable IDs
- Requirements: `REQ-###`
- Evals/tests: `EVAL-###`
- Evidence artifacts: `EVID-###`

---

## Evidence vs telemetry (two-lane model)
- **Evidence lane:** persisted artifacts required for audit defense.
- **Telemetry lane:** operational traces used for debugging/monitoring.
- Raw chain-of-thought persistence is forbidden.

---

## Evidence maturity ladder terms

- **T0**: Transcript-only deterministic evidence.
- **T1**: Process-backed evidence (for example SOP/ticket/SLA support).
- **T2**: System-backed evidence (for example logs, retention/deletion enforcement).
