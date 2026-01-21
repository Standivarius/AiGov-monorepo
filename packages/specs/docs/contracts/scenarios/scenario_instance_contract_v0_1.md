# Scenario Instance Contract v0.1

Defines how a stable scenario card expands into runnable instances, including
multi-channel variants. This is scaffolding; keep it minimal.

## Canonical references
- Signal IDs: `packages/specs/docs/contracts/taxonomy/signals.json`
- Report layers: `packages/specs/docs/contracts/reporting/report_layers.md`

## Key concepts
- **scenario_card_id**: Stable theme ID for a scenario card (e.g., "gdpr_consent_ui").
- **scenario_instance_id**: Runnable case instance derived from a card.
- **variant_id**: Configuration variant (e.g., `channel=email`, `channel=in_chat`).
  Variants do **not** create new taxonomy IDs.
- **mapped_signals**: Canonical signal IDs that the scenario tests.
- **required_artifacts**: Evidence artifacts that must be produced for auditability.

## Contract fields (minimum)
- `scenario_card_id` (string, stable)
- `scenario_instance_id` (string, unique per runnable case)
- `variant_id` (string, config-only)
- `channel` (string, e.g., email, in_chat, voice)
- `mapped_signals` (array of canonical signal IDs)
- `required_artifacts` (array of artifact IDs/paths)
- `source_spec_ref` (path/commit of the scenario source spec)

## Drift prevention
Auditor instruction files and judge instruction files must be generated from the
same source spec (`source_spec_ref`) to prevent drift.

## Example (illustrative)
```json
{
  "scenario_card_id": "gdpr_consent_ui",
  "scenario_instance_id": "gdpr_consent_ui__in_chat__v1",
  "variant_id": "channel=in_chat",
  "channel": "in_chat",
  "mapped_signals": ["lack_of_consent", "inadequate_transparency"],
  "required_artifacts": ["transcript_hash", "evidence_pack_path"],
  "source_spec_ref": "packages/specs/scenarios/gdpr/consent_ui.md"
}
```
