# Contracts Index

This folder is the contract authority for terminology, taxonomy, evidence pack schema, and module naming in this monorepo.

## Canonical contracts

- Terminology lock: `packages/specs/docs/contracts/terminology.md`
- Verdict and signal taxonomy: `packages/specs/docs/contracts/taxonomy/`
- Evidence pack contract: `packages/specs/docs/contracts/evidence_pack/`
- Module registry contract: `packages/specs/docs/contracts/modules/module_registry_v0.yaml`

## How to use this index

- Use these contracts as read-only inputs in EP/PE implementations.
- Do not inline taxonomy enums in runtime code when a contract file exists.
- If a contract change alters behavior at stage boundaries, open or update an ADR.

## Scope note

Detailed runtime usage guides and implementation playbooks belong in module-specific docs; this index is intentionally limited to contract authority pointers.
