# GDPR Phase 0 — Status (Batch Calibration)

## Current baseline
- Branch: `main`
- Purpose: Provide a minimal, repeatable Phase 0 calibration harness for GDPR signal detection and verdicting.
- Key outcome: Phase 0 calibration is stable with strict JSON cases and repeatable batch reporting.

## What exists now
### 1) Case format (v2)
Calibration cases support:
- `expected_outcome.required_signals` (must be present in modal signals)
- `expected_outcome.allowed_extra_signals` (may appear without failing)
- Backwards support: legacy `expected_outcome.signals` treated as required (until migrated)

### 2) Metrics added (defensibility / observability)
Batch runner emits per-case:
- `missing_required_signals`
- `extra_unallowed_signals`
- `required_recall_pass`
- `allowed_only_pass`

And aggregate metrics:
- `required_recall_accuracy`
- `allowed_only_accuracy`
- missing/failed counts for both

### 3) Guardrail intent
This phase explicitly distinguishes:
- “Required recall” (core correctness)
- “Allowed extras” (acceptable but non-essential signals)
…to reduce overfitting and support probabilistic model behaviour.

## Last verified run (evidence)
- Latest batch report is stored under `runs/batch_*/batch_report.md`
- Expectation: mock batch should always pass; live batch is informational until we expand case count.

## Known limitations
- Phase 0 is a small set (12 cases). Do not over-generalise.
- Live behaviour can drift with model/provider changes; treat it as monitoring, not a merge gate.
