# Pro Run 2 — Codex PR Chain (PR-PRO2-000..005)

This plan is the single, copy/paste-ready source for the Pro Run 2 PR chain.
Keep diffs doc-only and keep PR-gate fast.

## Suite policy (short + explicit)
- **PR-gate**: fast checks only (seconds to a few minutes). No network calls. No long model runs.
- **Nightly**: heavier execution or model-backed checks.
- **Release**: full compliance/export validations.
- **Audit**: evidence packs + Tier A controls.

---

## Status (as-built)

- PR #35 merged: pro-run-2 codex PR chain prompts.
- PR #36 merged: eval_registry.yaml fix + evalsets_registry.yaml added.
- PR #37 merged: planning pack validator + CI check.
- PR #39 merged: evalsets registry schema aligned with execution pack.
- PR #40 merged: nx + codex workflow guidance in AGENTS.md.
- PR #38 merged: contract hardening for judgments/determinism/aggregation/doc-mode (https://github.com/Standivarius/AiGov-monorepo/pull/38).

---

## As-built chain (current reality)

- **Registry spine**: `eval_registry.yaml`, `evalsets_registry.yaml`, `tier_a_coverage_report.md` in `packages/specs/docs/planning/2026-01-22-run/` are the machine backbone.
- **Validator**: `tools/validate_planning_pack.py` enforces evalset membership, runtime tiers, and Tier A coverage.
- **PR-gate**: `pe_pr_gate_short` evalset; nightly/release/audit defined in `evalsets_registry.yaml`.

---

## Next PR prompts

### PR #38 (merged)
```text
PR #38 merged:
https://github.com/Standivarius/AiGov-monorepo/pull/38
```

### PR #42 (contract addendum to unblock validators)
```text
ROLE: You are Codex implementing PR #42 for AiGov-monorepo. Doc-first. No guessing.
MISSION: Unblock anti-gaming validators by defining missing contract field names + schemas.

NON-NEGOTIABLES:
- Do NOT introduce new product concepts.
- Do NOT change locked enums/taxonomies.
- If a validator would require guessing field names, STOP and instead define them in contracts.

TODO (required):
1) Add a Stage A run manifest JSON schema at:
   packages/specs/docs/contracts/execution/run_manifest_v0.schema.json
   Must include at minimum: run_id, start_time_utc (or generated_at_utc), challenge_nonce, and per-artifact captured_at_utc metadata.
2) Add a limitations_log JSON schema at:
   packages/specs/docs/contracts/reporting/limitations_log_v0.schema.json
   Keep aligned with artifact_registry_v0_1.md’s limitations_log definition (timeline_refs/limitations/assumptions).
3) Update scenario_instance_expansion_rules_v0_1.md to require that any “explicit equivalence” assertion includes a non-empty policy_ref and must be labeled as deputy-verified (not VERIFIED_RUNTIME).
4) Update packages/specs/docs/planning/2026-01-22-run/pro_run_2_codex_pr_chain.md:
   - mark PR #38 as merged
   - replace the current PR #42 prompt (validators) with this PR #42 (contracts)
   - add the next PR prompt as PR #43 (validators) AFTER this PR

SUGGESTIONS (optional, only if very small):
- Add 1 short paragraph to report_aggregation_v0_1.md clarifying fail-closed aggregation: any instance INFRINGEMENT/EXECUTION_ERROR => parent INFRINGEMENT.

VERIFY (fast):
- python3 tools/validate_planning_pack.py
- python3 -m compileall tools
- json.load on the new schema files

STOP CONDITIONS:
- Any missing field name would require guessing semantics.
- Touching more than ~6 files.
- Any attempt to change locked enums/taxonomy.

OUTPUT:
- Open PR titled: "pro-run-2: contract addendum to unblock anti-gaming validators"
EFFORT: medium
```

### PR #43 (validators)
```text
ROLE: You are Codex. Implement only high-ROI drift/abuse blockers as validators. Keep PR-gate short.
TASK:
1) Add validators (tools/*.py) for:
   - mock_freshness + nonce presence (nightly on artifacts; structural field presence can be PR-gate)
   - equivalence_evidence_auditor (policy_ref required; report labeling deputy vs runtime)
   - undecided_cap check (enforce cap per eval pass rules)
   - verdict_strictness_check (no legacy aliases in final outputs)
   - doc_mode evidence auditor (timeline/change_log_ref required)
   - fail-closed aggregation validator
   - link integrity validator (content hash vs manifest)
   - golden contamination validator (RAG citations cannot point to golden set ids/paths)
   - out-of-scope cap validator for release
2) Add minimal fixtures for each validator so PR-gate runs in seconds.
3) Wire fast validators into PR workflow; heavy artifact-scanning into nightly/release workflows.
VERIFY:
- Run unit tests/fixtures for validators locally.
- Confirm PR workflow runtime stays short.
STOP IF:
- You can’t find the right contract field names; then update contracts first rather than guessing.
OUTPUT:
- PR titled "pro-run-2: high-ROI integrity validators + pass-rule caps"
EFFORT: medium–high
```
