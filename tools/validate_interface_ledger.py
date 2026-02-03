#!/usr/bin/env python3
"""Validate Interface Ledger v0 (GDPR-only) content and required rows."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "packages" / "specs" / "docs" / "contracts" / "interfaces" / "I_Ledger.md"
REQUIRED_HEADER = "| Module | Inputs | Outputs | Guarantees | Unknowns | Tests |"
REQUIRED_MODULES = [
    "AIGov bundle",
    "Exporter",
    "Inspect",
    "Petri",
    "Scout",
]


def _extract_table_rows(lines: list[str]) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in lines:
        if "|" not in line:
            continue
        if line.strip() == REQUIRED_HEADER:
            continue
        if line.strip().startswith("| ---"):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) >= 6:
            rows.append(parts)
    return rows


def validate_interface_ledger() -> list[str]:
    if not LEDGER_PATH.exists():
        return [f"interface ledger missing: {LEDGER_PATH}"]

    lines = LEDGER_PATH.read_text(encoding="utf-8").splitlines()
    if REQUIRED_HEADER not in lines:
        return ["interface ledger table header missing or misspelled"]

    rows = _extract_table_rows(lines)
    present = {row[0] for row in rows if row and row[0]}
    missing = [name for name in REQUIRED_MODULES if name not in present]
    if missing:
        return [f"interface ledger missing module row: {name}" for name in missing]
    return []


def main() -> int:
    errors = validate_interface_ledger()
    if errors:
        print("ERROR: interface ledger validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS: interface ledger validated: {LEDGER_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
