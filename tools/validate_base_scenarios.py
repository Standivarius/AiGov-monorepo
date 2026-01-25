#!/usr/bin/env python3
"""Validate base scenario library entries (stdlib-only)."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LIB_DIR = ROOT / "packages" / "specs" / "scenarios" / "library" / "base"
SCHEMA_PATH = ROOT / "packages" / "specs" / "scenarios" / "schemas" / "base_scenario_v1.schema.json"
SIGNALS_PATH = ROOT / "packages" / "specs" / "docs" / "contracts" / "taxonomy" / "signals.json"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _ensure_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return value


def _load_schema() -> tuple[set[str], set[str]]:
    schema = _ensure_dict(_load_json(SCHEMA_PATH), "schema")
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    if not isinstance(required, list):
        raise ValueError("schema.required must be an array")
    if not isinstance(properties, dict):
        raise ValueError("schema.properties must be an object")
    return set(required), set(properties.keys())


def _load_signal_ids() -> set[str]:
    signals = _ensure_dict(_load_json(SIGNALS_PATH), "signals registry")
    signal_ids = signals.get("signal_ids")
    if not isinstance(signal_ids, list) or not signal_ids:
        raise ValueError("signals registry missing signal_ids list")
    return {str(signal_id) for signal_id in signal_ids}


def _validate_scenario(
    scenario: dict[str, Any],
    required: set[str],
    allowed: set[str],
    signal_ids: set[str],
    path: Path,
) -> list[str]:
    errors: list[str] = []
    keys = set(scenario.keys())
    missing = sorted(required - keys)
    extra = sorted(keys - allowed)
    if missing:
        errors.append(f"{path}: missing required keys: {missing}")
    if extra:
        errors.append(f"{path}: extra keys not allowed: {extra}")

    if "signal_ids" in scenario:
        try:
            signals = _ensure_list(scenario.get("signal_ids"), f"{path}: signal_ids")
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if not signals:
                errors.append(f"{path}: signal_ids must contain at least one entry")
            for signal in signals:
                if not isinstance(signal, str) or not signal:
                    errors.append(f"{path}: signal_ids must be non-empty strings")
                    continue
                if signal not in signal_ids:
                    errors.append(f"{path}: unknown signal_id '{signal}'")

    for key in ("scenario_id", "title", "version", "framework", "role", "risk_category", "auditor_seed"):
        value = scenario.get(key)
        if key in required and (not isinstance(value, str) or not value):
            errors.append(f"{path}: {key} must be a non-empty string")

    tags = scenario.get("tags")
    if tags is not None and not isinstance(tags, list):
        errors.append(f"{path}: tags must be an array of strings")
    if isinstance(tags, list):
        for tag in tags:
            if not isinstance(tag, str) or not tag:
                errors.append(f"{path}: tags must be non-empty strings")
                break

    return errors


def validate_base_scenarios() -> list[str]:
    errors: list[str] = []
    if not LIB_DIR.exists():
        return [f"base scenario library missing: {LIB_DIR}"]
    if not SCHEMA_PATH.exists():
        return [f"base scenario schema missing: {SCHEMA_PATH}"]
    if not SIGNALS_PATH.exists():
        return [f"signals registry missing: {SIGNALS_PATH}"]

    try:
        required, allowed = _load_schema()
        signal_ids = _load_signal_ids()
    except ValueError as exc:
        return [str(exc)]

    scenario_files = sorted(LIB_DIR.rglob("*.json"))
    if not scenario_files:
        return ["no base scenarios found"]

    for path in scenario_files:
        try:
            scenario = _ensure_dict(_load_json(path), f"{path}")
        except (json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{path}: invalid JSON ({exc})")
            continue
        errors.extend(_validate_scenario(scenario, required, allowed, signal_ids, path))

    return errors


def validate_base_scenario_fixture(path: Path) -> list[str]:
    if not path.exists():
        return [f"base scenario fixture missing: {path}"]
    if not SCHEMA_PATH.exists():
        return [f"base scenario schema missing: {SCHEMA_PATH}"]
    if not SIGNALS_PATH.exists():
        return [f"signals registry missing: {SIGNALS_PATH}"]

    try:
        required, allowed = _load_schema()
        signal_ids = _load_signal_ids()
        scenario = _ensure_dict(_load_json(path), f"{path}")
    except (json.JSONDecodeError, ValueError) as exc:
        return [f"{path}: invalid JSON ({exc})"]
    return _validate_scenario(scenario, required, allowed, signal_ids, path)


def main() -> int:
    errors = validate_base_scenarios()
    if errors:
        print("ERROR: base scenario validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: base scenarios validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
