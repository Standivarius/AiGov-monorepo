# Claude Review Evidence v1

Curated excerpts for fast audit of PR stack #150-#154.

## 1) `git diff --name-status origin/main...HEAD`
```text
A	packages/specs/docs/contracts/intake/intake_bundle_stage_artifacts_v0_1.md
M	packages/specs/docs/contracts/intake/intake_bundle_v0_1.md
A	packages/specs/docs/planning/2026-02-08/m_intake_phase2_codex_roadmap.md
A	packages/specs/docs/planning/2026-02-08/m_intake_phase2_milestone_report.md
A	packages/specs/docs/planning/2026-02-08/m_intake_phase2_review_prompt_claude.md
A	packages/specs/docs/planning/2026-02-08/m_intake_phase2_review_prompt_gemini.md
A	packages/specs/schemas/intake_bundle_gap_v0_1.schema.json
A	packages/specs/schemas/intake_bundle_readiness_v0_1.schema.json
A	packages/specs/schemas/intake_bundle_reconcile_v0_1.schema.json
A	tools/fixtures/validators/intake_bundle_gap_questions_order.json
A	tools/fixtures/validators/intake_bundle_gap_questions_order_fail_unsorted.json
A	tools/fixtures/validators/intake_bundle_readiness_blocked_unknown.json
A	tools/fixtures/validators/intake_bundle_readiness_blocked_unknown_fail_status_ready.json
A	tools/fixtures/validators/intake_bundle_reconcile_conflict.json
A	tools/fixtures/validators/intake_bundle_reconcile_conflict_fail_no_critical.json
M	tools/fixtures/validators/scenario_schema_list.json
M	tools/validate_intake_bundle_v0_1.py
M	tools/validate_planning_pack.py
```

## 2) `git log --oneline origin/main..HEAD`
```text
bac0fbb Merge branch 'pr4-phase2-docs' into pr5-phase2-planning
2cfe778 Merge branch 'pr3-phase2-readiness' into pr4-phase2-docs
d919739 Phase 2: add readiness fail fixture gate
11b7782 Merge pr2-phase2-gap into pr3-phase2-readiness
12173d2 Merge origin/pr2-phase2-gap into pr2-phase2-gap
0c3c42a Phase 2: add gap fail fixture gate
1395db1 Phase 2: add gap stage schema + fixture + gates
208202b Phase 2: enforce const + add reconcile fail fixture gate
d256606 Planning: Phase 2 roadmap, milestone report, Claude/Gemini review prompts
c5934b7 Docs: describe stage artifacts and link from intake bundle contract
63aa4ee Phase 2: add readiness stage schema + fixture + gates
9437211 Phase 2: add gap stage schema + fixture + gates
9c919fd Phase 2: add reconcile stage schema + fixture + gates
```

## 3) `git show --stat <commit-sha>` (selected stack commits)

### git show --stat 9c919fd
```text
9c919fd Phase 2: add reconcile stage schema + fixture + gates
 .../intake_bundle_reconcile_v0_1.schema.json       |  80 ++++++++++++++
 .../intake_bundle_reconcile_conflict.json          |  29 +++++
 .../fixtures/validators/scenario_schema_list.json  |   4 +-
 tools/validate_intake_bundle_v0_1.py               | 119 ++++++++++++++++++++-
 tools/validate_planning_pack.py                    |  21 +++-
 5 files changed, 247 insertions(+), 6 deletions(-)
```

### git show --stat 9437211
```text
9437211 Phase 2: add gap stage schema + fixture + gates
 .../schemas/intake_bundle_gap_v0_1.schema.json     | 65 ++++++++++++++++++++++
 .../intake_bundle_gap_questions_order.json         | 27 +++++++++
 .../fixtures/validators/scenario_schema_list.json  |  3 +-
 tools/validate_intake_bundle_v0_1.py               | 49 +++++++++++++++-
 tools/validate_planning_pack.py                    | 17 ++++++
 5 files changed, 158 insertions(+), 3 deletions(-)
```

### git show --stat 63aa4ee
```text
63aa4ee Phase 2: add readiness stage schema + fixture + gates
 .../intake_bundle_readiness_v0_1.schema.json       | 79 ++++++++++++++++++++++
 .../intake_bundle_readiness_blocked_unknown.json   | 24 +++++++
 .../fixtures/validators/scenario_schema_list.json  |  3 +-
 tools/validate_intake_bundle_v0_1.py               | 73 ++++++++++++++++++--
 tools/validate_planning_pack.py                    | 17 +++++
 5 files changed, 191 insertions(+), 5 deletions(-)
```

### git show --stat c5934b7
```text
c5934b7 Docs: describe stage artifacts and link from intake bundle contract
 .../intake/intake_bundle_stage_artifacts_v0_1.md   | 43 ++++++++++++++++++++++
 .../docs/contracts/intake/intake_bundle_v0_1.md    |  3 ++
 2 files changed, 46 insertions(+)
```

### git show --stat d256606
```text
d256606 Planning: Phase 2 roadmap, milestone report, Claude/Gemini review prompts
 .../2026-02-08/m_intake_phase2_codex_roadmap.md    | 170 +++++++++++++++++++++
 .../2026-02-08/m_intake_phase2_milestone_report.md |  52 +++++++
 .../m_intake_phase2_review_prompt_claude.md        |  48 ++++++
 .../m_intake_phase2_review_prompt_gemini.md        |  47 ++++++
 4 files changed, 317 insertions(+)
```

### git show --stat 208202b
```text
208202b Phase 2: enforce const + add reconcile fail fixture gate
 ...bundle_reconcile_conflict_fail_no_critical.json | 18 ++++++++++++
 tools/validate_intake_bundle_v0_1.py               |  3 ++
 tools/validate_planning_pack.py                    | 32 ++++++++++++++++++++++
 3 files changed, 53 insertions(+)
```

### git show --stat 0c3c42a
```text
0c3c42a Phase 2: add gap fail fixture gate
 ...e_bundle_gap_questions_order_fail_unsorted.json | 27 ++++++++++++++++++
 tools/validate_planning_pack.py                    | 32 ++++++++++++++++++++++
 2 files changed, 59 insertions(+)
```

### git show --stat d919739
```text
d919739 Phase 2: add readiness fail fixture gate
 ...eadiness_blocked_unknown_fail_status_ready.json | 17 ++++++++++++
 tools/validate_planning_pack.py                    | 32 ++++++++++++++++++++++
 2 files changed, 49 insertions(+)
```

## 4) Validator excerpt: `tools/validate_intake_bundle_v0_1.py`
_Source commit: `d919739`_
```python
#!/usr/bin/env python3
"""Validate intake_bundle_v0_1 fixtures (stdlib-only, fail-closed)."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "packages" / "specs" / "schemas" / "intake_bundle_v0_1.schema.json"
RECONCILE_SCHEMA_PATH = ROOT / "packages" / "specs" / "schemas" / "intake_bundle_reconcile_v0_1.schema.json"
GAP_SCHEMA_PATH = ROOT / "packages" / "specs" / "schemas" / "intake_bundle_gap_v0_1.schema.json"
READINESS_SCHEMA_PATH = ROOT / "packages" / "specs" / "schemas" / "intake_bundle_readiness_v0_1.schema.json"
JURISDICTIONS_PATH = (
    ROOT / "packages" / "specs" / "docs" / "contracts" / "taxonomy" / "jurisdictions_v0.json"
)
SECTORS_PATH = ROOT / "packages" / "specs" / "docs" / "contracts" / "taxonomy" / "sectors_v0.json"
POLICY_PACKS_PATH = (
    ROOT / "packages" / "specs" / "docs" / "contracts" / "taxonomy" / "policy_packs_v0.json"
)
FORBIDDEN_ROOT_FIELDS = ("generated_at", "processed_at")


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _validate_schema(value: Any, schema: dict[str, Any], path: str, errors: list[str]) -> None:
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path} must equal constant {schema['const']!r}")

    schema_type = schema.get("type")
    if schema_type == "object":
        if not isinstance(value, dict):
            errors.append(f"{path} must be an object")
            return
        min_properties = schema.get("minProperties")
        if isinstance(min_properties, int) and len(value) < min_properties:
            errors.append(f"{path} must contain at least {min_properties} properties")
        max_properties = schema.get("maxProperties")
        if isinstance(max_properties, int) and len(value) > max_properties:
            errors.append(f"{path} must contain at most {max_properties} properties")
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in value:
                    errors.append(f"{path} missing required key '{key}'")

        properties = schema.get("properties", {})
        pattern_properties = schema.get("patternProperties", {})
        additional = schema.get("additionalProperties", True)

        if isinstance(properties, dict):
            for key, prop_schema in properties.items():
                if key in value and isinstance(prop_schema, dict):
                    _validate_schema(value[key], prop_schema, f"{path}.{key}", errors)

        for key in sorted(value.keys()):
            if isinstance(properties, dict) and key in properties:
                continue
            matched_patterns = []
            if isinstance(pattern_properties, dict):
                for pattern, prop_schema in pattern_properties.items():
                    if not isinstance(prop_schema, dict):
                        continue
                    if re.fullmatch(pattern, key):
                        matched_patterns.append((pattern, prop_schema))
            if matched_patterns:
                for pattern, prop_schema in sorted(matched_patterns, key=lambda item: item[0]):
                    _validate_schema(
                        value[key],
                        prop_schema,
                        f"{path}.{key}",
                        errors,
                    )
                continue

            if additional is False:
                errors.append(f"{path} has unexpected key '{key}'")
                continue
            if isinstance(additional, dict):
                _validate_schema(value[key], additional, f"{path}.{key}", errors)
        return

    if schema_type == "array":
        if not isinstance(value, list):
            errors.append(f"{path} must be an array")
            return
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(value) < min_items:
            errors.append(f"{path} must contain at least {min_items} item(s)")
        max_items = schema.get("maxItems")
        if isinstance(max_items, int) and len(value) > max_items:
            errors.append(f"{path} must contain at most {max_items} item(s)")
        items_schema = schema.get("items")
        if isinstance(items_schema, dict):
            for idx, item in enumerate(value):
                _validate_schema(item, items_schema, f"{path}[{idx}]", errors)
        return

    if schema_type == "string":
        if not isinstance(value, str):
            errors.append(f"{path} must be a string")
            return
        min_length = schema.get("minLength")
        if isinstance(min_length, int) and len(value) < min_length:
            errors.append(f"{path} must be at least {min_length} character(s)")
        enum = schema.get("enum")
        if isinstance(enum, list) and value not in enum:
            errors.append(f"{path} must be one of {enum}")
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.fullmatch(pattern, value) is None:
            errors.append(f"{path} must match pattern '{pattern}'")
        return

    if schema_type == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            errors.append(f"{path} must be an integer")
            return
        minimum = schema.get("minimum")
        if isinstance(minimum, int) and value < minimum:
            errors.append(f"{path} must be >= {minimum}")
        maximum = schema.get("maximum")
        if isinstance(maximum, int) and value > maximum:
            errors.append(f"{path} must be <= {maximum}")
        return

    if schema_type == "boolean":
        if not isinstance(value, bool):
            errors.append(f"{path} must be a boolean")
        return

    errors.append(f"{path} has unsupported schema type '{schema_type}'")


def _load_allowlist(path: Path, label: str) -> set[str]:
    if not path.exists():
        raise ValueError(f"{label} allowlist not found: {path}")
    data = _load_json(path)
    if not isinstance(data, list):
        raise ValueError(f"{label} allowlist must be an array")
    items: set[str] = set()
    for item in data:
        if not isinstance(item, str):
            raise ValueError(f"{label} allowlist must contain strings")
        if not item.strip():
            raise ValueError(f"{label} allowlist must not contain blank entries")
        items.add(item)
    if not items:
        raise ValueError(f"{label} allowlist must not be empty")
    return items


def _validate_context_profile(
    bundle: dict[str, Any],
    jurisdictions: set[str],
    sectors: set[str],
    policy_packs: set[str],
    errors: list[str],
) -> None:
    intake = bundle.get("intake")
    if not isinstance(intake, dict):
        return
    context_profile = intake.get("context_profile")
    if not isinstance(context_profile, dict):
        return

    jurisdiction = context_profile.get("jurisdiction")
    jurisdiction_valid = False
    if isinstance(jurisdiction, str):
        if jurisdiction in jurisdictions:
            jurisdiction_valid = True
        else:
            errors.append(
                f"intake.context_profile.jurisdiction contains unknown value '{jurisdiction}'"
            )

    sector = context_profile.get("sector")
    sector_valid = False
    if isinstance(sector, str):
        if sector in sectors:
            sector_valid = True
        else:
            errors.append(f"intake.context_profile.sector contains unknown value '{sector}'")

    policy_pack_stack = context_profile.get("policy_pack_stack")
    if not isinstance(policy_pack_stack, list):
        return
    if not jurisdiction_valid or not sector_valid:
        return
    unknown_packs = sorted(
        {
            pack
            for pack in policy_pack_stack
            if isinstance(pack, str) and pack not in policy_packs
        }
    )
    if unknown_packs:
        errors.append(
            "intake.context_profile.policy_pack_stack contains unknown value(s): "
            f"{unknown_packs}"
        )
        return

    expected_stack = ["GDPR_EU", jurisdiction, sector, "client"]
    if policy_pack_stack != expected_stack:
        errors.append(
            "intake.context_profile.policy_pack_stack must equal "
            f"{expected_stack}"
        )
```

## 5) Gate wiring excerpt: `tools/validate_planning_pack.py`
_Source commit: `d919739`_
```python
#!/usr/bin/env python3
"""Validate planning pack registries for Pro Run 2."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import validate_base_scenarios as base_scenarios
from validate_evidence_pack_v0_schema import validate_evidence_pack_v0_fixture
from validate_client_overrides import validate_override_fixture
from validate_bundle_integrity import validate_bundle
from validate_client_intake_to_bundle import validate_client_intake_to_bundle
from validate_client_intake_v0_2 import validate_client_intake
from validate_aigov_dataset_jsonl_v0_1 import validate_dataset_jsonl
from validate_interface_ledger import validate_interface_ledger
from validate_ep_deterministic_bundle_manifest import validate_ep_deterministic_bundle_manifest
from validate_export_bundle_to_petri_seed_instructions_alpha import (
    validate_export_bundle_to_petri_seed_instructions_alpha,
)
from validate_liverun_inspect_task_args_v0_1 import validate_inspect_task_args
from validate_liverun_output_artifacts_envelope_v0_1 import (
    validate_liverun_output_artifacts_dir,
)
from validate_intake_bundle_v0_1 import (
    validate_intake_bundle_fixture,
    validate_intake_bundle_gap_fixture,
    validate_intake_bundle_readiness_fixture,
    validate_intake_bundle_reconcile_fixture,
)
from validate_module_cards import validate_module_cards
from validate_module_dashboard_snapshot import validate_module_dashboard_snapshot
from validate_print_inspect_petri_run_command import validate_print_inspect_petri_run_command
from validate_scenario_determinism import validate_determinism
from validate_schema_strictness import validate_schema_strictness


ROOT = Path(__file__).resolve().parents[1]
EP_ROOT = ROOT / "packages" / "ep"
sys.path.insert(0, str(EP_ROOT))

from aigov_ep.intake.validate import validate_intake_payload
PLANNING_DIR = ROOT / "packages" / "specs" / "docs" / "planning" / "2026-01-22-run"
EVAL_REGISTRY_PATH = PLANNING_DIR / "eval_registry.yaml"
EVALSETS_REGISTRY_PATH = PLANNING_DIR / "evalsets_registry.yaml"
TIER_A_REPORT_PATH = PLANNING_DIR / "tier_a_coverage_report.md"
EVIDENCE_PACK_V0_PASS_PATH = ROOT / "tools" / "fixtures" / "validators" / "evidence_pack_v0_pass.json"
EVIDENCE_PACK_V0_FAIL_PATH = ROOT / "tools" / "fixtures" / "validators" / "evidence_pack_v0_fail.json"
CLIENT_OVERRIDE_PASS_PATH = ROOT / "tools" / "fixtures" / "validators" / "client_override_pass.json"
CLIENT_OVERRIDE_FAIL_PATH = ROOT / "tools" / "fixtures" / "validators" / "client_override_fail.json"
CLIENT_OVERRIDE_EMPTY_SUPPORTED_PATH = (
    ROOT / "tools" / "fixtures" / "validators" / "client_override_empty_supported.json"
)
CLIENT_OVERRIDE_UNKNOWN_VOCAB_PATH = (
    ROOT / "tools" / "fixtures" / "validators" / "client_override_fail_unknown_vocab.json"
)
CLIENT_OVERRIDE_NONDETERMINISTIC_FIELD_PATH = (
    ROOT / "tools" / "fixtures" / "validators" / "client_override_fail_nondeterministic_field.json"
)
CLIENT_INTAKE_FIXTURE = (
    ROOT / "tools" / "fixtures" / "validators" / "intake_output_context_pass_nl_public.json"
)
CLIENT_INTAKE_V0_2_PASS_PATH = ROOT / "tools" / "fixtures" / "validators" / "client_intake_v0_2_pass.json"
CLIENT_INTAKE_V0_2_FAIL_PATH = ROOT / "tools" / "fixtures" / "validators" / "client_intake_v0_2_fail.json"
INTAKE_OUTPUT_CONTEXT_PASS_NL_PUBLIC_PATH = (
    ROOT / "tools" / "fixtures" / "validators" / "intake_output_context_pass_nl_public.json"
)
INTAKE_OUTPUT_CONTEXT_PASS_NL_HEALTHCARE_PATH = (
    ROOT / "tools" / "fixtures" / "validators" / "intake_output_context_pass_nl_healthcare.json"
)
INTAKE_OUTPUT_CONTEXT_PASS_LEGACY_LOCALE_ONLY_PATH = (
    ROOT
    / "tools"
    / "fixtures"
    / "validators"
    / "intake_output_context_pass_legacy_locale_only_nl.json"
)
INTAKE_OUTPUT_CONTEXT_FAIL_PACK_ORDER_PATH = (
    ROOT / "tools" / "fixtures" / "validators" / "intake_output_context_fail_pack_order.json"
)
INTAKE_OUTPUT_CONTEXT_FAIL_LOCALE_CONTEXT_NULL_PATH = (
    ROOT
    / "tools"
    / "fixtures"
    / "validators"
    / "intake_output_context_fail_locale_context_null.json"
)
INTAKE_OUTPUT_CONTEXT_FAIL_UNKNOWN_JURISDICTION_PATH = (
    ROOT
    / "tools"
    / "fixtures"
    / "validators"
    / "intake_output_context_fail_unknown_jurisdiction.json"
)
INTAKE_OUTPUT_CONTEXT_FAIL_UNKNOWN_SECTOR_PATH = (
    ROOT / "tools" / "fixtures" / "validators" / "intake_output_context_fail_unknown_sector.json"
)
INTAKE_OUTPUT_CONTEXT_FAIL_MISSING_LOCALE_AND_CONTEXT_PATH = (
    ROOT
    / "tools"
    / "fixtures"
    / "validators"
    / "intake_output_context_fail_missing_locale_and_context.json"
)
INTAKE_BUNDLE_V0_1_PASS_PATH = (
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_pass.json"
)
INTAKE_BUNDLE_RECONCILE_CONFLICT_PATH = (
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_reconcile_conflict.json"
)
INTAKE_BUNDLE_RECONCILE_FAIL_PATHS = [
    ROOT
    / "tools"
    / "fixtures"
    / "validators"
    / "intake_bundle_reconcile_conflict_fail_no_critical.json",
]
INTAKE_BUNDLE_RECONCILE_FAIL_EXPECTED_SUBSTRINGS = {
    ROOT
    / "tools"
    / "fixtures"
    / "validators"
    / "intake_bundle_reconcile_conflict_fail_no_critical.json": "must contain at least one critical conflict",
}
INTAKE_BUNDLE_GAP_QUESTIONS_ORDER_PATH = (
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_gap_questions_order.json"
)
INTAKE_BUNDLE_READINESS_BLOCKED_UNKNOWN_PATH = (
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_readiness_blocked_unknown.json"
)
INTAKE_BUNDLE_READINESS_FAIL_PATHS = [
    ROOT
    / "tools"
    / "fixtures"
    / "validators"
    / "intake_bundle_readiness_blocked_unknown_fail_status_ready.json",
]
INTAKE_BUNDLE_READINESS_FAIL_EXPECTED_SUBSTRINGS = {
    ROOT
    / "tools"
    / "fixtures"
    / "validators"
    / "intake_bundle_readiness_blocked_unknown_fail_status_ready.json": "must be 'blocked'",
}
INTAKE_BUNDLE_GAP_FAIL_PATHS = [
    ROOT
    / "tools"
    / "fixtures"
    / "validators"
    / "intake_bundle_gap_questions_order_fail_unsorted.json",
]
INTAKE_BUNDLE_GAP_FAIL_EXPECTED_SUBSTRINGS = {
    ROOT
    / "tools"
    / "fixtures"
    / "validators"
    / "intake_bundle_gap_questions_order_fail_unsorted.json": "must be sorted by question_id",
}
INTAKE_BUNDLE_V0_1_FAIL_PATHS = [
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_missing_required.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_empty_evidence_index.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_empty_evidence_refs.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_extra_key.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_sha256_uppercase.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_timestamp_field.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_dangling_evidence_ref.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_evidence_refs_empty_array.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_unknown_jurisdiction.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_unknown_sector.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_unknown_policy_pack.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_empty_bundle_id.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_source_path_traversal.json",
]
INTAKE_BUNDLE_V0_1_FAIL_EXPECTED_SUBSTRINGS = {
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_missing_required.json": "missing required key",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_empty_evidence_index.json": "evidence_index",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_empty_evidence_refs.json": "evidence_refs",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_extra_key.json": "unexpected key",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_sha256_uppercase.json": "sha256",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_timestamp_field.json": "forbidden root-level nondeterministic field",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_dangling_evidence_ref.json": "dangling reference",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_evidence_refs_empty_array.json": "must contain at least 1 item",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_unknown_jurisdiction.json": "unknown value 'FR'",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_unknown_sector.json": "unknown value 'finance'",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_unknown_policy_pack.json": "unknown value(s): ['enterprise']",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_empty_bundle_id.json": "bundle_id",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_source_path_traversal.json": "traversal source_path",
}
# Single-mode count checks are limited to fixtures where exactly one policy error
# is contractually expected. Other fail fixtures assert the primary error via
# substring but may accumulate additional schema-derived errors by design.
INTAKE_BUNDLE_V0_1_SINGLE_MODE_FAIL_PATHS = {
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_timestamp_field.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_unknown_jurisdiction.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_unknown_sector.json",
    ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_unknown_policy_pack.json",
}
PETRI_SEED_INSTRUCTIONS_FIXTURE = (
    ROOT / "tools" / "fixtures" / "validators" / "petri_seed_instructions_from_bundle_pass.json"
)
RUNPACK_SEED_FIXTURE = ROOT / "tools" / "fixtures" / "runpack" / "seed_instructions_pass.json"
RUNPACK_EXPECTED_COMMAND = (
    ROOT / "tools" / "fixtures" / "runpack" / "expected_inspect_command_pass.txt"
)
RUNPACK_TOOL_PATH = ROOT / "tools" / "print_inspect_petri_run_command.py"
INSPECT_TASK_ARGS_PASS_PATH = ROOT / "tools" / "fixtures" / "validators" / "inspect_task_args_v0_1_pass.json"
INSPECT_TASK_ARGS_FAIL_PATH = ROOT / "tools" / "fixtures" / "validators" / "inspect_task_args_v0_1_fail.json"
LIVERUN_OUTPUT_ARTIFACTS_PASS_DIR = ROOT / "tools" / "fixtures" / "liverun_artifacts_v0_1" / "pass"
LIVERUN_OUTPUT_ARTIFACTS_FAIL_DIR = ROOT / "tools" / "fixtures" / "liverun_artifacts_v0_1" / "fail"
DATASET_JSONL_PASS_PATH = ROOT / "tools" / "fixtures" / "validators" / "dataset_jsonl_v0_1_pass.jsonl"
DATASET_JSONL_FAIL_NONDET_PATH = (
    ROOT
    / "tools"
    / "fixtures"
    / "validators"
    / "dataset_jsonl_v0_1_fail_nondeterministic_field.jsonl"
)
DATASET_JSONL_FAIL_SHA_PATH = (
    ROOT
    / "tools"
```

## 6) Stage schema headers (current branch)

### `packages/specs/schemas/intake_bundle_reconcile_v0_1.schema.json`
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Intake Bundle Reconcile v0.1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "bundle_id",
    "conflicts"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "const": "intake_bundle_reconcile_v0_1"
    },
    "bundle_id": {
      "type": "string",
      "minLength": 1
    },
    "conflicts": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "conflict_id",
          "field_path",
          "severity",
          "left_value",
          "right_value",
          "evidence_refs",
          "resolution"
        ],
        "properties": {
          "conflict_id": {
            "type": "string",
            "pattern": "^C-[0-9]{3}$"
          },
          "field_path": {
            "type": "string",
            "minLength": 1
          },
          "severity": {
            "type": "string",
            "enum": [
              "critical",
              "high",
              "medium",
              "low"
            ]
          },
          "left_value": {
            "type": "string",
            "minLength": 1
          },
          "right_value": {
            "type": "string",
            "minLength": 1
          },
          "evidence_refs": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "string",
              "minLength": 1
            }
          },
          "resolution": {
            "type": "string",
            "enum": [
              "unresolved",
              "resolved"
            ]
          }
        }
      }
    }
  }
}
```

### `packages/specs/schemas/intake_bundle_gap_v0_1.schema.json`
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Intake Bundle Gap v0.1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "bundle_id",
    "clarification_questions"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "const": "intake_bundle_gap_v0_1"
    },
    "bundle_id": {
      "type": "string",
      "minLength": 1
    },
    "clarification_questions": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "question_id",
          "field_path",
          "question",
          "priority",
          "blocking"
        ],
        "properties": {
          "question_id": {
            "type": "string",
            "pattern": "^Q-[0-9]{3}$"
          },
          "field_path": {
            "type": "string",
            "minLength": 1
          },
          "question": {
            "type": "string",
            "minLength": 1
          },
          "priority": {
            "type": "integer",
            "minimum": 1
          },
          "blocking": {
            "type": "boolean"
          },
          "evidence_refs": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "string",
              "minLength": 1
            }
          }
        }
      }
    }
  }
}
```

### `packages/specs/schemas/intake_bundle_readiness_v0_1.schema.json`
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Intake Bundle Readiness v0.1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "bundle_id",
    "status",
    "blocking_unknowns",
    "unresolved_conflict_ids",
    "allow_downstream"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "const": "intake_bundle_readiness_v0_1"
    },
    "bundle_id": {
      "type": "string",
      "minLength": 1
    },
    "status": {
      "type": "string",
      "enum": [
        "ready",
        "blocked"
      ]
    },
    "blocking_unknowns": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "field_path",
          "severity",
          "question_id"
        ],
        "properties": {
          "field_path": {
            "type": "string",
            "minLength": 1
          },
          "severity": {
            "type": "string",
            "enum": [
              "critical",
              "high",
              "medium",
              "low"
            ]
          },
          "question_id": {
            "type": "string",
            "pattern": "^Q-[0-9]{3}$"
          }
        }
      }
    },
    "unresolved_conflict_ids": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^C-[0-9]{3}$"
      }
    },
    "allow_downstream": {
      "type": "boolean"
    },
    "notes": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1
      }
    }
  }
}
```
