#!/usr/bin/env python3
"""Run deterministic intake export adapter v0.1 (tools-only)."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any


def canonical_json_bytes(payload: Any) -> bytes:
    return (
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
    ).encode("utf-8")


def write_canonical_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(payload))


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _guess_content_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "application/json"
    if suffix in {".md", ".txt"}:
        return "text/plain"
    return "application/octet-stream"


def _collect_source_files(export_dir: Path) -> list[dict[str, str]]:
    if not export_dir.exists():
        raise ValueError(f"export directory not found: {export_dir}")
    if not export_dir.is_dir():
        raise ValueError(f"export path must be a directory: {export_dir}")
    if export_dir.is_symlink():
        raise ValueError(f"export directory must not be a symlink: {export_dir}")

    root = export_dir.resolve(strict=True)
    source_files: list[dict[str, str]] = []

    for current_root, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        dirnames.sort()
        filenames.sort()
        current_path = Path(current_root)

        for dirname in dirnames:
            dir_path = current_path / dirname
            if dir_path.is_symlink():
                rel = dir_path.relative_to(root).as_posix()
                raise ValueError(f"symlink entry not allowed: {rel}")

        for filename in filenames:
            file_path = current_path / filename
            if file_path.is_symlink():
                rel = file_path.relative_to(root).as_posix()
                raise ValueError(f"symlink entry not allowed: {rel}")

            resolved = file_path.resolve(strict=True)
            try:
                resolved.relative_to(root)
            except ValueError as exc:
                raise ValueError(f"source path escapes export root: {file_path}") from exc

            rel_path = resolved.relative_to(root)
            source_files.append(
                {
                    "source_path": rel_path.as_posix(),
                    "sha256": _sha256_file(resolved),
                    "content_type": _guess_content_type(rel_path),
                }
            )

    source_files.sort(key=lambda item: item["source_path"])
    if not source_files:
        raise ValueError("export directory contains no regular files")

    return source_files


def _snapshot_id(source_files: list[dict[str, str]]) -> str:
    inventory = [
        {"source_path": item["source_path"], "sha256": item["sha256"]}
        for item in source_files
    ]
    digest = hashlib.sha256(canonical_json_bytes(inventory)).hexdigest()
    return f"snapshot-{digest[:16]}"


def build_source_snapshot(export_dir: Path) -> dict[str, Any]:
    source_files = _collect_source_files(export_dir)
    snapshot = {
        "schema_version": "intake_source_snapshot_v0_1",
        "snapshot_id": _snapshot_id(source_files),
        "source_type": "file_export",
        "source_files": source_files,
    }
    return snapshot


def emit_source_snapshot(export_dir: Path, snapshot_out: Path) -> dict[str, Any]:
    snapshot = build_source_snapshot(export_dir)
    write_canonical_json(snapshot_out, snapshot)
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Run intake export file adapter v0.1")
    parser.add_argument("--export-dir", required=True, help="Path to file export directory")
    parser.add_argument("--snapshot-out", required=True, help="Path to output source snapshot JSON")
    args = parser.parse_args()

    try:
        snapshot = emit_source_snapshot(Path(args.export_dir), Path(args.snapshot_out))
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    print(
        "PASS: intake export adapter emitted source snapshot "
        f"{args.snapshot_out} (snapshot_id={snapshot['snapshot_id']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
