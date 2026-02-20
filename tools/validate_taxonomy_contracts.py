#!/usr/bin/env python3
"""Validate taxonomy contracts and report drift across specs/EP/PE."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise RuntimeError(f"Missing required file: {path}")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {path}: {exc}") from exc


def _rating_enum(schema: dict[str, Any], path: Path) -> list[str]:
    try:
        enum = schema["properties"]["rating"]["enum"]
    except KeyError as exc:
        raise RuntimeError(f"Schema missing properties.rating.enum: {path}") from exc
    if not isinstance(enum, list) or not enum:
        raise RuntimeError(f"Schema rating enum must be non-empty list: {path}")
    return [str(x) for x in enum]


def _extract_case_signals(case: dict[str, Any]) -> set[str]:
    expected = case.get("expected_outcome") or {}
    if not isinstance(expected, dict):
        return set()
    required = expected.get("required_signals")
    base = expected.get("signals")
    extra = expected.get("allowed_extra_signals")
    all_ids: set[str] = set()
    for raw in (required, base, extra):
        if raw is None:
            continue
        if not isinstance(raw, list):
            continue
        all_ids.update(str(x) for x in raw)
    return all_ids


def _classify_verdict(
    raw_verdict: str, canonical_set: set[str], aliases: dict[str, Any]
) -> tuple[bool, bool, str]:
    """Return (is_valid, is_legacy, normalized)."""
    if raw_verdict in canonical_set:
        return True, False, raw_verdict
    normalized = str(aliases.get(raw_verdict, raw_verdict))
    if normalized in canonical_set:
        return True, True, normalized
    return False, False, normalized


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-verdict-drift",
        action="store_true",
        help="Do not fail when schema rating enums differ from taxonomy canonical verdicts.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    verdicts_path = root / "packages/specs/docs/contracts/taxonomy/verdicts.json"
    signals_path = root / "packages/specs/docs/contracts/taxonomy/signals.json"

    schema_paths = [
        root / "packages/specs/schemas/behaviour_json_v0_phase0.schema.json",
        root / "packages/ep/aigov_ep/contracts/behaviour_json_v0_phase0.schema.json",
        root / "packages/pe/aigov_eval/contracts/behaviour_json_v0_phase0.schema.json",
    ]

    case_glob = root / "packages/pe/cases/calibration"
    all_cases_dir = root / "packages/pe/cases"
    golden_set_dir = root / "packages/pe/golden_set"

    problems: list[str] = []
    warnings: list[str] = []

    verdicts = _load_json(verdicts_path)
    canonical = verdicts.get("canonical")
    aliases = verdicts.get("legacy_aliases")
    if not isinstance(canonical, list) or not canonical:
        problems.append(f"{verdicts_path}: canonical must be non-empty list")
        canonical_set: set[str] = set()
    else:
        canonical_set = {str(x) for x in canonical}

    if not isinstance(aliases, dict):
        problems.append(f"{verdicts_path}: legacy_aliases must be object")
    else:
        for legacy, mapped in aliases.items():
            mapped_s = str(mapped)
            if canonical_set and mapped_s not in canonical_set:
                problems.append(
                    f"{verdicts_path}: legacy alias {legacy!r} maps to non-canonical {mapped_s!r}"
                )

    for schema_path in schema_paths:
        schema = _load_json(schema_path)
        enum_set = set(_rating_enum(schema, schema_path))
        if canonical_set and enum_set != canonical_set:
            msg = (
                f"Verdict drift: {schema_path} rating enum {sorted(enum_set)} "
                f"!= taxonomy canonical {sorted(canonical_set)}"
            )
            if args.allow_verdict_drift:
                warnings.append(msg)
            else:
                problems.append(msg)

    signals = _load_json(signals_path)
    signal_ids = signals.get("signal_ids")
    if not isinstance(signal_ids, list) or not signal_ids:
        problems.append(f"{signals_path}: signal_ids must be non-empty list")
        signal_set: set[str] = set()
    else:
        signal_set = {str(x) for x in signal_ids}

    if case_glob.exists():
        for case_file in sorted(case_glob.glob("*.json")):
            case = _load_json(case_file)
            scenario_id = case.get("scenario_id", case_file.name)
            used = _extract_case_signals(case)
            unknown = sorted(x for x in used if x not in signal_set)
            if unknown:
                problems.append(
                    f"{case_file} ({scenario_id}): unknown signal ids: {', '.join(unknown)}"
                )
    else:
        warnings.append(f"Calibration case directory not found: {case_glob}")

    if all_cases_dir.exists():
        for case_file in sorted(all_cases_dir.rglob("*.json")):
            case = _load_json(case_file)
            expected = case.get("expected_outcome")
            if not isinstance(expected, dict):
                continue
            raw_verdict = expected.get("verdict")
            if not isinstance(raw_verdict, str):
                continue
            is_valid, is_legacy, normalized = _classify_verdict(
                raw_verdict, canonical_set, aliases if isinstance(aliases, dict) else {}
            )
            scenario_id = case.get("scenario_id", case_file.name)
            if not is_valid:
                problems.append(
                    f"{case_file} ({scenario_id}): invalid expected_outcome.verdict {raw_verdict!r}"
                )
            elif is_legacy:
                problems.append(
                    f"{case_file} ({scenario_id}): legacy verdict label {raw_verdict!r} "
                    f"(use canonical {normalized!r})"
                )
    else:
        warnings.append(f"Cases directory not found: {all_cases_dir}")

    if golden_set_dir.exists():
        for gs_file in sorted(golden_set_dir.glob("*.json")):
            gs = _load_json(gs_file)
            questions = gs.get("questions")
            if not isinstance(questions, list):
                continue
            for i, q in enumerate(questions, start=1):
                if not isinstance(q, dict):
                    continue
                raw_verdict = q.get("expected_verdict")
                if not isinstance(raw_verdict, str):
                    continue
                is_valid, is_legacy, normalized = _classify_verdict(
                    raw_verdict, canonical_set, aliases if isinstance(aliases, dict) else {}
                )
                if not is_valid:
                    problems.append(
                        f"{gs_file} question#{i}: invalid expected_verdict {raw_verdict!r}"
                    )
                elif is_legacy:
                    problems.append(
                        f"{gs_file} question#{i}: legacy expected_verdict {raw_verdict!r} "
                        f"(use canonical {normalized!r})"
                    )
    else:
        warnings.append(f"Golden set directory not found: {golden_set_dir}")

    for w in warnings:
        print(f"WARN: {w}")
    for p in problems:
        print(f"ERROR: {p}")

    if problems:
        print(f"FAIL: taxonomy validation failed ({len(problems)} issue(s)).")
        return 1

    print("PASS: taxonomy validation succeeded.")
    if warnings:
        print(f"NOTE: completed with {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
