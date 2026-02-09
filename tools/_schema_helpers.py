#!/usr/bin/env python3
"""Shared stdlib-only helpers for validating JSON-schema-like contracts."""
from __future__ import annotations

import json
import re
from typing import Any


_MISSING = object()


def _validate_schema(value: Any, schema: dict[str, Any], path: str, errors: list[str]) -> None:
    const_value = schema.get("const", _MISSING)
    if const_value is not _MISSING and value != const_value:
        errors.append(f"{path} must be {const_value!r}")

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
                    child_path = f"{path}.{key}" if path else key
                    _validate_schema(value[key], prop_schema, child_path, errors)

        for key in sorted(value.keys()):
            if isinstance(properties, dict) and key in properties:
                continue

            matched_patterns: list[tuple[str, dict[str, Any]]] = []
            if isinstance(pattern_properties, dict):
                for pattern, prop_schema in pattern_properties.items():
                    if not isinstance(prop_schema, dict):
                        continue
                    if re.fullmatch(pattern, key):
                        matched_patterns.append((pattern, prop_schema))
            if matched_patterns:
                child_path = f"{path}.{key}" if path else key
                for _, prop_schema in sorted(matched_patterns, key=lambda item: item[0]):
                    _validate_schema(value[key], prop_schema, child_path, errors)
                continue

            child_path = f"{path}.{key}" if path else key
            if additional is False:
                errors.append(f"{path} has unexpected key '{key}'")
                continue
            if isinstance(additional, dict):
                _validate_schema(value[key], additional, child_path, errors)
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
        if schema.get("uniqueItems") is True:
            seen: set[str] = set()
            for item in value:
                try:
                    canonical = json.dumps(item, sort_keys=True, separators=(",", ":"))
                except TypeError:
                    canonical = repr(item)
                if canonical in seen:
                    errors.append(f"{path} must contain unique items")
                    break
                seen.add(canonical)
        items_schema = schema.get("items")
        if isinstance(items_schema, dict):
            for idx, item in enumerate(value):
                child_path = f"{path}[{idx}]"
                _validate_schema(item, items_schema, child_path, errors)
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

    if schema_type == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            errors.append(f"{path} must be a number")
            return
        minimum = schema.get("minimum")
        if isinstance(minimum, (int, float)) and value < minimum:
            errors.append(f"{path} must be >= {minimum}")
        maximum = schema.get("maximum")
        if isinstance(maximum, (int, float)) and value > maximum:
            errors.append(f"{path} must be <= {maximum}")
        return

    if schema_type == "boolean":
        if not isinstance(value, bool):
            errors.append(f"{path} must be a boolean")
        return

    if schema_type == "null":
        if value is not None:
            errors.append(f"{path} must be null")
        return

    errors.append(f"{path} has unsupported schema type '{schema_type}'")
