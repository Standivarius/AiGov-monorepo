#!/usr/bin/env python3
"""Validate Pre2.4 scenario contract scaffolding."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


SPEC_PATH = Path("packages/specs/docs/contracts/scenarios/bespoke_scenario_spec_v0_1.md")
SIGNALS_PATH = Path("packages/specs/docs/contracts/taxonomy/signals.json")
INVARIANT = (
    "auditor and judge instructions MUST be generated from the same bespoke scenario spec"
)
REQUIRED_KEYS = {
    "bespoke_scenario_spec_id",
    "scenario_card_id",
    "scenario_instance_id",
    "canonical_signal_ids",
    "verification_mode",
    "required_evidence_artifacts",
    "instruction_generation",
}
REQUIRED_VERIFICATION_MODES = {"runtime", "doc", "timeline", "out-of-scope"}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> Any:
    return json.loads(_read_text(path))


def _extract_json_blocks(markdown: str) -> list[Any]:
    blocks = re.findall(r"```json\s*(.*?)\s*```", markdown, re.DOTALL)
    parsed: list[Any] = []
    for block in blocks:
        parsed.append(json.loads(block))
    return parsed


def _find_schema_block(blocks: list[Any]) -> dict[str, Any] | None:
    for block in blocks:
        if isinstance(block, dict) and "required_keys" in block:
            return block
    return None


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    spec_path = repo_root / SPEC_PATH
    signals_path = repo_root / SIGNALS_PATH

    for path in (spec_path, signals_path):
        if not path.exists():
            print(f"ERROR: missing required file: {path}")
            return 1

    spec_text = _read_text(spec_path)
    if INVARIANT not in spec_text:
        print("ERROR: invariant sentence missing from bespoke scenario spec")
        return 1

    blocks = _extract_json_blocks(spec_text)
    if not blocks:
        print("ERROR: no JSON blocks found in bespoke scenario spec")
        return 1

    schema = _find_schema_block(blocks)
    if schema is None:
        print("ERROR: authoritative validation block not found")
        return 1

    required_keys = schema.get("required_keys")
    if not isinstance(required_keys, list):
        print("ERROR: required_keys must be a list")
        return 1
    missing_required = REQUIRED_KEYS - set(required_keys)
    if missing_required:
        print(f"ERROR: required_keys missing entries: {sorted(missing_required)}")
        return 1

    allowed_modes = schema.get("allowed_verification_modes")
    if not isinstance(allowed_modes, list):
        print("ERROR: allowed_verification_modes must be a list")
        return 1
    missing_modes = REQUIRED_VERIFICATION_MODES - set(allowed_modes)
    if missing_modes:
        print(f"ERROR: allowed_verification_modes missing entries: {sorted(missing_modes)}")
        return 1

    signals_data = _load_json(signals_path)
    signal_ids = signals_data.get("signal_ids", [])
    if not isinstance(signal_ids, list) or not signal_ids:
        print("ERROR: signal_ids missing or invalid in signals.json")
        return 1
    signal_set = set(signal_ids)

    for block in blocks:
        if not isinstance(block, dict):
            continue
        if "canonical_signal_ids" in block:
            canonical_ids = block.get("canonical_signal_ids")
            if not isinstance(canonical_ids, list):
                print("ERROR: canonical_signal_ids must be a list")
                return 1
            invalid = [sid for sid in canonical_ids if sid not in signal_set]
            if invalid:
                print(f"ERROR: unknown canonical_signal_ids: {sorted(set(invalid))}")
                return 1
        if "verification_mode" in block:
            mode = block.get("verification_mode")
            if mode not in allowed_modes:
                print(f"ERROR: invalid verification_mode: {mode}")
                return 1

    print("PASS: Pre2.4 contracts validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
