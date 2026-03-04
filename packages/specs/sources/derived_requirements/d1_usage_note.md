# EDPB D1 Usage Note (Derived Requirements)

Status: `DERIVED` source class, not primary law.

## Classification

- EDPB D1 is a derived requirements catalogue for domain-specific test design.
- D1 is useful for scenario creation and requirement standardisation.
- D1 is not a substitute for GDPR legal text.

## Guardrails

1. D1 MUST/SHOULD/MAY language does not override GDPR articles.
2. D1 requirements must be cross-referenced to parent GDPR article references.
3. If D1 conflicts with GDPR legal text, GDPR legal text governs.
4. D1 should remain structurally separate from:
   - legal criteria pack (`LEGAL`)
   - audit methodology pack (`METHOD`)

## Current repository state

- D2 parsed artifact exists: `experiments/spikes/autogen-debate-s0/data/master_audit_rules.yaml`
- D1 parsed artifact does not yet exist in canonical source structure.

## Implementation note for future D1 parser task

- Follow D2 extraction pattern for deterministic structure and provenance.
- Store output under `packages/specs/sources/derived_requirements/` with explicit source metadata.
