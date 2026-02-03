#!/usr/bin/env python3
"""Export Petri seed_instructions from a compiled GDPR bundle (alpha, stdlib-only)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EP_ROOT = ROOT / "packages" / "ep"
sys.path.insert(0, str(EP_ROOT))

from aigov_ep.scenario.bundle_manifest_v0_1_0 import load_and_validate_manifest


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _write_json_list(path: Path, payload: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, sort_keys=True, separators=(",", ":"))


def export_seed_instructions(bundle_dir: Path) -> list[str]:
    scenario_paths = load_and_validate_manifest(bundle_dir)

    instructions: list[dict[str, str]] = []
    seen_instance_ids: set[str] = set()

    for scenario_path in scenario_paths:
        scenario = _ensure_dict(_load_json(scenario_path), str(scenario_path))

        scenario_id = scenario.get("scenario_id")
        scenario_instance_id = scenario.get("scenario_instance_id")
        auditor_seed = scenario.get("auditor_seed")
        framework = scenario.get("framework")

        if not isinstance(scenario_id, str) or not scenario_id:
            raise ValueError(f"{scenario_path}: scenario_id is required")
        if not isinstance(scenario_instance_id, str) or not scenario_instance_id:
            raise ValueError(f"{scenario_path}: scenario_instance_id is required")
        if not isinstance(auditor_seed, str) or not auditor_seed:
            raise ValueError(f"{scenario_path}: auditor_seed is required")
        if framework != "GDPR":
            raise ValueError(f"{scenario_path}: framework must be GDPR")
        if scenario_instance_id in seen_instance_ids:
            raise ValueError(f"duplicate scenario_instance_id: {scenario_instance_id}")
        seen_instance_ids.add(scenario_instance_id)

        instructions.append(
            {
                "scenario_instance_id": scenario_instance_id,
                "scenario_id": scenario_id,
                "instruction": f"{scenario_instance_id}: {auditor_seed}",
            }
        )

    instructions = sorted(
        instructions, key=lambda item: (item["scenario_instance_id"], item["scenario_id"])
    )
    return [item["instruction"] for item in instructions]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export Petri seed_instructions from a compiled GDPR bundle (alpha)."
    )
    parser.add_argument("--bundle-dir", required=True, help="Path to compiled bundle directory")
    parser.add_argument("--out", required=True, help="Output JSON file path")
    args = parser.parse_args()

    bundle_dir = Path(args.bundle_dir)
    out_path = Path(args.out)

    try:
        instructions = export_seed_instructions(bundle_dir)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    _write_json_list(out_path, instructions)
    print(f"PASS: wrote seed_instructions to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
