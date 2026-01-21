#!/usr/bin/env python3
"""Fail if forbidden L-layer mappings appear in docs (with allowlist)."""
from __future__ import annotations

import sys
from pathlib import Path


FORBIDDEN_PATTERNS = [
    "L2 (CISO",
    "L3 (CCO",
    "L2 = CISO",
    "L3 = CCO",
    "L2 is for the CISO",
    "L3 is for the CCO",
    "L2:CISO",
    "L3:CCO",
]

EXCLUDED_PREFIXES = [
    "packages/specs/docs/artifacts/",
]

EXCLUDED_FILES = {
    "packages/specs/docs/contracts/taxonomy/pre2.2/Pre2.2-TAXONOMY-Pro-Run.md",
}


def is_excluded(rel_path: str) -> bool:
    if rel_path in EXCLUDED_FILES:
        return True
    return any(rel_path.startswith(prefix) for prefix in EXCLUDED_PREFIXES)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    base_dir = repo_root / "packages" / "specs" / "docs"
    if not base_dir.exists():
        print(f"ERROR: base docs directory not found: {base_dir}")
        return 1

    matches: list[str] = []
    for path in base_dir.rglob("*"):
        if not path.is_file():
            continue
        rel_path = path.relative_to(repo_root).as_posix()
        if is_excluded(rel_path):
            continue
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as handle:
                for idx, line in enumerate(handle, start=1):
                    for pattern in FORBIDDEN_PATTERNS:
                        if pattern in line:
                            matches.append(
                                f"{rel_path}:{idx}: {pattern} | {line.strip()}"
                            )
        except OSError as exc:
            matches.append(f"{rel_path}:0: ERROR opening file: {exc}")

    if matches:
        print("FAIL: forbidden report-layer mappings found:")
        for entry in matches:
            print(entry)
        return 1

    print("PASS: no forbidden report-layer mappings found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
