#!/usr/bin/env python3
"""Validate deterministic export of Petri special_instructions (alpha, stdlib-only)."""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from export_bundle_to_petri_special_instructions_alpha import export_special_instructions


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return value


def _write_json_list(path: Path, payload: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, sort_keys=True, separators=(",", ":"))


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_export_bundle_to_petri_special_instructions_alpha(
    bundle_dir: Path, fixture_path: Path
) -> list[str]:
    errors: list[str] = []
    try:
        golden = _ensure_list(_load_json(fixture_path), str(fixture_path))
    except (json.JSONDecodeError, ValueError) as exc:
        return [f"{fixture_path}: invalid JSON ({exc})"]

    hashes: list[str] = []
    output_payload: list[str] | None = None

    for _ in range(3):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "special_instructions.json"
            try:
                payload = export_special_instructions(bundle_dir)
            except ValueError as exc:
                return [str(exc)]
            _write_json_list(output_path, payload)
            hashes.append(_sha256_file(output_path))
            output_payload = payload

    if len(set(hashes)) != 1:
        errors.append(f"special_instructions export hash mismatch across runs: {hashes}")

    if output_payload is None:
        errors.append("special_instructions export produced no output")
    elif output_payload != golden:
        errors.append("special_instructions export does not match golden fixture")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Petri special_instructions export.")
    parser.add_argument("--bundle-dir", required=True, help="Path to compiled bundle directory")
    parser.add_argument("--fixture", required=True, help="Path to golden fixture JSON list")
    args = parser.parse_args()

    errors = validate_export_bundle_to_petri_special_instructions_alpha(
        Path(args.bundle_dir), Path(args.fixture)
    )
    if errors:
        print("ERROR: special_instructions export validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: special_instructions export validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
