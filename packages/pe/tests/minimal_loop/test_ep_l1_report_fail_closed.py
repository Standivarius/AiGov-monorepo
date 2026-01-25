from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
EP_ROOT = ROOT.parent / "ep"
sys.path.insert(0, str(EP_ROOT))

from aigov_ep.reporting.generate import _generate_l1_report


FIXTURES = ROOT / "tests" / "fixtures"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_l1_report_missing_judgments_fail_closed(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    (run_dir / "evidence_pack.json").write_text(
        json.dumps(_load("l1_report_evidence_pack.json")),
        encoding="utf-8",
    )
    (run_dir / "run_meta.json").write_text(
        json.dumps(_load("l1_report_run_meta.json")),
        encoding="utf-8",
    )

    artifacts = _generate_l1_report(run_dir, run_dir)

    report = json.loads(artifacts.l1_report_path.read_text(encoding="utf-8"))
    assert "l1_overall_status" not in report.get("fields", {}), (
        "l1_overall_status must be omitted when judgments are missing"
    )

    limitations = json.loads(artifacts.limitations_log_path.read_text(encoding="utf-8"))
    required_keys = {
        "schema_version",
        "run_id",
        "generated_at",
        "timeline_refs",
        "operational_evidence_refs",
        "limitations",
        "assumptions",
    }
    assert required_keys.issubset(limitations.keys())
    assert any(
        "Missing judgments for l1_overall_status" in item
        for item in limitations.get("limitations", [])
    ), "limitations_log must mention missing judgments"
