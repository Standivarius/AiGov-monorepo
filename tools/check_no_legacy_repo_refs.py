#!/usr/bin/env python3
"""
Fail if legacy repo names appear in tracked text files, with an allowlist for docs/migration/.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


LEGACY_TOKENS = ("AiGov-specs", "AiGov-mvp", "Aigov-eval")
ALLOWLIST_PREFIX = "docs/migration/"
TEXT_EXTENSIONS = {".md", ".py", ".yml", ".yaml", ".json", ".toml"}


def iter_tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git ls-files failed: {result.stderr.strip()}")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def scan_file(path: Path) -> dict[str, list[int]]:
    hits: dict[str, list[int]] = {token: [] for token in LEGACY_TOKENS}
    try:
        contents = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        raise RuntimeError(f"Failed to read {path}: {exc}") from exc
    for idx, line in enumerate(contents, start=1):
        for token in LEGACY_TOKENS:
            if token in line:
                hits[token].append(idx)
    return {token: lines for token, lines in hits.items() if lines}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Fail if legacy repo names appear outside docs/migration/.",
    )
    parser.add_argument(
        "--help-only",
        action="store_true",
        help="Print help and exit 0.",
    )
    args, unknown = parser.parse_known_args(argv)
    if args.help_only:
        parser.print_help()
        return 0
    if unknown:
        parser.error(f"unknown arguments: {' '.join(unknown)}")

    failures = []
    for rel in iter_tracked_files():
        if rel.startswith(ALLOWLIST_PREFIX):
            continue
        if Path(rel).suffix not in TEXT_EXTENSIONS:
            continue
        hit_map = scan_file(Path(rel))
        for token, lines in hit_map.items():
            failures.append((rel, token, lines))

    if failures:
        print("Legacy repo references detected:", file=sys.stderr)
        for rel, token, lines in failures:
            line_list = ", ".join(str(n) for n in lines)
            print(f"- {rel}: {token} (lines {line_list})", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
