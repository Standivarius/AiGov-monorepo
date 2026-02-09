#!/usr/bin/env python3
"""Validate intake_bundle_extract_v0_1 fixtures (stdlib-only, fail-closed)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from validate_aigov_dataset_jsonl_v0_1 import _validate_schema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "packages" / "specs" / "schemas" / "intake_bundle_extract_v0_1.schema.json"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _validate_extract_policy(payload: dict[str, Any], errors: list[str]) -> None:
    extracted_fields = payload.get("extracted_fields")
    if not isinstance(extracted_fields, list):
        return

    field_paths: list[str] = []
    seen_field_paths: set[str] = set()

    for index, entry in enumerate(extracted_fields):
        if not isinstance(entry, dict):
            continue
        field_path = entry.get("field_path")
        if not isinstance(field_path, str):
            continue
        field_paths.append(field_path)

        if field_path in seen_field_paths:
            errors.append(
                "extract.extracted_fields.field_path values must be unique "
                f"(duplicate {field_path!r} at index {index})"
            )
        seen_field_paths.add(field_path)

        evidence_refs = entry.get("evidence_refs")
        if isinstance(evidence_refs, list) and evidence_refs != sorted(evidence_refs):
            errors.append(
                f"extract.extracted_fields[{index}].evidence_refs must be sorted"
            )
        if isinstance(evidence_refs, list) and len(evidence_refs) != len(set(evidence_refs)):
            errors.append(
                f"extract.extracted_fields[{index}].evidence_refs must be unique"
            )

    if field_paths != sorted(field_paths):
        errors.append("extract.extracted_fields must be sorted by field_path")


def validate_intake_bundle_extract_fixture(path: Path) -> list[str]:
    if not path.exists():
        return [f"fixture not found: {path}"]
    if not SCHEMA_PATH.exists():
        return [f"extract schema not found: {SCHEMA_PATH}"]

    try:
        schema = _ensure_dict(_load_json(SCHEMA_PATH), "schema")
    except (json.JSONDecodeError, ValueError) as exc:
        return [f"extract schema invalid: {exc}"]

    try:
        payload = _ensure_dict(_load_json(path), str(path))
    except (json.JSONDecodeError, ValueError) as exc:
        return [f"{path}: invalid JSON ({exc})"]

    errors: list[str] = []
    _validate_schema(payload, schema, "extract", errors)
    _validate_extract_policy(payload, errors)
    return sorted(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate intake_bundle_extract_v0_1 fixtures.")
    parser.add_argument("--fixture", required=True, help="Path to intake bundle extract fixture")
    args = parser.parse_args()

    errors = validate_intake_bundle_extract_fixture(Path(args.fixture))
    if errors:
        print("ERROR: intake bundle extract fixture failed validation:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS: intake bundle extract fixture validated: {args.fixture}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
