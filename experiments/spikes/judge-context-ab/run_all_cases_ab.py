#!/usr/bin/env python3
"""
Run generic vs enriched Judge prompt A/B for all 12 calibration cases.

Outputs:
- work/full12_ab_summary__<model_safe>.json
- work/full12_ab_summary__<model_safe>.md
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
CALIBRATION_DIR = REPO_ROOT / "packages" / "pe" / "cases" / "calibration"
ONE_CASE_RUNNER = REPO_ROOT / "experiments" / "spikes" / "judge-context-ab" / "run_cal001_context_ab.py"
WORK_DIR = REPO_ROOT / "experiments" / "spikes" / "judge-context-ab" / "work"


def _model_safe_name(model_id: str) -> str:
    return model_id.replace("/", "_").replace(":", "_")


def _collect_case_ids() -> list[str]:
    return sorted([p.stem for p in CALIBRATION_DIR.glob("*.json")])


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _run_case(case_id: str, model_id: str) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(ONE_CASE_RUNNER),
        "--case-id",
        case_id,
        "--openrouter-model",
        model_id,
    ]
    run = subprocess.run(cmd, capture_output=True, text=True)
    if run.returncode != 0:
        raise RuntimeError(
            f"Case {case_id} failed.\nSTDOUT:\n{run.stdout}\nSTDERR:\n{run.stderr}"
        )

    result_path = WORK_DIR / f"{case_id}_ab_result.json"
    if not result_path.exists():
        raise FileNotFoundError(f"Missing expected result file: {result_path}")
    return _load_json(result_path)


def _to_row(payload: dict[str, Any]) -> dict[str, Any]:
    generic = payload["generic"]["score"]
    enriched = payload["enriched"]["score"]
    return {
        "case_id": payload["case_id"],
        "generic_quality": float(generic["quality_score"]),
        "enriched_quality": float(enriched["quality_score"]),
        "delta": float(enriched["quality_score"] - generic["quality_score"]),
        "generic_verdict": generic["pred_verdict"],
        "enriched_verdict": enriched["pred_verdict"],
        "generic_citation_recall": float(generic["citation_recall"]),
        "enriched_citation_recall": float(enriched["citation_recall"]),
    }


def _write_outputs(model_id: str, rows: list[dict[str, Any]]) -> tuple[Path, Path]:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    model_safe = _model_safe_name(model_id)
    json_path = WORK_DIR / f"full12_ab_summary__{model_safe}.json"
    md_path = WORK_DIR / f"full12_ab_summary__{model_safe}.md"

    avg_generic = sum(r["generic_quality"] for r in rows) / len(rows)
    avg_enriched = sum(r["enriched_quality"] for r in rows) / len(rows)
    avg_delta = avg_enriched - avg_generic

    summary = {
        "model": model_id,
        "total_cases": len(rows),
        "avg_generic_quality": avg_generic,
        "avg_enriched_quality": avg_enriched,
        "avg_delta": avg_delta,
        "rows": rows,
    }
    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = []
    lines.append(f"# Full 12-case A/B summary ({model_id})")
    lines.append("")
    lines.append(f"- Cases: {len(rows)}")
    lines.append(f"- Avg generic quality: {avg_generic:.3f}")
    lines.append(f"- Avg enriched quality: {avg_enriched:.3f}")
    lines.append(f"- Avg delta (enriched-generic): {avg_delta:+.3f}")
    lines.append("")
    lines.append("| Case | Generic | Enriched | Delta | Generic Citation Recall | Enriched Citation Recall |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for r in rows:
        lines.append(
            f"| {r['case_id']} | {r['generic_quality']:.3f} | {r['enriched_quality']:.3f} | {r['delta']:+.3f} | "
            f"{r['generic_citation_recall']:.3f} | {r['enriched_citation_recall']:.3f} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--openrouter-model",
        default="mistralai/mistral-large-2512",
        help="OpenRouter model ID for all runs.",
    )
    args = parser.parse_args()

    case_ids = _collect_case_ids()
    print(f"Running {len(case_ids)} cases with model={args.openrouter_model}")
    rows = []
    for i, case_id in enumerate(case_ids, start=1):
        print(f"[{i}/{len(case_ids)}] {case_id}")
        payload = _run_case(case_id=case_id, model_id=args.openrouter_model)
        rows.append(_to_row(payload))

    json_path, md_path = _write_outputs(model_id=args.openrouter_model, rows=rows)
    print(f"OK: wrote {json_path}")
    print(f"OK: wrote {md_path}")


if __name__ == "__main__":
    main()

