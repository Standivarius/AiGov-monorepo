from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EP_ROOT = ROOT.parent / "ep"
sys.path.insert(0, str(EP_ROOT))

from aigov_ep.scenario import compile_bundle


def test_compile_bundle_manifest(tmp_path: Path) -> None:
    base_dir = ROOT.parent.parent / "tools" / "fixtures" / "scenario_compile" / "base"
    overrides_dir = ROOT.parent.parent / "tools" / "fixtures" / "scenario_compile" / "overrides"

    manifest = compile_bundle(base_dir=base_dir, overrides_dir=overrides_dir, output_dir=tmp_path)

    manifest_path = tmp_path / "manifest.json"
    assert manifest_path.exists()
    loaded = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["bundle_hash"] == loaded["bundle_hash"]
    assert loaded["schema_version"] == "0.1.0"
    assert len(loaded["scenarios"]) == 1
    scenario_entry = loaded["scenarios"][0]
    assert scenario_entry["scenario_id"] == "GDPR-001"
    scenario_path = tmp_path / scenario_entry["path"]
    assert scenario_path.exists()


def test_compile_bundle_missing_overrides_dir(tmp_path: Path) -> None:
    base_dir = ROOT.parent.parent / "tools" / "fixtures" / "scenario_compile" / "base"
    overrides_dir = tmp_path / "missing-overrides"

    try:
        compile_bundle(base_dir=base_dir, overrides_dir=overrides_dir, output_dir=tmp_path)
    except ValueError as exc:
        assert "Overrides directory does not exist" in str(exc)
    else:
        raise AssertionError("Expected ValueError for missing overrides_dir")


def test_compile_bundle_unknown_override_base_id(tmp_path: Path) -> None:
    base_dir = ROOT.parent.parent / "tools" / "fixtures" / "scenario_compile" / "base"
    overrides_dir = tmp_path / "overrides"
    overrides_dir.mkdir(parents=True, exist_ok=True)
    (overrides_dir / "unknown.json").write_text(
        json.dumps(
            {
                "schema_version": "0.1.0",
                "client_id": "client-unknown",
                "base_scenario_id": "GDPR-999",
                "override_type": "partial_patch",
                "policy_profile": {
                    "supported_dsar_channels": ["email"],
                    "right_to_erasure_handling": {
                        "primary_channel": "email",
                        "fallback_channels": ["portal"],
                        "constraints": ["identity_verification_required"],
                    },
                    "known_client_constraints": ["no_phone_support"],
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    try:
        compile_bundle(base_dir=base_dir, overrides_dir=overrides_dir, output_dir=tmp_path)
    except ValueError as exc:
        assert "unknown base_scenario_id" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unknown base_scenario_id")
