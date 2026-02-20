# ADR-005: Verdict Label Canonicalization (v0.1)

**Date**: 2026-02-20  
**Status**: Accepted  
**Owner**: AiGov Architecture / Product  
**Decision Type**: One-Way Door

---

## Context

Verdict labels diverged across layers:

- Taxonomy/terminology contracts used `INFRINGEMENT | COMPLIANT | UNDECIDED`.
- Behaviour schemas used `VIOLATED | COMPLIANT | UNDECIDED`.
- Judge internals used `VIOLATION | NO_VIOLATION | UNCLEAR`.

This created drift at schema gates and inconsistent audit language.

---

## Decision

Adopt **taxonomy-first canonical verdict labels** for persisted behavior outputs:

- `INFRINGEMENT`
- `COMPLIANT`
- `UNDECIDED`

Internal judge labels may remain (`VIOLATION`, `NO_VIOLATION`, `UNCLEAR`) but MUST be normalized before artifact persistence.

Chosen option: **align schema and mapper outputs to taxonomy canonical labels**.

**One-Way Door Notice**:
> Persisted audit outputs and downstream consumers now anchor to canonical `INFRINGEMENT` vocabulary. Reverting would require contract and artifact migration across historical runs and report tooling.

---

## Consequences

### Positive
- Single verdict vocabulary across contracts, schemas, and persisted outputs.
- Deterministic taxonomy validator can run in strict mode.
- Reduced mapper ambiguity and clearer audit wording.

### Tradeoffs
- Legacy references to `VIOLATED` remain in historical docs/tests and need staged cleanup.
- Internal verdict vocabulary still differs and depends on explicit mapping.

### Risks
- Risk: hidden consumer expecting `VIOLATED` breaks.
  - Mitigation: keep legacy alias map (`VIOLATED -> INFRINGEMENT`) in verdict taxonomy contracts during transition.

---

## Alternatives Considered

### Option A: Canonical `VIOLATED | COMPLIANT | UNDECIDED`
- Rejected: contradicts existing taxonomy/terminology contract direction.

### Option B: Canonical `INFRINGEMENT | COMPLIANT | UNDECIDED` (chosen)
- Accepted: aligns persisted schema outputs with taxonomy authority.

### Option C: Dual canonical forms
- Rejected: preserves ambiguity and weakens gate enforcement.

---

## Implementation

Applied in this change set:

1. Updated rating enums in:
   - `packages/specs/schemas/behaviour_json_v0_phase0.schema.json`
   - `packages/ep/aigov_ep/contracts/behaviour_json_v0_phase0.schema.json`
   - `packages/pe/aigov_eval/contracts/behaviour_json_v0_phase0.schema.json`
2. Updated mapper outputs:
   - `packages/ep/aigov_ep/judge/judge.py`
   - `packages/pe/aigov_eval/judge_output_mapper.py`
3. Kept backward-compatible alias normalization in verdict taxonomy contracts.

---

## Validation Criteria

- `python tools/validate_taxonomy_contracts.py` passes in strict mode.
- Judge mapping tests pass with `INFRINGEMENT` as rating for violation cases.

---

## References

- `packages/specs/docs/planning/2026-02-17/PLAN_OF_RECORD_v1.md` (ADR-005 stub)
- `packages/specs/docs/contracts/terminology.md`
- `packages/specs/docs/contracts/taxonomy/verdicts.json`
