#!/usr/bin/env python3
"""Fail-closed validator for canonical evidence IDs in judgments/citations fixtures."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANNING_DIR = ROOT / "packages" / "specs" / "docs" / "planning" / "2026-01-22-run"
EVAL_REGISTRY_PATH = PLANNING_DIR / "eval_registry.yaml"

EVID_RE = re.compile(r"EVID-\d{3}")


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _parse_allowed_evidence_ids(lines: list[str]) -> set[str]:
    allowed: set[str] = set()
    for line in lines:
        for match in EVID_RE.findall(line):
            allowed.add(match)
    return allowed


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _ensure_canonical_list(
    values: list[str],
    *,
    label: str,
    allowed: set[str],
    failures: list[str],
) -> None:
    if any(not isinstance(item, str) for item in values):
        failures.append(f"{label}: evidence IDs must be strings")
        return
    for item in values:
        if not EVID_RE.fullmatch(item):
            failures.append(f"{label}: invalid evidence ID format: {item}")
        elif item not in allowed:
            failures.append(f"{label}: unknown evidence ID: {item}")
    if values != sorted(values):
        failures.append(f"{label}: evidence IDs not sorted")
    if len(values) != len(set(values)):
        failures.append(f"{label}: evidence IDs contain duplicates")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate canonical evidence IDs in judgments/citations fixtures."
    )
    parser.add_argument("--judgments", action="append", default=[], help="Path to judgments JSON fixture.")
    parser.add_argument("--citations", action="append", default=[], help="Path to retrieval citations JSON fixture.")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    if not EVAL_REGISTRY_PATH.exists():
        print(f"ERROR: missing eval registry: {EVAL_REGISTRY_PATH}")
        return 1

    allowed_ids = _parse_allowed_evidence_ids(_read_lines(EVAL_REGISTRY_PATH))
    if not allowed_ids:
        print("ERROR: no evidence IDs detected in eval_registry.yaml")
        return 1

    failures: list[str] = []

    for judgment_path in args.judgments:
        path = Path(judgment_path)
        if not path.exists():
            failures.append(f"judgments: missing file {path}")
            continue
        payload = _load_json(path)
        judgments = payload.get("judgments", [])
        if not isinstance(judgments, list):
            failures.append(f"judgments: invalid list in {path}")
            continue
        for index, item in enumerate(judgments):
            evidence_ids = item.get("evidence_ids")
            label = f"{path}:judgments[{index}].evidence_ids"
            if not isinstance(evidence_ids, list) or not evidence_ids:
                failures.append(f"{label}: missing or not a list")
                continue
            _ensure_canonical_list(evidence_ids, label=label, allowed=allowed_ids, failures=failures)

    for citations_path in args.citations:
        path = Path(citations_path)
        if not path.exists():
            failures.append(f"citations: missing file {path}")
            continue
        payload = _load_json(path)
        citations = payload.get("citations", [])
        if not isinstance(citations, list):
            failures.append(f"citations: invalid list in {path}")
            continue
        for index, item in enumerate(citations):
            evidence_id = item.get("evidence_artifact_id")
            label = f"{path}:citations[{index}].evidence_artifact_id"
            if not isinstance(evidence_id, str):
                failures.append(f"{label}: missing or not a string")
                continue
            _ensure_canonical_list([evidence_id], label=label, allowed=allowed_ids, failures=failures)

    if failures:
        print("ERROR: evidence ID determinism violations detected:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("PASS: evidence IDs are canonical and registry-backed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
