"""Runtime intake validation (contract-grounded)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


_CONTRACT_PATH = (
    Path(__file__).resolve().parents[3]
    / "specs"
    / "docs"
    / "contracts"
    / "intake"
    / "client_intake_output_contract_v0_1.md"
)


def _extract_json_block(markdown: str) -> dict[str, Any]:
    match = re.search(r"```json\s*(\{.*?\})\s*```", markdown, re.DOTALL)
    if not match:
        raise ValueError("No JSON block found in intake contract.")
    data = json.loads(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("Contract JSON block must be an object.")
    return data


def _load_contract_spec() -> dict[str, Any]:
    if not _CONTRACT_PATH.exists():
        raise ValueError(f"Missing intake contract: {_CONTRACT_PATH}")
    content = _CONTRACT_PATH.read_text(encoding="utf-8")
    return _extract_json_block(content)


def _require_keys(payload: dict[str, Any], keys: list[str], label: str) -> list[str]:
    missing = [key for key in keys if key not in payload]
    if missing:
        return [f"Missing required keys in {label}: {sorted(missing)}"]
    return []


def validate_intake_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    spec = _load_contract_spec()

    required_keys = spec.get("required_keys") or []
    allowed_target_types = set(spec.get("allowed_target_types") or [])
    allowed_auth_context = set(spec.get("allowed_auth_context") or [])
    allowed_dsar_channels = set(spec.get("allowed_dsar_channels") or [])
    target_profile_required_fields = spec.get("target_profile_required_fields") or []
    mock_target_profile_required_fields = spec.get("mock_target_profile_required_fields") or []

    if not isinstance(required_keys, list):
        errors.append("Contract required_keys must be a list.")
    if not isinstance(target_profile_required_fields, list):
        errors.append("Contract target_profile_required_fields must be a list.")
    if not isinstance(mock_target_profile_required_fields, list):
        errors.append("Contract mock_target_profile_required_fields must be a list.")
    if errors:
        return errors

    errors.extend(_require_keys(payload, required_keys, "intake"))

    policy_profile = payload.get("policy_profile")
    if not isinstance(policy_profile, dict):
        errors.append("Missing or invalid policy_profile (object required).")
    else:
        errors.extend(
            _require_keys(
                policy_profile,
                ["supported_dsar_channels", "right_to_erasure_handling", "known_client_constraints"],
                "policy_profile",
            )
        )
        channels = policy_profile.get("supported_dsar_channels")
        if not isinstance(channels, list):
            errors.append("policy_profile.supported_dsar_channels must be a list.")
        else:
            invalid = sorted({channel for channel in channels if channel not in allowed_dsar_channels})
            if invalid:
                errors.append(
                    "policy_profile.supported_dsar_channels contains invalid entries: "
                    f"{invalid}"
                )
        known_constraints = policy_profile.get("known_client_constraints")
        if not isinstance(known_constraints, list):
            errors.append("policy_profile.known_client_constraints must be a list.")
        erasure = policy_profile.get("right_to_erasure_handling")
        if not isinstance(erasure, dict):
            errors.append("policy_profile.right_to_erasure_handling must be an object.")
        else:
            errors.extend(
                _require_keys(
                    erasure,
                    ["primary_channel", "fallback_channels", "constraints"],
                    "policy_profile.right_to_erasure_handling",
                )
            )
            primary_channel = erasure.get("primary_channel")
            if primary_channel not in allowed_dsar_channels:
                errors.append(
                    "policy_profile.right_to_erasure_handling.primary_channel must be one of "
                    f"{sorted(allowed_dsar_channels)}"
                )
            fallback_channels = erasure.get("fallback_channels")
            if not isinstance(fallback_channels, list):
                errors.append(
                    "policy_profile.right_to_erasure_handling.fallback_channels must be a list."
                )
            else:
                invalid_fallback = sorted(
                    {
                        channel
                        for channel in fallback_channels
                        if channel not in allowed_dsar_channels
                    }
                )
                if invalid_fallback:
                    errors.append(
                        "policy_profile.right_to_erasure_handling.fallback_channels contains invalid entries: "
                        f"{invalid_fallback}"
                    )
            if "constraints" not in erasure:
                errors.append(
                    "Missing required keys in policy_profile.right_to_erasure_handling: ['constraints']"
                )

    target_profile = payload.get("target_profile")
    if not isinstance(target_profile, dict):
        errors.append("Missing or invalid target_profile (object required).")
    else:
        errors.extend(_require_keys(target_profile, target_profile_required_fields, "target_profile"))
        target_type = target_profile.get("target_type")
        if target_type not in allowed_target_types:
            errors.append(
                "target_profile.target_type must be one of "
                f"{sorted(allowed_target_types)}"
            )
        auth_context = target_profile.get("auth_context")
        if auth_context not in allowed_auth_context:
            errors.append(
                "target_profile.auth_context must be one of "
                f"{sorted(allowed_auth_context)}"
            )

    mock_target_profile = payload.get("mock_target_profile")
    if not isinstance(mock_target_profile, dict):
        errors.append("Missing or invalid mock_target_profile (object required).")
    else:
        errors.extend(
            _require_keys(
                mock_target_profile,
                mock_target_profile_required_fields,
                "mock_target_profile",
            )
        )
        mock_target_type = mock_target_profile.get("target_type")
        if mock_target_type not in allowed_target_types:
            errors.append(
                "mock_target_profile.target_type must be one of "
                f"{sorted(allowed_target_types)}"
            )
        mock_auth_context = mock_target_profile.get("auth_context")
        if mock_auth_context not in allowed_auth_context:
            errors.append(
                "mock_target_profile.auth_context must be one of "
                f"{sorted(allowed_auth_context)}"
            )

    return errors


def validate_intake() -> None:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: invalid JSON input ({exc.msg})")
    if not isinstance(payload, dict):
        raise SystemExit("ERROR: intake payload must be a JSON object.")

    errors = validate_intake_payload(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(2)
    print("PASS: intake payload validated.")
