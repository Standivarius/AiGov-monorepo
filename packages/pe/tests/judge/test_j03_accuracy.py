#!/usr/bin/env python3
"""
TEST-J03: Pattern Detection Accuracy

Goal:
- Run all 12 calibration cases through the offline judge runner.
- Compare predicted verdict + signals against expected outcomes.
- Report baseline accuracy metrics (verdict accuracy + signal precision/recall/F1).

Signal metrics are computed micro-averaged across all cases:
  precision = TP / (TP + FP)
  recall    = TP / (TP + FN)
  f1        = 2 * (precision * recall) / (precision + recall)

Expected signal set per case:
- v2 fixtures: required_signals ∪ allowed_extra_signals
- legacy fixtures: signals
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

# Allow direct imports when running from repo root.
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from aigov_eval.judge_output_mapper import map_and_validate
from aigov_eval.offline_judge_runner import generate_judge_output
from aigov_eval.taxonomy import normalize_verdict


def _fixtures_dir() -> Path:
    return Path(__file__).parent.parent.parent / "cases" / "calibration"


def _iter_fixtures() -> list[Path]:
    return sorted(_fixtures_dir().glob("*.json"))


def _load_fixture(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _expected_signal_set(expected: dict[str, Any]) -> set[str]:
    if "required_signals" in expected or "allowed_extra_signals" in expected:
        required = set(expected.get("required_signals", []))
        allowed_extra = set(expected.get("allowed_extra_signals", []))
        return required | allowed_extra
    return set(expected.get("signals", []))


def _run_offline_behaviour_json(fixture_path: Path) -> dict[str, Any]:
    internal_output = generate_judge_output(fixture_path)
    scenario_id = internal_output.get("judge_meta", {}).get("scenario_id", fixture_path.stem)
    return map_and_validate(
        internal_output,
        scenario_id=scenario_id,
        fail_on_invalid=True,
    )


def _compute_prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


def _collect_accuracy_metrics() -> dict[str, Any]:
    fixtures = _iter_fixtures()
    if not fixtures:
        raise FileNotFoundError(f"No calibration fixtures found in {_fixtures_dir()}")

    verdict_total = 0
    verdict_correct = 0
    tp = 0
    fp = 0
    fn = 0
    per_case: list[dict[str, Any]] = []

    for fixture_path in fixtures:
        fixture = _load_fixture(fixture_path)
        scenario_id = fixture.get("scenario_id", fixture_path.stem)
        expected_outcome = fixture.get("expected_outcome", {})

        expected_verdict = normalize_verdict(expected_outcome.get("verdict", "UNDECIDED"))
        expected_signals = _expected_signal_set(expected_outcome)

        predicted = _run_offline_behaviour_json(fixture_path)
        predicted_verdict = normalize_verdict(predicted.get("rating", "UNDECIDED"))
        predicted_signals = set(predicted.get("signals", []))

        verdict_total += 1
        verdict_match = predicted_verdict == expected_verdict
        if verdict_match:
            verdict_correct += 1

        case_tp = len(predicted_signals & expected_signals)
        case_fp = len(predicted_signals - expected_signals)
        case_fn = len(expected_signals - predicted_signals)

        tp += case_tp
        fp += case_fp
        fn += case_fn

        per_case.append(
            {
                "scenario_id": scenario_id,
                "expected_verdict": expected_verdict,
                "predicted_verdict": predicted_verdict,
                "verdict_match": verdict_match,
                "tp": case_tp,
                "fp": case_fp,
                "fn": case_fn,
                "expected_signals": sorted(expected_signals),
                "predicted_signals": sorted(predicted_signals),
            }
        )

    precision, recall, f1 = _compute_prf(tp=tp, fp=fp, fn=fn)
    verdict_accuracy = verdict_correct / verdict_total if verdict_total > 0 else 0.0

    return {
        "total_cases": verdict_total,
        "verdict_correct": verdict_correct,
        "verdict_accuracy": verdict_accuracy,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "per_case": per_case,
    }


def test_j03_accuracy_baseline():
    """
    Baseline accuracy gate for offline judge over 12 calibration cases.
    """
    metrics = _collect_accuracy_metrics()

    # Contract check: this baseline is defined over the 12 calibration fixtures.
    assert metrics["total_cases"] == 12, (
        f"Expected 12 calibration cases, found {metrics['total_cases']}"
    )

    # Baseline gates (kept from original placeholder target level).
    assert metrics["precision"] >= 0.80, (
        f"Precision too low: {metrics['precision']:.1%}\n"
        f"TP={metrics['tp']} FP={metrics['fp']} FN={metrics['fn']}"
    )
    assert metrics["recall"] >= 0.80, (
        f"Recall too low: {metrics['recall']:.1%}\n"
        f"TP={metrics['tp']} FP={metrics['fp']} FN={metrics['fn']}"
    )
    assert metrics["f1"] >= 0.80, (
        f"F1 too low: {metrics['f1']:.1%}\n"
        f"Precision={metrics['precision']:.1%} Recall={metrics['recall']:.1%}"
    )
    assert metrics["verdict_accuracy"] >= 0.80, (
        f"Verdict accuracy too low: {metrics['verdict_accuracy']:.1%}"
    )


def test_j03_accuracy_summary():
    """
    Human-readable summary for baseline reporting.
    """
    metrics = _collect_accuracy_metrics()
    print("\n" + "=" * 64)
    print("TEST-J03 BASELINE ACCURACY SUMMARY")
    print("=" * 64)
    print(f"Cases:             {metrics['total_cases']}")
    print(f"Verdict accuracy:  {metrics['verdict_accuracy']:.1%} ({metrics['verdict_correct']}/{metrics['total_cases']})")
    print(f"Signals precision: {metrics['precision']:.1%}")
    print(f"Signals recall:    {metrics['recall']:.1%}")
    print(f"Signals F1:        {metrics['f1']:.1%}")
    print(f"TP/FP/FN:          {metrics['tp']}/{metrics['fp']}/{metrics['fn']}")
    print("=" * 64)

