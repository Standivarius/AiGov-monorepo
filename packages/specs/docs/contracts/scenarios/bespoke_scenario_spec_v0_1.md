# Bespoke Scenario Spec v0.1

Defines the single authoritative spec that generates both auditor and judge
instruction files. This is contract-only scaffolding.

## Canonical references
- Report layers: `packages/specs/docs/contracts/reporting/report_layers.md`
- Report evidence/verification modes: `packages/specs/docs/contracts/reporting/report_fields_crosswalk_v0_1.md`
- Canonical signals: `packages/specs/docs/contracts/taxonomy/signals.json`

## Required fields (minimum)
- `bespoke_scenario_spec_id` (string, stable)
- `scenario_card_id` (string, stable theme)
- `scenario_instance_id` (string, runnable case ID)
- `variant_id` (string, optional; config-only)
- `target_profile_ref` (string, hash/id from client intake output)
- `policy_profile_ref` (string, hash/id from client intake output)
- `canonical_signal_ids` (array; must exist in `signals.json`)
- `verification_mode` (runtime | doc | timeline | out-of-scope)
- `required_evidence_artifacts` (array of artifact IDs/types, not file paths)
- `instruction_generation` (object)
  - `auditor_instructions_template_ref`
  - `judge_instructions_template_ref`
  - `rule`: both outputs are generated from this spec (no drift)

## Authoritative validation block

```json
{
  "required_keys": [
    "bespoke_scenario_spec_id",
    "scenario_card_id",
    "scenario_instance_id",
    "canonical_signal_ids",
    "verification_mode",
    "required_evidence_artifacts",
    "instruction_generation"
  ],
  "allowed_verification_modes": [
    "runtime",
    "doc",
    "timeline",
    "out-of-scope"
  ]
}
```

## Invariants
- No scenario_instance without at least one canonical signal.
- Variant does not create taxonomy (no new signal IDs).
- Judge scope is the declared violation only; Scout can detect extra violations later.
auditor and judge instructions MUST be generated from the same bespoke scenario spec

## Example (minimal)
```json
{
  "bespoke_scenario_spec_id": "bss_001",
  "scenario_card_id": "gdpr_consent_ui",
  "scenario_instance_id": "gdpr_consent_ui__in_chat__v1",
  "variant_id": "channel=in_chat",
  "target_profile_ref": "intake_target_9f3a",
  "policy_profile_ref": "intake_policy_2b11",
  "canonical_signal_ids": ["lack_of_consent", "inadequate_transparency"],
  "verification_mode": "runtime",
  "required_evidence_artifacts": ["transcript_hash", "evidence_pack_path"],
  "instruction_generation": {
    "auditor_instructions_template_ref": "auditor_templates/gdpr_consent_ui.md",
    "judge_instructions_template_ref": "judge_templates/gdpr_consent_ui.md",
    "rule": "Generate both instruction files from this spec only."
  }
}
```

## Good looks like
- One spec produces both instruction files with no drift.
- Canonical signals are explicit and traceable to evidence artifacts.
- Verification mode matches client policy constraints.

## Bad looks like
- Separate sources for auditor vs judge instructions.
- Variant IDs treated as new taxonomy IDs.
- Missing or ambiguous evidence requirements.

## How to decide
- If a requirement is policy-only, choose `doc` or `timeline` over `runtime`.
- If multiple channels are supported, model them as variants, not new signals.
