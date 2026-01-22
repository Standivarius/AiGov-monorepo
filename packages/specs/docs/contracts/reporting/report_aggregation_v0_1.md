# Report Aggregation Contract v0.1

Defines aggregation rules for report generation. Fail-closed by default.

## Canonical references
- Report fields: `packages/specs/docs/contracts/reporting/report_fields_v0_1.md`
- Crosswalk: `packages/specs/docs/contracts/reporting/report_fields_crosswalk_v0_1.md`
- Limitations log: `packages/specs/docs/contracts/reporting/artifact_registry_v0_1.md`

## Rules (fail-closed)
- If any required field cannot be verified, aggregation MUST fail closed.
- Fail-closed means: the field is omitted from the output and a limitations_log
  entry is emitted describing the missing evidence or unmet verification mode.
- Aggregators MUST NOT infer compliance in the absence of required evidence.

## Good looks like
- Missing evidence yields an explicit limitations_log entry.

## Bad looks like
- Aggregation proceeds with default values when evidence is missing.

## How to decide
- If a field cannot be substantiated, treat it as a limitation and fail closed.
