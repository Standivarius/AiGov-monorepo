#!/usr/bin/env python3
"""Validate client intake v0.2 JSON against schema."""

import json
import re
import sys
from pathlib import Path


def load_schema():
    """Load client_intake_v0_2 schema."""
    schema_path = Path(__file__).parent.parent / "packages" / "specs" / "schemas" / "client_intake_v0_2.schema.json"
    with open(schema_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_intake(intake_path: Path, schema: dict) -> tuple[bool, list[str]]:
    """Validate intake JSON against schema. Returns (is_valid, errors)."""
    errors = []

    # Load intake
    try:
        with open(intake_path, "r", encoding="utf-8") as handle:
            intake = json.load(handle)
    except json.JSONDecodeError as exc:
        return False, [f"Invalid JSON: {exc}"]
    except FileNotFoundError:
        return False, [f"File not found: {intake_path}"]

    if not isinstance(intake, dict):
        return False, ["Intake root must be an object"]

    # Validate required fields
    required = schema.get("required", [])
    for field in required:
        if field not in intake:
            errors.append(f"Missing required field: {field}")

    # Validate schema_version
    schema_version = intake.get("schema_version")
    if schema_version != "0.2.0":
        errors.append(f"schema_version must be '0.2.0', got: {schema_version}")

    # Validate string fields are non-empty
    for field in ["client_id", "target_id", "intake_run_id", "policy_profile_ref", "target_profile_ref"]:
        value = intake.get(field)
        if not isinstance(value, str) or not value:
            errors.append(f"{field} must be a non-empty string")

    # Validate provenance
    provenance = intake.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("provenance must be an object")
    else:
        if "source_refs" not in provenance:
            errors.append("provenance missing required field: source_refs")
        if "capture_timestamp" not in provenance:
            errors.append("provenance missing required field: capture_timestamp")

        source_refs = provenance.get("source_refs")
        if not isinstance(source_refs, list) or len(source_refs) == 0:
            errors.append("provenance.source_refs must be a non-empty array")

    # Validate base_scenario_ids (CRITICAL)
    base_scenario_ids = intake.get("base_scenario_ids")
    if not isinstance(base_scenario_ids, list):
        errors.append("base_scenario_ids must be an array")
    elif len(base_scenario_ids) == 0:
        errors.append("base_scenario_ids must be a non-empty array")
    else:
        # Check uniqueness
        if len(base_scenario_ids) != len(set(base_scenario_ids)):
            errors.append("base_scenario_ids must contain unique entries (duplicates found)")

        # Check pattern: FRAMEWORK-NNN
        pattern = re.compile(r"^[A-Z_]+-[0-9]{3}$")
        for scenario_id in base_scenario_ids:
            if not isinstance(scenario_id, str):
                errors.append(f"base_scenario_ids entry must be string, got: {type(scenario_id).__name__}")
            elif not pattern.match(scenario_id):
                errors.append(f"base_scenario_ids entry '{scenario_id}' must match pattern FRAMEWORK-NNN (e.g., GDPR-001)")

    # Validate policy_profile
    policy_profile = intake.get("policy_profile")
    if policy_profile is not None:
        if not isinstance(policy_profile, dict):
            errors.append("policy_profile must be an object")
        else:
            required_pp = ["supported_dsar_channels", "right_to_erasure_handling", "known_client_constraints"]
            for field in required_pp:
                if field not in policy_profile:
                    errors.append(f"policy_profile missing required field: {field}")

            # Validate supported_dsar_channels
            channels = policy_profile.get("supported_dsar_channels")
            if isinstance(channels, list):
                allowed = {"email", "in_chat", "portal"}
                for ch in channels:
                    if ch not in allowed:
                        errors.append(f"policy_profile.supported_dsar_channels contains invalid channel: {ch}")

    # Validate target_profile
    target_profile = intake.get("target_profile")
    if target_profile is not None:
        if not isinstance(target_profile, dict):
            errors.append("target_profile must be an object")
        else:
            required_tp = ["target_type", "auth_context", "data_sources_touched", "integration_surfaces", "locale_context"]
            for field in required_tp:
                if field not in target_profile:
                    errors.append(f"target_profile missing required field: {field}")

            # Validate enums
            target_type = target_profile.get("target_type")
            if target_type not in {"chatbot", "chatbot_with_actions", "agent"}:
                errors.append(f"target_profile.target_type must be one of: chatbot, chatbot_with_actions, agent")

            auth_context = target_profile.get("auth_context")
            if auth_context not in {"logged_in", "public", "mixed"}:
                errors.append(f"target_profile.auth_context must be one of: logged_in, public, mixed")

            # Validate locale_context is 2-char country code
            locale = target_profile.get("locale_context")
            if isinstance(locale, str):
                if len(locale) != 2 or not locale.isupper():
                    errors.append(f"target_profile.locale_context must be 2-letter uppercase country code (e.g., RO, US)")

    # Check for additional properties (fail-closed)
    allowed_top_level = {
        "schema_version", "client_id", "target_id", "intake_run_id",
        "policy_profile_ref", "target_profile_ref", "provenance",
        "base_scenario_ids", "policy_profile", "target_profile"
    }
    for key in intake.keys():
        if key not in allowed_top_level:
            errors.append(f"Unexpected top-level field (additionalProperties:false): {key}")

    return (len(errors) == 0, errors)


def validate_client_intake_v0_2_fixture(intake_path: Path) -> list[str]:
    """Validate client intake v0.2 fixture. Returns list of errors (empty if valid)."""
    schema = load_schema()
    is_valid, errors = validate_intake(intake_path, schema)
    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_client_intake_v0_2.py <intake.json>", file=sys.stderr)
        sys.exit(1)

    intake_path = Path(sys.argv[1])
    errors = validate_client_intake_v0_2_fixture(intake_path)

    if not errors:
        print(f"PASS: client intake v0.2 validated: {intake_path}")
        sys.exit(0)
    else:
        print(f"FAIL: client intake v0.2 validation failed: {intake_path}", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
