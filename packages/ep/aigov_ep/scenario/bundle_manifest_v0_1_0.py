"""Load and validate deterministic bundle manifests (schema_version 0.1.0)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ensure_lowercase_hex_sha256(value: object, field_label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(field_label)
    if len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
        raise ValueError(field_label)
    return value


def _require_nonempty_str(value: object, field_label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(field_label)
    return value


def load_and_validate_manifest(bundle_dir: Path) -> list[Path]:
    manifest_path = bundle_dir / "manifest.json"
    if not manifest_path.exists():
        raise ValueError(f"manifest.json not found in {bundle_dir}")
    if manifest_path.is_symlink():
        raise ValueError("manifest.json must not be a symlink")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid manifest.json ({exc.msg})") from exc

    if not isinstance(manifest, dict):
        raise ValueError("manifest.json must be an object")

    schema_version = manifest.get("schema_version")
    if schema_version != "0.1.0":
        raise ValueError('manifest.json schema_version must be "0.1.0"')

    scenarios = manifest.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("manifest.json scenarios must be a non-empty list")

    bundle_root = bundle_dir.resolve()
    resolved_paths: list[Path] = []
    scenario_entries: list[tuple[int, str, str]] = []

    seen_scenario_ids: set[str] = set()
    seen_scenario_instance_ids: set[str] = set()
    seen_paths: set[str] = set()

    for index, entry in enumerate(scenarios):
        if not isinstance(entry, dict):
            raise ValueError(f"manifest.json scenarios[{index}] must be an object")
        scenario_id = _require_nonempty_str(
            entry.get("scenario_id"),
            f"manifest.json scenarios[{index}] missing scenario_id",
        )
        scenario_instance_id = _require_nonempty_str(
            entry.get("scenario_instance_id"),
            f"manifest.json scenarios[{index}] missing scenario_instance_id",
        )
        rel_path = _require_nonempty_str(
            entry.get("path"),
            f"manifest.json scenarios[{index}] missing path",
        )
        _ensure_lowercase_hex_sha256(
            entry.get("sha256"),
            f"manifest.json scenarios[{index}] missing sha256",
        )
        if scenario_id in seen_scenario_ids:
            raise ValueError(
                "manifest.json scenarios[*].scenario_id values must be unique "
                f"(duplicate {scenario_id!r})"
            )
        seen_scenario_ids.add(scenario_id)
        if scenario_instance_id in seen_scenario_instance_ids:
            raise ValueError(
                "manifest.json scenarios[*].scenario_instance_id values must be unique "
                f"(duplicate {scenario_instance_id!r})"
            )
        seen_scenario_instance_ids.add(scenario_instance_id)
        if rel_path in seen_paths:
            raise ValueError(
                "manifest.json scenarios[*].path values must be unique "
                f"(duplicate {rel_path!r})"
            )
        seen_paths.add(rel_path)
        scenario_entries.append((index, scenario_instance_id, rel_path))

    ordered_instance_ids = [instance_id for _, instance_id, _ in scenario_entries]
    if ordered_instance_ids != sorted(ordered_instance_ids):
        raise ValueError("manifest.json scenarios must be sorted by scenario_instance_id")

    for index, _, rel_path in scenario_entries:
        entry = scenarios[index]
        if not isinstance(entry, dict):
            raise ValueError(f"manifest.json scenarios[{index}] must be an object")
        expected_sha256 = _ensure_lowercase_hex_sha256(
            entry.get("sha256"),
            f"manifest.json scenarios[{index}] missing sha256",
        )
        scenario_path = (bundle_dir / rel_path).resolve()
        if bundle_root not in scenario_path.parents and scenario_path != bundle_root:
            raise ValueError(
                f"manifest.json scenarios[{index}].path escapes bundle_dir: {rel_path}"
            )
        if not scenario_path.exists():
            raise ValueError(
                f"manifest.json scenarios[{index}].path not found: {rel_path}"
            )
        if scenario_path.is_symlink():
            raise ValueError(
                f"manifest.json scenarios[{index}].path must not be a symlink: {rel_path}"
            )
        actual_sha256 = _sha256_file(scenario_path)
        if actual_sha256 != expected_sha256:
            raise ValueError(
                f"manifest.json scenarios[{index}].sha256 mismatch for {rel_path}"
            )
        resolved_paths.append(scenario_path)

    return resolved_paths
