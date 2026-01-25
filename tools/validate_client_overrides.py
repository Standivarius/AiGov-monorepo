#!/usr/bin/env python3
"""Validate client scenario overrides (stdlib-only)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "packages" / "specs" / "schemas" / "client_scenario_override_v0.schema.json"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _ensure_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return value


def _load_schema_keys(schema_path: Path) -> tuple[set[str], set[str]]:
    schema = _ensure_dict(_load_json(schema_path), "schema")
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    if not isinstance(required, list) or not isinstance(properties, dict):
        raise ValueError("override schema must define required + properties")
    return set(required), set(properties.keys())


def validate_override(override: dict[str, Any], path: Path, required: set[str], allowed: set[str]) -> list[str]:
    errors: list[str] = []
    keys = set(override.keys())
    missing = sorted(required - keys)
    extra = sorted(keys - allowed)
    if missing:
        errors.append(f"{path}: missing required keys: {missing}")
    if extra:
        errors.append(f"{path}: extra keys not allowed: {extra}")

    if override.get("schema_version") != "0.1.0":
        errors.append(f"{path}: schema_version must be '0.1.0'")

    for key in ("client_id", "base_scenario_id", "override_type"):
        value = override.get(key)
        if not isinstance(value, str) or not value:
            errors.append(f"{path}: {key} must be a non-empty string")
    if override.get("override_type") not in {"partial_patch"}:
        errors.append(f"{path}: override_type must be 'partial_patch'")

    policy_profile = override.get("policy_profile")
    if not isinstance(policy_profile, dict):
        errors.append(f"{path}: policy_profile must be an object")
        return errors

    policy_required = {"supported_dsar_channels", "right_to_erasure_handling", "known_client_constraints"}
    policy_allowed = set(policy_required)
    policy_keys = set(policy_profile.keys())
    missing_policy = sorted(policy_required - policy_keys)
    extra_policy = sorted(policy_keys - policy_allowed)
    if missing_policy:
        errors.append(f"{path}: policy_profile missing keys: {missing_policy}")
    if extra_policy:
        errors.append(f"{path}: policy_profile extra keys not allowed: {extra_policy}")

    supported = policy_profile.get("supported_dsar_channels")
    if isinstance(supported, list):
        supported_channels = []
        for channel in supported:
            if not isinstance(channel, str) or not channel:
                errors.append(f"{path}: supported_dsar_channels must be non-empty strings")
            else:
                supported_channels.append(channel)
    else:
        errors.append(f"{path}: supported_dsar_channels must be an array")
        supported_channels = []

    constraints = policy_profile.get("known_client_constraints")
    if not isinstance(constraints, list):
        errors.append(f"{path}: known_client_constraints must be an array")
    elif any(not isinstance(item, str) or not item for item in constraints):
        errors.append(f"{path}: known_client_constraints must be non-empty strings")

    r2e = policy_profile.get("right_to_erasure_handling")
    if not isinstance(r2e, dict):
        errors.append(f"{path}: right_to_erasure_handling must be an object")
        return errors

    r2e_required = {"primary_channel", "fallback_channels", "constraints"}
    r2e_keys = set(r2e.keys())
    missing_r2e = sorted(r2e_required - r2e_keys)
    extra_r2e = sorted(r2e_keys - r2e_required)
    if missing_r2e:
        errors.append(f"{path}: right_to_erasure_handling missing keys: {missing_r2e}")
    if extra_r2e:
        errors.append(f"{path}: right_to_erasure_handling extra keys not allowed: {extra_r2e}")

    primary = r2e.get("primary_channel")
    fallback = r2e.get("fallback_channels")
    r2e_constraints = r2e.get("constraints")
    if not isinstance(primary, str) or not primary:
        errors.append(f"{path}: primary_channel must be a non-empty string")
    if not isinstance(fallback, list):
        errors.append(f"{path}: fallback_channels must be an array")
        fallback = []
    if not isinstance(r2e_constraints, list):
        errors.append(f"{path}: constraints must be an array")
    elif any(not isinstance(item, str) or not item for item in r2e_constraints):
        errors.append(f"{path}: constraints must be non-empty strings")

    if supported_channels and isinstance(primary, str) and primary:
        if primary not in supported_channels:
            errors.append(f"{path}: primary_channel '{primary}' not in supported_dsar_channels")
    if supported_channels and isinstance(fallback, list):
        for channel in fallback:
            if not isinstance(channel, str) or not channel:
                errors.append(f"{path}: fallback_channels must be non-empty strings")
                continue
            if channel not in supported_channels:
                errors.append(f"{path}: fallback_channel '{channel}' not in supported_dsar_channels")

    return errors


def validate_override_fixture(fixture_path: Path) -> list[str]:
    if not fixture_path.exists():
        return [f"fixture not found: {fixture_path}"]
    if not SCHEMA_PATH.exists():
        return [f"override schema not found: {SCHEMA_PATH}"]
    try:
        required, allowed = _load_schema_keys(SCHEMA_PATH)
    except ValueError as exc:
        return [str(exc)]
    try:
        override = _ensure_dict(_load_json(fixture_path), str(fixture_path))
    except (json.JSONDecodeError, ValueError) as exc:
        return [f"{fixture_path}: invalid JSON ({exc})"]
    return validate_override(override, fixture_path, required, allowed)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate client override fixtures.")
    parser.add_argument("--fixture", required=True, help="Path to override fixture JSON")
    args = parser.parse_args()

    errors = validate_override_fixture(Path(args.fixture))
    if errors:
        print("ERROR: client override validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: client override validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
