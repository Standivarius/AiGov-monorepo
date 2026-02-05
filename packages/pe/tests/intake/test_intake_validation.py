from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EP_ROOT = ROOT.parent / "ep"
sys.path.insert(0, str(EP_ROOT))

from aigov_ep.intake.validate import validate_intake_payload


def test_validate_intake_payload_valid() -> None:
    payload = {
        "client_id": "client-001",
        "target_id": "target-001",
        "intake_run_id": "run-001",
        "policy_profile_ref": "policy-ref-001",
        "target_profile_ref": "target-ref-001",
        "provenance": {"source": "test"},
        "policy_profile": {
            "supported_dsar_channels": ["email", "in_chat"],
            "right_to_erasure_handling": {
                "primary_channel": "email",
                "fallback_channels": ["portal"],
                "constraints": [],
            },
            "known_client_constraints": [],
        },
        "target_profile": {
            "target_type": "chatbot",
            "auth_context": "logged_in",
            "data_sources_touched": ["kb"],
            "integration_surfaces": ["email"],
            "locale_context": "EU",
            "action_capabilities": ["send_email"],
            "logging_requirements": ["audit_log"],
        },
        "mock_target_profile": {
            "target_type": "chatbot",
            "auth_context": "logged_in",
            "action_capabilities": ["send_email"],
            "logging_requirements": ["audit_log"],
        },
    }

    errors = validate_intake_payload(payload)
    assert errors == []


def test_validate_intake_payload_valid_legacy_locale_nl() -> None:
    payload = {
        "client_id": "client-001",
        "target_id": "target-001",
        "intake_run_id": "run-001",
        "policy_profile_ref": "policy-ref-001",
        "target_profile_ref": "target-ref-001",
        "provenance": {"source": "test"},
        "policy_profile": {
            "supported_dsar_channels": ["email", "in_chat"],
            "right_to_erasure_handling": {
                "primary_channel": "email",
                "fallback_channels": ["portal"],
                "constraints": [],
            },
            "known_client_constraints": [],
        },
        "target_profile": {
            "target_type": "chatbot",
            "auth_context": "logged_in",
            "data_sources_touched": ["kb"],
            "integration_surfaces": ["email"],
            "locale_context": "NL",
            "action_capabilities": ["send_email"],
            "logging_requirements": ["audit_log"],
        },
        "mock_target_profile": {
            "target_type": "chatbot",
            "auth_context": "logged_in",
            "action_capabilities": ["send_email"],
            "logging_requirements": ["audit_log"],
        },
    }

    errors = validate_intake_payload(payload)
    assert errors == []


def test_validate_intake_payload_valid_context_profile_nl_public() -> None:
    payload = {
        "client_id": "client-001",
        "target_id": "target-001",
        "intake_run_id": "run-001",
        "policy_profile_ref": "policy-ref-001",
        "target_profile_ref": "target-ref-001",
        "provenance": {"source": "test"},
        "policy_profile": {
            "supported_dsar_channels": ["email", "in_chat"],
            "right_to_erasure_handling": {
                "primary_channel": "email",
                "fallback_channels": ["portal"],
                "constraints": [],
            },
            "known_client_constraints": [],
        },
        "target_profile": {
            "target_type": "chatbot",
            "auth_context": "logged_in",
            "data_sources_touched": ["kb"],
            "integration_surfaces": ["email"],
            "locale_context": "NL",
            "action_capabilities": ["send_email"],
            "logging_requirements": ["audit_log"],
        },
        "mock_target_profile": {
            "target_type": "chatbot",
            "auth_context": "logged_in",
            "action_capabilities": ["send_email"],
            "logging_requirements": ["audit_log"],
        },
        "context_profile": {
            "jurisdiction": "NL",
            "sector": "public",
            "policy_pack_stack": ["GDPR_EU", "NL", "public", "client"],
        },
    }

    errors = validate_intake_payload(payload)
    assert errors == []


def test_validate_intake_payload_invalid_context_profile_mismatch_fails() -> None:
    payload = {
        "client_id": "client-001",
        "target_id": "target-001",
        "intake_run_id": "run-001",
        "policy_profile_ref": "policy-ref-001",
        "target_profile_ref": "target-ref-001",
        "provenance": {"source": "test"},
        "policy_profile": {
            "supported_dsar_channels": ["email", "in_chat"],
            "right_to_erasure_handling": {
                "primary_channel": "email",
                "fallback_channels": ["portal"],
                "constraints": [],
            },
            "known_client_constraints": [],
        },
        "target_profile": {
            "target_type": "chatbot",
            "auth_context": "logged_in",
            "data_sources_touched": ["kb"],
            "integration_surfaces": ["email"],
            "locale_context": "NL",
            "action_capabilities": ["send_email"],
            "logging_requirements": ["audit_log"],
        },
        "mock_target_profile": {
            "target_type": "chatbot",
            "auth_context": "logged_in",
            "action_capabilities": ["send_email"],
            "logging_requirements": ["audit_log"],
        },
        "context_profile": {
            "jurisdiction": "EU",
            "sector": "public",
            "policy_pack_stack": ["GDPR_EU", "EU", "public", "client"],
        },
    }

    errors = validate_intake_payload(payload)
    assert errors
    assert any("locale_context" in error and "jurisdiction" in error for error in errors)


def test_validate_intake_payload_invalid_pack_order_fails() -> None:
    payload = {
        "client_id": "client-001",
        "target_id": "target-001",
        "intake_run_id": "run-001",
        "policy_profile_ref": "policy-ref-001",
        "target_profile_ref": "target-ref-001",
        "provenance": {"source": "test"},
        "policy_profile": {
            "supported_dsar_channels": ["email", "in_chat"],
            "right_to_erasure_handling": {
                "primary_channel": "email",
                "fallback_channels": ["portal"],
                "constraints": [],
            },
            "known_client_constraints": [],
        },
        "target_profile": {
            "target_type": "chatbot",
            "auth_context": "logged_in",
            "data_sources_touched": ["kb"],
            "integration_surfaces": ["email"],
            "locale_context": "NL",
            "action_capabilities": ["send_email"],
            "logging_requirements": ["audit_log"],
        },
        "mock_target_profile": {
            "target_type": "chatbot",
            "auth_context": "logged_in",
            "action_capabilities": ["send_email"],
            "logging_requirements": ["audit_log"],
        },
        "context_profile": {
            "jurisdiction": "NL",
            "sector": "public",
            "policy_pack_stack": ["NL", "GDPR_EU", "public", "client"],
        },
    }

    errors = validate_intake_payload(payload)
    assert errors
    assert any("policy_pack_stack" in error for error in errors)


def test_validate_intake_payload_invalid() -> None:
    payload = {
        "client_id": "client-001",
        "target_id": "target-001",
        "intake_run_id": "run-001",
        "policy_profile_ref": "policy-ref-001",
        "target_profile_ref": "target-ref-001",
        "provenance": {"source": "test"},
        "policy_profile": {"supported_dsar_channels": ["sms"]},
        "target_profile": {
            "target_type": "widget",
            "auth_context": "logged_in",
            "data_sources_touched": [],
            "integration_surfaces": [],
            "locale_context": "EU",
            "action_capabilities": [],
            "logging_requirements": [],
        },
        "mock_target_profile": {
            "target_type": "widget",
            "auth_context": "logged_in",
            "action_capabilities": [],
            "logging_requirements": [],
        },
    }

    errors = validate_intake_payload(payload)
    assert errors
    assert any("policy_profile.supported_dsar_channels" in error for error in errors)
    assert any("policy_profile.right_to_erasure_handling" in error for error in errors)
    assert any("policy_profile.known_client_constraints" in error for error in errors)
    assert any("target_profile.target_type" in error for error in errors)
