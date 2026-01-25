from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EP_ROOT = ROOT.parent / "ep"
sys.path.insert(0, str(EP_ROOT))

from aigov_ep.evidence import build_evidence_pack_v0, write_evidence_pack


def test_evidence_pack_v0_minimal_shape(tmp_path: Path) -> None:
    scenario = {"scenario_id": "scn-001"}
    scores = [
        {
            "verdict": "VIOLATION",
            "signals": ["signal_a", "signal_b"],
            "judge_meta": {"base_url": "https://example.com"},
        }
    ]
    run_meta = {"target": "mock"}

    pack = build_evidence_pack_v0(
        scenario=scenario,
        scores=scores,
        run_dir="runs/RUN-001",
        run_meta=run_meta,
    )

    required_keys = {
        "schema_version",
        "run_dir",
        "scenario_id",
        "target",
        "signals",
        "items",
    }
    assert required_keys.issubset(pack.keys())
    assert pack["schema_version"] == "0.1.0"
    assert pack["target"] == "mock"
    assert "telemetry" not in pack
    assert pack["items"] == []
    assert pack["signals"] == [
        {"signal_id": "signal_a", "verdict": "INFRINGEMENT"},
        {"signal_id": "signal_b", "verdict": "INFRINGEMENT"},
    ]

    output_path = tmp_path / "evidence_pack_v0.json"
    write_evidence_pack(str(output_path), pack)
    loaded = json.loads(output_path.read_text(encoding="utf-8"))
    assert loaded == pack
