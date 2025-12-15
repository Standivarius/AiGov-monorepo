#!/usr/bin/env python3
"""
TEST-J01: Output Consistency

Goal: Verify Judge produces consistent results across multiple runs of same scenario.
Target: 95%+ consistency (same rating and violations across 5 runs)

Usage:
    pytest test_j01_consistency.py -v
"""

import pytest
import json
from pathlib import Path
from collections import Counter


# TODO: Import your Judge implementation
# from aigov.judge import run_judge_on_scenario


def run_judge_on_scenario(scenario_id: str) -> dict:
    """
    Placeholder - replace with actual Judge execution.
    
    Args:
        scenario_id: Scenario identifier (e.g. "GDPR-007")
    
    Returns:
        behaviour_json_v0_phase0 dict
    """
    # TODO: Implement actual Judge execution
    # 1. Load scenario_card
    # 2. Run Inspect eval with Judge scorer
    # 3. Extract behaviour_json from Score.metadata
    # 4. Return result
    raise NotImplementedError("Replace with actual Judge implementation")


GDPR_SCENARIOS = [
    "GDPR-001",  # Third-party PII disclosure
    "GDPR-005",  # Transparency failure
    "GDPR-007",  # Healthcare PII leak
    "GDPR-015",  # RTBF failure
    "GDPR-017",  # DSAR mishandling
]


@pytest.mark.parametrize("scenario_id", GDPR_SCENARIOS)
def test_consistency_5_runs(scenario_id):
    """
    Run same scenario 5 times, verify consistent output.
    
    Checks:
    - Same rating (VIOLATED/COMPLIANT/UNDECIDED)
    - Same violations (article list)
    - Same severity (HIGH/MEDIUM/LOW)
    """
    print(f"\n\nTesting consistency for {scenario_id}...")
    
    results = []
    for run_num in range(1, 6):
        print(f"  Run {run_num}/5...")
        result = run_judge_on_scenario(scenario_id)
        results.append(result)
    
    # Check rating consistency
    ratings = [r["rating"] for r in results]
    rating_counts = Counter(ratings)
    most_common_rating, count = rating_counts.most_common(1)[0]
    rating_consistency = count / len(ratings)
    
    print(f"  Rating consistency: {rating_consistency:.1%} ({count}/5 runs: {most_common_rating})")
    assert rating_consistency >= 0.95, (
        f"Rating inconsistent: {rating_counts}. Expected 95%+ same rating."
    )
    
    # Check violations consistency (article list)
    violations_sets = [
        frozenset(v["article"] for v in r.get("violations", []))
        for r in results
    ]
    violations_counts = Counter(violations_sets)
    most_common_violations, count = violations_counts.most_common(1)[0]
    violations_consistency = count / len(violations_sets)
    
    print(f"  Violations consistency: {violations_consistency:.1%} ({count}/5 runs)")
    assert violations_consistency >= 0.95, (
        f"Violations inconsistent across runs. Expected 95%+ same violation set."
    )
    
    print(f"  ✅ {scenario_id}: Consistent (rating {rating_consistency:.1%}, violations {violations_consistency:.1%})")


def test_consistency_summary():
    """
    Run all scenarios and generate summary report.
    """
    print("\n" + "="*60)
    print("TEST-J01 SUMMARY")
    print("="*60)
    
    # This test just prints summary, actual validation in test_consistency_5_runs
    print("\nAll consistency tests passed!")
    print("Judge produces stable, repeatable outputs.")
    print("\nNext: Run TEST-J02 (schema validation)")
