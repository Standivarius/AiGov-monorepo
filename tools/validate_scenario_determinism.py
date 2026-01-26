#!/usr/bin/env python3
"""Validate scenario bundle determinism by compiling multiple times."""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP_ROOT = ROOT / "packages" / "ep"
sys.path.insert(0, str(EP_ROOT))

from aigov_ep.scenario.compiler import compile_bundle


def _bundle_hash_for(run_dir: Path) -> str:
    manifest = (run_dir / "manifest.json").read_text(encoding="utf-8")
    import json

    data = json.loads(manifest)
    if not isinstance(data, dict):
        raise ValueError("manifest.json must be an object")
    bundle_hash = data.get("bundle_hash")
    if not isinstance(bundle_hash, str) or not bundle_hash:
        raise ValueError("bundle_hash missing from manifest")
    return bundle_hash


def validate_determinism(base_dir: Path, overrides_dir: Path | None) -> list[str]:
    hashes: list[str] = []
    for _ in range(3):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            compile_bundle(base_dir=base_dir, overrides_dir=overrides_dir, output_dir=output_dir)
            hashes.append(_bundle_hash_for(output_dir))
    if len(set(hashes)) != 1:
        return [f"bundle_hash mismatch across runs: {hashes}"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate deterministic scenario bundle compilation.")
    parser.add_argument("--base-dir", required=True, help="Base scenario directory")
    parser.add_argument("--overrides-dir", required=False, help="Override directory")
    args = parser.parse_args()

    base_dir = Path(args.base_dir)
    overrides_dir = Path(args.overrides_dir) if args.overrides_dir else None
    errors = validate_determinism(base_dir, overrides_dir)
    if errors:
        print("ERROR: determinism validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: scenario determinism validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
