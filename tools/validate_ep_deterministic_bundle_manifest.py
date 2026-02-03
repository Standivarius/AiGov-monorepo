#!/usr/bin/env python3
"""Validate deterministic bundle manifest fixtures for EP execution."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP_ROOT = ROOT / "packages" / "ep"
sys.path.insert(0, str(EP_ROOT))

from aigov_ep.scenario.bundle_manifest_v0_1_0 import load_and_validate_manifest


def validate_ep_deterministic_bundle_manifest(bundle_dir: Path) -> list[str]:
    deterministic_manifest = bundle_dir / "manifest.json"
    legacy_manifest = bundle_dir / "bundle_manifest.json"
    if deterministic_manifest.exists() and legacy_manifest.exists():
        return ["bundle contains both manifest.json and bundle_manifest.json"]
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
    bundle_dir = ROOT / "tools" / "fixtures" / "bundles" / "good"
    errors = validate_ep_deterministic_bundle_manifest(bundle_dir)
    if errors:
        print("ERROR: deterministic bundle manifest validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS: deterministic bundle manifest validated: {bundle_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
