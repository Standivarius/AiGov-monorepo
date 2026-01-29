#!/usr/bin/env python3
"""Validate GDPR-only client intake v0.2 fixtures (stdlib-only)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "0.2.0"
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "packages" / "specs" / "schemas" / "client_intake_v0_2.schema.json"


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


def _require_keys(payload: dict[str, Any], required: set[str], label: str) -> list[str]:
    keys = set(payload.keys())
    missing = sorted(required - keys)
    extra = sorted(keys - required)
    errors = []
    if missing:
        errors.append(f"{label} missing required keys: {missing}")
    if extra:
        errors.append(f"{label} contains extra keys: {extra}")
    return errors


def validate_client_intake(payload: dict[str, Any], path: Path) -> list[str]:
    errors: list[str] = []
    required = {"schema_version", "client_id", "base_scenario_ids", "policy_profile"}
    errors.extend(_require_keys(payload, required, str(path)))

    if payload.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"{path}: schema_version must be '{SCHEMA_VERSION}'")

    client_id = payload.get("client_id")
    if not isinstance(client_id, str) or not client_id:
        errors.append(f"{path}: client_id must be a non-empty string")

    base_ids = payload.get("base_scenario_ids")
    if isinstance(base_ids, list):
        if not base_ids:
            errors.append(f"{path}: base_scenario_ids must contain at least one entry")
        seen: set[str] = set()
        for item in base_ids:
            if not isinstance(item, str) or not item:
                errors.append(f"{path}: base_scenario_ids must be non-empty strings")
                continue
            if item in seen:
                errors.append(f"{path}: base_scenario_ids must be unique")
            seen.add(item)
            if not _matches_gdpr_id(item):
                errors.append(f"{path}: base_scenario_ids entry '{item}' must match GDPR-###")
    else:
        errors.append(f"{path}: base_scenario_ids must be an array")

    policy_profile = payload.get("policy_profile")
    if not isinstance(policy_profile, dict):
        errors.append(f"{path}: policy_profile must be an object")
        return errors

    policy_required = {"supported_dsar_channels", "right_to_erasure_handling", "known_client_constraints"}
    errors.extend(_require_keys(policy_profile, policy_required, f"{path}: policy_profile"))

    supported = policy_profile.get("supported_dsar_channels")
    supported_channels: list[str] = []
    if isinstance(supported, list):
        if not supported:
            errors.append(f"{path}: supported_dsar_channels must contain at least one entry")
        for channel in supported:
            if not isinstance(channel, str) or not channel:
                errors.append(f"{path}: supported_dsar_channels must be non-empty strings")
            else:
                supported_channels.append(channel)
    else:
        errors.append(f"{path}: supported_dsar_channels must be an array")

    constraints = policy_profile.get("known_client_constraints")
    if not isinstance(constraints, list):
        errors.append(f"{path}: known_client_constraints must be an array")
    elif any(not isinstance(item, str) or not item for item in constraints):
        errors.append(f"{path}: known_client_constraints must be non-empty strings")

    r2e = policy_profile.get("right_to_erasure_handling")
    if not isinstance(r2e, dict):
        errors.append(f"{path}: right_to_erasure_handling must be an object")
        return errors

    r2e_required = {"primary_channel", "fallback_channels"}
    errors.extend(_require_keys(r2e, r2e_required, f"{path}: right_to_erasure_handling"))

    primary = r2e.get("primary_channel")
    fallback = r2e.get("fallback_channels")
    if not isinstance(primary, str) or not primary:
        errors.append(f"{path}: primary_channel must be a non-empty string")
    if not isinstance(fallback, list):
        errors.append(f"{path}: fallback_channels must be an array")
        fallback = []
    for channel in fallback:
        if not isinstance(channel, str) or not channel:
            errors.append(f"{path}: fallback_channels must be non-empty strings")

    if supported_channels:
        if isinstance(primary, str) and primary and primary not in supported_channels:
            errors.append(f"{path}: primary_channel '{primary}' not in supported_dsar_channels")
        for channel in fallback:
            if isinstance(channel, str) and channel and channel not in supported_channels:
                errors.append(f"{path}: fallback_channel '{channel}' not in supported_dsar_channels")

    return errors


def _matches_gdpr_id(value: str) -> bool:
    if len(value) != 8:
        return False
    if not value.startswith("GDPR-"):
        return False
    suffix = value.split("-", 1)[1]
    return suffix.isdigit() and len(suffix) == 3


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate client intake v0.2 fixtures.")
    parser.add_argument("--fixture", required=True, help="Path to intake fixture JSON")
    args = parser.parse_args()

    fixture_path = Path(args.fixture)
    if not fixture_path.exists():
        print(f"ERROR: fixture not found: {fixture_path}")
        return 1
    if not SCHEMA_PATH.exists():
        print(f"ERROR: intake schema not found: {SCHEMA_PATH}")
        return 1

    try:
        payload = _ensure_dict(_load_json(fixture_path), str(fixture_path))
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {fixture_path}: invalid JSON ({exc})")
        return 1

    errors = validate_client_intake(payload, fixture_path)
    if errors:
        print("ERROR: client intake validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: client intake fixture validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
