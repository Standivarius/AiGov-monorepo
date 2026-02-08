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
RECONCILE_SCHEMA_PATH = ROOT / "packages" / "specs" / "schemas" / "intake_bundle_reconcile_v0_1.schema.json"
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

    if schema_type == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            errors.append(f"{path} must be an integer")
            return
        minimum = schema.get("minimum")
        if isinstance(minimum, int) and value < minimum:
            errors.append(f"{path} must be >= {minimum}")
        maximum = schema.get("maximum")
        if isinstance(maximum, int) and value > maximum:
            errors.append(f"{path} must be <= {maximum}")
        return

    if schema_type == "boolean":
        if not isinstance(value, bool):
            errors.append(f"{path} must be a boolean")
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


def _validate_stage_schema(path: Path, schema_path: Path, label: str) -> tuple[dict[str, Any] | None, list[str]]:
    if not path.exists():
        return None, [f"fixture not found: {path}"]
    if not schema_path.exists():
        return None, [f"{label} schema not found: {schema_path}"]

    try:
        schema = _ensure_dict(_load_json(schema_path), "schema")
    except (json.JSONDecodeError, ValueError) as exc:
        return None, [f"{label} schema invalid: {exc}"]

    try:
        payload = _ensure_dict(_load_json(path), str(path))
    except (json.JSONDecodeError, ValueError) as exc:
        return None, [f"{path}: invalid JSON ({exc})"]

    errors: list[str] = []
    _validate_schema(payload, schema, label, errors)
    return payload, errors


def _validate_reconcile_policy(payload: dict[str, Any], errors: list[str]) -> None:
    conflicts = payload.get("conflicts")
    if not isinstance(conflicts, list):
        return

    order_keys: list[tuple[str, str]] = []
    has_unresolved = False
    has_critical = False

    for idx, conflict in enumerate(conflicts):
        if not isinstance(conflict, dict):
            continue
        conflict_id = conflict.get("conflict_id")
        field_path = conflict.get("field_path")
        if isinstance(field_path, str) and isinstance(conflict_id, str):
            order_keys.append((field_path, conflict_id))

        severity = conflict.get("severity")
        if severity == "critical":
            has_critical = True

        if conflict.get("resolution") == "unresolved":
            has_unresolved = True

        left_value = conflict.get("left_value")
        right_value = conflict.get("right_value")
        if isinstance(left_value, str) and isinstance(right_value, str) and left_value == right_value:
            errors.append(f"reconcile.conflicts[{idx}] must capture disagreement (left_value != right_value)")

        evidence_refs = conflict.get("evidence_refs")
        if isinstance(evidence_refs, list):
            refs = [item for item in evidence_refs if isinstance(item, str)]
            if refs != sorted(refs):
                errors.append(f"reconcile.conflicts[{idx}].evidence_refs must be sorted")
            if len(refs) != len(set(refs)):
                errors.append(f"reconcile.conflicts[{idx}].evidence_refs must be unique")

    if order_keys and order_keys != sorted(order_keys):
        errors.append("reconcile.conflicts must be sorted by (field_path, conflict_id)")
    if conflicts and not has_critical:
        errors.append("reconcile.conflicts must contain at least one critical conflict")
    if conflicts and not has_unresolved:
        errors.append("reconcile.conflicts must contain at least one unresolved conflict")


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


def validate_intake_bundle_reconcile_fixture(path: Path) -> list[str]:
    payload, errors = _validate_stage_schema(path, RECONCILE_SCHEMA_PATH, "reconcile")
    if payload is None:
        return sorted(errors)
    _validate_reconcile_policy(payload, errors)
    return sorted(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate intake_bundle_v0_1 and reconcile fixture.")
    parser.add_argument(
        "--mode",
        choices=("bundle", "reconcile"),
        default="bundle",
        help="Validation mode.",
    )
    parser.add_argument("--fixture", required=True, help="Path to intake bundle fixture JSON")
    args = parser.parse_args()

    fixture_path = Path(args.fixture)
    if args.mode == "bundle":
        errors = validate_intake_bundle_fixture(fixture_path)
        error_header = "ERROR: intake bundle v0.1 validation failed:"
        success_message = "PASS: intake bundle v0.1 validated."
    elif args.mode == "reconcile":
        errors = validate_intake_bundle_reconcile_fixture(fixture_path)
        error_header = "ERROR: intake bundle reconcile validation failed:"
        success_message = "PASS: intake bundle reconcile fixture validated."
    else:
        errors = [f"unsupported mode: {args.mode}"]
        error_header = "ERROR: intake bundle validation failed:"
        success_message = ""

    if errors:
        print(error_header)
        for error in errors:
            print(f"  - {error}")
        return 1
    print(success_message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
