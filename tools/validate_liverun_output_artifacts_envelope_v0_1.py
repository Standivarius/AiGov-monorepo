#!/usr/bin/env python3
"""Validate LiveRun output artifacts envelope v0.1 (stdlib-only)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_FILES = ["inspect_logs.json", "petri_transcripts.json"]


def _parse_json(path: Path) -> tuple[object | None, str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, f"missing required file: {path}"
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON in {path}: {exc.msg}"
    return data, None


def _validate_json_container(data: Any, path: Path) -> str | None:
    if not isinstance(data, (dict, list)):
        return f"{path} must be a JSON object or array"
    return None


def validate_liverun_output_artifacts_dir(dir_path: Path) -> list[str]:
    errors: list[str] = []
    if not dir_path.exists():
        return [f"output directory missing: {dir_path}"]
    if not dir_path.is_dir():
        return [f"output directory must be a directory: {dir_path}"]

    for filename in REQUIRED_FILES:
        path = dir_path / filename
        if not path.exists():
            errors.append(f"missing required file: {path}")
            continue
        if not path.is_file():
            errors.append(f"required path is not a file: {path}")
            continue
        data, error = _parse_json(path)
        if error:
            errors.append(error)
            continue
        container_error = _validate_json_container(data, path)
        if container_error:
            errors.append(container_error)

    return sorted(errors)
