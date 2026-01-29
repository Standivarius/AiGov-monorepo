#!/usr/bin/env python3
"""Validate intake -> overrides -> bundle determinism (stdlib-only)."""
from __future__ import annotations

import json
import sys
import tempfile
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


def _read_bundle_manifest(output_dir: Path) -> tuple[str, list[dict[str, Any]]]:
    manifest_path = output_dir / "manifest.json"
    manifest = _ensure_dict(_load_json(manifest_path), str(manifest_path))
    bundle_hash = manifest.get("bundle_hash")
    if not isinstance(bundle_hash, str) or not bundle_hash:
        raise ValueError("manifest.json missing bundle_hash")
    scenarios = manifest.get("scenarios")
    if not isinstance(scenarios, list):
        raise ValueError("manifest.json scenarios must be a list")
    return bundle_hash, scenarios


def validate_client_intake_to_bundle(base_dir: Path, intake_path: Path) -> list[str]:
    try:
        intake = _ensure_dict(_load_json(intake_path), str(intake_path))
    except (json.JSONDecodeError, ValueError) as exc:
        return [f"{intake_path}: invalid JSON ({exc})"]

    intake_errors = validate_intake_payload(intake)
    if intake_errors:
        return [f"{intake_path}: {error}" for error in intake_errors]

    base_dir = Path(base_dir)
    if not base_dir.exists():
        return [f"base scenario directory missing: {base_dir}"]

    bundle_hashes: list[str] = []
    base_files = sorted(base_dir.rglob("*.json"))
    if not base_files:
        return [f"No base scenarios found in {base_dir}"]

    for _ in range(3):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            overrides_dir = temp_path / "overrides"
            bundle_dir = temp_path / "bundle"
            override_errors: list[str] = []

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

                override_path = overrides_dir / f"{scenario_id}.json"
                _write_json(override_path, override)
                override_errors.extend(validate_override_fixture(override_path))

            if override_errors:
                return override_errors

            try:
                compile_bundle(base_dir=base_dir, overrides_dir=overrides_dir, output_dir=bundle_dir)
                bundle_hash, scenarios = _read_bundle_manifest(bundle_dir)
            except ValueError as exc:
                return [str(exc)]

            if not scenarios:
                return ["bundle manifest contains no scenarios"]
            bundle_hashes.append(bundle_hash)

    if len(set(bundle_hashes)) != 1:
        return [f"bundle_hash mismatch across runs: {bundle_hashes}"]
    return []
