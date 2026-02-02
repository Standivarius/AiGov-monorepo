# Inspect + Petri Audit Harness Module Card

## Header
- **Module ID**: inspect_petri_audit
- **Module Name**: Inspect + Petri Audit Harness
- **Version**: 0.1.0
- **Owner**: eval-harness
- **Status**: alpha
- **Last Updated**: 2026-02-02

## Purpose
Provide a deterministic, repeatable audit harness for GDPR scenario probes using Inspect + Petri.

## Scope
- **In-scope**:
  - Running Petri audits via Inspect CLI
  - Passing seed instructions via task args
- **Out-of-scope**:
  - Scenario generation
  - Report generation

## Inputs
- **Input Artifacts**:
  - Seed instructions (string or list) passed via task args
- **Preconditions**:
  - Inspect and Petri installed

## Outputs
- **Output Artifacts**:
  - Inspect logs under `./logs/aigov/`
  - Petri transcripts under `./outputs/`
- **Determinism**:
  - Deterministic behavior depends on fixed inputs and deterministic seed instructions.

## Interfaces
- **CLI**:
  - Exact example command:

```bash
inspect eval petri/audit \
  --model-role auditor=anthropic/claude-sonnet-4-20250514 \
  --model-role target=openai/gpt-4o-mini \
  --model-role judge=google/gemini-2.0-flash \
  --log-format=json \
  --log-dir="./logs/aigov" \
  -T max_turns=20 \
  -T seed_instructions="$(python load_scenario.py GDPR-007)" \
  -T transcript_save_dir="./outputs"
```

- **Task args**:
  - Task args are passed via `-T` and Inspect also supports `--task-config`.

## Failure Modes
- Missing task args or malformed seed instructions (Inspect CLI).
- Petri task arg mismatch or unsupported args (Petri task layer).

## Verification
- **Canonical Checks**:
  - `python3 tools/validate_planning_pack.py`

## Notes
- Keep seed instructions deterministic and GDPR-only.
