"""Deterministic scenario compiler + bundle manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be a JSON object")
    return data


def _safe_name(value: str) -> str:
    safe = []
    for char in value:
        if char.isalnum() or char in {"-", "_"}:
            safe.append(char)
        else:
            safe.append("_")
    return "".join(safe)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def compute_bundle_hash(entries: Iterable[dict[str, Any]]) -> str:
    lines = []
    for entry in entries:
        path = entry.get("path")
        sha256 = entry.get("sha256")
        if isinstance(path, str) and isinstance(sha256, str):
            lines.append(f"{path}:{sha256}")
    digest = _sha256_bytes(("\n".join(sorted(lines)) + "\n").encode("utf-8"))
    return digest


def compile_scenario(base_scenario: Dict[str, Any], override: Dict[str, Any] | None) -> Dict[str, Any]:
    compiled = dict(base_scenario)
    scenario_id = base_scenario.get("scenario_id", "unknown")
    instance_id = scenario_id
    if override:
        policy_profile = override.get("policy_profile")
        if not isinstance(policy_profile, dict) or not policy_profile:
            raise ValueError(f"Override missing policy_profile for base scenario '{scenario_id}'")
        client_id = override.get("client_id", "unknown")
        instance_id = f"{scenario_id}__{client_id}"
        compiled["override"] = {
            "client_id": override.get("client_id"),
            "override_type": override.get("override_type"),
            "base_scenario_id": override.get("base_scenario_id"),
        }
        compiled["policy_profile"] = policy_profile
    compiled["scenario_instance_id"] = instance_id
    return compiled


def compile_bundle(
    base_dir: str | Path,
    overrides_dir: str | Path | None,
    output_dir: str | Path,
) -> Dict[str, Any]:
    base_dir = Path(base_dir)
    if isinstance(overrides_dir, str) and overrides_dir == "":
        raise ValueError("overrides_dir must not be an empty string")
    overrides_dir = Path(overrides_dir) if overrides_dir is not None else None
    output_dir = Path(output_dir)
    scenarios_dir = output_dir / "scenarios"

    base_files = sorted(base_dir.rglob("*.json"))
    if not base_files:
        raise ValueError(f"No base scenarios found in {base_dir}")

    overrides_by_scenario: Dict[str, Dict[str, Any]] = {}
    if overrides_dir:
        if not overrides_dir.exists():
            raise ValueError(f"Overrides directory does not exist: {overrides_dir}")
        override_files = sorted(overrides_dir.rglob("*.json"))
        if not override_files:
            raise ValueError(f"Overrides directory contains no overrides: {overrides_dir}")
        for override_path in override_files:
            override = _load_json(override_path)
            base_scenario_id = override.get("base_scenario_id")
            if not isinstance(base_scenario_id, str) or not base_scenario_id:
                raise ValueError(f"{override_path} missing base_scenario_id")
            if base_scenario_id in overrides_by_scenario:
                raise ValueError(f"Duplicate override for {base_scenario_id}")
            overrides_by_scenario[base_scenario_id] = override

    scenario_entries: list[dict[str, Any]] = []
    base_scenario_ids: set[str] = set()

    for base_path in base_files:
        base_scenario = _load_json(base_path)
        scenario_id = base_scenario.get("scenario_id")
        if not isinstance(scenario_id, str) or not scenario_id:
            raise ValueError(f"{base_path} missing scenario_id")
        base_scenario_ids.add(scenario_id)

        override = overrides_by_scenario.get(scenario_id)
        compiled = compile_scenario(base_scenario, override)
        instance_id = compiled.get("scenario_instance_id", scenario_id)
        filename = f"{_safe_name(str(instance_id))}.json"
        rel_path = f"scenarios/{filename}"
        output_path = scenarios_dir / filename

        _write_json(output_path, compiled)
        sha256 = _sha256_file(output_path)
        scenario_entries.append(
            {
                "path": rel_path,
                "sha256": sha256,
                "scenario_id": scenario_id,
                "scenario_instance_id": instance_id,
            }
        )

    unknown_overrides = sorted(set(overrides_by_scenario.keys()) - base_scenario_ids)
    if unknown_overrides:
        raise ValueError(f"Overrides reference unknown base_scenario_id(s): {unknown_overrides}")

    scenario_entries = sorted(scenario_entries, key=lambda item: item["path"])
    bundle_hash = compute_bundle_hash(scenario_entries)

    manifest = {
        "schema_version": "0.1.0",
        "bundle_dir": str(output_dir),
        "scenarios": scenario_entries,
        "bundle_hash": bundle_hash,
    }
    _write_json(output_dir / "manifest.json", manifest)
    return manifest
