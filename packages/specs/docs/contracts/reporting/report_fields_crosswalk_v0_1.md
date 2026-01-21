# Report Fields Crosswalk v0.1

Crosswalk from report field IDs to source, evidence artifact, and verification mode.
Layer semantics are canonical in `packages/specs/docs/contracts/reporting/report_layers.md`.
Signal references must use `packages/specs/docs/contracts/taxonomy/signals.json`.

## Crosswalk

| field_id | layer | source | evidence_artifact | verification_mode |
| --- | --- | --- | --- | --- |
| l1_scope_snapshot | L1 | Intake | intake_form_hash | doc |
| l1_overall_status | L1 | Both | judge_output_manifest | runtime |
| l1_risk_summary | L1 | Both | evidence_pack_ref | runtime |
| l1_key_findings | L1 | Judge | evidence_pack_ref | runtime |
| l1_recommendations | L1 | Both | evidence_pack_ref | doc |
| l2_article_coverage | L2 | Judge | evidence_pack_ref | runtime |
| l2_findings_summary | L2 | Judge | evidence_pack_ref | runtime |
| l2_evidence_excerpts | L2 | Judge | transcript_hash | runtime |
| l2_provenance_chain | L2 | Both | run_manifest_path | timeline |
| l2_judge_manifest | L2 | Judge | judge_manifest_path | doc |
| l3_transcript_bundle_ref | L3 | Judge | transcript_hash | runtime |
| l3_evidence_pack_ref | L3 | Judge | evidence_pack_path | runtime |
| l3_run_manifest | L3 | Both | run_manifest_path | timeline |
| l3_raw_outputs_ref | L3 | Judge | raw_outputs_path | runtime |
| gdpr_gr_audit_scope | GDPR-GR | Intake | intake_form_hash | doc |
| gdpr_gr_compliance_statement | GDPR-GR | Both | judge_output_manifest | doc |
| gdpr_gr_article_matrix | GDPR-GR | Judge | evidence_pack_ref | runtime |
| gdpr_gr_limitations | GDPR-GR | Both | limitations_log | doc |

## Verification modes
- **runtime**: Verifiable from generated artifacts and run outputs.
- **doc**: Verified against documented inputs/assumptions.
- **timeline**: Verified by run sequencing and provenance metadata.
- **out-of-scope**: Not verifiable in this phase (avoid unless explicitly approved).

## Completeness rules
- Every field_id listed in `report_fields_v0_1.md` must appear exactly once here.
- No extra field_ids may appear without adding them to `report_fields_v0_1.md`.
- Source and evidence_artifact must be non-empty for every field.
