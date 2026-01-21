# Report Fields v0.1 (Contract)

This document defines the minimum required report fields by layer.
Canonical layer definitions live in `packages/specs/docs/contracts/reporting/report_layers.md`.
Do not redefine L1/L2/L3 semantics here.

## Field IDs (minimum required)

### L1 (EXEC)
- `l1_scope_snapshot`: Audit scope, target system, dates, and run identifiers.
- `l1_overall_status`: One-line compliance posture statement.
- `l1_risk_summary`: Primary risks and business impact summary.
- `l1_key_findings`: Top findings list (brief, decision-ready).
- `l1_recommendations`: Priority actions for leadership.

### L2 (COMPLIANCE)
- `l2_article_coverage`: Coverage matrix of GDPR articles tested vs. not tested.
- `l2_findings_summary`: Detailed findings with canonical signal IDs.
- `l2_evidence_excerpts`: Evidence excerpts supporting findings.
- `l2_provenance_chain`: End-to-end provenance chain for the run.
- `l2_judge_manifest`: Judge model/version/config used for decisions.

### L3 (SECURITY)
- `l3_transcript_bundle_ref`: Reference to full transcripts (hash/path).
- `l3_evidence_pack_ref`: Reference to evidence pack bundle.
- `l3_run_manifest`: Full run manifest for reproducibility.
- `l3_raw_outputs_ref`: Raw system outputs (logs, traces, artifacts).

### GDPR-GR (Regulator-Ready)
- `gdpr_gr_audit_scope`: Scope and method statement suitable for regulator review.
- `gdpr_gr_compliance_statement`: Compliance statement with limitations.
- `gdpr_gr_article_matrix`: Regulator-facing article matrix (mapped to L2).
- `gdpr_gr_limitations`: Explicit limitations, exclusions, and assumptions.

## Good looks like
- Minimal, schema-friendly field IDs with stable meaning.
- L2 references canonical signal IDs from `packages/specs/docs/contracts/taxonomy/signals.json`.
- Clear separation between layer purposes and audience intent.

## Bad looks like
- Layer semantics redefined here instead of `report_layers.md`.
- Fields that embed non-canonical signal IDs or ad-hoc labels.
- Mixing executive summary content into L3 technical artifacts.

## How to decide
- If the field is decision-ready and concise, place it in L1.
- If it requires legal/audit precision and citations, place it in L2.
- If it is raw technical evidence or reproducibility data, place it in L3.
- If it must be regulator-facing, place it in GDPR-GR and map back to L2.
