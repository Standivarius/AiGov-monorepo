# GDPR-only MVP — Milestone 1 summary (through GDPR-203)

## What we shipped
- Deterministic PR-gate workflow in CI
- Base scenario library coverage now includes GDPR-001..GDPR-203
- SOURCES.md traceability approach (URLs may be missing by convention; no new domains unless explicitly allowed)

## What “done” means for this milestone
- GDPR-only scenario library is complete through GDPR-203 with deterministic, schema-valid JSON
- Traceability entries exist in SOURCES.md for every GDPR-001..GDPR-203 scenario
- PR-gate validators and migration smoke pass on the branch
- No non-GDPR scenarios or scope changes introduced

## Canonical PR-gate commands
- python3 tools/validate_planning_pack.py
- bash tools/run_pr_gate_validators.sh
- NX_DAEMON=false npx nx run evalsets:migration-smoke

## MVP scope statement
GDPR-only. Any non-GDPR work is out of scope.

## Next milestone options
1) Sourcing backlog focused on children/minors enforcement cases (within existing allowed domains)
2) Next tranche PR: GDPR-204..253 once an authoritative case list is available
