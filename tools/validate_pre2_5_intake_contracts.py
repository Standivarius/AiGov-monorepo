#!/usr/bin/env python3
"""Validate Pre2.5 client intake contract scaffolding."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


CONTRACT_PATH = Path(
    "packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md"
)
REQUIRED_KEYS = {
    "client_id",
    "target_id",
    "intake_run_id",
    "policy_profile_ref",
    "target_profile_ref",
    "provenance",
}
REQUIRED_TARGET_TYPES = {"chatbot", "chatbot_with_actions", "agent"}
REQUIRED_AUTH_CONTEXT = {"logged_in", "public", "mixed"}
REQUIRED_DSAR_CHANNELS = {"email", "in_chat", "portal"}
REQUIRED_MOCK_FIELDS = {
    "target_type",
    "auth_context",
    "action_capabilities",
    "logging_requirements",
}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_json_block(markdown: str) -> dict[str, Any]:
    match = re.search(r"```json\s*(\{.*?\})\s*```", markdown, re.DOTALL)
    if not match:
        raise ValueError("No JSON block found in intake contract.")
    data = json.loads(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("JSON block must be an object.")
    return data


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    contract_path = repo_root / CONTRACT_PATH

    if not contract_path.exists():
        print(f"ERROR: missing intake contract: {contract_path}")
        return 1

    contract_text = _read_text(contract_path)
    try:
        block = _extract_json_block(contract_text)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    required_keys = block.get("required_keys")
    if not isinstance(required_keys, list):
        print("ERROR: required_keys must be a list")
        return 1
    missing_required = REQUIRED_KEYS - set(required_keys)
    if missing_required:
        print(f"ERROR: required_keys missing entries: {sorted(missing_required)}")
        return 1

    target_types = block.get("allowed_target_types")
    if not isinstance(target_types, list):
        print("ERROR: allowed_target_types must be a list")
        return 1
    missing_target_types = REQUIRED_TARGET_TYPES - set(target_types)
    if missing_target_types:
        print(
            "ERROR: allowed_target_types missing entries: "
            f"{sorted(missing_target_types)}"
        )
        return 1

    auth_context = block.get("allowed_auth_context")
    if not isinstance(auth_context, list):
        print("ERROR: allowed_auth_context must be a list")
        return 1
    missing_auth_context = REQUIRED_AUTH_CONTEXT - set(auth_context)
    if missing_auth_context:
        print(
            "ERROR: allowed_auth_context missing entries: "
            f"{sorted(missing_auth_context)}"
        )
        return 1

    dsar_channels = block.get("allowed_dsar_channels")
    if not isinstance(dsar_channels, list):
        print("ERROR: allowed_dsar_channels must be a list")
        return 1
    missing_channels = REQUIRED_DSAR_CHANNELS - set(dsar_channels)
    if missing_channels:
        print(
            "ERROR: allowed_dsar_channels missing entries: "
            f"{sorted(missing_channels)}"
        )
        return 1

    target_fields = block.get("target_profile_required_fields")
    if not isinstance(target_fields, list):
        print("ERROR: target_profile_required_fields must be a list")
        return 1
    mock_fields = block.get("mock_target_profile_required_fields")
    if not isinstance(mock_fields, list):
        print("ERROR: mock_target_profile_required_fields must be a list")
        return 1
    missing_mock = REQUIRED_MOCK_FIELDS - set(mock_fields)
    if missing_mock:
        print(
            "ERROR: mock_target_profile_required_fields missing entries: "
            f"{sorted(missing_mock)}"
        )
        return 1
    if not set(mock_fields).issubset(set(target_fields)):
        extra = sorted(set(mock_fields) - set(target_fields))
        print(
            "ERROR: mock_target_profile_required_fields must be subset of target_profile_required_fields: "
            f"{extra}"
        )
        return 1

    print("PASS: Pre2.5 intake contract validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
