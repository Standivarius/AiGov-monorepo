#!/usr/bin/env python3
"""Validate deterministic bundle manifest fixtures for EP execution."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP_ROOT = ROOT / "packages" / "ep"
sys.path.insert(0, str(EP_ROOT))

from aigov_ep.scenario.bundle_manifest_v0_1_0 import load_and_validate_manifest
from validate_aigov_dataset_jsonl_v0_1 import _validate_schema


SCHEMA_PATH = (
    ROOT / "packages" / "specs" / "schemas" / "deterministic_bundle_manifest_v0_1_0.schema.json"
)


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


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
