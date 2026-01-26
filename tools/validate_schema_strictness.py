#!/usr/bin/env python3
"""Validate scenario schema strictness (additionalProperties=false)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _walk_schema(schema: Any, path: str, errors: list[str], allowlist: set[str]) -> None:
    if isinstance(schema, dict):
        schema_type = schema.get("type")
        if schema_type == "object" or "properties" in schema:
            additional = schema.get("additionalProperties")
            if additional is not False and path not in allowlist:
                errors.append(f"{path}: additionalProperties must be false")
        for key, value in schema.items():
            next_path = f"{path}/{key}"
            _walk_schema(value, next_path, errors, allowlist)
    elif isinstance(schema, list):
        for idx, item in enumerate(schema):
            _walk_schema(item, f"{path}/{idx}", errors, allowlist)


def validate_schema_strictness(schema_paths: list[Path], allowlist: set[str]) -> list[str]:
    errors: list[str] = []
    for schema_path in schema_paths:
        if not schema_path.exists():
            errors.append(f"schema not found: {schema_path}")
            continue
        try:
            schema = _load_json(schema_path)
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"{schema_path}: invalid JSON ({exc})")
            continue
        _walk_schema(schema, f"{schema_path}", errors, allowlist)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate scenario schema strictness.")
    parser.add_argument("--schema-list", required=True, help="Path to JSON list of schema paths")
    parser.add_argument("--allowlist", required=False, help="Path to JSON list of allowed schema paths")
    args = parser.parse_args()

    schema_list_path = Path(args.schema_list)
    if not schema_list_path.exists():
        print(f"ERROR: schema list not found: {schema_list_path}")
        return 1
    schema_list = _load_json(schema_list_path)
    if not isinstance(schema_list, list) or not schema_list:
        print("ERROR: schema list must be a non-empty array")
        return 1

    allowlist: set[str] = set()
    if args.allowlist:
        allowlist_path = Path(args.allowlist)
        if not allowlist_path.exists():
            print(f"ERROR: allowlist not found: {allowlist_path}")
            return 1
        allowlist_data = _load_json(allowlist_path)
        if not isinstance(allowlist_data, list):
            print("ERROR: allowlist must be an array")
            return 1
        allowlist = {str(item) for item in allowlist_data}

    schema_paths = [Path(item) for item in schema_list]
    errors = validate_schema_strictness(schema_paths, allowlist)
    if errors:
        print("ERROR: scenario schema strictness failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: scenario schema strictness validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
