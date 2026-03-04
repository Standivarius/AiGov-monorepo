# Report: Inspect/Petri Naming Alignment + Branch Control

Generated: 2026-03-04 13:25 local  
Prepared for: Claude handoff review  
Scope: naming map artifact creation + branch strategy recommendation.

## 1) What was completed

Created a bounded naming map artifact:

- `packages/specs/docs/contracts/inspect_petri_naming_map_v1.md`

This file contains:

1. source anchors (Inspect/Petri commit pins + AiGov canonical docs)
2. concept-level mapping (Inspect term, Petri term, AiGov alignment)
3. explicit naming conventions (decorators/role contracts)
4. implicit file/module naming conventions
5. bounded recommendations for AiGov alignment

No runtime code was changed as part of this task.

## 2) Key conclusions

1. Petri already aligns to Inspect primitives (`Task`, `Sample`, `solver`, `scorer`) and introduces role names (`auditor`, `target`, `judge`, optional `realism`).
2. AiGov should keep module taxonomy (`M_*`) separate from runtime role names.
3. Best practical alignment:
   - runtime: `auditor/target/judge`
   - architecture: `M_*`
   - primitives: `task/dataset/sample/solver/scorer`
4. Current AiGov taxonomy contracts are strong enough to prevent verdict/signal drift if preserved as source of truth.

## 3) Branch state concern and recommendation

Observed state: branch is carrying a large mixed WIP surface (many generated spike outputs + prompt experiments + docs).

Recommended control policy (immediate):

1. Treat this branch as integration/WIP only.
2. Open a fresh branch from `origin/main` for each atomic deliverable:
   - docs-contract-only
   - prompt-runner-only
   - eval-results-only
3. Keep each PR small enough for deterministic review:
   - target <= 20 files
   - target <= 600 changed lines (excluding generated result artifacts)
4. Generated run artifacts (`work/*.json`, `work/*.md`) should be split from logic changes.
5. Stop adding to current branch once next atomic diff is ready; cut immediately to fresh branch.

## 4) Suggested next action for execution discipline

1. Keep this naming map file as canonical reference for runtime-role naming.
2. Create the next branch from `origin/main` before further implementation.
3. Move only one scope to that branch (either prompt refactor or eval reruns, not both).
4. Use one report artifact per branch to simplify Claude/Codex cross-review.
