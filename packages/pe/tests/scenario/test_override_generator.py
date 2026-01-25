from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EP_ROOT = ROOT.parent / "ep"
sys.path.insert(0, str(EP_ROOT))

from aigov_ep.scenario import generate_override


def test_generate_override_deterministic() -> None:
    intake = {
        "client_id": "client-001",
        "policy_profile": {
            "supported_dsar_channels": ["email", "portal"],
            "right_to_erasure_handling": {
                "primary_channel": "email",
                "fallback_channels": ["portal"],
                "constraints": ["manual_verification_required"],
            },
            "known_client_constraints": ["no_canary_delete"],
        },
    }
    base_meta = {"scenario_id": "GDPR-001"}

    override = generate_override(intake, base_meta)

    assert override["schema_version"] == "0.1.0"
    assert override["client_id"] == "client-001"
    assert override["base_scenario_id"] == "GDPR-001"
    assert override["override_type"] == "partial_patch"
    assert override["policy_profile"]["supported_dsar_channels"] == ["email", "portal"]
    assert override["policy_profile"]["right_to_erasure_handling"]["primary_channel"] == "email"
