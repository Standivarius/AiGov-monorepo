#!/usr/bin/env python3
"""Validate Pre2.3 contract scaffolding for report fields and signals."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


REPORT_FIELDS_PATH = Path(
    "packages/specs/docs/contracts/reporting/report_fields_v0_1.md"
)
CROSSWALK_PATH = Path(
    "packages/specs/docs/contracts/reporting/report_fields_crosswalk_v0_1.md"
)
SIGNALS_PATH = Path("packages/specs/docs/contracts/taxonomy/signals.json")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> Any:
    return json.loads(_read_text(path))


def _extract_field_ids(markdown: str) -> list[str]:
    field_ids: list[str] = []
    in_field_section = False
    for line in markdown.splitlines():
        if line.strip().startswith("## Field IDs"):
            in_field_section = True
            continue
        if in_field_section and line.startswith("## "):
            break
        if in_field_section and line.strip().startswith("- `"):
            match = re.search(r"`([a-z0-9_]+)`", line)
            if match:
                field_ids.append(match.group(1))
    return field_ids


def _extract_crosswalk_json(markdown: str) -> list[dict[str, Any]]:
    match = re.search(r"```json\s*(\[.*?\])\s*```", markdown, re.DOTALL)
    if not match:
        raise ValueError("No JSON block found in crosswalk document.")
    return json.loads(match.group(1))


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    report_fields_path = repo_root / REPORT_FIELDS_PATH
    crosswalk_path = repo_root / CROSSWALK_PATH
    signals_path = repo_root / SIGNALS_PATH

    for path in (report_fields_path, crosswalk_path, signals_path):
        if not path.exists():
            print(f"ERROR: missing required file: {path}")
            return 1

    report_fields_md = _read_text(report_fields_path)
    crosswalk_md = _read_text(crosswalk_path)
    signals_data = _load_json(signals_path)

    field_ids = _extract_field_ids(report_fields_md)
    if not field_ids:
        print("ERROR: no field IDs found in report_fields_v0_1.md")
        return 1

    try:
        crosswalk_entries = _extract_crosswalk_json(crosswalk_md)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    if not isinstance(crosswalk_entries, list) or not crosswalk_entries:
        print("ERROR: crosswalk JSON must be a non-empty array")
        return 1

    crosswalk_field_ids: list[str] = []
    for entry in crosswalk_entries:
        if not isinstance(entry, dict):
            print("ERROR: each crosswalk entry must be an object")
            return 1
        field_id = entry.get("field_id")
        if not isinstance(field_id, str) or not field_id:
            print("ERROR: crosswalk entry missing field_id")
            return 1
        crosswalk_field_ids.append(field_id)

    missing = sorted(set(field_ids) - set(crosswalk_field_ids))
    extra = sorted(set(crosswalk_field_ids) - set(field_ids))
    if missing:
        print(f"ERROR: missing field_ids in crosswalk: {missing}")
        return 1
    if extra:
        print(f"ERROR: extra field_ids in crosswalk: {extra}")
        return 1

    signal_ids = signals_data.get("signal_ids", [])
    if not isinstance(signal_ids, list) or not signal_ids:
        print("ERROR: signal_ids missing or invalid in signals.json")
        return 1
    signal_set = set(signal_ids)

    invalid_signals: list[str] = []
    for entry in crosswalk_entries:
        signal_refs = entry.get("signal_ids")
        if signal_refs is None:
            continue
        if not isinstance(signal_refs, list):
            print(
                f"ERROR: signal_ids must be an array in field {entry.get('field_id')}"
            )
            return 1
        for signal_id in signal_refs:
            if not isinstance(signal_id, str):
                print(
                    f"ERROR: signal_id must be string in field {entry.get('field_id')}"
                )
                return 1
            if signal_id not in signal_set:
                invalid_signals.append(signal_id)

    if invalid_signals:
        print(f"ERROR: unknown signal_ids referenced: {sorted(set(invalid_signals))}")
        return 1

    print("PASS: Pre2.3 contracts validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
