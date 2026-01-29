#!/usr/bin/env python3
"""Build GDPR overrides + deterministic bundle from a client intake JSON (stdlib-only)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EP_ROOT = ROOT / "packages" / "ep"
sys.path.insert(0, str(EP_ROOT))

from aigov_ep.intake.validate import validate_intake_payload
from aigov_ep.scenario.override import generate_override
from aigov_ep.scenario.compiler import compile_bundle
from validate_client_overrides import validate_override_fixture


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def _read_bundle_hash(bundle_dir: Path) -> str:
    manifest_path = bundle_dir / "manifest.json"
    manifest = _ensure_dict(_load_json(manifest_path), str(manifest_path))
    bundle_hash = manifest.get("bundle_hash")
    if not isinstance(bundle_hash, str) or not bundle_hash:
        raise ValueError("manifest.json missing bundle_hash")
    return bundle_hash


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build GDPR scenario overrides and deterministic bundle from intake JSON."
    )
    parser.add_argument("--intake-json", required=True, help="Path to client intake JSON")
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Output directory for overrides/ and bundle/ subdirectories",
    )
    parser.add_argument(
        "--base-dir",
        default=str(ROOT / "packages" / "specs" / "scenarios" / "library" / "base" / "gdpr"),
        help="Base scenario directory (default: GDPR base library)",
    )
    args = parser.parse_args()

    intake_path = Path(args.intake_json)
    output_dir = Path(args.output_dir)
    base_dir = Path(args.base_dir)

    try:
        intake = _ensure_dict(_load_json(intake_path), str(intake_path))
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {intake_path}: invalid JSON ({exc})")
        return 2

    intake_errors = validate_intake_payload(intake)
    if intake_errors:
        for error in intake_errors:
            print(f"ERROR: {error}")
        return 2

    base_files = sorted(base_dir.rglob("*.json"))
    if not base_files:
        print(f"ERROR: no base scenarios found in {base_dir}")
        return 2

    overrides_dir = output_dir / "overrides"
    bundle_dir = output_dir / "bundle"
    overrides_dir.mkdir(parents=True, exist_ok=True)
    bundle_dir.mkdir(parents=True, exist_ok=True)

    override_errors: list[str] = []
    client_id = intake.get("client_id")
    if not isinstance(client_id, str) or not client_id:
        print("ERROR: client_id must be a non-empty string")
        return 2
    for base_path in base_files:
        try:
            base_scenario = _ensure_dict(_load_json(base_path), str(base_path))
        except (json.JSONDecodeError, ValueError) as exc:
            override_errors.append(f"{base_path}: invalid JSON ({exc})")
            continue

        scenario_id = base_scenario.get("scenario_id")
        if not isinstance(scenario_id, str) or not scenario_id:
            override_errors.append(f"{base_path}: scenario_id must be a non-empty string")
            continue

        try:
            override = generate_override(intake, base_scenario)
        except ValueError as exc:
            override_errors.append(f"{base_path}: override generation failed ({exc})")
            continue

        filename = f"{scenario_id}__{client_id}.json"
        override_path = overrides_dir / filename
        _write_json(override_path, override)
        override_errors.extend(validate_override_fixture(override_path))

    if override_errors:
        for error in override_errors:
            print(f"ERROR: {error}")
        return 2

    try:
        compile_bundle(base_dir=base_dir, overrides_dir=overrides_dir, output_dir=bundle_dir)
        bundle_hash = _read_bundle_hash(bundle_dir)
    except ValueError as exc:
        print(f"ERROR: bundle compilation failed ({exc})")
        return 2

    print(f"PASS: bundle built at {bundle_dir} (bundle_hash={bundle_hash})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
