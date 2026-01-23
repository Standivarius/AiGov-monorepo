#!/usr/bin/env python3
"""Validate that verdicts are canonical (no legacy aliases)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERDICTS_PATH = ROOT / "packages" / "specs" / "docs" / "contracts" / "taxonomy" / "verdicts.json"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate canonical verdicts in judgments fixtures.")
    parser.add_argument(
        "--fixture",
        action="append",
        default=[],
        help="Path to a judgments fixture JSON file (repeatable).",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    fixture_paths = [Path(path) for path in args.fixture]
    if not fixture_paths:
        print("ERROR: provide at least one --fixture path")
        return 1

    if not VERDICTS_PATH.exists():
        print(f"ERROR: missing verdicts taxonomy: {VERDICTS_PATH}")
        return 1

    verdicts = _load_json(VERDICTS_PATH)
    canonical = set(verdicts.get("canonical", []))
    if not canonical:
        print("ERROR: verdicts.json missing canonical verdict list")
        return 1

    failures: list[str] = []
    for path in fixture_paths:
        if not path.exists():
            failures.append(f"{path}: missing fixture")
            continue
        payload = _load_json(path)
        for index, item in enumerate(payload.get("judgments", [])):
            verdict = item.get("verdict")
            if verdict not in canonical:
                failures.append(f"{path}:judgments[{index}].verdict={verdict}")

    if failures:
        print("ERROR: non-canonical verdicts found:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("PASS: canonical verdicts only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
