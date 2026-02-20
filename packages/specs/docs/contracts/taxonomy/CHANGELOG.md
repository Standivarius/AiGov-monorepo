# Changelog

## 0.1.3
- Added module registry gate hook to taxonomy validation:
  - `tools/validate_taxonomy_contracts.py` now runs `tools/validate_module_cards.py` by default.
- Added `--skip-module-registry-check` flag for controlled local bypass.

## 0.1.2
- Resolved ADR-005 by locking canonical verdict labels across schemas and runtime persistence:
  - `INFRINGEMENT | COMPLIANT | UNDECIDED`
- Kept legacy alias mapping only for backward-compatible input normalization.

## 0.1.1
- Clarified canonical monorepo ownership path (`packages/specs/docs/contracts/taxonomy/`).
- Added explicit cross-links to terminology lock and module registry contracts.

## 0.1.0
- Initial canonical taxonomy contracts for signal IDs and verdict enums.
