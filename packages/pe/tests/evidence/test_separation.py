from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EP_ROOT = ROOT.parent / "ep"
sys.path.insert(0, str(EP_ROOT))

from aigov_ep.evidence import admissible_evidence_pack, build_evidence_pack


def test_admissible_pack_excludes_telemetry() -> None:
    scenario = {
        "scenario_id": "scn-001",
        "title": "Test scenario",
        "category": "PII_DISCLOSURE",
        "framework": "GDPR",
        "role": "assistant",
        "failure_criteria": [],
        "source_path": "scenarios/test.json",
    }
    transcript = [
        {
            "role": "user",
            "content": "Hello",
            "metadata": {"mock_audit": {"leaked_fields": ["email"]}},
        }
    ]
    scores = [{"verdict": "COMPLIANT"}]
    runner_config = {"target": "mock"}

    pack = build_evidence_pack(
        scenario=scenario,
        transcript=transcript,
        scores=scores,
        runner_config=runner_config,
        mock_audit={"leaked_fields": []},
        http_audit=[],
        http_raw_response=[],
    )
    assert "telemetry" in pack

    admissible = admissible_evidence_pack(pack)
    assert "telemetry" not in admissible
    assert admissible["transcript"][0].get("metadata") is None
