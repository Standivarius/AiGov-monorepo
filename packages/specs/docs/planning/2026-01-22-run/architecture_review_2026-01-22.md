# AiGov Architecture Review Report

**Reviewer:** Senior Systems Architect
**Date:** 2026-01-22
**Scope:** End-to-end feasibility and conceptual consistency review

---

## 1. Executive Summary (5 bullets)

1. **Pipeline coherence is solid at the contract level** — Stage A/B/C separation, single-source scenario spec rule, and report layer contracts form a defensible backbone.

2. **eval_registry.yaml is malformed YAML** — This is a BLOCKER; the file cannot be parsed as machine-readable input, breaking the "docs-as-code" premise of PR-001.

3. **Evidence artifact IDs (EVID-###) lack a central registry/validator** — Drift between PRD, tier_a_coverage_report, and eval_registry is undetected by CI, creating a high-risk traceability gap.

4. **Evidence pack schema does not enforce taxonomy constraints** — `signal_id` and `verdict` fields accept arbitrary strings, allowing taxonomy drift to bypass validators.

5. **Stage B determinism tolerance is referenced but undefined** — EVAL-009 depends on "defined tolerances" that do not exist, creating an implementation trap.

---

## 2. Top 10 Issues Table

| # | Issue | Why It Matters | Exact File(s) | Minimal Fix | Severity |
|---|-------|----------------|---------------|-------------|----------|
| 1 | **eval_registry.yaml is invalid YAML** | File cannot be parsed; breaks PR-001 "machine-readable backbone" assumption. All references to `eval_registry.yaml` in codex_execution_pack assume it is parseable. | `packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml` | Fix YAML syntax: add colons after keys (e.g., `- eval_id: EVAL-001`). Add a CI validator for the file. | **BLOCKER** |
| 2 | **evalsets_registry.yaml does not exist** | PR-001 in codex_execution_pack references this file as deliverable, but it is missing from the planning folder. | `packages/specs/docs/planning/2026-01-22-run/` (missing file) | Either create the file with runtime tier groupings (pe_pr_gate_short, pe_nightly, pe_release, audit_pack) or remove reference from codex_execution_pack. | **BLOCKER** |
| 3 | **Evidence pack schema allows any verdict string** | `evidence_pack_v0.schema.json` does not validate `verdict` against `verdicts.json`, allowing drift past the taxonomy gate. | `packages/specs/docs/contracts/evidence_pack/evidence_pack_v0.schema.json` | Add doc note: "Runtime validation MUST reject verdicts not in verdicts.json canonical or legacy_aliases." (Schema-level enum is fragile; doc-level contract + validator is preferred.) | **IMPORTANT** |
| 4 | **Evidence pack schema allows any signal_id string** | Same issue—`signal_id` is not validated against `signals.json`, allowing unknown signals into evidence packs. | `packages/specs/docs/contracts/evidence_pack/evidence_pack_v0.schema.json` | Add doc note: "Runtime validation MUST reject signal_ids not in signals.json." Consider adding a validator script (like existing `validate_pre2_4_contracts.py`). | **IMPORTANT** |
| 5 | **No central EVID-### artifact registry** | Evidence artifact IDs are scattered across PRD, tier_a_coverage_report, and eval_registry with no validator to detect typos or drift. | `packages/specs/docs/planning/2026-01-22-run/PRD_PACk_v0.1.md`, `tier_a_coverage_report.md`, `eval_registry.yaml` | Add `evidence_artifacts_registry.yaml` under `packages/specs/docs/contracts/` with canonical list; add validator to CI. (Doc-level note is insufficient—needs machine-checkable list.) | **IMPORTANT** |
| 6 | **"audit_pack" runtime tier is undefined** | Tier A evals (EVAL-201 through EVAL-210) use `runtime_tier: audit_pack` but this tier is not defined in the PRD or state_object. | `packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml`, `PRD_PACk_v0.1.md` | Add one sentence to PRD runtime tier section: "audit_pack: Periodic/on-demand for Tier A enterprise defensibility controls; not part of release-blocking gates." | **IMPORTANT** |
| 7 | **Stage B determinism tolerance is undefined** | EVAL-009 says "within defined tolerances" but no tolerance definition exists. This will cause implementation confusion (what % variance is acceptable?). | `packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml` (EVAL-009) | Add doc note in eval_registry EVAL-009: "Tolerance definition: TBD in judgments contract (e.g., exact match on verdict enum; ±N% on confidence)." Mark as open variable until defined. | **IMPORTANT** |
| 8 | **No judgments.json schema/contract** | PRD references "judgments.json (or equivalent)" but no schema exists. Stage B outputs will drift. | `packages/specs/docs/contracts/` (missing) | Add placeholder contract file `packages/specs/docs/contracts/judgments/judgments_output_contract_v0_1.md` with minimum required fields (run_id, scenario_instance_id, verdicts array with citations). | **IMPORTANT** |
| 9 | **report_fields_crosswalk references `limitations_log` artifact** | Field `gdpr_gr_limitations` requires `limitations_log` evidence artifact, but this artifact is not defined in any schema or registry. | `packages/specs/docs/contracts/reporting/report_fields_crosswalk_v0_1.md` | Either add `limitations_log` to evidence pack schema (as optional field) or add to EVID registry with definition. | **NICE-TO-HAVE** |
| 10 | **additionalProperties: true in evidence pack schema** | Schema allows arbitrary extra fields, which could let telemetry leak into admissible evidence (violating AC-008). | `packages/specs/docs/contracts/evidence_pack/evidence_pack_v0.schema.json` | Add doc note: "additionalProperties is allowed for extensibility but telemetry-class fields MUST be stripped by the evidence pack builder (whitelist-only policy)." Consider future schema version with `additionalProperties: false`. | **NICE-TO-HAVE** |

---

## 3. "Do NOT Change" List

These elements are already correct and should be preserved:

| Element | Location | Why It's Correct |
|---------|----------|------------------|
| **Single-source bespoke scenario spec rule** | `bespoke_scenario_spec_v0_1.md` | Prevents auditor/judge instruction drift; validated by `validate_pre2_4_contracts.py`. |
| **Stage A/B/C separation** | `terminology.md`, `PRD_PACk_v0.1.md` | Clear, defensible pipeline boundary; no scoring in Stage A is enforced by contract. |
| **Report layers contract (L1/L2/L3)** | `report_layers.md` | Audience semantics are locked; drift gate exists in CI. |
| **Verdict enum with legacy aliases** | `verdicts.json` | Migration path is explicit and machine-readable. |
| **Signal taxonomy centralization** | `signals.json`, `signals.meta.json` | Single source of truth; validated by `build_signal_synonyms.py --check`. |
| **Verification modes in scenario spec** | `bespoke_scenario_spec_v0_1.md` | `runtime|doc|timeline|out-of-scope` covers policy constraints correctly. |
| **Existing CI validators** | `tools/*.py`, `.github/workflows/*.yml` | Report layer drift, signal synonyms, intake contracts, scenario contracts all have fail-closed checks. |
| **PR-gate vs nightly vs release partition concept** | `PRD_PACk_v0.1.md` | Runtime budget discipline is defined (needs audit_pack addition only). |

---

## 4. Suggested Next-Review Checkpoint

**When to rerun this review:**

1. **After PR-001 and PR-002 merge** — Once eval registries are parseable and contract validation gates are wired, re-validate that the pipeline is actually machine-checkable end-to-end.

2. **Before PR-006 (Stage B judge harness)** — The judgments output contract must exist before implementing Stage B, or the implementation will create de facto schema that's hard to change.

3. **If any new EVID-### artifact is added** — Until a central registry + validator exists, any new artifact ID should trigger a manual cross-check.

**Recommended cadence:** Re-run this architecture review after every 3 PRs in the chain, or whenever a new contract file is added.

---

## Appendix: Detailed Analysis

### A. Pipeline Coherence Assessment

**Strengths:**
- Clear intake → scenario compilation → execution → judgment → reporting flow
- Contracts exist at each major boundary point
- Single-source rule for instruction generation prevents a common drift trap

**Interface Contract Gaps:**
- Intake → Bundle compilation: `client_intake_output_contract_v0_1.md` exists but no explicit "bundle manifest contract"
- Stage A output → Evidence Pack: `evidence_pack_v0.schema.json` exists but no transform contract
- Evidence Pack → Stage B Judge: No judge input contract (only output is referenced)
- Stage B → Stage C Reports: Crosswalk exists but no explicit report generation input contract

### B. Drift Risk Hotspots

| Term/Concept | Where It Appears | Drift Risk | Mitigation Status |
|--------------|------------------|------------|-------------------|
| L1/L2/L3 layer names | report_layers.md, crosswalk, PRD | Low | Validator exists |
| Signal IDs | signals.json, evidence packs, scenarios | Medium | Partially validated (scenarios only) |
| Verdict enum | verdicts.json, evidence packs, judgments | Medium | Not enforced in schema |
| EVID-### artifact IDs | PRD, tier_a, eval_registry | High | No validator |
| EVAL-### eval IDs | eval_registry, PRD | High | No validator |

### C. Runtime Budget Assessment

| Runtime Tier | Defined In | Evals Assigned | Budget Risk |
|--------------|------------|----------------|-------------|
| pr_gate | PRD | EVAL-001,002,003,006,014,017 | OK if schema-only |
| nightly | PRD | EVAL-004,005,007,009,012,013,016,018 | OK |
| release | PRD | EVAL-008,010,011,015 | OK |
| audit_pack | (undefined) | EVAL-201 through EVAL-210 | UNDEFINED—needs scope |

---

## Review Metadata

- **Authoritative inputs reviewed:**
  - `state_object_v0_1.json`
  - `PRD_PACk_v0.1.md`
  - `codex_execution_pack.md`
  - `tier_a_coverage_report.md`

- **Secondary references checked:**
  - All files under `packages/specs/docs/contracts/**`
  - All validators in `tools/*.py`
  - All CI workflows in `.github/workflows/*.yml`

- **Review approach:** No new product concepts proposed; focus on closing gaps for clean PR chain implementation.
