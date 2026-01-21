# Scenario Instance Expansion Rules v0.1

Defines how to expand scenario cards and client intake into bespoke scenario
specs and runnable instances. This is contract-only scaffolding.

## Canonical references
- Report layers: `packages/specs/docs/contracts/reporting/report_layers.md`
- Report evidence/verification modes: `packages/specs/docs/contracts/reporting/report_fields_crosswalk_v0_1.md`
- Canonical signals: `packages/specs/docs/contracts/taxonomy/signals.json`

## Inputs
- **scenario_card**: stable theme definition (what violation is tested).
- **client_intake**: policy rules, target specs, industry/country context.

## Outputs
- List of **bespoke_scenario_specs**, each yielding one runnable
  `scenario_instance_id` and its instruction files.

## Expansion rules
- **One violation != one instance**: a single scenario_card can expand into
  multiple instances due to policy constraints or channel variants.
- **Multi-channel variants**: if client policy supports multiple channels for
  a right (email vs in-chat vs portal), create one instance per channel unless
  explicitly marked equivalent.
- **Verification mode constraints**: if client policy indicates a requirement
  is only doc- or timeline-verifiable, set `verification_mode` accordingly and
  do not force runtime verification.
- **Human-approval option**: instances may be reviewed, but the pipeline must be
  valid without review.
- **Variants do not create taxonomy**: variant_id is configuration only; no new
  signal IDs are introduced.

## Minimal example (illustrative)
```json
{
  "scenario_card_id": "gdpr_erasure_request",
  "client_policy": {
    "channels": ["email", "portal"],
    "verification": "doc"
  },
  "instances": [
    {
      "scenario_instance_id": "gdpr_erasure_request__email__v1",
      "variant_id": "channel=email",
      "verification_mode": "doc"
    },
    {
      "scenario_instance_id": "gdpr_erasure_request__portal__v1",
      "variant_id": "channel=portal",
      "verification_mode": "doc"
    }
  ]
}
```

## Good looks like
- Explicit mapping from card + intake to multiple runnable instances.
- Verification modes reflect what the client can actually prove.
- Variants stay configuration-only and reuse canonical signals.

## Bad looks like
- Collapsing multiple channels into one instance with ambiguous evidence.
- Marking doc-only policies as runtime verification.
- Treating variant_id as a new taxonomy ID.

## How to decide
- If the policy or channel changes evidence collection, create a new instance.
- If the channel is equivalent and evidence is identical, allow explicit
  equivalence to reuse a single instance.
