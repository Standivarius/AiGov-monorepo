# Client Intake Output Contract v0.1

Defines the schema-driven intake output that feeds Pre2.3 reporting crosswalks
and Pre2.4 scenario generation. This is contract-only scaffolding.

## Canonical references
- Report crosswalk: `packages/specs/docs/contracts/reporting/report_fields_crosswalk_v0_1.md`
- Scenario expansion: `packages/specs/docs/contracts/scenarios/scenario_instance_expansion_rules_v0_1.md`
- Bespoke spec: `packages/specs/docs/contracts/scenarios/bespoke_scenario_spec_v0_1.md`

## Required top-level objects
- `client_id` (opaque)
- `target_id` (opaque; supports multiple targets per client)
- `intake_run_id` (opaque)
- `policy_profile_ref` (hash/id)
- `target_profile_ref` (hash/id)
- `provenance` (source refs, hashes, capture timestamps)

## policy_profile (minimum fields)
- `supported_dsar_channels` (array; e.g., ["email", "in_chat", "portal"])
- `right_to_erasure_handling`
  - `primary_channel`
  - `fallback_channels`
  - `constraints` (e.g., timeline-based verification)
- `known_client_constraints` (array; e.g., cannot do canary deletion verification)

## target_profile (minimum fields)
- `target_type` ("chatbot" | "chatbot_with_actions" | "agent")
- `auth_context` ("logged_in" | "public" | "mixed")
- `data_sources_touched` (array of high-level sources)
- `integration_surfaces` (array; email, CRM, ticketing, etc.)
- `locale_context` (country/region)

## mock_target_profile mapping
Derived from `target_profile` and must remain schema-aligned.

Required mock fields:
- `target_type`
- `auth_context`
- `action_capabilities` (send_email, delete_data, escalate, etc.)
- `logging_requirements` (must log intentional leaks/decisions)

## Authoritative validation block

```json
{
  "required_keys": [
    "client_id",
    "target_id",
    "intake_run_id",
    "policy_profile_ref",
    "target_profile_ref",
    "provenance"
  ],
  "allowed_target_types": [
    "chatbot",
    "chatbot_with_actions",
    "agent"
  ],
  "allowed_auth_context": [
    "logged_in",
    "public",
    "mixed"
  ],
  "allowed_dsar_channels": [
    "email",
    "in_chat",
    "portal"
  ],
  "target_profile_required_fields": [
    "target_type",
    "auth_context",
    "data_sources_touched",
    "integration_surfaces",
    "locale_context"
  ],
  "mock_target_profile_required_fields": [
    "target_type",
    "auth_context"
  ],
  "allowed_verification_modes": [
    "runtime",
    "doc",
    "timeline",
    "out-of-scope"
  ]
}
```

## Good looks like
- Intake output provides stable refs to policy and target profiles.
- Channels are treated as configuration (not taxonomy IDs).
- Mock target profile stays aligned with target_profile fields.

## Bad looks like
- Overloading intake with full GDPR doctrine.
- Introducing new taxonomy IDs for channels.
- Missing provenance hashes or timestamps.

## How to decide
- If a field is needed to map report evidence, keep it in policy/target profile.
- If a field configures simulation, it must exist in mock_target_profile.
- If verification is policy-limited, set verification mode to doc/timeline.
