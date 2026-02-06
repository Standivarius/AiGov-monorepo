#!/usr/bin/env python3
"""Validate intake_bundle_v0_1 fixtures (stdlib-only, fail-closed)."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "packages" / "specs" / "schemas" / "intake_bundle_v0_1.schema.json"
JURISDICTIONS_PATH = (
    ROOT / "packages" / "specs" / "docs" / "contracts" / "taxonomy" / "jurisdictions_v0.json"
)
SECTORS_PATH = ROOT / "packages" / "specs" / "docs" / "contracts" / "taxonomy" / "sectors_v0.json"
POLICY_PACKS_PATH = (
    ROOT / "packages" / "specs" / "docs" / "contracts" / "taxonomy" / "policy_packs_v0.json"
)
FORBIDDEN_ROOT_FIELDS = ("generated_at", "processed_at")


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _validate_schema(value: Any, schema: dict[str, Any], path: str, errors: list[str]) -> None:
    schema_type = schema.get("type")
    if schema_type == "object":
        if not isinstance(value, dict):
            errors.append(f"{path} must be an object")
            return
        min_properties = schema.get("minProperties")
        if isinstance(min_properties, int) and len(value) < min_properties:
            errors.append(f"{path} must contain at least {min_properties} properties")
        max_properties = schema.get("maxProperties")
        if isinstance(max_properties, int) and len(value) > max_properties:
            errors.append(f"{path} must contain at most {max_properties} properties")
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in value:
                    errors.append(f"{path} missing required key '{key}'")

        properties = schema.get("properties", {})
        pattern_properties = schema.get("patternProperties", {})
        additional = schema.get("additionalProperties", True)

        if isinstance(properties, dict):
            for key, prop_schema in properties.items():
                if key in value and isinstance(prop_schema, dict):
                    _validate_schema(value[key], prop_schema, f"{path}.{key}", errors)

        for key in sorted(value.keys()):
            if isinstance(properties, dict) and key in properties:
                continue
            matched_patterns = []
            if isinstance(pattern_properties, dict):
                for pattern, prop_schema in pattern_properties.items():
                    if not isinstance(prop_schema, dict):
                        continue
                    if re.fullmatch(pattern, key):
                        matched_patterns.append((pattern, prop_schema))
            if matched_patterns:
                for pattern, prop_schema in sorted(matched_patterns, key=lambda item: item[0]):
                    _validate_schema(
                        value[key],
                        prop_schema,
                        f"{path}.{key}",
                        errors,
                    )
                continue

            if additional is False:
                errors.append(f"{path} has unexpected key '{key}'")
                continue
            if isinstance(additional, dict):
                _validate_schema(value[key], additional, f"{path}.{key}", errors)
        return

    if schema_type == "array":
        if not isinstance(value, list):
            errors.append(f"{path} must be an array")
            return
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(value) < min_items:
            errors.append(f"{path} must contain at least {min_items} item(s)")
        max_items = schema.get("maxItems")
        if isinstance(max_items, int) and len(value) > max_items:
            errors.append(f"{path} must contain at most {max_items} item(s)")
        items_schema = schema.get("items")
        if isinstance(items_schema, dict):
            for idx, item in enumerate(value):
                _validate_schema(item, items_schema, f"{path}[{idx}]", errors)
        return

    if schema_type == "string":
        if not isinstance(value, str):
            errors.append(f"{path} must be a string")
            return
        min_length = schema.get("minLength")
        if isinstance(min_length, int) and len(value) < min_length:
            errors.append(f"{path} must be at least {min_length} character(s)")
        enum = schema.get("enum")
        if isinstance(enum, list) and value not in enum:
            errors.append(f"{path} must be one of {enum}")
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.fullmatch(pattern, value) is None:
            errors.append(f"{path} must match pattern '{pattern}'")
        return

    errors.append(f"{path} has unsupported schema type '{schema_type}'")


def _load_allowlist(path: Path, label: str) -> set[str]:
    if not path.exists():
        raise ValueError(f"{label} allowlist not found: {path}")
    data = _load_json(path)
    if not isinstance(data, list):
        raise ValueError(f"{label} allowlist must be an array")
    items: set[str] = set()
    for item in data:
        if not isinstance(item, str):
            raise ValueError(f"{label} allowlist must contain strings")
        if not item.strip():
            raise ValueError(f"{label} allowlist must not contain blank entries")
        items.add(item)
    if not items:
        raise ValueError(f"{label} allowlist must not be empty")
    return items


def _validate_context_profile(
    bundle: dict[str, Any],
    jurisdictions: set[str],
    sectors: set[str],
    policy_packs: set[str],
    errors: list[str],
) -> None:
    intake = bundle.get("intake")
    if not isinstance(intake, dict):
        return
    context_profile = intake.get("context_profile")
    if not isinstance(context_profile, dict):
        return

    jurisdiction = context_profile.get("jurisdiction")
    jurisdiction_valid = False
    if isinstance(jurisdiction, str):
        if jurisdiction in jurisdictions:
            jurisdiction_valid = True
        else:
            errors.append(
                f"intake.context_profile.jurisdiction contains unknown value '{jurisdiction}'"
            )

    sector = context_profile.get("sector")
    sector_valid = False
    if isinstance(sector, str):
        if sector in sectors:
            sector_valid = True
        else:
            errors.append(f"intake.context_profile.sector contains unknown value '{sector}'")

    policy_pack_stack = context_profile.get("policy_pack_stack")
    if not isinstance(policy_pack_stack, list):
        return
    if not jurisdiction_valid or not sector_valid:
        return
    unknown_packs = sorted(
        {
            pack
            for pack in policy_pack_stack
            if isinstance(pack, str) and pack not in policy_packs
        }
    )
    if unknown_packs:
        errors.append(
            "intake.context_profile.policy_pack_stack contains unknown value(s): "
            f"{unknown_packs}"
        )
        return

    expected_stack = ["GDPR_EU", jurisdiction, sector, "client"]
    if policy_pack_stack != expected_stack:
        errors.append(
            "intake.context_profile.policy_pack_stack must equal "
            f"{expected_stack}"
        )


def _validate_evidence_refs(bundle: dict[str, Any], errors: list[str]) -> None:
    evidence_index = bundle.get("evidence_index")
    if not isinstance(evidence_index, dict):
        return
    # Keep empty-index failures single-mode: schema minProperties already reports this.
    if not evidence_index:
        return
    evidence_keys = set(evidence_index.keys())

    evidence_refs = bundle.get("evidence_refs")
    if not isinstance(evidence_refs, dict):
        return

    for field_path in sorted(evidence_refs.keys()):
        refs = evidence_refs.get(field_path)
        if not isinstance(refs, list):
            continue
        for evidence_id in refs:
            if not isinstance(evidence_id, str):
                continue
            if evidence_id not in evidence_keys:
                errors.append(
                    "evidence_refs contains dangling reference: "
                    f"field_path '{field_path}' -> '{evidence_id}'"
                )


def _validate_source_paths(bundle: dict[str, Any], errors: list[str]) -> None:
    evidence_index = bundle.get("evidence_index")
    if not isinstance(evidence_index, dict):
        return

    for evidence_id in sorted(evidence_index.keys()):
        entry = evidence_index.get(evidence_id)
        if not isinstance(entry, dict):
            continue
        source_path = entry.get("source_path")
        if not isinstance(source_path, str) or not source_path:
            continue
        candidate = Path(source_path)
        if candidate.is_absolute():
            errors.append(
                "evidence_index contains absolute source_path for "
                f"'{evidence_id}': {source_path}"
            )
            continue
        if any(part == ".." for part in candidate.parts):
            errors.append(
                "evidence_index contains traversal source_path for "
                f"'{evidence_id}': {source_path}"
            )


def validate_intake_bundle_fixture(path: Path) -> list[str]:
    if not path.exists():
        return [f"fixture not found: {path}"]
    if not SCHEMA_PATH.exists():
        return [f"schema not found: {SCHEMA_PATH}"]

    try:
        schema = _ensure_dict(_load_json(SCHEMA_PATH), "schema")
    except (json.JSONDecodeError, ValueError) as exc:
        return [f"schema invalid: {exc}"]

    try:
        jurisdictions = _load_allowlist(JURISDICTIONS_PATH, "jurisdictions")
        sectors = _load_allowlist(SECTORS_PATH, "sectors")
        policy_packs = _load_allowlist(POLICY_PACKS_PATH, "policy_packs")
    except (json.JSONDecodeError, ValueError) as exc:
        return [str(exc)]

    try:
        payload = _ensure_dict(_load_json(path), str(path))
    except (json.JSONDecodeError, ValueError) as exc:
        return [f"{path}: invalid JSON ({exc})"]

    errors: list[str] = []
    schema_errors: list[str] = []
    _validate_schema(payload, schema, "bundle", schema_errors)

    forbidden_fields_present: list[str] = []
    for field_name in sorted(FORBIDDEN_ROOT_FIELDS):
        if field_name in payload:
            forbidden_fields_present.append(field_name)
            errors.append(f"bundle contains forbidden root-level nondeterministic field '{field_name}'")
    if forbidden_fields_present:
        for field_name in forbidden_fields_present:
            schema_error = f"bundle has unexpected key '{field_name}'"
            schema_errors = [error for error in schema_errors if error != schema_error]

    errors.extend(schema_errors)

    _validate_context_profile(payload, jurisdictions, sectors, policy_packs, errors)
    _validate_evidence_refs(payload, errors)
    _validate_source_paths(payload, errors)

    return sorted(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate intake_bundle_v0_1 fixture.")
    parser.add_argument("--fixture", required=True, help="Path to intake bundle fixture JSON")
    args = parser.parse_args()

    errors = validate_intake_bundle_fixture(Path(args.fixture))
    if errors:
        print("ERROR: intake bundle v0.1 validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: intake bundle v0.1 validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
