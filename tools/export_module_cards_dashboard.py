#!/usr/bin/env python3
"""Export module cards into a deterministic human-facing dashboard markdown."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "packages" / "specs" / "docs" / "contracts" / "modules" / "module_registry_v0.yaml"
CARDS_DIR = ROOT / "packages" / "specs" / "docs" / "contracts" / "modules" / "cards"
DEFAULT_OUTPUT_PATH = ROOT / "packages" / "specs" / "docs" / "contracts" / "modules" / "M_Dashboard.md"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _ensure_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _load_registry(path: Path) -> list[str]:
    if not path.exists():
        raise ValueError(f"registry missing: {path}")
    module_ids: list[str] = []
    in_modules = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("modules:"):
            in_modules = True
            continue
        if line.startswith("registries:"):
            in_modules = False
            continue
        if in_modules and line.startswith("- module_id:"):
            module_id = line.split(":", 1)[1].strip()
            if module_id:
                module_ids.append(module_id)
    if not module_ids:
        raise ValueError("registry contains no module_id entries")
    return module_ids


def _load_cards(cards_dir: Path) -> dict[str, dict[str, Any]]:
    if not cards_dir.exists():
        raise ValueError(f"cards directory missing: {cards_dir}")
    cards: dict[str, dict[str, Any]] = {}
    card_paths = sorted(cards_dir.glob("*.card.json"))
    if not card_paths:
        raise ValueError(f"no module cards found in {cards_dir}")
    for path in card_paths:
        card = _ensure_dict(_load_json(path), str(path))
        module_id = card.get("module_id")
        if not isinstance(module_id, str) or not module_id:
            raise ValueError(f"{path}: module_id must be a non-empty string")
        cards[module_id] = card
    return cards


def _format_default(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def render_dashboard(module_ids: list[str], cards: dict[str, dict[str, Any]]) -> str:
    missing = sorted(module_id for module_id in module_ids if module_id not in cards)
    if missing:
        raise ValueError(f"missing module cards for: {missing}")

    lines: list[str] = [
        "# Module Dashboard (v0.1.0)",
        "",
        "Purpose: Human-facing run-configuration checklist generated from module cards.",
        "",
    ]

    for module_id in sorted(module_ids):
        card = cards[module_id]
        summary = card.get("summary")
        if not isinstance(summary, str) or not summary:
            raise ValueError(f"{module_id}: summary must be a non-empty string")
        knobs = card.get("knobs")
        if not isinstance(knobs, list):
            raise ValueError(f"{module_id}: knobs must be an array")

        lines.append(f"## {module_id}")
        lines.append("")
        lines.append(summary)
        lines.append("")
        lines.append("### Knobs")

        if not knobs:
            lines.append("- None.")
        else:
            for knob in sorted(knobs, key=lambda item: str(item.get("id", ""))):
                knob_id = knob.get("id")
                value_type = knob.get("value_type")
                required = knob.get("required")
                description = knob.get("description")
                if not isinstance(knob_id, str) or not knob_id:
                    raise ValueError(f"{module_id}: knob id must be a non-empty string")
                if not isinstance(value_type, str) or not value_type:
                    raise ValueError(f"{module_id}:{knob_id}: value_type must be a string")
                if not isinstance(required, bool):
                    raise ValueError(f"{module_id}:{knob_id}: required must be boolean")
                if not isinstance(description, str) or not description:
                    raise ValueError(f"{module_id}:{knob_id}: description must be a non-empty string")
                required_label = "required" if required else "optional"
                default_text = ""
                if "default" in knob:
                    default_text = f"; default={_format_default(knob['default'])}"
                lines.append(
                    f"- `{knob_id}` ({value_type}, {required_label}{default_text}) — {description}"
                )

        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Export module dashboard markdown from module cards.")
    parser.add_argument("--out", default=str(DEFAULT_OUTPUT_PATH), help="Output markdown path")
    args = parser.parse_args()

    try:
        module_ids = _load_registry(REGISTRY_PATH)
        cards = _load_cards(CARDS_DIR)
        content = render_dashboard(module_ids, cards)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    output_path = Path(args.out)
    output_path.write_text(content, encoding="utf-8")
    print(f"PASS: wrote module dashboard to {output_path}")
    return 0


if __name__ == "__main__":
    main()
