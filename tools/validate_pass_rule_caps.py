#!/usr/bin/env python3
"""Fail-closed checks for pass-rule caps in the planning eval registry."""
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANNING_DIR = ROOT / "packages" / "specs" / "docs" / "planning" / "2026-01-22-run"
EVAL_REGISTRY_PATH = PLANNING_DIR / "eval_registry.yaml"
EVALSETS_REGISTRY_PATH = PLANNING_DIR / "evalsets_registry.yaml"

UNDECIDED_CAP_RE = re.compile(r"UNDECIDED\s*<=\s*\d+(?:\.\d+)?%", re.IGNORECASE)
OUT_OF_SCOPE_CAP_RE = re.compile(r"out-of-scope\s*(?:==|<=)\s*0", re.IGNORECASE)
LIMITATIONS_LOG_RE = re.compile(r"limitations[_ ]log", re.IGNORECASE)


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _parse_eval_registry(lines: list[str]) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    in_evidence = False

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- eval_id:"):
            current = {"eval_id": stripped.split(":", 1)[1].strip()}
            entries.append(current)
            in_evidence = False
            continue

        if current is None:
            continue

        if stripped.startswith("evidence_artifacts:"):
            current["evidence_artifacts"] = []
            in_evidence = True
            continue

        if in_evidence and stripped.startswith("-"):
            artifact = stripped.lstrip("-").strip()
            if artifact:
                current.setdefault("evidence_artifacts", []).append(artifact)
            continue

        if stripped.startswith("-") and not stripped.startswith("- eval_id:"):
            in_evidence = False
            continue

        if ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key in {"runtime_tier", "pass_rule"}:
                current[key] = value
            in_evidence = False

    return entries


def _parse_evalsets_registry(lines: list[str]) -> list[dict[str, object]]:
    evalsets: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    section: str | None = None

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- evalset_id:"):
            current = {
                "evalset_id": stripped.split(":", 1)[1].strip(),
                "eval_ids": [],
            }
            evalsets.append(current)
            section = None
            continue

        if current is None:
            continue

        if stripped.startswith("runtime_tier:"):
            current["runtime_tier"] = stripped.split(":", 1)[1].strip()
            section = None
            continue

        if stripped.startswith("eval_ids:"):
            section = "eval_ids"
            continue

        if stripped.startswith("-") and section == "eval_ids":
            item = stripped.lstrip("-").strip()
            if item:
                current["eval_ids"].append(item)
            continue

    return evalsets


def _requires_judgments(entry: dict[str, object]) -> bool:
    for artifact in entry.get("evidence_artifacts", []):
        text = str(artifact)
        if "EVID-006" in text or "Stage B judgments" in text:
            return True
    return False


def main() -> int:
    for path in (EVAL_REGISTRY_PATH, EVALSETS_REGISTRY_PATH):
        if not path.exists():
            print(f"ERROR: missing required file: {path}")
            return 1

    eval_entries = _parse_eval_registry(_read_lines(EVAL_REGISTRY_PATH))
    if not eval_entries:
        print("ERROR: eval_registry.yaml contains no eval entries")
        return 1

    evalsets = _parse_evalsets_registry(_read_lines(EVALSETS_REGISTRY_PATH))
    release_eval_ids = {
        eval_id
        for entry in evalsets
        if entry.get("runtime_tier") == "release"
        for eval_id in entry.get("eval_ids", [])
    }

    missing_undecided_caps: list[str] = []
    missing_out_of_scope_caps: list[str] = []
    missing_limitations_log: list[str] = []

    for entry in eval_entries:
        eval_id = entry.get("eval_id")
        pass_rule = str(entry.get("pass_rule") or "")
        requires_judgments = _requires_judgments(entry)

        if requires_judgments and not UNDECIDED_CAP_RE.search(pass_rule):
            missing_undecided_caps.append(str(eval_id))

        if requires_judgments and eval_id in release_eval_ids:
            if not OUT_OF_SCOPE_CAP_RE.search(pass_rule):
                missing_out_of_scope_caps.append(str(eval_id))
            if not LIMITATIONS_LOG_RE.search(pass_rule):
                missing_limitations_log.append(str(eval_id))

    if missing_undecided_caps:
        print("ERROR: missing UNDECIDED caps in pass_rule:")
        for eval_id in sorted(missing_undecided_caps):
            print(f"  - {eval_id}")
        return 1

    if missing_out_of_scope_caps:
        print("ERROR: missing out-of-scope caps in release pass_rule:")
        for eval_id in sorted(missing_out_of_scope_caps):
            print(f"  - {eval_id}")
        return 1

    if missing_limitations_log:
        print("ERROR: release pass_rule missing limitations_log waiver note:")
        for eval_id in sorted(missing_limitations_log):
            print(f"  - {eval_id}")
        return 1

    print("PASS: pass-rule caps present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
