# M_Execution: Deterministic Bundle Consumption (GDPR-only)

Date: 2026-02-08  
Status: Planned (planning-first)

## Objective
Make EP execution consume deterministic bundles through a contract-first, fail-closed boundary:
- canonical Specs schema + contract for deterministic `manifest.json`
- stdlib-only validator coverage with PASS/FAIL fixtures
- planning-pack gate assertions for deterministic PASS and expected FAIL
- runtime hardening for dual-manifest ambiguity (`manifest.json` + `bundle_manifest.json`)

## Non-Goals
- No OPA runtime execution.
- No PAR adapter implementation.
- No LLM council / multi-agent extraction.
- No non-GDPR expansion.
- No new repo structure.

## Guardrails
- Contract-first + fail-closed.
- Deterministic behavior and deterministic error messages.
- Stdlib-only validators where possible.
- PR size strictness: `<=6 files changed per PR`.
- Prefer checks in `tools/validate_planning_pack.py` over `tools/run_pr_gate_validators.sh`.
- Allowed proof commands (and only these):
  - `python3 tools/validate_planning_pack.py`
  - `bash tools/run_pr_gate_validators.sh`
  - `NX_DAEMON=false npx nx run evalsets:migration-smoke`

## Repo Reality Alignment
- Deterministic runtime loader exists: `packages/ep/aigov_ep/scenario/bundle_manifest_v0_1_0.py`.
- CLI currently prefers deterministic `manifest.json`, else legacy `bundle_manifest.json`: `packages/ep/aigov_ep/cli.py`.
- Existing good deterministic fixture: `tools/fixtures/bundles/good/manifest.json`.
- Existing good fixture includes `schema_version`, `scenarios`, `bundle_hash`, and `bundle_dir`.

## Manifest Contract Decisions (Non-Negotiable)
- Canonical schema version: `0.1.0`.
- Stage shape must include:
  - root `schema_version == "0.1.0"`
  - root `scenarios[]`
  - each scenario requires `scenario_id`, `scenario_instance_id`, `path`, `sha256`
- `bundle_hash` and `bundle_dir` are optional but validated when present; do not require them in `v0_1_0` schema.
- Schema strictness: `additionalProperties: false`.
- Schema/policy boundary must be explicit:
  - schema: structural fields + strictness
  - runtime policy: traversal/symlink/hash verification

## PR Slice Plan (4 slices total)

### PR1 — Specs Contract + Schema Baseline
Effort: M  
Status: Done

Exact file list (`<=6`):
- `packages/specs/schemas/deterministic_bundle_manifest_v0_1_0.schema.json` (new)
- `packages/specs/docs/contracts/execution/deterministic_bundle_manifest_v0_1_0.md` (new)
- `tools/fixtures/validators/scenario_schema_list.json` (register new schema)
- `packages/specs/docs/contracts/interfaces/I_Ledger.md` (point deterministic bundle row to canonical schema/contract)
- `packages/specs/docs/planning/2026-02-08/m_exec_deterministic_bundles_codex_roadmap.md` (status stamping)

Fixtures to add:
- none

Acceptance criteria (test-first):
- schema strictness list includes new schema before runtime changes land.
- schema and contract match runtime manifest shape/version (`0.1.0`) and strictness policy.
- schema-vs-policy boundary documented in contract text.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

Execution tracking:
- Branch: `mexec-det-bundles-integration` (slice commit for later cherry-pick)
- PR: TBD
- Proofs: PASS (`python3 tools/validate_planning_pack.py`, `bash tools/run_pr_gate_validators.sh`, `NX_DAEMON=false npx nx run evalsets:migration-smoke`)
- Smoke log: `docs/logs/EVALSET-MIGRATION-SMOKE-v1_20260209_075225.log`

### PR2 — Schema Validator + PASS/FAIL Fixture Gate
Effort: M  
Status: Planned

Exact file list (`<=6`):
- `tools/validate_ep_deterministic_bundle_manifest.py` (extend to validate `manifest.json` against new Specs schema using stdlib-only schema helper patterns)
- `tools/fixtures/bundles/fail_manifest_bad_schema_version/manifest.json` (new fail fixture)
- `tools/validate_planning_pack.py` (wire PASS + expected FAIL substring assertions)
- `packages/specs/docs/planning/2026-02-08/m_exec_deterministic_bundles_codex_roadmap.md` (status stamping)

Fixtures to add:
- PASS (existing): `tools/fixtures/bundles/good`
- FAIL (new): `tools/fixtures/bundles/fail_manifest_bad_schema_version`
- FAIL fixture is manifest-only; gate asserts schema-fail and does not attempt scenario file verification for that fixture.

Expected failure substring:
- `schema_version must be \"0.1.0\"` (or equivalent deterministic schema-validation message agreed in implementation)

Acceptance criteria (test-first):
- planning-pack reports deterministic manifest PASS on good bundle.
- planning-pack reports deterministic manifest FAIL on new fail fixture with expected substring.
- no brittle free-form check; explicit substring assertion in planning-pack.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

### PR3 — EP CLI Ambiguity Hardening (Fail-Closed)
Effort: M  
Status: Planned

Exact file list (`<=6`):
- `packages/ep/aigov_ep/cli.py` (if both manifests exist, print explicit error and exit `2`)
- `tools/validate_ep_deterministic_bundle_manifest.py` (add deterministic ambiguity probe)
- `tools/fixtures/bundles/fail_dual_manifest/manifest.json` (committed dual-manifest fixture)
- `tools/fixtures/bundles/fail_dual_manifest/bundle_manifest.json` (committed dual-manifest fixture)
- `tools/validate_planning_pack.py` (assert ambiguity failure path)
- `packages/specs/docs/planning/2026-02-08/m_exec_deterministic_bundles_codex_roadmap.md` (status stamping)

Fixtures to add:
- Add committed fixture `tools/fixtures/bundles/fail_dual_manifest/` containing both `manifest.json` and `bundle_manifest.json`; planning-pack asserts ambiguity fail.

Acceptance criteria (test-first):
- dual-manifest case fails closed deterministically with explicit message.
- legacy-only bundle path remains backward compatible.
- deterministic-only manifest path continues to work.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

### PR4 — Closeout Docs + Review Prompts + Roadmap Stamping
Effort: S  
Status: Planned

Exact file list (`<=6`):
- `packages/specs/docs/planning/2026-02-08/m_exec_deterministic_bundles_milestone_report.md` (new, final report)
- `packages/specs/docs/planning/2026-02-08/m_exec_deterministic_bundles_milestone_report_skeleton.md` (mark as consumed/finalized)
- `packages/specs/docs/planning/2026-02-08/m_exec_deterministic_bundles_review_prompt_claude.md` (new)
- `packages/specs/docs/planning/2026-02-08/m_exec_deterministic_bundles_review_prompt_claude_adversarial.md` (new)
- `packages/specs/docs/planning/2026-02-08/m_exec_deterministic_bundles_codex_roadmap.md` (final statuses + PR numbers + proof logs)

Fixtures to add:
- none

Acceptance criteria (test-first):
- report includes delivered files, merged PR links, proof evidence, and residual risks.
- roadmap fully stamped (Planned -> Done, PR numbers, proof log refs).
- two Claude review prompts are self-contained with commands and invariants.

Proof commands:
- `python3 tools/validate_planning_pack.py`
- `bash tools/run_pr_gate_validators.sh`
- `NX_DAEMON=false npx nx run evalsets:migration-smoke`

## Definition of Done
- [ ] Specs schema + contract exist for deterministic manifest `0.1.0` and match runtime shape.
- [ ] Schema is strict (`additionalProperties: false`) and enforces scenario required fields.
- [ ] `bundle_hash` + `bundle_dir` modeled as optional and validated when present.
- [ ] Tools validator validates `manifest.json` against Specs schema (stdlib-only path).
- [ ] planning-pack gates deterministic bundle PASS + expected FAIL substring.
- [ ] EP CLI fails closed on dual-manifest ambiguity with explicit error and exit code `2`.
- [ ] Legacy-only `bundle_manifest.json` flow remains operational.
- [ ] Every PR in milestone is `<=6` files.
- [ ] Allowed proof commands pass for each slice.
- [ ] Closeout docs and review prompts are published.

## Stop Conditions / Rescope Triggers
- If schema requirements diverge from actual runtime manifest shape, pause and resolve contract/schema first.
- If fail-fixture design forces broad fixture duplication beyond guardrails, split fixture strategy into additional small PRs.
- If CLI hardening requires non-GDPR behavior changes, split those out of this milestone.
