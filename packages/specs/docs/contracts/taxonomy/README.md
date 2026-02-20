# Taxonomy Contracts (Canonical)

This taxonomy package is the single source of truth for:
- Allowed signal IDs
- Verdict/rating enums (including legacy normalization rules)
- Minimal evidence schema references to those enums

## Ownership and Usage
- **Canonical ownership:** `packages/specs/docs/contracts/taxonomy/`
- EP/PE **must** treat this taxonomy as read-only contract data.
- Any runtime or test logic should consume this taxonomy; do not fork or inline values.

Related contract anchors:
- Terminology lock: `packages/specs/docs/contracts/terminology.md`
- Module ID registry: `packages/specs/docs/contracts/modules/module_registry_v0.yaml`

## Versioning
- `taxonomy_version` is required in each contract artifact.
- Update `CHANGELOG.md` for every taxonomy change.
- Breaking changes require a new version and explicit migration guidance.

## Validation command
- Strict: `python tools/validate_taxonomy_contracts.py`
  - Also enforces module registry/card consistency through `tools/validate_module_cards.py`.
- Transition override (only for planned migrations): `python tools/validate_taxonomy_contracts.py --allow-verdict-drift`
- Local bypass (only when debugging registry tooling): `python tools/validate_taxonomy_contracts.py --skip-module-registry-check`
