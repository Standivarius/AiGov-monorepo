#!/usr/bin/env python3
"""Validate evidence_id resolution against the evidence pack manifest (fixture-only)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dict(value: object, label: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _ensure_list(value: object, label: str) -> list:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate evidence_id resolution fixtures.")
    parser.add_argument("--fixture", required=True, help="Path to fixture JSON")
    args = parser.parse_args()

    fixture_path = Path(args.fixture)
    if not fixture_path.exists():
        print(f"ERROR: fixture not found: {fixture_path}")
        return 1

    try:
        fixture = _ensure_dict(_load_json(fixture_path), "fixture")
        manifest = _ensure_dict(fixture.get("manifest"), "manifest")
        judgments = _ensure_dict(fixture.get("judgments"), "judgments")
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: invalid fixture format: {exc}")
        return 1

    try:
        manifest_files = _ensure_list(manifest.get("files"), "manifest.files")
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    manifest_index: dict[str, dict] = {}
    for entry in manifest_files:
        if not isinstance(entry, dict):
            print("ERROR: manifest.files entries must be objects")
            return 1
        evidence_id = entry.get("evidence_id")
        relpath = entry.get("relpath")
        sha256 = entry.get("sha256")
        if not isinstance(evidence_id, str) or not evidence_id:
            print("ERROR: manifest.files entry missing evidence_id")
            return 1
        if not isinstance(relpath, str) or not relpath:
            print(f"ERROR: manifest.files entry {evidence_id} missing relpath")
            return 1
        if not isinstance(sha256, str):
            print(f"ERROR: manifest.files entry {evidence_id} missing sha256")
            return 1
        manifest_index[evidence_id] = entry

    try:
        judgment_items = _ensure_list(judgments.get("judgments"), "judgments.judgments")
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    missing_ids: list[str] = []
    missing_sha: list[str] = []

    for item in judgment_items:
        if not isinstance(item, dict):
            print("ERROR: judgments.judgments entries must be objects")
            return 1
        if "evidence_ids" not in item:
            print("ERROR: missing judgments.judgments[].evidence_ids (required by schema)")
            return 1
        evidence_ids = item.get("evidence_ids")
        if evidence_ids is None:
            print("ERROR: evidence_ids must not be null")
            return 1
        if not isinstance(evidence_ids, list):
            print("ERROR: judgments.judgments.evidence_ids must be an array")
            return 1
        for evidence_id in evidence_ids:
            if not isinstance(evidence_id, str) or not evidence_id:
                print("ERROR: evidence_ids must be non-empty strings")
                return 1
            entry = manifest_index.get(evidence_id)
            if entry is None:
                missing_ids.append(evidence_id)
                continue
            sha256 = entry.get("sha256")
            if not isinstance(sha256, str) or not sha256.strip():
                missing_sha.append(evidence_id)

    if missing_ids:
        print("ERROR: evidence_ids missing from manifest.files:")
        for evidence_id in sorted(set(missing_ids)):
            print(f"  - {evidence_id}")
        return 1

    if missing_sha:
        print("ERROR: manifest.files entries missing sha256 for referenced ids:")
        for evidence_id in sorted(set(missing_sha)):
            print(f"  - {evidence_id}")
        return 1

    print("PASS: evidence_id resolution validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
