# Repo Coherence Report (duplicates, contradictions, stale docs, missing links)

## Inventory (current repo reality)
- packages/specs: canonical specs/contracts/schemas
  - Phase2 specs: `packages/specs/docs/specs/phase2-*.md`
  - Canonical schema: `packages/specs/schemas/behaviour_json_v0_phase0.schema.json`
  - Templates: `packages/specs/scenarios/templates/scenario-template-v1.2.yaml`
- packages/pe: PE harness but currently holds EP runtime code
  - EP-like runtime: `packages/pe/aigov_eval/*`
  - PE tests: `packages/pe/tests/**`
  - Cases: `packages/pe/cases/calibration/*.json`
- packages/ep: target repo for EP runtime; currently contains TargetLab target system
  - `packages/ep/services/targetlab_rag/app.py`
  - `packages/ep/docs/eval-status.md` (deprecated)

---

## Duplicate / conflicting docs

| Paths | Conflict | Canonical | Consolidation edit |
|---|---|---|---|
| `packages/specs/docs/contracts/terminology.md` vs `packages/pe/docs/GLOSSARY.md` | glossary uses old names/labels | `packages/specs/docs/contracts/terminology.md` | add “DEPRECATED” banner to `packages/pe/docs/GLOSSARY.md` pointing to canonical terminology |
| `packages/specs/schemas/behaviour_json_v0_phase0.schema.json` vs `packages/pe/schemas/behaviour_json_v0_phase0.schema-*.json` | schema duplication drift risk | specs schema | delete eval copies OR vendor with hash-sync rule |
| `packages/specs/docs/specs/phase2-reporting-exports-v0.1.md` vs `packages/pe/docs/REPORTING_SPEC.md` | “reporting” means EP client reports vs PE batch reports | keep both but scope | rename eval doc to PE scope or add banner + cross-link |

---

## Stale/legacy docs

| Path | Why stale | Deprecation mechanism |
|---|---|---|
| `packages/ep/docs/eval-status.md` | explicitly deprecated and out of date | keep, add banner + link to Program Pack |
| `packages/pe/docs/Refactor_summary-eval.md` | status claims conflict with ongoing refactor | add banner linking to Action Plan |

---

## Missing cross-links
- Add links from `packages/pe/README_MINIMAL_LOOP.md` to:
  - `packages/specs/schemas/behaviour_json_v0_phase0.schema.json`
  - `packages/specs/docs/specs/phase2-index.md`

---

## Repo move/merge/deprecate map (workspace-relative paths)

| FROM_PATH | TO_PATH | Reason |
|---|---|---|
| `packages/pe/aigov_eval/targets/*` | `packages/ep/aigov_ep/targets/*` | required for client runs (EP) |
| `packages/pe/aigov_eval/runner.py` | `packages/ep/aigov_ep/execute/runner.py` | Stage A is EP |
| `packages/pe/aigov_eval/judge.py` | `packages/ep/aigov_ep/judge/judge.py` | Stage B judge is EP |
| `packages/pe/aigov_eval/judge_output_mapper.py` | `packages/ep/aigov_ep/judge/mapper.py` | EP outputs must validate against canonical schema |
| `packages/pe/aigov_eval/evidence.py` | `packages/ep/aigov_ep/artifacts/evidence.py` | evidence packs are EP deliverables |

---

## Discrepancy log (desired behavior vs repo reality)
1) EP runtime currently lives in `packages/pe/aigov_eval/*` but must be migrated to `packages/ep/`.
2) Stage A currently scores inline (must become transcript-only).
3) Verdict label mismatch across code/schema must be standardized per terminology lock.
4) Scenario library in specs is currently empty; runnable examples are in evals repo.
