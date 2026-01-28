# GDPR-only MVP — Milestone 1 summary (through GDPR-253)

- MVP scope is GDPR-only. Non-GDPR work is out of scope.

## What’s complete
- Scenario library coverage: GDPR-001..GDPR-253
  - packages/specs/scenarios/library/base/gdpr/
  - packages/specs/scenarios/library/base/gdpr/SOURCES.md
- Deterministic maintainability tooling:
  - tools/report_gdpr_library_status.py
    - checks: ID gaps, role/surface/signal counts, SOURCES heading match, missing URL count + domain histogram, population children/general counts

## Canonical PR-gate commands
- python3 tools/validate_planning_pack.py
- bash tools/run_pr_gate_validators.sh
- NX_DAEMON=false npx nx run evalsets:migration-smoke

## How to run the report locally
- python3 tools/report_gdpr_library_status.py

## Next milestone options (GDPR-only)
- Backlog sourcing focused on children/minors enforcement cases (existing allowed domains only).
- Next tranche PR: GDPR-254..GDPR-303 once an authoritative case list is available.
- Coverage hardening for underrepresented roles/surfaces in GDPR scenarios.
