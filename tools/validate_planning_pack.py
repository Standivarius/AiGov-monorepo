#!/usr/bin/env python3
"""Validate planning pack registries for Pro Run 2."""
from __future__ import annotations

import sys
from pathlib import Path

from validate_evidence_pack_v0_schema import validate_evidence_pack_v0_fixture


ROOT = Path(__file__).resolve().parents[1]
PLANNING_DIR = ROOT / "packages" / "specs" / "docs" / "planning" / "2026-01-22-run"
EVAL_REGISTRY_PATH = PLANNING_DIR / "eval_registry.yaml"
EVALSETS_REGISTRY_PATH = PLANNING_DIR / "evalsets_registry.yaml"
TIER_A_REPORT_PATH = PLANNING_DIR / "tier_a_coverage_report.md"
EVIDENCE_PACK_V0_PASS_PATH = ROOT / "tools" / "fixtures" / "validators" / "evidence_pack_v0_pass.json"
EVIDENCE_PACK_V0_FAIL_PATH = ROOT / "tools" / "fixtures" / "validators" / "evidence_pack_v0_fail.json"


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


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

    print("PASS: planning pack validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
