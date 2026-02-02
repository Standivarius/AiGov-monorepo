#!/usr/bin/env python3
"""Print deterministic Inspect command for Petri audit runs."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _load_seed_instructions(path: Path) -> list[str]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, list) or not payload:
        raise ValueError("seed instructions must be a non-empty JSON list")
    for item in payload:
        if not isinstance(item, str) or not item:
            raise ValueError("seed instructions must contain non-empty strings")
    return payload


def _json_dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=False)


def build_command(
    seed_instructions: list[str],
    auditor_model: str,
    target_model: str,
    judge_model: str,
    limit: int,
    max_turns: int,
    log_dir: str,
    transcript_dir: str,
) -> str:
    seed_json = _json_dump(seed_instructions)
    return (
        "inspect eval petri/audit"
        f" --limit {limit} --log-format=json --log-dir=\"{log_dir}\""
        f" --model-role auditor={auditor_model}"
        f" --model-role target={target_model}"
        f" --model-role judge={judge_model}"
        f" -T max_turns={max_turns}"
        f" -T transcript_save_dir=\"{transcript_dir}\""
        f" -T seed_instructions='{seed_json}'"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Print Inspect Petri audit run command.")
    parser.add_argument("--seed-instructions-json", required=True)
    parser.add_argument("--auditor-model", required=True)
    parser.add_argument("--target-model", required=True)
    parser.add_argument("--judge-model", required=True)
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--max-turns", type=int, default=2)
    parser.add_argument("--log-dir", default="./logs/aigov")
    parser.add_argument("--transcript-dir", default="./outputs")
    args = parser.parse_args()

    try:
        seed_instructions = _load_seed_instructions(Path(args.seed_instructions_json))
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.limit < 1:
        print("ERROR: limit must be >= 1")
        return 1
    if args.max_turns < 1:
        print("ERROR: max_turns must be >= 1")
        return 1

    command = build_command(
        seed_instructions,
        args.auditor_model,
        args.target_model,
        args.judge_model,
        args.limit,
        args.max_turns,
        args.log_dir,
        args.transcript_dir,
    )
    print(command)
    return 0


if __name__ == "__main__":
    sys.exit(main())
