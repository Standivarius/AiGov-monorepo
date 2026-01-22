# Pro Run 2 — Codex PR Chain (PR-PRO2-000..005)

This plan is the single, copy/paste-ready source for the Pro Run 2 PR chain.
Keep diffs doc-only and keep PR-gate fast.

## Suite policy (short + explicit)
- **PR-gate**: fast checks only (seconds to a few minutes). No network calls. No long model runs.
- **Nightly**: heavier execution or model-backed checks.
- **Release**: full compliance/export validations.
- **Audit**: evidence packs + Tier A controls.

---

## PR-PRO2-000 — Scaffold run pack + invariants

**Goal**: Establish the Pro Run 2 pack index and invariants in one place.

**TODOs**
- Add pack index doc (list of required run artifacts + ownership).
- Define invariants (no drift between pack items).

**Suggestions**
- Use short bullet lists, no prose walls.

**Good looks like**
- Single index for the run pack with stable IDs.

**Bad looks like**
- Invariants spread across multiple files.

**How to decide**
- If a future PR needs a new artifact, add it to the index here.

**File touch list (exact)**
- `packages/specs/docs/planning/2026-01-22-run/pro_run_2_pack_index.md`

**Verification commands**
```bash
rg -n "Pro Run 2 pack index" packages/specs/docs/planning/2026-01-22-run/pro_run_2_pack_index.md
```

**Stop conditions**
- Any non-doc file changes.
- Any new product feature proposals.

**Evidence artifacts**
- Pack index doc committed.

**Codex prompt (copy/paste)**
```text
Implement PR-PRO2-000:
- Create pro_run_2_pack_index.md under packages/specs/docs/planning/2026-01-22-run.
- Include required artifacts list + ownership + invariants.
- Doc-only changes. Keep PR-gate short in notes.
- Verify with rg for the title.
```

---

## PR-PRO2-001 — Update EP↔eval spine and pass-rule anchors

**Goal**: Ensure EP → acceptance criteria → eval links are consistent and referenced in one place.

**TODOs**
- Reconcile EP list with eval_registry ownership.
- Confirm each EP has ≥1 eval and evidence artifacts.

**Suggestions**
- Add a small consistency note for CROSS_CUTTING evals.

**Good looks like**
- No dangling EPs or evals.

**Bad looks like**
- Eval IDs in PRD that don’t exist in registry.

**How to decide**
- If an eval is internal, use CROSS_CUTTING.

**File touch list (exact)**
- `packages/specs/docs/planning/2026-01-22-run/PRD_PACk_v0.1.md`
- `packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml`

**Verification commands**
```bash
python3 - <<'PY'
import re, pathlib, sys
root = pathlib.Path('packages/specs/docs/planning/2026-01-22-run')
prd = root / 'PRD_PACk_v0.1.md'
ev = root / 'eval_registry.yaml'
prd_text = prd.read_text(encoding='utf-8')
ev_text = ev.read_text(encoding='utf-8')
prd_caps = set(re.findall(r"CAP-\\d{3}", prd_text))
ev_caps = set(re.findall(r"\\bep_id\\s+(CAP-\\d{3}|CROSS_CUTTING)", ev_text))
owners = {}
for m in re.finditer(r"eval_id\\s+(EVAL-\\d{3}).*?\\n\\s*ep_id\\s+(CAP-\\d{3}|CROSS_CUTTING)", ev_text, re.S):
    owners.setdefault(m.group(2), []).append(m.group(1))
missing = sorted([c for c in prd_caps if c not in owners])
dangling = sorted([c for c in ev_caps if c != 'CROSS_CUTTING' and c not in prd_caps])
print('PRD caps:', sorted(prd_caps))
print('Eval ep_ids:', sorted(ev_caps))
print('Dangling eval ep_ids (should be empty):', dangling)
print('PRD caps with zero evals (should be empty):', missing)
sys.exit(1 if dangling or missing else 0)
PY
```

**Stop conditions**
- Any change to contracts or runtime code.

**Evidence artifacts**
- Updated PRD + eval_registry.

**Codex prompt (copy/paste)**
```text
Implement PR-PRO2-001:
- Reconcile EP links in PRD with eval_registry ownership.
- Ensure every EP has >=1 eval; re-tag internal evals to CROSS_CUTTING.
- Doc-only changes in planning files.
- Run the verification python snippet in the plan.
```

---

## PR-PRO2-002 — Stage A evidence pack linkage

**Goal**: Lock the Stage A evidence artifacts and manifests referenced in PRD and registry.

**TODOs**
- Ensure Stage A evidence artifacts are consistent across PRD and eval_registry.

**Suggestions**
- Keep artifact names/types stable and short.

**Good looks like**
- Stage A artifacts are referenced consistently across docs.

**Bad looks like**
- Artifact name drift or mixed naming conventions.

**How to decide**
- If an artifact is used in multiple stages, keep a single canonical label.

**File touch list (exact)**
- `packages/specs/docs/planning/2026-01-22-run/PRD_PACk_v0.1.md`
- `packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml`

**Verification commands**
```bash
rg -n "Stage A|EVID-004|transcript" packages/specs/docs/planning/2026-01-22-run/PRD_PACk_v0.1.md
rg -n "EVID-004" packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml
```

**Stop conditions**
- Any new artifact type without explicit rationale.

**Evidence artifacts**
- Consistent Stage A artifact references.

**Codex prompt (copy/paste)**
```text
Implement PR-PRO2-002:
- Align Stage A evidence artifact labels between PRD and eval_registry.
- Doc-only changes; do not add new concepts.
- Run the rg checks in the plan.
```

---

## PR-PRO2-003 — Stage B judge evidence + determinism

**Goal**: Ensure Stage B judgment artifacts and determinism checks are anchored consistently.

**TODOs**
- Align judgment artifact names and determinism checks.

**Suggestions**
- Keep determinism notes in eval_registry only.

**Good looks like**
- Judgments artifacts appear once, with consistent labels.

**Bad looks like**
- Mixed labels for the same judgment artifact.

**How to decide**
- If output is produced by Stage B, label it once and reuse.

**File touch list (exact)**
- `packages/specs/docs/planning/2026-01-22-run/PRD_PACk_v0.1.md`
- `packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml`

**Verification commands**
```bash
rg -n "Stage B|EVID-006|judgment" packages/specs/docs/planning/2026-01-22-run/PRD_PACk_v0.1.md
rg -n "EVID-006" packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml
```

**Stop conditions**
- Any change outside planning docs.

**Evidence artifacts**
- Consistent Stage B artifact references.

**Codex prompt (copy/paste)**
```text
Implement PR-PRO2-003:
- Align Stage B judgment artifact labels between PRD and eval_registry.
- Doc-only changes; run rg checks.
```

---

## PR-PRO2-004 — Reporting + export crosswalk validation

**Goal**: Keep report/export artifact references aligned with the crosswalk contracts.

**TODOs**
- Confirm report/export artifact naming consistency.

**Suggestions**
- Keep PRD high-level; put details in eval_registry.

**Good looks like**
- Report artifact names align with eval_registry evidence artifacts.

**Bad looks like**
- PRD mentions artifacts that eval_registry does not list.

**How to decide**
- If an artifact is required by crosswalk, ensure it is in eval_registry evidence_artifacts.

**File touch list (exact)**
- `packages/specs/docs/planning/2026-01-22-run/PRD_PACk_v0.1.md`
- `packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml`

**Verification commands**
```bash
rg -n "EVID-007|EVID-008|EVID-009|EVID-010" packages/specs/docs/planning/2026-01-22-run/PRD_PACk_v0.1.md
rg -n "EVID-007|EVID-008|EVID-009|EVID-010" packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml
```

**Stop conditions**
- Introducing new report layers or changing L1/L2/L3 semantics.

**Evidence artifacts**
- Crosswalk-aligned evidence artifacts.

**Codex prompt (copy/paste)**
```text
Implement PR-PRO2-004:
- Align report/export artifact references between PRD and eval_registry.
- Keep it doc-only and run the rg checks.
```

---

## PR-PRO2-005 — Tier A controls consistency note

**Goal**: Keep Tier A coverage map consistent with eval registry and PRD notes.

**TODOs**
- Ensure Tier A coverage report references eval IDs that exist.

**Suggestions**
- Add a small note about CROSS_CUTTING evals in the Tier A report.

**Good looks like**
- Tier A controls map to existing eval IDs.

**Bad looks like**
- Tier A control references missing eval IDs.

**How to decide**
- If a control is purely internal, keep its eval ep_id as CROSS_CUTTING.

**File touch list (exact)**
- `packages/specs/docs/planning/2026-01-22-run/tier_a_coverage_report.md`
- `packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml`

**Verification commands**
```bash
rg -n "EVAL-20[1-9]|EVAL-210" packages/specs/docs/planning/2026-01-22-run/tier_a_coverage_report.md
rg -n "EVAL-20[1-9]|EVAL-210" packages/specs/docs/planning/2026-01-22-run/eval_registry.yaml
```

**Stop conditions**
- Removing any Tier A control without replacement.

**Evidence artifacts**
- Tier A coverage report stays consistent.

**Codex prompt (copy/paste)**
```text
Implement PR-PRO2-005:
- Reconcile Tier A coverage report eval IDs with eval_registry.
- Keep it doc-only and run rg checks.
```
