#!/usr/bin/env python3
"""Run deterministic intake export adapter v0.1 (tools-only)."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

GITHUB_EXPORT_TOP_LEVEL_DIRS = ("repo", "issues", "pull_requests", "comments")


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


def _detect_source_type(export_root: Path) -> str:
    top_level_entries = sorted(
        [entry.name for entry in export_root.iterdir()],
    )
    github_expected = set(GITHUB_EXPORT_TOP_LEVEL_DIRS)
    github_seen = github_expected.intersection(top_level_entries)

    if not github_seen:
        return "file_export"

    extra = sorted(name for name in top_level_entries if name not in github_expected)
    missing = sorted(name for name in github_expected if name not in top_level_entries)
    if extra or missing:
        raise ValueError(
            "github export pack top-level entries must be exactly "
            "repo/, issues/, pull_requests/, comments/"
        )

    for dirname in GITHUB_EXPORT_TOP_LEVEL_DIRS:
        dir_path = export_root / dirname
        if dir_path.is_symlink():
            raise ValueError(
                f"github export pack top-level entry must not be a symlink: {dirname}"
            )
        if not dir_path.is_dir():
            raise ValueError(
                "github export pack top-level entry must be a directory: "
                f"{dirname}"
            )
    return "github_export_pack"


def _load_json_object_for_path(path: Path, rel_path: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"github export pack JSON parse error in {rel_path}: {exc.msg}"
        ) from exc
    if not isinstance(payload, dict):
        raise ValueError(f"github export pack file must be a JSON object: {rel_path}")
    return payload


def _validate_github_export_pack(root: Path, source_files: list[dict[str, str]]) -> None:
    if not source_files:
        raise ValueError("github export pack contains no regular files")

    seen_paths: set[str] = set()
    has_issue = False
    has_pr = False
    has_comment = False

    for entry in source_files:
        rel_path = entry.get("source_path")
        if not isinstance(rel_path, str) or not rel_path:
            raise ValueError("github export pack source_path must be a non-empty string")
        seen_paths.add(rel_path)

        rel = Path(rel_path)
        if len(rel.parts) < 2:
            raise ValueError(
                "github export pack files must be under repo/, issues/, "
                f"pull_requests/, or comments/: {rel_path}"
            )
        top = rel.parts[0]
        if top not in GITHUB_EXPORT_TOP_LEVEL_DIRS:
            raise ValueError(f"github export pack has unsupported top-level path: {rel_path}")
        if rel.suffix.lower() != ".json":
            raise ValueError(f"github export pack only supports .json files: {rel_path}")
        if len(rel.parts) != 2:
            raise ValueError(
                "github export pack nested paths are not supported in v0.1: "
                f"{rel_path}"
            )

        file_path = root / rel_path
        _load_json_object_for_path(file_path, rel_path)

        if top == "issues":
            has_issue = True
        elif top == "pull_requests":
            has_pr = True
        elif top == "comments":
            has_comment = True
        elif rel_path != "repo/metadata.json":
            raise ValueError(
                "github export pack repo directory only allows metadata.json: "
                f"{rel_path}"
            )

    if "repo/metadata.json" not in seen_paths:
        raise ValueError("github export pack missing required file: repo/metadata.json")
    if not has_issue:
        raise ValueError("github export pack requires at least one issues/*.json file")
    if not has_pr:
        raise ValueError("github export pack requires at least one pull_requests/*.json file")
    if not has_comment:
        raise ValueError("github export pack requires at least one comments/*.json file")


def build_source_snapshot(export_dir: Path) -> dict[str, Any]:
    root = export_dir.resolve(strict=True)
    source_type = _detect_source_type(root)
    source_files = _collect_source_files(export_dir)
    if source_type == "github_export_pack":
        _validate_github_export_pack(root, source_files)
    return {
        "schema_version": "intake_source_snapshot_v0_1",
        "snapshot_id": _snapshot_id(source_files),
        "source_type": source_type,
        "source_files": source_files,
    }


def emit_source_snapshot(export_dir: Path, snapshot_out: Path) -> dict[str, Any]:
    snapshot = build_source_snapshot(export_dir)
    write_canonical_json(snapshot_out, snapshot)
    return snapshot


def _canonical_value_string(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _value_kind(value: Any) -> str:
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    return "scalar"


def _load_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON export file {path}: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"export JSON file must be an object: {path}")
    return payload


def build_extract_bundle(
    export_dir: Path,
    snapshot: dict[str, Any],
    *,
    bundle_id: str | None = None,
) -> dict[str, Any]:
    source_files = snapshot.get("source_files")
    snapshot_id = snapshot.get("snapshot_id")
    source_type = snapshot.get("source_type")
    if not isinstance(source_files, list) or not isinstance(snapshot_id, str) or not snapshot_id:
        raise ValueError("snapshot payload missing source_files or snapshot_id")
    if source_type not in {"file_export", "github_export_pack"}:
        raise ValueError("snapshot payload has unsupported source_type for extract adapter")

    root = export_dir.resolve(strict=True)
    candidates: dict[str, dict[str, Any]] = {}

    mapping = [
        ("context_profile", "jurisdiction", "intake.context_profile.jurisdiction"),
        ("context_profile", "sector", "intake.context_profile.sector"),
        ("policy_profile", "retention_days", "intake.policy_profile.retention_days"),
    ]

    def _merge_candidate(field_path: str, raw_value: Any, evidence_ref: str) -> None:
        value = _canonical_value_string(raw_value)
        value_kind = _value_kind(raw_value)

        if field_path in candidates:
            existing = candidates[field_path]
            if existing["value"] != value:
                raise ValueError(
                    "conflicting values for extracted field "
                    f"{field_path!r} from multiple source files"
                )
            refs = set(existing["evidence_refs"])
            refs.add(evidence_ref)
            existing["evidence_refs"] = sorted(refs)
            return

        candidates[field_path] = {
            "field_path": field_path,
            "value": value,
            "value_kind": value_kind,
            "evidence_refs": [evidence_ref],
        }

    for index, entry in enumerate(source_files):
        if not isinstance(entry, dict):
            continue
        source_path = entry.get("source_path")
        if not isinstance(source_path, str) or not source_path:
            continue
        evidence_ref = f"EV-{index + 1:03d}"

        source_file_path = (root / source_path).resolve(strict=True)
        try:
            source_file_path.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"source file escapes export root: {source_path}") from exc

        if source_file_path.suffix.lower() != ".json":
            if source_type == "github_export_pack":
                raise ValueError(f"github export pack only supports .json files: {source_path}")
            continue

        if source_type == "github_export_pack":
            payload = _load_json_object_for_path(source_file_path, source_path)
        else:
            payload = _load_json_object(source_file_path)

        if source_type == "github_export_pack":
            top = Path(source_path).parts[0] if Path(source_path).parts else ""
            if top == "repo":
                jurisdiction = payload.get("jurisdiction")
                if isinstance(jurisdiction, str) and jurisdiction:
                    _merge_candidate(
                        "intake.context_profile.jurisdiction",
                        jurisdiction.upper(),
                        evidence_ref,
                    )
                sector = payload.get("sector")
                if isinstance(sector, str) and sector:
                    _merge_candidate(
                        "intake.context_profile.sector",
                        sector.lower(),
                        evidence_ref,
                    )
                retention_days = payload.get("retention_days")
                if (
                    isinstance(retention_days, (int, float, str))
                    and not isinstance(retention_days, bool)
                ):
                    _merge_candidate(
                        "intake.policy_profile.retention_days",
                        str(retention_days),
                        evidence_ref,
                    )
                continue

            text_parts: list[str] = []
            for key in ("title", "body", "comment", "description"):
                value = payload.get(key)
                if isinstance(value, str) and value:
                    text_parts.append(value)

            labels = payload.get("labels")
            if isinstance(labels, list):
                for label in labels:
                    if isinstance(label, str) and label:
                        text_parts.append(label)

            normalized = " ".join(text_parts).lower()
            if normalized:
                if " nl " in f" {normalized} ":
                    _merge_candidate(
                        "intake.context_profile.jurisdiction",
                        "NL",
                        evidence_ref,
                    )
                if "public-sector" in normalized or "public sector" in normalized:
                    _merge_candidate(
                        "intake.context_profile.sector",
                        "public",
                        evidence_ref,
                    )

                retention_match = re.search(r"\b(\d+)\s+days?\b", normalized)
                if retention_match:
                    _merge_candidate(
                        "intake.policy_profile.retention_days",
                        retention_match.group(1),
                        evidence_ref,
                    )
            continue

        for section, key, field_path in mapping:
            section_payload = payload.get(section)
            if not isinstance(section_payload, dict) or key not in section_payload:
                continue

            raw_value = section_payload[key]
            _merge_candidate(field_path, raw_value, evidence_ref)

    extracted_fields = sorted(candidates.values(), key=lambda item: item["field_path"])
    if not extracted_fields:
        raise ValueError("no extractable fields found in export payloads")

    final_bundle_id = bundle_id or f"bundle-{snapshot_id}"
    return {
        "schema_version": "intake_bundle_extract_v0_1",
        "bundle_id": final_bundle_id,
        "source_snapshot_id": snapshot_id,
        "extracted_fields": extracted_fields,
    }


def emit_snapshot_and_extract(
    export_dir: Path,
    snapshot_out: Path,
    extract_out: Path,
    *,
    bundle_id: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    snapshot = build_source_snapshot(export_dir)
    extract = build_extract_bundle(export_dir, snapshot, bundle_id=bundle_id)
    write_canonical_json(snapshot_out, snapshot)
    write_canonical_json(extract_out, extract)
    return snapshot, extract


def main() -> int:
    parser = argparse.ArgumentParser(description="Run intake export file adapter v0.1")
    parser.add_argument("--export-dir", required=True, help="Path to file export directory")
    parser.add_argument("--snapshot-out", required=True, help="Path to output source snapshot JSON")
    parser.add_argument(
        "--extract-out",
        help="Optional path to output extract JSON (when omitted, snapshot-only mode is used)",
    )
    parser.add_argument("--bundle-id", help="Optional bundle_id override for extract output")
    args = parser.parse_args()

    export_dir = Path(args.export_dir)
    snapshot_out = Path(args.snapshot_out)

    try:
        if args.extract_out:
            snapshot, extract = emit_snapshot_and_extract(
                export_dir,
                snapshot_out,
                Path(args.extract_out),
                bundle_id=args.bundle_id,
            )
            print(
                "PASS: intake export adapter emitted snapshot+extract "
                f"(snapshot_id={snapshot['snapshot_id']}, bundle_id={extract['bundle_id']})"
            )
            return 0

        snapshot = emit_source_snapshot(export_dir, snapshot_out)
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
