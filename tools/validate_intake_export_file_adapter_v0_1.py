#!/usr/bin/env python3
"""Validate deterministic intake export adapter v0.1 outputs."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from run_intake_export_file_adapter_v0_1 import emit_source_snapshot
from validate_intake_source_snapshot_v0_1 import validate_intake_source_snapshot_fixture

ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def validate_export_adapter_snapshot_pass(
    export_dir: Path,
    expected_snapshot_fixture: Path,
) -> list[str]:
    errors: list[str] = []

    if not expected_snapshot_fixture.exists():
        return [f"expected snapshot fixture not found: {expected_snapshot_fixture}"]

    try:
        expected_snapshot = _ensure_dict(
            _load_json(expected_snapshot_fixture), str(expected_snapshot_fixture)
        )
    except (json.JSONDecodeError, ValueError) as exc:
        return [f"{expected_snapshot_fixture}: invalid JSON ({exc})"]

    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        run1_path = temp_dir / "snapshot_run1.json"
        run2_path = temp_dir / "snapshot_run2.json"

        try:
            emit_source_snapshot(export_dir, run1_path)
            emit_source_snapshot(export_dir, run2_path)
        except ValueError as exc:
            return [str(exc)]

        run1_bytes = run1_path.read_bytes()
        run2_bytes = run2_path.read_bytes()
        if run1_bytes != run2_bytes:
            errors.append("snapshot bytes mismatch across repeated runs")

        try:
            run1_payload = _ensure_dict(_load_json(run1_path), str(run1_path))
        except (json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{run1_path}: invalid JSON ({exc})")
            run1_payload = None

        if run1_payload is not None and run1_payload != expected_snapshot:
            errors.append("snapshot output does not match expected fixture")

        stage_errors = validate_intake_source_snapshot_fixture(run1_path)
        if stage_errors:
            errors.append("snapshot output failed intake_source_snapshot_v0_1 validator")
            errors.extend(stage_errors)

    return sorted(errors)


def validate_export_adapter_snapshot_fail_symlink(fail_fixture: Path) -> list[str]:
    if not fail_fixture.exists():
        return [f"snapshot symlink fail fixture not found: {fail_fixture}"]

    try:
        fixture = _ensure_dict(_load_json(fail_fixture), str(fail_fixture))
    except (json.JSONDecodeError, ValueError) as exc:
        return [f"{fail_fixture}: invalid JSON ({exc})"]

    fixture_dir_raw = fixture.get("fixture_dir")
    symlink_name = fixture.get("symlink_name")
    symlink_target = fixture.get("symlink_target")
    expected_substring = fixture.get("expected_error_substring")

    if not isinstance(fixture_dir_raw, str) or not fixture_dir_raw:
        return [f"{fail_fixture}: fixture_dir must be a non-empty string"]
    if not isinstance(symlink_name, str) or not symlink_name:
        return [f"{fail_fixture}: symlink_name must be a non-empty string"]
    if not isinstance(symlink_target, str) or not symlink_target:
        return [f"{fail_fixture}: symlink_target must be a non-empty string"]
    if not isinstance(expected_substring, str) or not expected_substring:
        return [f"{fail_fixture}: expected_error_substring must be a non-empty string"]

    source_dir = ROOT / fixture_dir_raw
    if not source_dir.exists() or not source_dir.is_dir():
        return [f"{fail_fixture}: fixture_dir not found: {source_dir}"]

    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        copied_dir = temp_dir / "export_input"
        shutil.copytree(source_dir, copied_dir)

        symlink_path = copied_dir / symlink_name
        symlink_path.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(symlink_target, symlink_path)

        try:
            emit_source_snapshot(copied_dir, temp_dir / "snapshot.json")
        except ValueError as exc:
            message = str(exc)
            if expected_substring not in message:
                return [
                    "snapshot symlink fail fixture missing expected failure mode "
                    f"'{expected_substring}': {message}"
                ]
            return []

    return [
        "snapshot symlink fail fixture unexpectedly passed adapter execution: "
        f"{fail_fixture}"
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate intake export adapter snapshot behavior")
    parser.add_argument("--export-dir", required=True, help="Path to pass export directory")
    parser.add_argument(
        "--snapshot-fixture",
        required=True,
        help="Path to expected pass snapshot fixture",
    )
    parser.add_argument(
        "--fail-symlink-fixture",
        required=True,
        help="Path to symlink fail fixture metadata",
    )
    args = parser.parse_args()

    pass_errors = validate_export_adapter_snapshot_pass(
        Path(args.export_dir), Path(args.snapshot_fixture)
    )
    fail_errors = validate_export_adapter_snapshot_fail_symlink(Path(args.fail_symlink_fixture))

    all_errors = sorted(pass_errors + fail_errors)
    if all_errors:
        print("ERROR: intake export adapter snapshot validation failed:")
        for error in all_errors:
            print(f"  - {error}")
        return 1

    print(
        "PASS: intake export adapter snapshot validation succeeded "
        f"(export_dir={args.export_dir})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
