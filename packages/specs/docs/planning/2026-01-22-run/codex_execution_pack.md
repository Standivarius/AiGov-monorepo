codex_execution_pack.md
Codex Execution Pack (Conceptual PR chain — no repo paths)

This pack translates the PRD + eval registries into small, auditable PR slices with verification, evidence artifacts, and stop conditions. Small-slice rules are aligned with the existing “one concern per PR / minimal file touch / explicit stop conditions” guidance.

Small PR slices rules (must follow)

One concern per PR (no drive-by refactors).

Minimal file touch set (target 1–5 files per PR slice).

Every PR includes:

before/after self-check commands

explicit stop conditions

expected success signal

evidence artifacts produced/updated

Mark migration-dependent work explicitly as MIGRATION_BLOCKED (do not handwave).

Verification command conventions (conceptual)

Run all commands from workspace root.

Schema validation: validate-schemas

Run evalset: run-evalset <evalset_id>

Generate artifacts: generate-reports --from <evidence_pack>

Link check: check-links --report <report_bundle>

CI dry-run: ci-local --required

(Exact command names are implementation details; the required behavior is defined by the eval pass rules in eval_registry.yaml.)

PR chain proposal (ordered, small diffs)
PR-001 — Add eval registries (docs-as-code)

Goal

Introduce eval_registry.yaml + evalsets_registry.yaml + tier_a_coverage_report.md as the machine-readable backbone.

Scope

Included:

Add/update YAML registries and coverage report

Excluded:

No runtime code changes

Expected files touched (types)

YAML registry files (2)

Markdown coverage report (1)

Verification commands

validate-yaml eval_registry.yaml

validate-yaml evalsets_registry.yaml

Evidence artifacts

EVID-001 (updated docs snapshot)

EVID-011 (lint/validation report)

STOP conditions

YAML is not parseable

Any eval referenced in PRD is missing from registry

Any Tier A control lacks an eval mapping or evidence artifact

Good looks like

Registries parse cleanly and CI can treat them as inputs.

Bad looks like

IDs mismatch (typos) or missing eval IDs break mapping.

How to decide

If a mapping is unclear, do not invent: move to Open Variables, and leave eval entry UNREADY (not referenced by any EP).

PR-002 — Add contract validation gates (fail-closed)

Goal

Ensure all contract-defined artifacts (intake, bundle manifest, evidence pack, judge output, reports, exports) are validated fail-closed.

Scope

Included:

Add schema validation utilities and minimal tests

Excluded:

No Stage A/B runner behavior changes

Expected files touched

Schema validation utility module

A small test file / fixture set

Documentation snippet describing fail-closed behavior

Verification commands

validate-schemas

run-evalset pe_pr_gate_short

Evidence artifacts

EVID-011 (schema validation logs)

EVID-002 (contract provenance snapshot)

STOP conditions

Any contract artifact can be produced without validation

Validation failures do not return non-zero exit

Good looks like

Invalid artifacts reliably fail PR-gate.

Bad looks like

“Warnings only” behavior; CI passes with invalid schema.

How to decide

If validation adds heavy runtime, keep it structural-only in PR-gate and move heavy checks to nightly.

PR-003 — Deterministic bundle hash + manifest canonicalization

Goal

Make bundle compilation reproducible: stable bundle_hash, canonical manifest encoding rules.

Scope

Included:

Deterministic serialization rules (canonical JSON)

Bundle hash definition doc + implementation

Excluded:

No Stage A execution

Expected files touched

Bundle compiler module

Manifest schema/contract (only if already versioned)

One test fixture

Verification commands

run-evalset pe_pr_gate_short (focus: EVAL-003, EVAL-014)

Evidence artifacts

EVID-003 (scenario bundle + manifest)

EVID-011 (determinism test report)

STOP conditions

Bundle hash changes between identical inputs

Manifest ordering is unstable between runs

Good looks like

Identical inputs → identical manifest bytes and hash.

Bad looks like

Hash depends on timestamps, random IDs, or nondeterministic ordering.

How to decide

If byte-for-byte determinism is too strict, define canonical equivalence rules explicitly and encode them in EVAL-003.

PR-004 — Stage A smoke runner (mock target) produces required artifacts

Goal

Implement minimal Stage A that produces transcripts + run_manifest for a smoke bundle, with no judging.

Scope

Included:

Mock target adapter

Stage A orchestration for smoke bundle

Excluded:

No Stage B judge

Expected files touched

Stage A runner module

Mock target adapter module

Minimal fixture bundle

Verification commands

run-evalset pe_nightly (focus: EVAL-004)

validate-schemas

Evidence artifacts

EVID-004 (transcripts/raw artifacts)

EVID-011 (nightly run report)

STOP conditions

Any judge logic runs during Stage A

Artifacts missing or incomplete

Good looks like

A single nightly run produces a complete Stage A evidence directory equivalent.

Bad looks like

“Stage A” includes verdicts or judge prompts.

How to decide

If reviewers see any scoring in Stage A, split into a separate PR and remove it.

PR-005 — Evidence pack builder (admissible + portable)

Goal

Produce an admissible evidence pack with manifest + hashes and evidence/telemetry separation.

Scope

Included:

Evidence pack assembly and hashing

Evidence/telemetry separation policy enforcement

Excluded:

No report generation

Expected files touched

Evidence pack builder module

Hashing/manifest utility module

Tests/fixtures

Verification commands

run-evalset pe_nightly (focus: EVAL-004 structural + EVAL-005 input readiness)

validate-schemas

Evidence artifacts

EVID-005 (evidence pack + manifest)

EVID-011 (validation logs)

STOP conditions

Evidence pack requires network to evaluate

Telemetry leaks into admissible pack

Good looks like

Evidence pack is portable and self-contained for Stage B.

Bad looks like

Missing manifest/hashes or unclear provenance.

How to decide

If portability fails, define the missing artifact as required evidence and add it to the pack schema before proceeding.

PR-006 — Stage B judge harness (offline) + verdict enum enforcement

Goal

Run Stage B offline against an evidence pack to produce normalized, schema-valid judgments with citations.

Scope

Included:

Stage B runner (offline)

Canonical verdict enum enforcement

Excluded:

No exports

Expected files touched

Stage B runner module

Verdict normalization module

Tests (golden-case fixtures)

Verification commands

run-evalset pe_nightly (EVAL-005, EVAL-009)

run-evalset pe_pr_gate_short (EVAL-006)

Evidence artifacts

EVID-006 (judgments JSON)

EVID-011 (test reports)

STOP conditions

Outputs are not schema-valid

Verdict labels drift beyond canonical enum

Citations don’t resolve to evidence IDs

Good looks like

Stage B produces stable, replayable results on fixed evidence packs.

Bad looks like

Judge output structure changes ad hoc; citations point to “text spans” instead of evidence IDs.

How to decide

If citations can’t be resolved deterministically, fix the evidence indexing first (don’t weaken traceability).

PR-007 — Reporting generator (EXEC/COMPLIANCE/SECURITY) + link checker

Goal

Generate L1 EXEC, L2 COMPLIANCE, L3 SECURITY reports from evidence + judgments; verify all evidence links.

Scope

Included:

Report generator

Link integrity checker

Excluded:

No GDPR-GR export yet

Expected files touched

Report generation module

Link checker module

One fixture run pack

Verification commands

run-evalset pe_nightly (EVAL-007)

validate-schemas

Evidence artifacts

EVID-007/008/009 (reports)

EVID-011 (link check report)

STOP conditions

Reports don’t validate against report-fields contract

Links don’t resolve to evidence pack IDs

Good looks like

Reports regenerate without rerunning Stage A.

Bad looks like

Reports embed raw telemetry or missing provenance.

How to decide

If contract fields mismatch, stop and update contract/crosswalk via the CAP-108 process (version bump required).

PR-008 — GDPR-GR export pack validation

Goal

Produce GDPR-GR export pack aligned to report-fields crosswalk and validate schema.

Scope

Included:

Export generator

Crosswalk validation

Excluded:

No additional scenario coverage

Expected files touched

Export generation module

Export schema validator

Fixtures

Verification commands

run-evalset pe_release (focus: EVAL-008, EVAL-015)

Evidence artifacts

EVID-010 (exports)

EVID-011 (export validation report)

STOP conditions

Export schema invalid

Evidence pointers in export don’t resolve

Good looks like

Export pack is shareable and integrity-checked.

Bad looks like

Export requires manual editing or includes unstable internal IDs.

How to decide

If regulators need extra fields, propose a future contract change; do not silently add fields.

PR-009 — Wire CI gates to evalsets + artifact publishing

Goal

Make PR-gate short and enforce required checks; publish evidence artifacts.

Scope

Included:

CI config updates

Artifact publishing conventions

Excluded:

No new evaluations

Expected files touched

CI workflow config (1)

Documentation for required checks

Verification commands

run-evalset pe_pr_gate_short (in CI and locally)

ci-local --required

Evidence artifacts

EVID-011 (CI reports)

Published artifacts for PR review

STOP conditions

PRs can merge without PR-gate passing

Required artifacts aren’t produced

Good looks like

Engineers cannot bypass eval-first gates.

Bad looks like

PR-gate is slow enough that teams disable it.

How to decide

If PR-gate exceeds budget, move heavy evals to nightly and keep PR-gate structural/determinism-only.