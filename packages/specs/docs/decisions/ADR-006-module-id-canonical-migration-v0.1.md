# ADR-006 (Stub): Module ID Canonical Migration for 6-Stage Spine

**Date**: 2026-02-20  
**Status**: Proposed (stub)  
**Decision Type**: Contested naming migration

## Context

Current contract/runtime tooling uses module IDs:
- `M_Library`, `M_Intake`, `M_Bundle`, `M_LiveRun`, `M_Judge`, `M_Report` (+ `M_Dashboard`)

Planning vocabulary for spine-aligned naming expects:
- `M_Library`, `M_Intake`, `M_BespokePrep`, `M_TestTarget`, `M_Judge`, `M_Reporting`

This mismatch creates taxonomy drift in specs, traceability queries, and PR scope labeling.

## Options

1. **Option A — Keep current operational IDs**
- Keep `M_Bundle`, `M_LiveRun`, `M_Report` as canonical.
- Treat spine-aligned names as documentation-only aliases.

2. **Option B — Migrate to spine-aligned canonical IDs**
- Canonicalize to `M_BespokePrep`, `M_TestTarget`, `M_Reporting`.
- Keep legacy aliases (`M_Bundle`, `M_LiveRun`, `M_Report`) for backward-compatible lookup only.
- Update module registry, module cards, validators, and planning references in a controlled migration.

3. **Option C — Dual canonical sets (co-equal)**
- Allow both old and new IDs as canonical indefinitely.
- Resolve per-context mapping at query/report time.
