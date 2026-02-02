#!/usr/bin/env python3
"""Validate module dashboard snapshot is deterministic and up-to-date."""
from __future__ import annotations

import argparse
from pathlib import Path

from export_module_cards_dashboard import (
    CARDS_DIR,
    DEFAULT_OUTPUT_PATH,
    REGISTRY_PATH,
    _load_cards,
    _load_registry,
    render_dashboard,
)


def validate_module_dashboard_snapshot(output_path: Path) -> list[str]:
    errors: list[str] = []
    if not output_path.exists():
        return [f"snapshot missing: {output_path}"]

    try:
        module_ids = _load_registry(REGISTRY_PATH)
        cards = _load_cards(CARDS_DIR)
        expected = render_dashboard(module_ids, cards)
    except ValueError as exc:
        return [str(exc)]

    actual = output_path.read_text(encoding="utf-8")
    if actual != expected:
        errors.append(f"snapshot mismatch: {output_path}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate module dashboard snapshot.")
    parser.add_argument(
        "--snapshot",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Path to the committed dashboard markdown",
    )
    args = parser.parse_args()

    errors = validate_module_dashboard_snapshot(Path(args.snapshot))
    if errors:
        print("ERROR: module dashboard snapshot validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: module dashboard snapshot validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
