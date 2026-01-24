"""Minimal L1 report generator with fail-closed limitations log."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..utils.io import read_json, write_json


_CROSSWALK_PATH = Path(__file__).resolve().parents[3] / "specs" / "docs" / "contracts" / "reporting" / "report_fields_crosswalk_v0_1.md"


@dataclass
class ReportArtifacts:
    l1_report_path: Path
    limitations_log_path: Path


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_crosswalk() -> list[dict[str, Any]]:
    content = _CROSSWALK_PATH.read_text(encoding="utf-8")
    start = content.find("```json")
    if start == -1:
        raise ValueError("Crosswalk JSON block not found")
    start = content.find("\n", start) + 1
    end = content.find("```", start)
    if end == -1:
        raise ValueError("Crosswalk JSON block not terminated")
    block = content[start:end].strip()
    return json.loads(block)


def _load_manifest_evidence_ids(run_dir: Path) -> list[str]:
    manifest_path = run_dir / "run_manifest_v0.json"
    if not manifest_path.exists():
        return []
    manifest = read_json(manifest_path)
    artifacts = manifest.get("artifacts", [])
    evidence_ids: list[str] = []
    for item in artifacts:
        if isinstance(item, dict):
            artifact_id = item.get("artifact_id")
            if isinstance(artifact_id, str) and artifact_id:
                evidence_ids.append(artifact_id)
    return sorted(set(evidence_ids))


def _overall_status(verdicts: list[str]) -> str:
    if any(verdict == "INFRINGEMENT" for verdict in verdicts):
        return "INFRINGEMENT detected"
    if any(verdict == "UNDECIDED" for verdict in verdicts):
        return "UNDECIDED findings present"
    return "COMPLIANT"


def _risk_summary(verdicts: list[str]) -> str:
    counts = {
        "INFRINGEMENT": verdicts.count("INFRINGEMENT"),
        "UNDECIDED": verdicts.count("UNDECIDED"),
        "COMPLIANT": verdicts.count("COMPLIANT"),
    }
    return (
        "Verdict counts: "
        f"INFRINGEMENT={counts['INFRINGEMENT']}, "
        f"UNDECIDED={counts['UNDECIDED']}, "
        f"COMPLIANT={counts['COMPLIANT']}"
    )


def _key_findings(judgments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for judgment in judgments:
        entry = {
            "scenario_instance_id": judgment.get("scenario_instance_id"),
            "verdict": judgment.get("verdict"),
        }
        rationale = judgment.get("rationale")
        if isinstance(rationale, str) and rationale:
            entry["rationale"] = rationale
        findings.append(entry)
    return findings


def _generate_l1_report(run_dir: Path, out_dir: Path) -> ReportArtifacts:
    evidence_pack_path = run_dir / "evidence_pack.json"
    judgments_path = run_dir / "judgments.json"
    run_meta_path = run_dir / "run_meta.json"

    if not evidence_pack_path.exists():
        raise ValueError(f"Missing evidence pack: {evidence_pack_path}")
    if not judgments_path.exists():
        raise ValueError(f"Missing judgments: {judgments_path}")

    run_meta = read_json(run_meta_path) if run_meta_path.exists() else {}
    run_id = run_meta.get("run_id") or run_dir.name

    judgments_payload = read_json(judgments_path)
    judgments = judgments_payload.get("judgments", [])
    verdicts = [item.get("verdict", "UNDECIDED") for item in judgments]

    crosswalk = _load_crosswalk()
    l1_fields = [entry for entry in crosswalk if entry.get("layer") == "L1"]

    available_artifacts = {
        "evidence_pack_ref": str(evidence_pack_path),
        "judge_output_manifest": str(judgments_path),
    }

    fields: dict[str, Any] = {}
    limitations: list[str] = []

    for entry in l1_fields:
        field_id = entry.get("field_id")
        evidence_artifact = entry.get("evidence_artifact")
        verification_mode = entry.get("verification_mode")

        if evidence_artifact not in available_artifacts:
            limitations.append(
                f"Missing evidence for {field_id} (requires {evidence_artifact}; verification_mode={verification_mode})."
            )
            continue

        if field_id == "l1_overall_status":
            fields[field_id] = _overall_status(verdicts)
        elif field_id == "l1_risk_summary":
            fields[field_id] = _risk_summary(verdicts)
        elif field_id == "l1_key_findings":
            fields[field_id] = _key_findings(judgments)
        else:
            limitations.append(
                f"Unimplemented field {field_id} (verification_mode={verification_mode})."
            )

    report = {
        "layer": "L1",
        "run_id": run_id,
        "generated_at": _utc_now(),
        "fields": fields,
    }

    evidence_ids = _load_manifest_evidence_ids(run_dir)
    limitations_log = {
        "schema_version": "0.1.0",
        "run_id": run_id,
        "generated_at": _utc_now(),
        "timeline_refs": evidence_ids,
        "operational_evidence_refs": [],
        "limitations": limitations,
        "assumptions": [],
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    l1_report_path = out_dir / "l1_report.json"
    limitations_log_path = out_dir / "limitations_log.json"
    write_json(l1_report_path, report)
    write_json(limitations_log_path, limitations_log)

    return ReportArtifacts(l1_report_path=l1_report_path, limitations_log_path=limitations_log_path)


def _resolve_run_dir() -> Path:
    explicit = os.getenv("AIGOV_RUN_DIR")
    if explicit:
        return Path(explicit).resolve()
    runs_dir = Path("runs")
    if not runs_dir.exists():
        raise ValueError("AIGOV_RUN_DIR not set and no runs/ directory found")
    run_dirs = [path for path in runs_dir.iterdir() if path.is_dir()]
    if not run_dirs:
        raise ValueError("No run directories found under runs/")
    return max(run_dirs, key=lambda path: path.stat().st_mtime)


def generate_report() -> None:
    run_dir = _resolve_run_dir()
    out_dir = Path(os.getenv("AIGOV_REPORT_OUT") or run_dir)
    artifacts = _generate_l1_report(run_dir, out_dir)
    print(f"L1_REPORT={artifacts.l1_report_path}")
    print(f"LIMITATIONS_LOG={artifacts.limitations_log_path}")
