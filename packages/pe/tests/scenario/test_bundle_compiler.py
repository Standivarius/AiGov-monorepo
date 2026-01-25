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
