# Business readiness requirements — v0.x

Purpose: track business-level readiness items (security, privacy, governance) that impact product decisions.

Legend:
- Stage A: must-have for early enterprise pilots
- Stage B: segment-triggered / later
- Assurance: SD (self-declared with evidence), 3P (third-party assessed), CERT (certification)

## BR-00 Governance & document control
- **BR-001 (A, SD)** Maintain versioned assurance templates and an approval/change log per release.
- **BR-002 (A, SD)** Maintain a claims/limitations register; marketing claims must match evidence.

## BR-10 GDPR operational readiness (company)
- **BR-101 (A, SD+legal)** RoPA maintained and reviewable.
- **BR-102 (A, SD+legal)** DPIA process and template; run triggers defined.
- **BR-103 (A, SD)** Retention & deletion policy aligned to product defaults.
- **BR-104 (A, SD)** DSAR handling procedure (even if minimal data at rest).
- **BR-105 (A, SD)** Incident/breach procedure and escalation contacts.

## BR-20 Security management posture
- **BR-201 (A→CERT)** ISO/IEC 27001 pathway: scope statement, risk register, SoA, internal audit rhythm.
- **BR-202 (A→CERT)** ISO/IEC 42001 pathway: AI governance scope, AI risk register, change control triggers.
- **BR-203 (A, 3P recommended)** Targeted security assessment scope (supply chain, artefact tampering, secrets).

## BR-30 Supply chain and vulnerability handling
- **BR-301 (A, SD)** SBOM produced per release (where feasible).
- **BR-302 (A, SD)** Vulnerability disclosure policy and triage process.

## BR-40 Segment-triggered items
- **BR-401 (B, 3P)** ISAE 3000-style assurance engagement (integrity/traceability controls).
- **BR-402 (B, CERT)** ISO/IEC 27701 (PIMS) if procurement requires.
- **BR-403 (B, CERT)** EUCC/Common Criteria if buyers require product certification.
- **BR-404 (B, SD+legal)** DORA-heavy annexes and oversight mechanisms for financial sector.
