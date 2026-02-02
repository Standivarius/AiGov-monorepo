#!/usr/bin/env python3
"""Validate module registry and module cards (stdlib-only)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "packages" / "specs" / "docs" / "contracts" / "modules" / "module_registry_v0.yaml"
SCHEMA_PATH = ROOT / "packages" / "specs" / "schemas" / "module_card_v0.schema.json"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _ensure_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return value


def _load_registry(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"registry missing: {path}")
    module_ids: set[str] = set()
    test_ids: set[str] = set()
    in_modules = False
    in_registries = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("modules:"):
            in_modules = True
            in_registries = False
            continue
        if line.startswith("registries:"):
            in_registries = True
            in_modules = False
            continue
        if line.startswith("- module_id:"):
            module_id = line.split(":", 1)[1].strip()
            if in_modules:
                module_ids.add(module_id)
            elif in_registries:
                test_ids.add(module_id)
    if not module_ids:
        raise ValueError("registry contains no module_id entries")
    return {"module_ids": module_ids, "test_ids": test_ids}


def _load_schema(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"schema missing: {path}")
    return _ensure_dict(_load_json(path), str(path))


def _schema_required_and_allowed(schema: dict[str, Any]) -> tuple[set[str], set[str]]:
    required = schema.get("required", [])
    props = schema.get("properties", {})
    if not isinstance(required, list) or not isinstance(props, dict):
        raise ValueError("schema must define required and properties")
    return set(required), set(props.keys())


def _validate_card(card: dict[str, Any], path: Path, schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required, allowed = _schema_required_and_allowed(schema)
    keys = set(card.keys())
    missing = sorted(required - keys)
    extra = sorted(keys - allowed)
    if missing:
        errors.append(f"{path}: missing required keys: {missing}")
    if extra:
        errors.append(f"{path}: extra keys not allowed: {extra}")

    if card.get("schema_version") != "0.1.0":
        errors.append(f"{path}: schema_version must be '0.1.0'")

    module_id = card.get("module_id")
    if not isinstance(module_id, str) or not module_id:
        errors.append(f"{path}: module_id must be a non-empty string")

    boundaries = card.get("boundaries")
    if not isinstance(boundaries, dict):
        errors.append(f"{path}: boundaries must be an object")
    else:
        for field in ("inputs", "outputs"):
            if field not in boundaries:
                errors.append(f"{path}: boundaries missing '{field}'")
            else:
                items = boundaries.get(field)
                if not isinstance(items, list):
                    errors.append(f"{path}: boundaries.{field} must be an array")
                else:
                    for item in items:
                        if not isinstance(item, dict):
                            errors.append(f"{path}: boundaries.{field} entries must be objects")
                            continue
                        if set(item.keys()) != {"name", "contract_ref_path"}:
                            errors.append(
                                f"{path}: boundaries.{field} entries must have name and contract_ref_path"
                            )
                        if not isinstance(item.get("name"), str) or not item.get("name"):
                            errors.append(f"{path}: boundaries.{field}.name must be a non-empty string")
                        if not isinstance(item.get("contract_ref_path"), str) or not item.get("contract_ref_path"):
                            errors.append(
                                f"{path}: boundaries.{field}.contract_ref_path must be a non-empty string"
                            )

    knobs = card.get("knobs")
    if not isinstance(knobs, list):
        errors.append(f"{path}: knobs must be an array")
    else:
        seen_ids: set[str] = set()
        for knob in knobs:
            if not isinstance(knob, dict):
                errors.append(f"{path}: knobs entries must be objects")
                continue
            knob_id = knob.get("id")
            if not isinstance(knob_id, str) or not knob_id:
                errors.append(f"{path}: knob id must be a non-empty string")
            elif knob_id in seen_ids:
                errors.append(f"{path}: knob id '{knob_id}' must be unique")
            else:
                seen_ids.add(knob_id)

    risks = card.get("risks")
    if not isinstance(risks, list):
        errors.append(f"{path}: risks must be an array")
    return errors


def validate_module_cards(cards_dir: Path) -> list[str]:
    errors: list[str] = []
    try:
        registry = _load_registry(REGISTRY_PATH)
        schema = _load_schema(SCHEMA_PATH)
    except ValueError as exc:
        return [str(exc)]

    module_ids = registry["module_ids"]
    card_paths = sorted(cards_dir.glob("*.card.yaml")) + sorted(cards_dir.glob("*.card.json"))
    if not card_paths:
        return [f"no module cards found in {cards_dir}"]

    for path in card_paths:
        try:
            card = _ensure_dict(_load_json(path), str(path))
        except (json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{path}: invalid JSON ({exc})")
            continue

        errors.extend(_validate_card(card, path, schema))
        module_id = card.get("module_id")
        if isinstance(module_id, str) and module_id and module_id not in module_ids:
            errors.append(f"{path}: module_id '{module_id}' not in registry")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate module cards against registry + schema.")
    parser.add_argument("--cards-dir", required=True, help="Directory containing module cards")
    args = parser.parse_args()

    errors = validate_module_cards(Path(args.cards_dir))
    if errors:
        print("ERROR: module cards validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: module cards validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
