#!/usr/bin/env python3
"""Validate equivalence assertions include policy_ref and deputy labeling.

Expected fixture shape:
{
  "equivalence_assertions": [
    {
      "policy_ref": "policy-profile-hash",
      "verification_label": "VERIFIED_BY_DEPUTY"
    }
  ]
}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate equivalence labeling fixtures.")
    parser.add_argument("--fixture", required=True, help="Path to an equivalence fixture JSON file.")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    fixture_path = Path(args.fixture)
    if not fixture_path.exists():
        print(f"ERROR: missing fixture: {fixture_path}")
        return 1

    payload = _load_json(fixture_path)
    assertions = payload.get("equivalence_assertions", [])
    failures: list[str] = []

    for index, item in enumerate(assertions):
        policy_ref = item.get("policy_ref")
        label = item.get("verification_label")
        if not isinstance(policy_ref, str) or not policy_ref.strip():
            failures.append(f"equivalence_assertions[{index}].policy_ref missing")
        if label != "VERIFIED_BY_DEPUTY":
            failures.append(f"equivalence_assertions[{index}].verification_label={label}")

    if failures:
        print("ERROR: equivalence assertions invalid:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("PASS: equivalence labeling requirements satisfied.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
