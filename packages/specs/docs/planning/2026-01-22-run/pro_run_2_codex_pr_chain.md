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
- PR #42 merged: contract addendum for anti-gaming validators (run_manifest/limitations_log schemas + expansion rules).

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

### PR #42 (merged)
```text
PR #42 merged:
https://github.com/Standivarius/AiGov-monorepo/pull/42
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
