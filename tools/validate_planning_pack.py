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
from validate_export_bundle_to_petri_special_instructions_alpha import (
    validate_export_bundle_to_petri_special_instructions_alpha,
)
from validate_scenario_determinism import validate_determinism
from validate_schema_strictness import validate_schema_strictness


ROOT = Path(__file__).resolve().parents[1]
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
CLIENT_INTAKE_FIXTURE = ROOT / "tools" / "fixtures" / "intake" / "client_intake_output_pass.json"
CLIENT_INTAKE_V0_2_PASS_PATH = ROOT / "tools" / "fixtures" / "validators" / "client_intake_v0_2_pass.json"
CLIENT_INTAKE_V0_2_FAIL_PATH = ROOT / "tools" / "fixtures" / "validators" / "client_intake_v0_2_fail.json"
PETRI_SPECIAL_INSTRUCTIONS_FIXTURE = (
    ROOT / "tools" / "fixtures" / "validators" / "petri_special_instructions_from_bundle_pass.json"
)
CLIENT_INTAKE_V0_2_FAIL_CHANNEL_MISMATCH_PATH = (
    ROOT / "tools" / "fixtures" / "validators" / "client_intake_v0_2_fail_channel_mismatch.json"
)
CLIENT_INTAKE_V0_2_FAIL_EMPTY_SUPPORTED_PATH = (
    ROOT / "tools" / "fixtures" / "validators" / "client_intake_v0_2_fail_empty_supported.json"
)
BASE_SCENARIO_EMPTY_SIGNALS_PATH = (
    ROOT / "tools" / "fixtures" / "validators" / "base_scenario_empty_signals.json"
)
BUNDLE_GOOD_DIR = ROOT / "tools" / "fixtures" / "bundles" / "good"
BUNDLE_POISON_DIR = ROOT / "tools" / "fixtures" / "bundles" / "poison"
SCENARIO_COMPILE_BASE_DIR = ROOT / "tools" / "fixtures" / "scenario_compile" / "base"
SCENARIO_COMPILE_OVERRIDE_DIR = ROOT / "tools" / "fixtures" / "scenario_compile" / "overrides"
SCHEMA_LIST_PATH = ROOT / "tools" / "fixtures" / "validators" / "scenario_schema_list.json"


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_base_scenario_fixture(path: Path) -> list[str]:
    if hasattr(base_scenarios, "validate_base_scenario_fixture"):
        return base_scenarios.validate_base_scenario_fixture(path)
    if not path.exists():
        return [f"base scenario fixture missing: {path}"]
    if not base_scenarios.SCHEMA_PATH.exists():
        return [f"base scenario schema missing: {base_scenarios.SCHEMA_PATH}"]
    if not base_scenarios.SIGNALS_PATH.exists():
        return [f"signals registry missing: {base_scenarios.SIGNALS_PATH}"]

    try:
        required, allowed = base_scenarios._load_schema()
        signal_ids = base_scenarios._load_signal_ids()
    except ValueError as exc:
        return [str(exc)]

    try:
        scenario = base_scenarios._ensure_dict(base_scenarios._load_json(path), f"{path}")
    except (json.JSONDecodeError, ValueError) as exc:
        return [f"{path}: invalid JSON ({exc})"]

    errors = base_scenarios._validate_scenario(scenario, required, allowed, signal_ids, path)
    if isinstance(scenario.get("signal_ids"), list) and not scenario.get("signal_ids"):
        errors.append(f"{path}: signal_ids must contain at least one entry")
    return errors


def _parse_eval_registry(lines: list[str]) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    in_evidence = False

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- eval_id:"):
            current = {"eval_id": stripped.split(":", 1)[1].strip()}
            entries.append(current)
            in_evidence = False
            continue

        if current is None:
            continue

        if stripped.startswith("evidence_artifacts:"):
            current["evidence_artifacts"] = []
            in_evidence = True
            continue

        if in_evidence and stripped.startswith("-"):
            artifact = stripped.lstrip("-").strip()
            if artifact:
                current.setdefault("evidence_artifacts", []).append(artifact)
            continue

        if stripped.startswith("-") and not stripped.startswith("- eval_id:"):
            in_evidence = False
            continue

        if ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key in {"ep_id", "runtime_tier", "description", "pass_rule", "notes"}:
                current[key] = value
            in_evidence = False

    return entries


def _parse_evalsets_registry(lines: list[str]) -> list[dict[str, object]]:
    evalsets: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    section: str | None = None

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- evalset_id:"):
            current = {
                "evalset_id": stripped.split(":", 1)[1].strip(),
                "eval_ids": [],
                "stop_conditions": [],
                "required_evidence_artifacts": [],
            }
            evalsets.append(current)
            section = None
            continue

        if current is None:
            continue

        if stripped.startswith("purpose:"):
            current["purpose"] = stripped.split(":", 1)[1].strip()
            section = None
            continue
        if stripped.startswith("runtime_tier:"):
            current["runtime_tier"] = stripped.split(":", 1)[1].strip()
            section = None
            continue
        if stripped.startswith("max_runtime_seconds:"):
            current["max_runtime_seconds"] = stripped.split(":", 1)[1].strip()
            section = None
            continue
        if stripped.startswith("eval_ids:"):
            section = "eval_ids"
            continue
        if stripped.startswith("stop_conditions:"):
            section = "stop_conditions"
            continue
        if stripped.startswith("required_evidence_artifacts:"):
            section = "required_evidence_artifacts"
            continue

        if stripped.startswith("-") and section in {
            "eval_ids",
            "stop_conditions",
            "required_evidence_artifacts",
        }:
            item = stripped.lstrip("-").strip()
            if item:
                current[section].append(item)
            continue

    return evalsets


def _parse_tier_a_controls(lines: list[str]) -> list[dict[str, object]]:
    controls: list[dict[str, object]] = []
    in_section = False
    current: dict[str, object] | None = None

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if stripped == "tier_a_controls:":
            in_section = True
            continue
        if not in_section:
            continue
        if stripped.startswith("coverage_assertion:"):
            break
        if stripped.startswith("- control_id:"):
            current = {
                "control_id": stripped.split(":", 1)[1].strip(),
                "eval_ids": [],
                "evidence_artifacts": [],
            }
            controls.append(current)
            continue
        if current is None:
            continue
        if stripped.startswith("eval_ids:"):
            payload = stripped.split(":", 1)[1]
            current["eval_ids"] = [item.strip() for item in payload.strip(" []").split(",") if item.strip()]
            continue
        if stripped.startswith("evidence_artifacts:"):
            payload = stripped.split(":", 1)[1]
            current["evidence_artifacts"] = [
                item.strip() for item in payload.strip(" []").split(",") if item.strip()
            ]
            continue

    return controls


def main() -> int:
    for path in (EVAL_REGISTRY_PATH, EVALSETS_REGISTRY_PATH, TIER_A_REPORT_PATH):
        if not path.exists():
            print(f"ERROR: missing required file: {path}")
            return 1

    eval_entries = _parse_eval_registry(_read_lines(EVAL_REGISTRY_PATH))
    if not eval_entries:
        print("ERROR: eval_registry.yaml contains no eval entries")
        return 1

    eval_ids = {entry.get("eval_id") for entry in eval_entries if entry.get("eval_id")}
    runtime_tiers = {entry.get("runtime_tier") for entry in eval_entries if entry.get("runtime_tier")}

    evalsets = _parse_evalsets_registry(_read_lines(EVALSETS_REGISTRY_PATH))
    if not evalsets:
        print("ERROR: evalsets_registry.yaml missing evalset entries")
        return 1

    defined_tiers = set()
    missing_fields: list[str] = []
    missing_eval_ids: list[str] = []
    for entry in evalsets:
        evalset_id = entry.get("evalset_id")
        if not evalset_id:
            missing_fields.append("<missing evalset_id>")
            continue
        for field in (
            "purpose",
            "runtime_tier",
            "max_runtime_seconds",
            "eval_ids",
            "stop_conditions",
            "required_evidence_artifacts",
        ):
            value = entry.get(field)
            if value is None or value == "" or value == []:
                missing_fields.append(f"{evalset_id}:{field}")
        runtime_tier = entry.get("runtime_tier")
        if runtime_tier:
            defined_tiers.add(runtime_tier)
        for eval_id in entry.get("eval_ids", []):
            if eval_id not in eval_ids:
                missing_eval_ids.append(f"{evalset_id}:{eval_id}")

    if missing_fields:
        print("ERROR: evalsets_registry.yaml missing required fields:")
        for item in sorted(missing_fields):
            print(f"  - {item}")
        return 1

    if not defined_tiers:
        print("ERROR: evalsets_registry.yaml missing runtime_tier values")
        return 1
    if missing_eval_ids:
        print("ERROR: evalsets reference unknown eval_id values:")
        for item in sorted(missing_eval_ids):
            print(f"  - {item}")
        return 1

    invalid_tiers = sorted([tier for tier in runtime_tiers if tier not in defined_tiers])
    if invalid_tiers:
        print(f"ERROR: runtime_tier values not in evalsets_registry: {invalid_tiers}")
        return 1

    controls = _parse_tier_a_controls(_read_lines(TIER_A_REPORT_PATH))
    if not controls:
        print("ERROR: tier_a_coverage_report.md missing tier_a_controls block")
        return 1

    missing_controls = []
    missing_control_eval_ids: list[str] = []
    for control in controls:
        eval_list = control.get("eval_ids", [])
        evidence_list = control.get("evidence_artifacts", [])
        if not eval_list or not evidence_list:
            missing_controls.append(control.get("control_id", "UNKNOWN"))
        for eval_id in eval_list:
            if eval_id not in eval_ids:
                missing_control_eval_ids.append(
                    f"{control.get('control_id', 'UNKNOWN')}:{eval_id}"
                )
    if missing_controls:
        print("ERROR: Tier A controls missing eval_ids or evidence_artifacts:")
        for control_id in missing_controls:
            print(f"  - {control_id}")
        return 1
    if missing_control_eval_ids:
        print("ERROR: Tier A controls reference unknown eval_ids:")
        for item in sorted(missing_control_eval_ids):
            print(f"  - {item}")
        return 1

    evidence_pack_errors = validate_evidence_pack_v0_fixture(EVIDENCE_PACK_V0_PASS_PATH)
    if evidence_pack_errors:
        print("ERROR: evidence_pack_v0 pass fixture failed validation:")
        for error in evidence_pack_errors:
            print(f"  - {error}")
        return 1
    print(f"PASS: evidence_pack_v0 fixture validated: {EVIDENCE_PACK_V0_PASS_PATH}")

    evidence_pack_fail_errors = validate_evidence_pack_v0_fixture(EVIDENCE_PACK_V0_FAIL_PATH)
    if not evidence_pack_fail_errors:
        print("ERROR: evidence_pack_v0 fail fixture unexpectedly passed validation.")
        return 1
    print(f"FAIL (as expected): evidence_pack_v0 fixture validated: {EVIDENCE_PACK_V0_FAIL_PATH}")

    scenario_errors = base_scenarios.validate_base_scenarios()
    if scenario_errors:
        print("ERROR: base scenario validation failed:")
        for error in scenario_errors:
            print(f"  - {error}")
        return 1

    base_scenario_fail_errors = _validate_base_scenario_fixture(BASE_SCENARIO_EMPTY_SIGNALS_PATH)
    if not base_scenario_fail_errors:
        print("ERROR: base scenario empty signal_ids fixture unexpectedly passed validation.")
        return 1
    print(f"FAIL (as expected): base scenario fixture validated: {BASE_SCENARIO_EMPTY_SIGNALS_PATH}")

    override_errors = validate_override_fixture(CLIENT_OVERRIDE_PASS_PATH)
    if override_errors:
        print("ERROR: client override pass fixture failed validation:")
        for error in override_errors:
            print(f"  - {error}")
        return 1
    print(f"PASS: client override validated: {CLIENT_OVERRIDE_PASS_PATH}")

    override_fail_errors = validate_override_fixture(CLIENT_OVERRIDE_FAIL_PATH)
    if not override_fail_errors:
        print("ERROR: client override fail fixture unexpectedly passed validation.")
        return 1
    print(f"FAIL (as expected): client override validated: {CLIENT_OVERRIDE_FAIL_PATH}")

    override_empty_supported_errors = validate_override_fixture(CLIENT_OVERRIDE_EMPTY_SUPPORTED_PATH)
    if not override_empty_supported_errors:
        print("ERROR: client override empty supported_dsar_channels fixture unexpectedly passed validation.")
        return 1
    print(
        "FAIL (as expected): client override validated: "
        f"{CLIENT_OVERRIDE_EMPTY_SUPPORTED_PATH}"
    )

    intake_v0_2_errors = validate_client_intake(_read_json(CLIENT_INTAKE_V0_2_PASS_PATH), CLIENT_INTAKE_V0_2_PASS_PATH)
    if intake_v0_2_errors:
        print("ERROR: client intake v0.2 pass fixture failed validation:")
        for error in intake_v0_2_errors:
            print(f"  - {error}")
        return 1
    print(f"PASS: client intake v0.2 fixture validated: {CLIENT_INTAKE_V0_2_PASS_PATH}")

    intake_v0_2_fail_errors = validate_client_intake(
        _read_json(CLIENT_INTAKE_V0_2_FAIL_PATH), CLIENT_INTAKE_V0_2_FAIL_PATH
    )
    if not intake_v0_2_fail_errors:
        print("ERROR: client intake v0.2 fail fixture unexpectedly passed validation.")
        return 1
    print(f"FAIL (as expected): client intake v0.2 fixture validated: {CLIENT_INTAKE_V0_2_FAIL_PATH}")

    intake_v0_2_channel_mismatch_errors = validate_client_intake(
        _read_json(CLIENT_INTAKE_V0_2_FAIL_CHANNEL_MISMATCH_PATH),
        CLIENT_INTAKE_V0_2_FAIL_CHANNEL_MISMATCH_PATH,
    )
    if not intake_v0_2_channel_mismatch_errors:
        print("ERROR: client intake v0.2 channel mismatch fixture unexpectedly passed validation.")
        return 1
    print(
        "FAIL (as expected): client intake v0.2 fixture validated: "
        f"{CLIENT_INTAKE_V0_2_FAIL_CHANNEL_MISMATCH_PATH}"
    )

    intake_v0_2_empty_supported_errors = validate_client_intake(
        _read_json(CLIENT_INTAKE_V0_2_FAIL_EMPTY_SUPPORTED_PATH),
        CLIENT_INTAKE_V0_2_FAIL_EMPTY_SUPPORTED_PATH,
    )
    if not intake_v0_2_empty_supported_errors:
        print("ERROR: client intake v0.2 empty supported_dsar_channels fixture unexpectedly passed validation.")
        return 1
    print(
        "FAIL (as expected): client intake v0.2 fixture validated: "
        f"{CLIENT_INTAKE_V0_2_FAIL_EMPTY_SUPPORTED_PATH}"
    )

    intake_errors = validate_client_intake_to_bundle(SCENARIO_COMPILE_BASE_DIR, CLIENT_INTAKE_FIXTURE)
    if intake_errors:
        print("ERROR: client intake -> bundle validation failed:")
        for error in intake_errors:
            print(f"  - {error}")
        return 1
    print(f"PASS: client intake bundle determinism validated: {CLIENT_INTAKE_FIXTURE}")

    bundle_errors = validate_bundle(BUNDLE_GOOD_DIR)
    if bundle_errors:
        print("ERROR: bundle integrity validation failed:")
        for error in bundle_errors:
            print(f"  - {error}")
        return 1
    print(f"PASS: bundle integrity validated: {BUNDLE_GOOD_DIR}")

    bundle_poison_errors = validate_bundle(BUNDLE_POISON_DIR)
    if not bundle_poison_errors:
        print("ERROR: poisoned bundle unexpectedly passed integrity validation.")
        return 1
    print(f"FAIL (as expected): bundle integrity validated: {BUNDLE_POISON_DIR}")

    export_errors = validate_export_bundle_to_petri_special_instructions_alpha(
        BUNDLE_GOOD_DIR, PETRI_SPECIAL_INSTRUCTIONS_FIXTURE
    )
    if export_errors:
        print("ERROR: special_instructions export validation failed:")
        for error in export_errors:
            print(f"  - {error}")
        return 1
    print(
        "PASS: special_instructions export validated: "
        f"{PETRI_SPECIAL_INSTRUCTIONS_FIXTURE}"
    )

    determinism_errors = validate_determinism(SCENARIO_COMPILE_BASE_DIR, SCENARIO_COMPILE_OVERRIDE_DIR)
    if determinism_errors:
        print("ERROR: scenario determinism validation failed:")
        for error in determinism_errors:
            print(f"  - {error}")
        return 1
    print("PASS: scenario determinism validated.")

    schema_list = _read_json(SCHEMA_LIST_PATH)
    if not isinstance(schema_list, list) or not schema_list:
        print(f"ERROR: schema list must be a non-empty array: {SCHEMA_LIST_PATH}")
        return 1
    schema_paths = [Path(item) for item in schema_list if str(item).strip()]
    strictness_errors = validate_schema_strictness(schema_paths, set())
    if strictness_errors:
        print("ERROR: scenario schema strictness failed:")
        for error in strictness_errors:
            print(f"  - {error}")
        return 1
    print("PASS: scenario schema strictness validated.")
    print("PASS: planning pack validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
