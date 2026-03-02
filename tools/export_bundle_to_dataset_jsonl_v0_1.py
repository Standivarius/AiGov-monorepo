#!/usr/bin/env python3
"""Export Dataset JSONL v0.1 from a deterministic GDPR bundle (stdlib-only)."""
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
from export_bundle_to_petri_seed_instructions_alpha import export_seed_instructions

LAWFUL_BASIS = {
    "contract",
    "legal_obligation",
    "legitimate_interests",
    "consent",
    "vital_interests",
    "public_task",
}
DSAR_TYPES = {"access", "erasure"}
VERDICTS = {"INFRINGEMENT", "COMPLIANT", "UNDECIDED"}


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _ensure_str(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty string")
    return value


def _is_lower_hex_64(value: str) -> bool:
    return len(value) == 64 and all(ch in "0123456789abcdef" for ch in value)


def _load_manifest(bundle_dir: Path) -> dict[str, Any]:
    manifest_path = bundle_dir / "manifest.json"
    if not manifest_path.exists():
        raise ValueError(f"manifest.json not found in {bundle_dir}")
    manifest = _ensure_dict(_load_json(manifest_path), str(manifest_path))
    if manifest.get("schema_version") != "0.1.0":
        raise ValueError("manifest.json schema_version must be '0.1.0'")
    return manifest


def _build_instruction_map(instructions: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for instruction in instructions:
        if not isinstance(instruction, str) or not instruction:
            raise ValueError("seed instructions must be non-empty strings")
        prefix = ": "
        if prefix not in instruction:
            raise ValueError("seed instruction missing scenario_instance_id prefix")
        instance_id, _ = instruction.split(prefix, 1)
        if not instance_id:
            raise ValueError("seed instruction missing scenario_instance_id prefix")
        if instance_id in mapping:
            raise ValueError(f"duplicate seed instruction for {instance_id}")
        mapping[instance_id] = instruction
    return mapping


def export_dataset_jsonl(bundle_dir: Path) -> list[str]:
    manifest = _load_manifest(bundle_dir)
    scenarios = manifest.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("manifest.json scenarios must be a non-empty list")
    bundle_hash = _ensure_str(manifest.get("bundle_hash"), "manifest.json bundle_hash")
    if not _is_lower_hex_64(bundle_hash):
        raise ValueError("manifest.json bundle_hash must be 64-char lowercase hex")

    scenario_paths = load_and_validate_manifest(bundle_dir)
    instructions = export_seed_instructions(bundle_dir)
    instruction_map = _build_instruction_map(instructions)

    records: list[str] = []
    if len(scenarios) != len(scenario_paths):
        raise ValueError("manifest.json scenarios length mismatch")

    for entry, scenario_path in zip(scenarios, scenario_paths):
        entry_obj = _ensure_dict(entry, "manifest.json scenarios entry")
        rel_path = _ensure_str(entry_obj.get("path"), "manifest.json scenarios entry path")
        expected_path = (bundle_dir / rel_path).resolve()
        if expected_path != scenario_path:
            raise ValueError("manifest.json scenario path mismatch")
        scenario_id = _ensure_str(entry_obj.get("scenario_id"), "manifest.json scenario_id")
        scenario_instance_id = _ensure_str(
            entry_obj.get("scenario_instance_id"), "manifest.json scenario_instance_id"
        )
        scenario_sha256 = _ensure_str(
            entry_obj.get("sha256"), "manifest.json scenario sha256"
        )
        if not _is_lower_hex_64(scenario_sha256):
            raise ValueError("manifest.json scenario sha256 must be 64-char lowercase hex")

        scenario = _ensure_dict(_load_json(scenario_path), str(scenario_path))
        if scenario.get("scenario_id") != scenario_id:
            raise ValueError(f"scenario_id mismatch for {scenario_path}")
        if scenario.get("scenario_instance_id") != scenario_instance_id:
            raise ValueError(f"scenario_instance_id mismatch for {scenario_path}")

        gdpr = _ensure_dict(scenario.get("gdpr"), f"{scenario_path}: gdpr")
        lawful_basis = _ensure_str(gdpr.get("lawful_basis"), f"{scenario_path}: gdpr.lawful_basis")
        dsar_type = _ensure_str(gdpr.get("dsar_type"), f"{scenario_path}: gdpr.dsar_type")
        if lawful_basis not in LAWFUL_BASIS:
            raise ValueError(f"{scenario_path}: gdpr.lawful_basis '{lawful_basis}' not allowed")
        if dsar_type not in DSAR_TYPES:
            raise ValueError(f"{scenario_path}: gdpr.dsar_type '{dsar_type}' not allowed")

        expected = _ensure_dict(scenario.get("expected"), f"{scenario_path}: expected")
        verdict = _ensure_str(expected.get("verdict"), f"{scenario_path}: expected.verdict")
        if verdict not in VERDICTS:
            raise ValueError(f"{scenario_path}: expected.verdict '{verdict}' not allowed")

        instruction = instruction_map.get(scenario_instance_id)
        if instruction is None:
            raise ValueError(f"missing seed instruction for {scenario_instance_id}")

        record = {
            "schema_version": "aigov_dataset_jsonl_v0_1",
            "dataset_id": f"bundle_{bundle_hash}",
            "item_id": f"item_{scenario_instance_id}_{scenario_id}",
            "source": {
                "bundle_hash": bundle_hash,
                "scenario_id": scenario_id,
                "scenario_instance_id": scenario_instance_id,
                "scenario_sha256": scenario_sha256,
            },
            "gdpr": {
                "lawful_basis": lawful_basis,
                "dsar_type": dsar_type,
            },
            "prompt": {
                "seed_instructions": [instruction],
            },
            "expected": {
                "verdict": verdict,
            },
        }
        records.append(json.dumps(record, sort_keys=True, separators=(",", ":")))

    return records


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export Dataset JSONL v0.1 from a deterministic GDPR bundle."
    )
    parser.add_argument("--bundle-dir", required=True, help="Path to bundle directory")
    parser.add_argument("--out", required=True, help="Output JSONL file path")
    args = parser.parse_args()

    bundle_dir = Path(args.bundle_dir)
    out_path = Path(args.out)

    try:
        records = export_dataset_jsonl(bundle_dir)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(records) + "\n", encoding="utf-8")
    print(f"PASS: wrote dataset JSONL to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
