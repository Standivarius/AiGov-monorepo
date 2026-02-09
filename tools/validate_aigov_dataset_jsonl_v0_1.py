#!/usr/bin/env python3
"""Validate AiGov Dataset JSONL v0.1 fixtures (stdlib-only)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from _schema_helpers import _validate_schema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "packages" / "specs" / "schemas" / "aigov_dataset_jsonl_v0_1.schema.json"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def validate_dataset_jsonl(path: Path) -> list[tuple[int, str]]:
    if not path.exists():
        return [(0, f"dataset jsonl not found: {path}")]
    if not SCHEMA_PATH.exists():
        return [(0, f"dataset jsonl schema not found: {SCHEMA_PATH}")]
    try:
        schema = _ensure_dict(_load_json(SCHEMA_PATH), "schema")
    except (json.JSONDecodeError, ValueError) as exc:
        return [(0, f"schema invalid: {exc}")]

    errors: list[tuple[int, str]] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append((line_no, f"invalid JSON ({exc})"))
            continue
        if not isinstance(value, dict):
            errors.append((line_no, "line must be a JSON object"))
            continue
        line_errors: list[str] = []
        _validate_schema(value, schema, "record", line_errors)
        for message in sorted(line_errors):
            errors.append((line_no, message))

    return sorted(errors, key=lambda item: (item[0], item[1]))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AiGov Dataset JSONL v0.1 fixtures.")
    parser.add_argument("--fixture", required=True, help="Path to dataset JSONL fixture")
    args = parser.parse_args()

    errors = validate_dataset_jsonl(Path(args.fixture))
    if errors:
        print("ERROR: dataset JSONL validation failed:")
        for line_no, message in errors:
            if line_no:
                print(f"  - line {line_no}: {message}")
            else:
                print(f"  - {message}")
        return 1
    print("PASS: dataset JSONL validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
