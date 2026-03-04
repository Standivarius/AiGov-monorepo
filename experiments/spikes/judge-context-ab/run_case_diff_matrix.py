#!/usr/bin/env python3
"""
Run a focused 3-case A/B matrix across selected models and produce
an explanatory diff report for enriched-vs-generic behavior.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
ONE_CASE_RUNNER = REPO_ROOT / "experiments" / "spikes" / "judge-context-ab" / "run_cal001_context_ab.py"
WORK_DIR = REPO_ROOT / "experiments" / "spikes" / "judge-context-ab" / "work"
OUT_DIR = REPO_ROOT / "experiments" / "spikes" / "autogen-debate-s0" / "data"

MAPPING_PATH = REPO_ROOT / "experiments" / "spikes" / "autogen-debate-s0" / "data" / "calibration_to_gdpr_rules_v1.json"
LEGAL_RULES = REPO_ROOT / "experiments" / "spikes" / "autogen-debate-s0" / "data" / "master_audit_rules_gdpr_v1.json"
PROCEDURAL_RULES = REPO_ROOT / "experiments" / "spikes" / "autogen-debate-s0" / "data" / "master_audit_rules.json"
CROSSWALK = REPO_ROOT / "experiments" / "spikes" / "autogen-debate-s0" / "data" / "gdpr_rule_signal_crosswalk_v1.json"

CASES = [
    "cal_001_lack_of_consent",
    "cal_006_cross_border_transfer",
    "cal_007_automated_decision",
]

MODELS = [
    "mistralai/mistral-large-2512",
    "qwen/qwen3.5-plus-02-15",
    "openai/gpt-5.3-chat",
    "anthropic/claude-opus-4.6",
]


def _model_safe(model_id: str) -> str:
    return model_id.replace("/", "_").replace(":", "_")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _dominant_reason(generic_score: dict[str, Any], enriched_score: dict[str, Any]) -> str:
    if enriched_score["verdict_correct"] < generic_score["verdict_correct"]:
        return "verdict_regression"
    if enriched_score["required_recall"] < generic_score["required_recall"]:
        return "required_signal_miss"
    if enriched_score["signal_precision_allowed"] < generic_score["signal_precision_allowed"]:
        return "signal_precision_drop"
    if enriched_score["citation_recall"] < generic_score["citation_recall"]:
        return "citation_recall_drop"
    if enriched_score["quality_score"] < generic_score["quality_score"]:
        return "mixed_minor_regression"
    return "no_regression_or_improved"


def _run_one(case_id: str, model_id: str) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(ONE_CASE_RUNNER),
        "--case-id",
        case_id,
        "--openrouter-model",
        model_id,
        "--mapping-path",
        str(MAPPING_PATH),
        "--legal-rules-path",
        str(LEGAL_RULES),
        "--procedural-rules-path",
        str(PROCEDURAL_RULES),
        "--crosswalk-path",
        str(CROSSWALK),
    ]
    run = subprocess.run(cmd, capture_output=True, text=True)
    if run.returncode != 0:
        raise RuntimeError(f"{case_id} / {model_id} failed\nSTDOUT:\n{run.stdout}\nSTDERR:\n{run.stderr}")

    result_path = WORK_DIR / f"{case_id}_ab_result.json"
    payload = _load_json(result_path)

    # Persist model-scoped copy to avoid overwrite.
    model_dir = WORK_DIR / "case_diffs" / _model_safe(model_id)
    model_dir.mkdir(parents=True, exist_ok=True)
    case_out = model_dir / f"{case_id}_ab_result.json"
    case_out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload


def main() -> None:
    rows: list[dict[str, Any]] = []
    for model_id in MODELS:
        for case_id in CASES:
            payload = _run_one(case_id=case_id, model_id=model_id)
            g = payload["generic"]["score"]
            e = payload["enriched"]["score"]
            row = {
                "model": model_id,
                "case_id": case_id,
                "delta": float(e["quality_score"] - g["quality_score"]),
                "generic_quality": float(g["quality_score"]),
                "enriched_quality": float(e["quality_score"]),
                "generic_verdict": g["pred_verdict"],
                "enriched_verdict": e["pred_verdict"],
                "expected_verdict": payload["expected"]["verdict"],
                "generic_signals": g["pred_signals"],
                "enriched_signals": e["pred_signals"],
                "expected_required_signals": payload["expected"]["required_signals"],
                "expected_citations": payload["expected"]["gdpr_citations"],
                "generic_citation_recall": float(g["citation_recall"]),
                "enriched_citation_recall": float(e["citation_recall"]),
                "generic_required_recall": float(g["required_recall"]),
                "enriched_required_recall": float(e["required_recall"]),
                "generic_signal_precision_allowed": float(g["signal_precision_allowed"]),
                "enriched_signal_precision_allowed": float(e["signal_precision_allowed"]),
                "rule_count": len(payload.get("edpb_rule_ids", [])),
                "dominant_regression_reason": _dominant_reason(g, e),
                "rules_used": payload.get("edpb_rule_ids", []),
            }
            rows.append(row)

    summary: dict[str, Any] = {"cases": CASES, "models": MODELS, "rows": rows}

    # Model summary over the 3 cases.
    by_model: dict[str, dict[str, Any]] = {}
    for model in MODELS:
        model_rows = [r for r in rows if r["model"] == model]
        avg_delta = sum(r["delta"] for r in model_rows) / len(model_rows)
        reasons: dict[str, int] = {}
        for r in model_rows:
            reasons[r["dominant_regression_reason"]] = reasons.get(r["dominant_regression_reason"], 0) + 1
        by_model[model] = {
            "avg_delta": avg_delta,
            "rows": model_rows,
            "reason_counts": reasons,
        }
    summary["by_model"] = by_model

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_json = OUT_DIR / "gdpr_case_diff_matrix_3cases_4models_v1.json"
    out_md = OUT_DIR / "gdpr_case_diff_matrix_3cases_4models_v1.md"

    out_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    lines: list[str] = []
    lines.append("# GDPR Case Diff Matrix (3 cases x 4 models) v1")
    lines.append("")
    lines.append("Cases: `cal_001`, `cal_006`, `cal_007`")
    lines.append("")
    lines.append("## Model Summary (avg enriched-generic delta)")
    for model in MODELS:
        md = by_model[model]
        lines.append(f"- `{model}`: `{md['avg_delta']:+.3f}` | reasons: `{md['reason_counts']}`")
    lines.append("")
    lines.append("## Per-case rows")
    lines.append("| Model | Case | Delta | GQ | EQ | G Verdict | E Verdict | Dominant Reason | Rules |")
    lines.append("|---|---|---:|---:|---:|---|---|---|---:|")
    for r in rows:
        lines.append(
            f"| {r['model']} | {r['case_id']} | {r['delta']:+.3f} | "
            f"{r['generic_quality']:.3f} | {r['enriched_quality']:.3f} | "
            f"{r['generic_verdict']} | {r['enriched_verdict']} | {r['dominant_regression_reason']} | {r['rule_count']} |"
        )

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OK: wrote {out_json}")
    print(f"OK: wrote {out_md}")


if __name__ == "__main__":
    main()
