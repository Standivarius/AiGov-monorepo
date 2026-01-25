"""Evidence pack builder."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, List

from .taxonomy import normalize_verdict


LIMITATIONS = [
    "Heuristic detection only; results may include false positives or miss context.",
    "Transcript-only evaluation; no backend controls or logs are assessed.",
]

_TELEMETRY_KEYS = {"telemetry"}
_TRANSCRIPT_METADATA_TELEMETRY_KEYS = {"mock_audit", "http_audit", "http_raw_response"}


def build_evidence_pack(
    scenario: Dict[str, Any],
    transcript: List[Dict[str, Any]],
    scores: List[Dict[str, Any]],
    runner_config: Dict[str, Any],
    mock_audit: Any = None,
    http_audit: Any = None,
    http_raw_response: Any = None,
) -> Dict[str, Any]:
    evidence_pack = {
        "generated_at": _utc_now(),
        "scenario": {
            "scenario_id": scenario.get("scenario_id"),
            "title": scenario.get("title"),
            "category": scenario.get("category"),
            "framework": scenario.get("framework"),
            "role": scenario.get("role"),
            "failure_criteria": scenario.get("failure_criteria"),
            "source_path": scenario.get("source_path"),
        },
        "transcript": transcript,
        "scores": scores,
        "limitations": LIMITATIONS,
    }
    evidence_pack["telemetry"] = {
        "runner_config": runner_config,
        "mock_audit": mock_audit,
        "http_audit": http_audit,
        "http_raw_response": http_raw_response,
    }
    return evidence_pack


def build_evidence_pack_v0(
    *,
    scenario: Dict[str, Any],
    scores: List[Dict[str, Any]],
    run_dir: str,
    run_meta: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Build a contract-shaped evidence pack without telemetry."""
    scenario_id = scenario.get("scenario_id") or "unknown"
    target = None
    if isinstance(run_meta, dict):
        target = run_meta.get("target")
        if not target:
            runner_config = run_meta.get("runner_config") or {}
            if isinstance(runner_config, dict):
                target = runner_config.get("target")
    if not isinstance(target, str) or not target:
        target = "unknown"

    return {
        "schema_version": "0.1.0",
        "run_dir": str(run_dir),
        "scenario_id": str(scenario_id),
        "target": target,
        "signals": _signals_from_scores(scores),
        "items": [],
    }


def admissible_evidence_pack(evidence_pack: Dict[str, Any]) -> Dict[str, Any]:
    """Return an admissible evidence pack with debug/telemetry fields removed."""
    cleaned = dict(evidence_pack)
    for key in _TELEMETRY_KEYS:
        cleaned.pop(key, None)
    transcript = cleaned.get("transcript")
    if isinstance(transcript, list):
        scrubbed: list[Dict[str, Any]] = []
        for entry in transcript:
            if not isinstance(entry, dict):
                scrubbed.append(entry)
                continue
            entry_copy = dict(entry)
            metadata = entry_copy.get("metadata")
            if isinstance(metadata, dict):
                metadata_copy = {
                    key: value
                    for key, value in metadata.items()
                    if key not in _TRANSCRIPT_METADATA_TELEMETRY_KEYS
                }
                if metadata_copy:
                    entry_copy["metadata"] = metadata_copy
                else:
                    entry_copy.pop("metadata", None)
            scrubbed.append(entry_copy)
        cleaned["transcript"] = scrubbed
    return cleaned


def _signals_from_scores(scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    seen: set[str] = set()
    for score in scores:
        if not isinstance(score, dict):
            continue
        raw_signals = score.get("signals")
        if not isinstance(raw_signals, list):
            continue
        verdict = score.get("verdict")
        verdict_value = normalize_verdict(verdict) if isinstance(verdict, str) else "UNDECIDED"
        for signal_id in raw_signals:
            if not isinstance(signal_id, str) or not signal_id:
                continue
            if signal_id in seen:
                continue
            entries.append({"signal_id": signal_id, "verdict": verdict_value})
            seen.add(signal_id)
    return entries


def write_evidence_pack(path: str, evidence_pack: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(evidence_pack, handle, indent=2, sort_keys=True)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
