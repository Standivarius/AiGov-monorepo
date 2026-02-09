#!/usr/bin/env python3
"""Validate intake_source_snapshot_v0_1 fixtures (stdlib-only, fail-closed)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from validate_aigov_dataset_jsonl_v0_1 import _validate_schema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "packages" / "specs" / "schemas" / "intake_source_snapshot_v0_1.schema.json"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _validate_snapshot_policy(payload: dict[str, Any], errors: list[str]) -> None:
    source_files = payload.get("source_files")
    if not isinstance(source_files, list):
        return

    source_paths: list[str] = []
    seen_paths: set[str] = set()

    for index, entry in enumerate(source_files):
        if not isinstance(entry, dict):
            continue
        source_path = entry.get("source_path")
        if not isinstance(source_path, str):
            continue

        source_paths.append(source_path)
        if source_path in seen_paths:
            errors.append(
                "source_snapshot.source_files.source_path values must be unique "
                f"(duplicate {source_path!r} at index {index})"
            )
        seen_paths.add(source_path)

        path_obj = Path(source_path)
        if path_obj.is_absolute():
            errors.append(
                f"source_snapshot.source_files[{index}].source_path must be relative"
            )
        if any(part == ".." for part in path_obj.parts):
            errors.append(
                f"source_snapshot.source_files[{index}].source_path must not contain traversal segments"
            )

    if source_paths != sorted(source_paths):
        errors.append("source_snapshot.source_files must be sorted by source_path")


def validate_intake_source_snapshot_fixture(path: Path) -> list[str]:
    if not path.exists():
        return [f"fixture not found: {path}"]
    if not SCHEMA_PATH.exists():
        return [f"source snapshot schema not found: {SCHEMA_PATH}"]

    try:
        schema = _ensure_dict(_load_json(SCHEMA_PATH), "schema")
    except (json.JSONDecodeError, ValueError) as exc:
        return [f"source snapshot schema invalid: {exc}"]

    try:
        payload = _ensure_dict(_load_json(path), str(path))
    except (json.JSONDecodeError, ValueError) as exc:
        return [f"{path}: invalid JSON ({exc})"]

    errors: list[str] = []
    _validate_schema(payload, schema, "source_snapshot", errors)
    _validate_snapshot_policy(payload, errors)
    return sorted(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate intake_source_snapshot_v0_1 fixtures.")
    parser.add_argument("--fixture", required=True, help="Path to source snapshot fixture")
    args = parser.parse_args()

    errors = validate_intake_source_snapshot_fixture(Path(args.fixture))
    if errors:
        print("ERROR: intake source snapshot fixture failed validation:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS: intake source snapshot fixture validated: {args.fixture}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
