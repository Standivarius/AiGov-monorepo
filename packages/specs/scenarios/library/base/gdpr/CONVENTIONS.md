# GDPR Base Scenario Conventions

These rules govern the GDPR base scenario catalog. Structure is defined by the schema:
`packages/specs/scenarios/schemas/base_scenario_v1.schema.json`.

## IDs and filenames
- `scenario_id` format: `GDPR-###` (three digits).
- Filename format: `gdpr_###_<slug>.json`.
- Filename number must match the `scenario_id` number.
- `scenario_id` must be unique across the catalog.

## Add the next scenario (step-by-step)
1) Pick the next unused number (e.g., `GDPR-012`).
2) Choose a short slug (lowercase, words separated by underscores).
3) Create the file: `gdpr_012_<slug>.json`.
4) Set `scenario_id` to `GDPR-012` in the JSON.
5) Validate with the planning-pack validators before committing.
