# Reporting Artifact Registry v0.1

Defines contract-level reporting artifacts used in crosswalks.

## limitations_log
- **Purpose**: Doc-mode operational evidence timeline references and explicit limitations.
- **Required fields**:
  - `run_id`
  - `generated_at`
  - `timeline_refs` (array of evidence IDs or timestamps)
  - `limitations` (array of strings)
  - `assumptions` (array of strings)

## Notes
- limitations_log is required for doc-mode operational evidence claims.
- Evidence IDs referenced here must exist in the evidence pack manifest.
