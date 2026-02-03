#!/usr/bin/env python3
"""Validate deterministic Inspect Petri run command output."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _run_tool(tool_path: Path, seed_path: Path) -> str:
    cmd = [
        sys.executable,
        str(tool_path),
        "--seed-instructions-json",
        str(seed_path),
        "--auditor-model",
        "openai/gpt-4o-mini",
        "--target-model",
        "openai/gpt-4o-mini",
        "--judge-model",
        "openai/gpt-4o-mini",
    ]
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        details = stderr or stdout or "unknown error"
        raise ValueError(f"tool failed: {details}")
    return result.stdout.strip()


def _validate_fixture(tool_path: Path, seed_path: Path, expected_path: Path) -> list[str]:
    errors: list[str] = []
    if not tool_path.exists():
        return [f"tool missing: {tool_path}"]
    if not seed_path.exists():
        return [f"seed fixture missing: {seed_path}"]
    if not expected_path.exists():
        return [f"expected fixture missing: {expected_path}"]

    try:
        first = _run_tool(tool_path, seed_path)
        second = _run_tool(tool_path, seed_path)
    except ValueError as exc:
        return [str(exc)]

    if first != second:
        errors.append(f"command output is not deterministic across runs for {seed_path.name}")

    expected = expected_path.read_text(encoding="utf-8").strip()
    if first != expected:
        errors.append(f"command output does not match expected fixture for {seed_path.name}")

    return errors


def validate_print_inspect_petri_run_command(
    tool_path: Path, seed_path: Path, expected_path: Path
) -> list[str]:
    errors = _validate_fixture(tool_path, seed_path, expected_path)
    edge_seed = seed_path.parent / "seed_instructions_edge_cases.json"
    edge_expected = seed_path.parent / "expected_inspect_command_edge_cases.txt"
    if edge_seed.exists() or edge_expected.exists():
        errors.extend(_validate_fixture(tool_path, edge_seed, edge_expected))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Inspect Petri run command output.")
    parser.add_argument("--tool", required=True)
    parser.add_argument("--seed", required=True)
    parser.add_argument("--expected", required=True)
    args = parser.parse_args()

    errors = validate_print_inspect_petri_run_command(
        Path(args.tool), Path(args.seed), Path(args.expected)
    )
    if errors:
        print("ERROR: inspect run command validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: inspect run command validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
