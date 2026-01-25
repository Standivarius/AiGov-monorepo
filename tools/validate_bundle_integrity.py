#!/usr/bin/env python3
"""Validate bundle manifest integrity against on-disk fixtures."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _compute_bundle_hash(entries: list[dict[str, Any]]) -> str:
    lines = []
    for entry in entries:
        path = entry.get("path")
        sha256 = entry.get("sha256")
        if isinstance(path, str) and isinstance(sha256, str):
            lines.append(f"{path}:{sha256}")
    return _sha256_bytes(("\n".join(sorted(lines)) + "\n").encode("utf-8"))


def validate_bundle(bundle_dir: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = bundle_dir / "manifest.json"
    if not manifest_path.exists():
        return [f"manifest not found: {manifest_path}"]
    try:
        manifest = _load_json(manifest_path)
    except (json.JSONDecodeError, OSError) as exc:
        return [f"invalid manifest JSON: {exc}"]
    if not isinstance(manifest, dict):
        return ["manifest must be an object"]

    scenarios = manifest.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        return ["manifest.scenarios must be a non-empty array"]

    for entry in scenarios:
        if not isinstance(entry, dict):
            errors.append("manifest.scenarios entries must be objects")
            continue
        rel_path = entry.get("path")
        sha256 = entry.get("sha256")
        if not isinstance(rel_path, str) or not rel_path:
            errors.append("manifest.scenarios entry missing path")
            continue
        if not isinstance(sha256, str) or not sha256:
            errors.append(f"{rel_path}: missing sha256")
            continue
        file_path = bundle_dir / rel_path
        if not file_path.exists():
            errors.append(f"{rel_path}: file missing")
            continue
        actual = _sha256_bytes(file_path.read_bytes())
        if actual != sha256:
            errors.append(f"{rel_path}: sha256 mismatch")

    bundle_hash = manifest.get("bundle_hash")
    if not isinstance(bundle_hash, str) or not bundle_hash:
        errors.append("manifest.bundle_hash missing or invalid")
    else:
        expected_hash = _compute_bundle_hash(scenarios)
        if expected_hash != bundle_hash:
            errors.append("manifest.bundle_hash mismatch")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate bundle integrity fixtures.")
    parser.add_argument("--bundle-dir", required=True, help="Path to bundle directory")
    args = parser.parse_args()

    errors = validate_bundle(Path(args.bundle_dir))
    if errors:
        print("ERROR: bundle integrity validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: bundle integrity validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
