#!/usr/bin/env python3
"""Validate doc/timeline/out-of-scope judgments require operational evidence refs."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate doc-mode operational evidence requirements.")
    parser.add_argument("--judgments", required=True, help="Path to a judgments fixture JSON file.")
    parser.add_argument("--limitations", required=True, help="Path to a limitations_log fixture JSON file.")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    judgments_path = Path(args.judgments)
    limitations_path = Path(args.limitations)

    if not judgments_path.exists():
        print(f"ERROR: missing judgments fixture: {judgments_path}")
        return 1
    if not limitations_path.exists():
        print(f"ERROR: missing limitations fixture: {limitations_path}")
        return 1

    judgments = _load_json(judgments_path)
    limitations = _load_json(limitations_path)

    needs_operational = any(
        item.get("verification_mode") == "doc"
        for item in judgments.get("judgments", [])
    )

    operational_refs = limitations.get("operational_evidence_refs", [])
    if needs_operational and not operational_refs:
        print("ERROR: doc-mode judgments require operational_evidence_refs")
        return 1

    print("PASS: doc-mode operational evidence requirements satisfied.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
