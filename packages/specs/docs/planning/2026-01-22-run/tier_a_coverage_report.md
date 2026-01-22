tier_a_coverage_report.md
Tier A Coverage Report (AiGov)
Tier A control → mapped eval_ids → evidence artifacts
Tier A control	Mapped eval_ids	Required evidence artifacts
CO-001 Audit logging & traceability	EVAL-201	EVID-TIERA-001
CO-002 RBAC	EVAL-202	EVID-TIERA-002
CO-003 DSAR/erasure procedure evidence	EVAL-203	EVID-TIERA-003
CO-004 Data retention & deletion controls	EVAL-204	EVID-TIERA-004
CO-005 Model/prompt change management	EVAL-205	EVID-TIERA-005
CO-006 Monitoring & incident response readiness	EVAL-206	EVID-TIERA-006
CO-007 Privacy notice + lawful basis disclosure	EVAL-207	EVID-TIERA-007
CO-008 Security controls (PII leakage / prompt injection evidence)	EVAL-208	EVID-TIERA-008
CO-009 Vendor/subprocessor list + contracts evidence	EVAL-209	EVID-TIERA-009
CO-010 Audit-ready reporting & export integrity	EVAL-210 (also supported by EVAL-007/EVAL-008/EVAL-015)	EVID-TIERA-010 (+ EVID-007/008/009/010 as applicable)
100% coverage (machine-checkable)

STOP if any Tier A control has zero eval coverage or zero evidence artifact definition.

tier_a_controls:
  - control_id: CO-001
    eval_ids: [EVAL-201]
    evidence_artifacts: [EVID-TIERA-001]
  - control_id: CO-002
    eval_ids: [EVAL-202]
    evidence_artifacts: [EVID-TIERA-002]
  - control_id: CO-003
    eval_ids: [EVAL-203]
    evidence_artifacts: [EVID-TIERA-003]
  - control_id: CO-004
    eval_ids: [EVAL-204]
    evidence_artifacts: [EVID-TIERA-004]
  - control_id: CO-005
    eval_ids: [EVAL-205]
    evidence_artifacts: [EVID-TIERA-005]
  - control_id: CO-006
    eval_ids: [EVAL-206]
    evidence_artifacts: [EVID-TIERA-006]
  - control_id: CO-007
    eval_ids: [EVAL-207]
    evidence_artifacts: [EVID-TIERA-007]
  - control_id: CO-008
    eval_ids: [EVAL-208]
    evidence_artifacts: [EVID-TIERA-008]
  - control_id: CO-009
    eval_ids: [EVAL-209]
    evidence_artifacts: [EVID-TIERA-009]
  - control_id: CO-010
    eval_ids: [EVAL-210]
    evidence_artifacts: [EVID-TIERA-010]
coverage_assertion:
  all_controls_have_eval_coverage: true
  all_controls_have_evidence_artifacts: true