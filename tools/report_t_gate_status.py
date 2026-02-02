#!/usr/bin/env python3
"""Report evalsets/evals status from planning registries (deterministic)."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLANNING_DIR = ROOT / "packages" / "specs" / "docs" / "planning" / "2026-01-22-run"
EVAL_REGISTRY_NAME = "eval_registry.yaml"
EVALSETS_REGISTRY_NAME = "evalsets_registry.yaml"


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _load_eval_registry(path: Path) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    current: dict[str, str] | None = None
    for raw in _read_lines(path):
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- eval_id:"):
            eval_id = stripped.split(":", 1)[1].strip()
            current = {"eval_id": eval_id}
            entries[eval_id] = current
            continue
        if current is None:
            continue
        if stripped.startswith("description:"):
            current["description"] = stripped.split(":", 1)[1].strip()
            continue
        if stripped.startswith("runtime_tier:"):
            current["runtime_tier"] = stripped.split(":", 1)[1].strip()
            continue
    return entries


def _load_evalsets_registry(path: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    in_eval_ids = False
    for raw in _read_lines(path):
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- evalset_id:"):
            evalset_id = stripped.split(":", 1)[1].strip()
            current = {"evalset_id": evalset_id, "eval_ids": []}
            entries.append(current)
            in_eval_ids = False
            continue
        if current is None:
            continue
        if stripped.startswith("purpose:"):
            current["purpose"] = stripped.split(":", 1)[1].strip()
            continue
        if stripped.startswith("runtime_tier:"):
            current["runtime_tier"] = stripped.split(":", 1)[1].strip()
            continue
        if stripped.startswith("eval_ids:"):
            in_eval_ids = True
            continue
        if in_eval_ids and stripped.startswith("-"):
            eval_id = stripped.lstrip("-").strip()
            if eval_id:
                current["eval_ids"].append(eval_id)
            continue
        if stripped and not stripped.startswith("-") and in_eval_ids:
            in_eval_ids = False
    return entries


def report_t_gate_status(planning_dir: Path) -> str:
    eval_registry_path = planning_dir / EVAL_REGISTRY_NAME
    evalsets_registry_path = planning_dir / EVALSETS_REGISTRY_NAME

    if not eval_registry_path.exists():
        raise ValueError(f"missing eval registry: {eval_registry_path}")
    if not evalsets_registry_path.exists():
        raise ValueError(f"missing evalsets registry: {evalsets_registry_path}")

    evals = _load_eval_registry(eval_registry_path)
    evalsets = _load_evalsets_registry(evalsets_registry_path)

    lines: list[str] = []
    lines.append("T_Gate status")
    lines.append("")
    lines.append(f"eval_registry: {eval_registry_path}")
    lines.append(f"evalsets_registry: {evalsets_registry_path}")
    lines.append("")
    lines.append("Evalsets:")

    for entry in sorted(evalsets, key=lambda item: str(item.get("evalset_id", ""))):
        evalset_id = str(entry.get("evalset_id", ""))
        tier = str(entry.get("runtime_tier", ""))
        purpose = str(entry.get("purpose", ""))
        eval_ids = sorted(str(item) for item in entry.get("eval_ids", []))
        lines.append(f"- {evalset_id} | {tier} | {purpose} | evals: {', '.join(eval_ids)}")

    lines.append("")
    lines.append("Evals:")
    for eval_id in sorted(evals.keys()):
        entry = evals[eval_id]
        tier = entry.get("runtime_tier", "")
        description = entry.get("description", "")
        lines.append(f"- {eval_id} | {tier} | {description}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Report evalsets/evals status (T_Gate).")
    parser.add_argument(
        "--planning-dir",
        default=str(DEFAULT_PLANNING_DIR),
        help="Planning directory containing eval_registry.yaml",
    )
    args = parser.parse_args()

    try:
        output = report_t_gate_status(Path(args.planning_dir))
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
