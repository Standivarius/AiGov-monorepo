# AiGov Source Classes (Development Phase)

Purpose: canonical index for source classes used by skills and Judge context loading.

## Source classes

1. `LEGAL` (what law requires)
   - Path: `packages/specs/sources/gdpr_legal/`
   - Canonical file: `gdpr_principles_layer1.yml`
   - Authority: GDPR text (articles/recitals). Guidance is interpretive, not replacing law.

2. `METHOD` (how compliance is assessed)
   - Path: `packages/specs/sources/auditor_method/`
   - Canonical file: `audit_principles.yml`
   - Authority: audit methodology (ISO 19011, EDPB D2, ICO framework).

3. `DERIVED` (domain-specific requirement catalogs)
   - Path: `packages/specs/sources/derived_requirements/`
   - Canonical file: `d1_usage_note.md`
   - Authority: derived translation of legal obligations into test requirements (e.g., EDPB D1).

## Cross-referenced canonical artifacts (existing)

- EDPB D2 extracted rules: `experiments/spikes/autogen-debate-s0/data/master_audit_rules.yaml`
- Evaluation criteria: `packages/specs/schemas/evaluation_criteria/gdpr-evaluation-criteria-v1.0.yaml`
- Dutch UAVG/AP mapping: `packages/specs/docs/artifacts/2026-03-02__nl-uavg-ap__chatbot-testing-mapping_v1.md`

## Ownership and usage rules

1. Do not merge LEGAL, METHOD, and DERIVED into one blob.
2. Skills must load from canonical files, not duplicated copies.
3. If conflict exists:
   - GDPR legal text > derived requirements.
   - Methodology governs assessment process, not legal authority.
