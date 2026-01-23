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

### PR #42 (contract addendum to unblock validators: labels, doc evidence, citations)
```text
ROLE: You are Codex in VS Code with full repo access.
MISSION: Contract addendum to unblock PR #43 validators. Doc/contracts only. No guessing.

NON-NEGOTIABLES:
- Do NOT add product features.
- Do NOT change existing taxonomies/enums except to codify already-stated labels/modes.
- Make fields machine-checkable (schema or authoritative JSON block), not prose-only.

TODO:
1) Update packages/specs/docs/contracts/reporting/limitations_log_v0.schema.json:
   - add operational_evidence_refs: string[]
   - optionally add change_log_refs: string[] (only if clearly needed; prefer generic)
2) Add a machine-checkable deputy/runtime labeling field:
   - Define verification_label enum with values VERIFIED_RUNTIME and VERIFIED_BY_DEPUTY
   - Place it in the most canonical reporting/scenario contract so outputs can carry it.
3) Update the judgments output schema:
   - add verification_mode field using allowed modes: runtime|doc|timeline|out-of-scope
   - ensure it is present wherever a per-item judgment/finding is represented
4) Define minimal citation tracing schema for golden contamination checks:
   - create packages/specs/docs/contracts/retrieval/retrieval_citations_v0.schema.json
     with citations: [{ evidence_artifact_id: string }]
5) Update packages/specs/docs/planning/2026-01-22-run/pro_run_2_codex_pr_chain.md:
   - insert this PR as the next step before validators
   - add the revised PR #43 validators prompt (now that field names exist)

VERIFY:
- python3 tools/validate_planning_pack.py
- json.load on any modified/new schema file

STOP IF:
- You can’t find the correct existing schema file to edit (search repo first; don’t guess).
- Changes exceed ~6 files; split if needed.

OUTPUT:
- Open PR titled "pro-run-2: contract addendum to unblock validators (labels, doc evidence, citations)"
EFFORT: medium
```

### PR #43 (validators)
```text
ROLE: You are Codex (implementation agent) in VS Code with full repo access.
MISSION: Implement the highest-ROI anti-gaming protections that are now contract-grounded, without guessing. Keep PR-gate short.

PRE-REQ:
- PR #42 is merged. If not, STOP.

NON-NEGOTIABLES:
- No new product features.
- No guessing field names.
- PR-gate stays short; heavy artifact scanning goes nightly/release later.

TODOs (required):
1) Update pass rules in:
   packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml
   Add explicit caps:
   - UNDECIDED cap (e.g., <= 5%) for relevant Stage B evals.
   - Out-of-scope cap for release candidates (e.g., 0 unless explicitly waived and recorded in limitations_log).
   Keep this as edits to existing eval entries; do NOT invent new eval IDs unless absolutely required.

2) Add a fast, fail-closed validator that enforces “pass-rule caps exist”:
   - tools/validate_pass_rule_caps.py
   Checks:
   - Any eval that can emit UNDECIDED must have a numeric cap in pass_rule text.
   - Any evalset marked release must have an out-of-scope cap rule present somewhere (per registry conventions).
   Output: non-zero exit on failure.

3) Add a fast, fail-closed validator for canonical verdicts (fixture-based):
   - tools/validate_verdict_strictness.py
   Inputs:
   - judgments fixture JSON (matching the judgments schema introduced in PR #38)
   - verdict taxonomy (verdicts.json)
   Checks:
   - No legacy aliases appear in final verdicts; canonical-only.

4) Add tiny fixtures + a single PR-gate command:
   - Place fixtures under a repo-consistent location (e.g., tools/fixtures/ or packages/pe/fixtures/).
   - Include one passing + one failing case for each validator.
   - Add a minimal runner command (documented in PR body) that runs both validators in seconds.

5) Wire PR-gate workflow to run ONLY the fixture validators (fast):
   - Add or update .github/workflows accordingly, but do not expand PR-gate runtime.

SUGGESTIONS (optional):
- Add tools/validators_manifest.md describing each validator, what it checks, and where it runs.

VERIFY (must run locally):
- python3 tools/validate_planning_pack.py
- python3 tools/validate_pass_rule_caps.py
- python3 tools/validate_verdict_strictness.py --fixtures <path>
- yaml parse sanity still passes.

STOP CONDITIONS:
- If any validator requires guessing a field name from runtime artifacts, STOP and leave it for a later PR once contracts define those fields.
- If PR-gate runtime increases meaningfully; keep it short.

OUTPUT:
- PR title: "pro-run-2: pass-rule caps + fast fixture validators"
EFFORT: medium
```
