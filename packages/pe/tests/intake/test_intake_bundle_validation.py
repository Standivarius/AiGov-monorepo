from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "tools"))

from validate_intake_bundle_v0_1 import validate_intake_bundle_fixture


PASS_FIXTURE = REPO_ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_pass.json"
FAIL_FIXTURE = (
    REPO_ROOT / "tools" / "fixtures" / "validators" / "intake_bundle_v0_1_fail_missing_required.json"
)


def test_intake_bundle_v0_1_pass_fixture() -> None:
    errors = validate_intake_bundle_fixture(PASS_FIXTURE)
    assert errors == []


def test_intake_bundle_v0_1_fail_fixture() -> None:
    errors = validate_intake_bundle_fixture(FAIL_FIXTURE)
    assert errors
    assert any("missing required key" in error for error in errors)
