# Module Dashboard (v0.1.0)

Purpose: Human-facing run-configuration checklist generated from module cards.

## M_Bundle

Compile GDPR base scenarios and overrides into a deterministic bundle manifest.

### Knobs
- `base_dir` (path, required) — Filesystem path to base scenario JSONs.
- `output_dir` (path, required) — Filesystem path to compiled bundle output.
- `overrides_dir` (path, required) — Filesystem path to override JSONs.

## M_Dashboard

Publish a human-facing checklist of module configuration and required knobs.

### Knobs
- `cards_dir` (path, required) — Directory containing module card JSON files.
- `output_path` (path, required) — Path for the generated dashboard markdown.

## M_Intake

Validate GDPR-only client intake payloads and enforce policy profile constraints.

### Knobs
- `fail_closed` (boolean, required; default=true) — Fail validation on any schema or policy error.
- `intake_json_path` (path, required) — Filesystem path to a client intake JSON payload.

## M_Judge

Score GDPR audit runs and emit structured judge outputs for reporting.

### Knobs
- `judge_model` (string, required) — Model identifier used for judging outputs.
- `score_schema` (path, optional) — Path to score schema or rubric reference.

## M_Library

Maintain the GDPR base scenario library and ensure scenarios conform to schema and taxonomy.

### Knobs
- `library_root` (path, required) — Filesystem path to the GDPR base scenario library.

## M_LiveRun

Execute GDPR audit runs via Inspect + Petri with seed instructions and collect logs.

### Knobs
- `max_turns` (number, required; default=20) — Maximum number of turns per audit run.
- `seed_instructions` (json, required) — Seed instructions string or list for Petri audit.
- `transcript_save_dir` (path, required; default="./outputs") — Directory for Petri transcript JSON outputs.

## M_Report

Generate GDPR audit reports from judge outputs and run metadata.

### Knobs
- `include_raw_logs` (boolean, optional; default=false) — Whether to include raw logs in report bundles.
- `report_output_dir` (path, required) — Directory for generated report artifacts.
