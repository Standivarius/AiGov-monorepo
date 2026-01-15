# Specs Repo Structure Cleanup v0.1

**Date**: 2025-12-19  
**Status**: Accepted  
**Owner**: AiGov Specs

## Context
Schema, template, and evaluation criteria files were split across multiple paths,
with overlapping names and unclear sources of truth. This caused ambiguity about
which files were active vs legacy.

## Decision Summary
- Establish canonical locations for scenario cards and evaluation criteria in `schemas/`.
- Keep scenario instances in `scenarios/library/` and templates in `scenarios/templates/`.
- Archive duplicates and legacy files under `scenarios/_deprecated/`.
- Add in-repo docs that point to canonical sources.

## Before (Top ~3 Levels)
```
.
├─ docs/
│  ├─ custom-instructions/
│  ├─ planning/
│  └─ specs/
├─ projects/
├─ research/
├─ scenarios/
│  ├─ evaluation_criteria/
│  ├─ research/
│  └─ templates/
└─ schemas/
   ├─ behaviour_json_v0_phase0.schema.json
   ├─ gdpr_evaluation_criteria_v0.1.yaml
   └─ judge_scenario_instruction_v0.1.json
```

## After (Top ~3 Levels)
```
.
├─ docs/
│  ├─ _index.md
│  ├─ decisions/
│  ├─ custom-instructions/
│  ├─ planning/
│  └─ specs/
├─ projects/
├─ research/
├─ scenarios/
│  ├─ _deprecated/
│  ├─ library/
│  ├─ research/
│  └─ templates/
└─ schemas/
   ├─ evaluation_criteria/
   ├─ scenario_card/
   ├─ behaviour_json_v0_phase0.schema.json
   └─ judge_scenario_instruction_v0.1.json
```

## Deprecated Files
- `scenarios/_deprecated/gdpr-evaluation-criteria-v0.1.yaml`
  - Legacy criteria file; superseded by the canonical v1.0 evaluation criteria.
- `docs/specs/scenario-card-schema.md`
  - Converted to a redirect stub; canonical schema now lives in `schemas/`.

## Canonical Files and Intended Usage
- `schemas/scenario_card/scenario-card-schema-v1.2.md`
  - Canonical scenario card schema and guidance.
- `schemas/evaluation_criteria/gdpr-evaluation-criteria-v1.0.yaml`
  - Canonical GDPR evaluation criteria used by judges.
- `scenarios/templates/scenario-template-v1.2.yaml`
  - Canonical template for creating new scenarios.
- `scenarios/library/`
  - Home for authored scenario instances.
- `docs/_index.md`
  - Entry point for key specs and canonical paths.

## Next Recommended Changes
- Add `iso27001-evaluation-criteria-v1.0.yaml` and `iso42001-evaluation-criteria-v1.0.yaml` when those rubrics are finalized.
- Migrate any future scenario instances into `scenarios/library/` and keep `scenarios/templates/` limited to canonical templates.
