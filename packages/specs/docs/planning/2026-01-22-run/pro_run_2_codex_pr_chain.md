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
- PR #42 merged: contract addendum for run_manifest + limitations_log + equivalence rule (https://github.com/Standivarius/AiGov-monorepo/pull/42).
- PR #43 merged: contract addendum for labels + doc evidence + citations (https://github.com/Standivarius/AiGov-monorepo/pull/43).

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

### PR #43 (merged)
```text
PR #43 merged:
https://github.com/Standivarius/AiGov-monorepo/pull/43
```

### PR #44a (pass-rule caps + validator)
```text
ROLE: You are Codex (implementation agent) in VS Code with full repo access + merge rights.
PR TITLE: "pro-run-2: pass-rule caps + fast fixture validators (short PR-gate)"
EFFORT: medium

MISSION:
Implement the highest-ROI, contract-grounded validators + pass-rule caps, keeping PR-gate fast.
Do NOT add product features. Do NOT guess field names.

TODOs (required):
1) Update pass rules in:
   packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml
   - Add explicit numeric cap for UNDECIDED (e.g., <= 5%) to relevant Stage B evals.
   - Add explicit out-of-scope cap for release context (e.g., 0 unless waived and recorded in limitations_log).

2) Add a fast validator:
   - tools/validate_pass_rule_caps.py
   - Fail-closed on missing caps.

3) Update this plan doc to split PR #44 into #44a/#44b/#44c.

VERIFY:
- python3 tools/validate_planning_pack.py
- python3 tools/validate_pass_rule_caps.py
- NX_DAEMON=false npx nx run evalsets:migration-smoke

OUTPUT:
- PR title: "pro-run-2: pass-rule caps + fast fixture validators (short PR-gate)"
```

### PR #44b (fixture validators)
```text
ROLE: You are Codex. Keep PR-gate fast; fixtures only.
TASK:
- Add verdict/doc-mode/equivalence validators + minimal fixtures only.
- No workflow wiring yet.
OUTPUT:
- PR title: "pro-run-2: fixture validators for verdict/doc-mode/equivalence"
```

### PR #44c (golden validator + runner + workflow)
```text
ROLE: You are Codex. Keep PR-gate short; heavy scans stay nightly/release.
TASK:
- Add golden contamination validator (fixture-based), add a tiny runner, wire PR workflow to run fast checks only.
OUTPUT:
- PR title: "pro-run-2: PR-gate validator runner + golden fixture check"
```
