# PR Split Manifest (Local Worktree)
**Date:** 2026-03-02  
**Execution mode:** EX  
**Purpose:** Record the local micro-PR branches created from the oversized working set.

## Clean split worktree
- Path: `C:\aigov-prsplit`
- Base branch: `codex/prsplit-base`
- Base start-point: `origin/main`

## Micro-PR branches created

1. `codex/pr-01-test-j03-accuracy`  
   Commit: `26cdee8`  
   Scope: `packages/pe/tests/judge/test_j03_accuracy.py`

2. `codex/pr-02-uavg-ap-mapping`  
   Commit: `7750ac9`  
   Scope: `packages/specs/docs/artifacts/2026-03-02__nl-uavg-ap__chatbot-testing-mapping_v1.md`

3. `codex/pr-03-judge-context-ab`  
   Commit: `f44b5ae`  
   Scope: judge context A/B scripts + full-12 summary artifact

4. `codex/pr-04-autogen-edpb-spike-core`  
   Commit: `0db2b4e`  
   Scope: AutoGen spike code + extraction/mapping utilities (no generated catalogs)

5. `codex/pr-05-pm-checkpoint-triage`  
   Commit: `fa6bcff`  
   Scope: PM checkpoint artifact + proposal triage register update

6. `codex/pr-06-autogen-generated-catalogs`  
   Commit: `0323278`  
   Scope: generated EDPB catalogs/mappings (large data-only branch)

## Notes
- Original working branch remains untouched and still contains all uncommitted/untracked local files.
- Branch 6 is intentionally isolated due size (57k+ inserted lines).
- Recommended merge order: 1 -> 2 -> 3 -> 4 -> 5, and treat 6 as optional/parked.

