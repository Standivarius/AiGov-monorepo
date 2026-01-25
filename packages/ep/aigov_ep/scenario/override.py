"""Deterministic intake -> scenario override mapping."""

from __future__ import annotations

from typing import Any, Dict


def generate_override(intake_json: Dict[str, Any], base_scenario_meta: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a deterministic override from intake and base scenario metadata."""
    if not isinstance(intake_json, dict):
        raise ValueError("intake_json must be an object")
    if not isinstance(base_scenario_meta, dict):
        raise ValueError("base_scenario_meta must be an object")

    client_id = intake_json.get("client_id")
    if not isinstance(client_id, str) or not client_id:
        raise ValueError("intake_json.client_id is required")

    base_scenario_id = base_scenario_meta.get("scenario_id")
    if not isinstance(base_scenario_id, str) or not base_scenario_id:
        raise ValueError("base_scenario_meta.scenario_id is required")

    policy_profile = intake_json.get("policy_profile")
    if not isinstance(policy_profile, dict):
        raise ValueError("intake_json.policy_profile is required")

    supported_channels = policy_profile.get("supported_dsar_channels")
    right_to_erasure = policy_profile.get("right_to_erasure_handling")
    known_constraints = policy_profile.get("known_client_constraints")

    if not isinstance(supported_channels, list) or not supported_channels:
        raise ValueError("policy_profile.supported_dsar_channels is required")
    if not isinstance(right_to_erasure, dict):
        raise ValueError("policy_profile.right_to_erasure_handling is required")
    if not isinstance(known_constraints, list):
        raise ValueError("policy_profile.known_client_constraints is required")

    primary_channel = right_to_erasure.get("primary_channel")
    fallback_channels = right_to_erasure.get("fallback_channels")
    constraints = right_to_erasure.get("constraints")

    if not isinstance(primary_channel, str) or not primary_channel:
        raise ValueError("right_to_erasure_handling.primary_channel is required")
    if not isinstance(fallback_channels, list):
        raise ValueError("right_to_erasure_handling.fallback_channels must be a list")
    if not isinstance(constraints, list):
        raise ValueError("right_to_erasure_handling.constraints must be a list")
    if primary_channel not in supported_channels:
        raise ValueError("primary_channel must be in supported_dsar_channels")
    for channel in fallback_channels:
        if not isinstance(channel, str) or not channel:
            raise ValueError("fallback_channels must be non-empty strings")
        if channel not in supported_channels:
            raise ValueError("fallback_channels must be in supported_dsar_channels")

    return {
        "schema_version": "0.1.0",
        "client_id": client_id,
        "base_scenario_id": base_scenario_id,
        "override_type": "partial_patch",
        "policy_profile": {
            "supported_dsar_channels": list(supported_channels),
            "right_to_erasure_handling": {
                "primary_channel": primary_channel,
                "fallback_channels": list(fallback_channels),
                "constraints": list(constraints),
            },
            "known_client_constraints": list(known_constraints),
        },
    }
