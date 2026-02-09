#!/usr/bin/env python3
"""Validate deterministic bundle manifest fixtures for EP execution."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EP_ROOT = ROOT / "packages" / "ep"
sys.path.insert(0, str(EP_ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from aigov_ep.scenario.bundle_manifest_v0_1_0 import load_and_validate_manifest
from _schema_helpers import _validate_schema


SCHEMA_PATH = (
    ROOT / "packages" / "specs" / "schemas" / "deterministic_bundle_manifest_v0_1_0.schema.json"
)


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_manifest_semantics(manifest: dict[str, Any]) -> list[str]:
    scenarios = manifest.get("scenarios")
    if not isinstance(scenarios, list):
        return []

    errors: list[str] = []
    scenario_instance_ids: list[str] = []
    order_ready = True

    seen_scenario_ids: set[str] = set()
    seen_scenario_instance_ids: set[str] = set()
    seen_paths: set[str] = set()

    for index, entry in enumerate(scenarios):
        if not isinstance(entry, dict):
            continue
        scenario_id = entry.get("scenario_id")
        scenario_instance_id = entry.get("scenario_instance_id")
        scenario_path = entry.get("path")

        if isinstance(scenario_id, str):
            if scenario_id in seen_scenario_ids:
                errors.append(
                    "manifest.scenarios[*].scenario_id values must be unique "
                    f"(duplicate {scenario_id!r} at index {index})"
                )
            seen_scenario_ids.add(scenario_id)

        if isinstance(scenario_instance_id, str):
            scenario_instance_ids.append(scenario_instance_id)
            if scenario_instance_id in seen_scenario_instance_ids:
                errors.append(
                    "manifest.scenarios[*].scenario_instance_id values must be unique "
                    f"(duplicate {scenario_instance_id!r} at index {index})"
                )
            seen_scenario_instance_ids.add(scenario_instance_id)
        else:
            order_ready = False

        if isinstance(scenario_path, str):
            if scenario_path in seen_paths:
                errors.append(
                    "manifest.scenarios[*].path values must be unique "
                    f"(duplicate {scenario_path!r} at index {index})"
                )
            seen_paths.add(scenario_path)

    if order_ready and scenario_instance_ids != sorted(scenario_instance_ids):
        errors.append("manifest.scenarios must be sorted by scenario_instance_id")

    return errors


def _validate_manifest_schema(manifest_path: Path) -> list[str]:
    if not manifest_path.exists():
        return [f"manifest.json not found in {manifest_path.parent}"]
    if manifest_path.is_symlink():
        return ["manifest.json must not be a symlink"]

    try:
        manifest = _load_json(manifest_path)
    except json.JSONDecodeError as exc:
        return [f"Invalid manifest.json ({exc.msg})"]

    if not isinstance(manifest, dict):
        return ["manifest must be an object"]

    if not SCHEMA_PATH.exists():
        return [f"schema not found: {SCHEMA_PATH}"]
    schema = _load_json(SCHEMA_PATH)
    if not isinstance(schema, dict):
        return [f"schema must be an object: {SCHEMA_PATH}"]

    errors: list[str] = []
    _validate_schema(manifest, schema, "manifest", errors)
    errors.extend(_validate_manifest_semantics(manifest))
    return sorted(errors)


def validate_ep_deterministic_bundle_manifest(
    bundle_dir: Path,
    *,
    verify_scenario_paths: bool = True,
) -> list[str]:
    deterministic_manifest = bundle_dir / "manifest.json"
    legacy_manifest = bundle_dir / "bundle_manifest.json"
    if deterministic_manifest.exists() and legacy_manifest.exists():
        return ["bundle contains both manifest.json and bundle_manifest.json"]

    schema_errors = _validate_manifest_schema(deterministic_manifest)
    if schema_errors:
        return schema_errors
    if not verify_scenario_paths:
        return []

    try:
        scenario_paths = load_and_validate_manifest(bundle_dir)
    except (ValueError, OSError) as exc:
        return [str(exc)]
    if not scenario_paths:
        return ["manifest returned no scenarios"]
    missing = [path for path in scenario_paths if not path.exists()]
    if missing:
        return [f"scenario path missing: {path}" for path in missing]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate deterministic bundle manifest fixtures.")
    parser.add_argument(
        "--bundle-dir",
        default=str(ROOT / "tools" / "fixtures" / "bundles" / "good"),
        help="Path to bundle fixture directory.",
    )
    parser.add_argument(
        "--no-scenario-path-check",
        action="store_true",
        help="Validate manifest schema only (skip runtime scenario path/hash checks).",
    )
    args = parser.parse_args()

    bundle_dir = Path(args.bundle_dir)
    errors = validate_ep_deterministic_bundle_manifest(
        bundle_dir,
        verify_scenario_paths=not args.no_scenario_path_check,
    )
    if errors:
        print("ERROR: deterministic bundle manifest validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS: deterministic bundle manifest validated: {bundle_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
