#!/usr/bin/env python3
"""Validate deterministic export of Dataset JSONL v0.1 from a bundle."""
from __future__ import annotations

import argparse
import hashlib
import tempfile
from pathlib import Path
from typing import Any

from export_bundle_to_dataset_jsonl_v0_1 import export_dataset_jsonl
from validate_aigov_dataset_jsonl_v0_1 import validate_dataset_jsonl


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_export_bundle_to_dataset_jsonl_v0_1(bundle_dir: Path, fixture_path: Path) -> list[str]:
    errors: list[str] = []
    if not fixture_path.exists():
        return [f"fixture not found: {fixture_path}"]
    expected = fixture_path.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = Path(temp_dir) / "dataset.jsonl"
        try:
            records = export_dataset_jsonl(bundle_dir)
        except ValueError as exc:
            return [str(exc)]
        output_path.write_text("\n".join(records) + "\n", encoding="utf-8")
        actual = output_path.read_text(encoding="utf-8")
        if actual != expected:
            errors.append("dataset export does not match golden fixture")

        validation_errors = validate_dataset_jsonl(output_path)
        if validation_errors:
            errors.extend([f"line {line_no}: {msg}" for line_no, msg in validation_errors])

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Dataset JSONL export from bundle.")
    parser.add_argument("--bundle-dir", required=True, help="Path to bundle directory")
    parser.add_argument("--fixture", required=True, help="Path to golden JSONL fixture")
    args = parser.parse_args()

    errors = validate_export_bundle_to_dataset_jsonl_v0_1(Path(args.bundle_dir), Path(args.fixture))
    if errors:
        print("ERROR: dataset export validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: dataset export validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
