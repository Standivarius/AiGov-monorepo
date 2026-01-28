#!/usr/bin/env python3
"""Report GDPR base scenario library status (stdlib-only)."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
GDPR_DIR = ROOT / "packages" / "specs" / "scenarios" / "library" / "base" / "gdpr"
SOURCES_PATH = GDPR_DIR / "SOURCES.md"

FILENAME_RE = re.compile(r"^gdpr_(\d{3})_[a-z0-9_]+\.json$")
SCENARIO_ID_RE = re.compile(r"^GDPR-(\d{3})$")
SOURCES_HEADING_RE = re.compile(r"^## GDPR-(\d{3})\b")

SURFACE_TAGS = ["surface:chatbot", "surface:agent", "surface:both"]


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


def _extract_required(scenario: dict[str, Any], key: str, path: Path) -> Any:
    if key not in scenario:
        raise ValueError(f"{path}: missing required key '{key}'")
    return scenario[key]


def _read_sources_ids() -> set[str]:
    if not SOURCES_PATH.exists():
        raise ValueError(f"SOURCES file missing: {SOURCES_PATH}")
    ids: set[str] = set()
    for line in SOURCES_PATH.read_text(encoding="utf-8").splitlines():
        match = SOURCES_HEADING_RE.match(line.strip())
        if match:
            ids.add(match.group(1))
    return ids


def _read_sources_url_health() -> tuple[list[str], Counter[str]]:
    missing_url_ids: set[str] = set()
    domain_counts: Counter[str] = Counter()
    current_id: str | None = None
    for line in SOURCES_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        match = SOURCES_HEADING_RE.match(stripped)
        if match:
            current_id = match.group(1)
            continue
        if not stripped.startswith("URL:") or current_id is None:
            continue
        url_value = stripped.split("URL:", 1)[1].strip()
        if url_value == "(missing in backlog doc)":
            missing_url_ids.add(current_id)
            continue
        parsed = urlparse(url_value if "://" in url_value else f"https://{url_value}")
        domain = (parsed.netloc or url_value.split("/", 1)[0]).lower()
        if domain:
            domain_counts[domain] += 1
    return sorted(missing_url_ids, key=int), domain_counts


def main() -> int:
    errors: list[str] = []
    if not GDPR_DIR.exists():
        print(f"ERROR: GDPR library missing: {GDPR_DIR}")
        return 1

    scenario_files = sorted(GDPR_DIR.glob("gdpr_*.json"))
    if not scenario_files:
        print("ERROR: no GDPR scenario files found.")
        return 1

    scenario_ids: set[str] = set()
    numeric_ids: set[int] = set()
    role_counts: Counter[str] = Counter()
    surface_counts: Counter[str] = Counter()
    signal_counts: Counter[str] = Counter()
    population_counts: Counter[str] = Counter()

    for path in scenario_files:
        filename_match = FILENAME_RE.match(path.name)
        if not filename_match:
            errors.append(f"{path}: filename must match gdpr_###_<slug>.json")
            continue
        filename_num = filename_match.group(1)

        try:
            scenario = _ensure_dict(_load_json(path), f"{path}")
            scenario_id = _extract_required(scenario, "scenario_id", path)
            role = _extract_required(scenario, "role", path)
            risk_category = _extract_required(scenario, "risk_category", path)
            signal_ids = _extract_required(scenario, "signal_ids", path)
            tags = _extract_required(scenario, "tags", path)
        except (json.JSONDecodeError, ValueError) as exc:
            errors.append(str(exc))
            continue

        if not isinstance(scenario_id, str) or not scenario_id:
            errors.append(f"{path}: scenario_id must be a non-empty string")
            continue
        id_match = SCENARIO_ID_RE.match(scenario_id)
        if not id_match:
            errors.append(f"{path}: scenario_id must match GDPR-###")
            continue
        scenario_num = id_match.group(1)
        if scenario_num != filename_num:
            errors.append(
                f"{path}: scenario_id number ({scenario_num}) does not match filename ({filename_num})"
            )

        if not isinstance(role, str) or not role:
            errors.append(f"{path}: role must be a non-empty string")
        if not isinstance(risk_category, str) or not risk_category:
            errors.append(f"{path}: risk_category must be a non-empty string")

        try:
            signal_list = _ensure_list(signal_ids, f"{path}: signal_ids")
            tags_list = _ensure_list(tags, f"{path}: tags")
        except ValueError as exc:
            errors.append(str(exc))
            continue

        for signal in signal_list:
            if not isinstance(signal, str) or not signal:
                errors.append(f"{path}: signal_ids must be non-empty strings")
                break

        for tag in tags_list:
            if not isinstance(tag, str) or not tag:
                errors.append(f"{path}: tags must be non-empty strings")
                break

        scenario_ids.add(scenario_num)
        numeric_ids.add(int(scenario_num))
        role_counts[role] += 1
        for surface_tag in SURFACE_TAGS:
            if surface_tag in tags_list:
                surface_counts[surface_tag] += 1
        for signal in signal_list:
            if isinstance(signal, str) and signal:
                signal_counts[signal] += 1
        population_tags = [tag for tag in tags_list if isinstance(tag, str) and tag.startswith("population:")]
        if population_tags:
            for tag in population_tags:
                population_counts[tag] += 1
        else:
            population_counts["population:unknown"] += 1

    if numeric_ids:
        min_id = min(numeric_ids)
        max_id = max(numeric_ids)
    else:
        min_id = max_id = None

    missing_ids: list[int] = []
    if min_id is not None and max_id is not None:
        missing_ids = [num for num in range(min_id, max_id + 1) if num not in numeric_ids]

    print(f"Total scenarios: {len(numeric_ids)}")
    if min_id is not None and max_id is not None:
        print(f"Min ID: {min_id:03d}")
        print(f"Max ID: {max_id:03d}")
        missing_display = ", ".join(f"{num:03d}" for num in missing_ids) or "(none)"
        print(f"Missing IDs: {missing_display}")

    print("Counts by role:")
    for role, count in sorted(role_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  - {role}: {count}")

    print("Counts by surface tag:")
    for surface_tag in SURFACE_TAGS:
        print(f"  - {surface_tag}: {surface_counts.get(surface_tag, 0)}")

    print("Counts by population tag:")
    for population_tag in ["population:children", "population:general", "population:unknown"]:
        print(f"  - {population_tag}: {population_counts.get(population_tag, 0)}")

    print("Counts by signal_id:")
    for signal_id, count in sorted(signal_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  - {signal_id}: {count}")

    try:
        sources_ids = _read_sources_ids()
    except ValueError as exc:
        errors.append(str(exc))
        sources_ids = set()

    missing_in_sources = sorted(scenario_ids - sources_ids)
    extra_in_sources = sorted(sources_ids - scenario_ids)

    if missing_in_sources:
        print("SOURCES missing scenario headings:")
        for scenario_num in missing_in_sources:
            print(f"  - GDPR-{scenario_num}")
    if extra_in_sources:
        print("SOURCES headings without scenarios:")
        for scenario_num in extra_in_sources:
            print(f"  - GDPR-{scenario_num}")

    if SOURCES_PATH.exists():
        missing_url_ids, domain_counts = _read_sources_url_health()
        missing_display = ", ".join(f"GDPR-{scenario_num}" for scenario_num in missing_url_ids) or "(none)"
        print("SOURCES URL health summary:")
        print(f"  - Missing URL count: {len(missing_url_ids)}")
        print(f"  - Missing URL IDs: {missing_display}")
        print("  - Domain histogram:")
        for domain, count in sorted(domain_counts.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"    - {domain}: {count}")

    if errors:
        print("ERROR: structural checks failed:")
        for error in errors:
            print(f"  - {error}")

    if missing_in_sources or extra_in_sources:
        return 1
    if errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
