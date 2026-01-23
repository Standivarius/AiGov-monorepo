#!/usr/bin/env python3
"""Fail-closed check for golden-set contamination in retrieval citations (fixture-based)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANNING_DIR = ROOT / "packages" / "specs" / "docs" / "planning" / "2026-01-22-run"
EVAL_REGISTRY_PATH = PLANNING_DIR / "eval_registry.yaml"

GOLDEN_HINT_RE = re.compile(r"golden", re.IGNORECASE)
GOLDEN_ID_RE = re.compile(r"EVID-012")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _parse_golden_artifacts(lines: list[str]) -> set[str]:
    golden_ids: set[str] = set()
    in_evidence = False

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- eval_id:"):
            in_evidence = False
            continue

        if stripped.startswith("evidence_artifacts:"):
            in_evidence = True
            continue

        if in_evidence and stripped.startswith("-"):
            artifact = stripped.lstrip("-").strip()
            if GOLDEN_ID_RE.search(artifact) or GOLDEN_HINT_RE.search(artifact):
                match = GOLDEN_ID_RE.search(artifact)
                if match:
                    golden_ids.add(match.group(0))
                else:
                    golden_ids.add(artifact)
            continue

        if stripped.startswith("-") and not stripped.startswith("- eval_id:"):
            in_evidence = False
            continue

    return golden_ids


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate golden-set contamination in citations fixtures.")
    parser.add_argument("--citations", required=True, help="Path to retrieval_citations fixture JSON file.")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    citations_path = Path(args.citations)
    if not citations_path.exists():
        print(f"ERROR: missing citations fixture: {citations_path}")
        return 1
    if not EVAL_REGISTRY_PATH.exists():
        print(f"ERROR: missing eval registry: {EVAL_REGISTRY_PATH}")
        return 1

    golden_ids = _parse_golden_artifacts(_read_lines(EVAL_REGISTRY_PATH))
    if not golden_ids:
        print("ERROR: no golden artifacts detected in eval_registry.yaml")
        return 1

    payload = _load_json(citations_path)
    failures: list[str] = []

    for index, item in enumerate(payload.get("citations", [])):
        evidence_id = item.get("evidence_artifact_id")
        if evidence_id in golden_ids:
            failures.append(f"citations[{index}].evidence_artifact_id={evidence_id}")

    if failures:
        print("ERROR: golden-set contamination detected:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("PASS: no golden-set contamination in citations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
