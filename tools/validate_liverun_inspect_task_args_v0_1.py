#!/usr/bin/env python3
"""Validate LiveRun inspect_task_args v0.1 (stdlib-only)."""
from __future__ import annotations

from typing import Any


REQUIRED_KEYS = {
    "auditor_model",
    "target_model",
    "judge_model",
    "limit",
    "max_turns",
    "log_dir",
    "transcript_dir",
}


def _ensure_dict(value: Any, label: str, errors: list[str]) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return None
    return value


def validate_inspect_task_args(payload: object, label: str) -> list[str]:
    errors: list[str] = []
    data = _ensure_dict(payload, label, errors)
    if data is None:
        return sorted(errors)

    keys = set(data.keys())
    missing = sorted(REQUIRED_KEYS - keys)
    extra = sorted(keys - REQUIRED_KEYS)
    if missing:
        errors.append(f"{label} missing required keys: {missing}")
    if extra:
        errors.append(f"{label} contains unknown keys: {extra}")

    def _require_nonempty_str(field: str) -> None:
        value = data.get(field)
        if not isinstance(value, str) or not value:
            errors.append(f"{label}.{field} must be a non-empty string")

    def _require_positive_int(field: str) -> None:
        value = data.get(field)
        if not isinstance(value, int) or value < 1:
            errors.append(f"{label}.{field} must be an integer >= 1")

    _require_nonempty_str("auditor_model")
    _require_nonempty_str("target_model")
    _require_nonempty_str("judge_model")
    _require_positive_int("limit")
    _require_positive_int("max_turns")
    _require_nonempty_str("log_dir")
    _require_nonempty_str("transcript_dir")

    return sorted(errors)
