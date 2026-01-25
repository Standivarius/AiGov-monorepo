#!/usr/bin/env python3
"""Validate evidence_pack_v0 fixtures against contract shape (stdlib only)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "schema_version",
    "run_dir",
    "scenario_id",
    "target",
    "signals",
    "items",
}


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _validate_signal(signal: Any, idx: int) -> list[str]:
    errors: list[str] = []
    if not isinstance(signal, dict):
        return [f"signals[{idx}] must be an object"]
    signal_id = signal.get("signal_id")
    verdict = signal.get("verdict")
    if not isinstance(signal_id, str) or not signal_id:
        errors.append(f"signals[{idx}].signal_id must be a non-empty string")
    if not isinstance(verdict, str) or not verdict:
        errors.append(f"signals[{idx}].verdict must be a non-empty string")
    confidence = signal.get("confidence")
    if confidence is not None:
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
            errors.append(f"signals[{idx}].confidence must be a number")
        elif confidence < 0 or confidence > 1:
            errors.append(f"signals[{idx}].confidence must be between 0 and 1")
    notes = signal.get("notes")
    if notes is not None and not isinstance(notes, str):
        errors.append(f"signals[{idx}].notes must be a string")
    return errors


def _validate_item(item: Any, idx: int) -> list[str]:
    errors: list[str] = []
    if not isinstance(item, dict):
        return [f"items[{idx}] must be an object"]
    kind = item.get("kind")
    payload = item.get("payload")
    if not isinstance(kind, str) or not kind:
        errors.append(f"items[{idx}].kind must be a non-empty string")
    if not isinstance(payload, dict):
        errors.append(f"items[{idx}].payload must be an object")
    for key in ("signal_id", "verdict", "source", "timestamp_utc"):
        value = item.get(key)
        if value is not None and not isinstance(value, str):
            errors.append(f"items[{idx}].{key} must be a string")
    return errors


def validate_evidence_pack_v0(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["evidence_pack_v0 must be an object"]

    missing = [key for key in REQUIRED_TOP_LEVEL if key not in data]
    if missing:
        errors.append(f"missing required keys: {sorted(missing)}")
        return errors

    if data.get("schema_version") != "0.1.0":
        errors.append("schema_version must be '0.1.0'")
    for key in ("run_dir", "scenario_id", "target"):
        value = data.get(key)
        if not isinstance(value, str) or not value:
            errors.append(f"{key} must be a non-empty string")

    signals = data.get("signals")
    if not isinstance(signals, list):
        errors.append("signals must be an array")
    else:
        for idx, signal in enumerate(signals):
            errors.extend(_validate_signal(signal, idx))

    items = data.get("items")
    if not isinstance(items, list):
        errors.append("items must be an array")
    else:
        for idx, item in enumerate(items):
            errors.extend(_validate_item(item, idx))

    return errors


def validate_evidence_pack_v0_fixture(fixture_path: Path) -> list[str]:
    if not fixture_path.exists():
        return [f"fixture not found: {fixture_path}"]
    try:
        data = _load_json(fixture_path)
    except (json.JSONDecodeError, OSError) as exc:
        return [f"invalid JSON fixture: {exc}"]
    return validate_evidence_pack_v0(data)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate evidence_pack_v0 fixtures against contract shape."
    )
    parser.add_argument("--fixture", required=True, help="Path to fixture JSON")
    args = parser.parse_args()

    errors = validate_evidence_pack_v0_fixture(Path(args.fixture))
    if errors:
        print("ERROR: evidence_pack_v0 fixture failed validation:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("PASS: evidence_pack_v0 fixture validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
