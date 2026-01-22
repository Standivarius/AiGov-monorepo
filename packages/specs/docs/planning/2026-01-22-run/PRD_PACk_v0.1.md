PRD_PACK.md
AiGov — PRD Pack (MVP, GDPR-only)
Product overview (1 page max)
AiGov is an evaluation product for enterprise chatbots/agents: it turns a target system into a portable evidence pack plus layered reports that a privacy team, security team, and external auditor can rely on.
The backbone is a strict, defensible stage split:
•	Stage A (Execute + capture evidence): run a deterministic scenario bundle against the target and capture transcripts + artifacts, without scoring/judging.
•	Stage B (Offline judgment on frozen evidence): evaluate Stage A outputs offline to produce schema-valid judgments, citations, and normalized findings.
•	Stage C (Reporting + exports): generate audience-layered reports and exports from the frozen evidence + judgments (regenerable without rerunning the target).
This “evidence-first” architecture directly supports the GDPR accountability principle (ability to demonstrate compliance) and separation of runtime behavior from post-hoc assessment. (EUR-Lex)
Enterprise expectation anchor (non-contract): align to widely used risk management language so outputs are “auditor-ready, no more/no less” (e.g., governance + measurement orientation in NIST AI RMF). (European Data Protection Board)
Target customer + MVP scope
Target customer (buyer):
•	Enterprise deploying a GDPR-relevant chatbot/assistant (customer support, HR, finance, healthcare).
•	Buyer typically sits in Compliance/Privacy with Security/CISO as co-sponsor.
Primary users:
•	Compliance/Privacy: wants demonstrable findings, DSAR/erasure routing checks, transparency checks.
•	Security: wants leakage/prompt-injection signals, evidence trail, and incident-readiness framing.
•	External auditor / regulator-facing counsel: wants traceability, reproducibility, and admissible evidence.
MVP scope (GDPR-only, end-to-end demoable):
•	Deterministic client intake → deterministic bespoke scenario bundle compilation (≈20 scenarios is fine).
•	Stage A runner against either:
o	real target, or
o	mocked target wrapper (allowed) that emits clean internal decision logs for evidence.
•	Evidence pack (schema-driven, portable, offline-judgeable).
•	Stage B judge harness producing normalized judgments with citations.
•	Stage C layered reports:
o	L1 = EXEC
o	L2 = COMPLIANCE
o	L3 = SECURITY
•	GDPR-GR export pack (contract-defined fields/crosswalk; no new standards invented here).
MVP boundary note on “timeline obligations” (non-contract anchor):
•	Many GDPR rights requests require response “without undue delay and in any event within one month” (Art. 12), and right to erasure exists with conditions (Art. 17). AiGov MVP can verify routing + disclosure + evidence in runtime transcripts, while full timeline completion may require documentary/process evidence. (EUR-Lex)
EP list (customer-paid capabilities)
EP IDs are the existing CAP-### capability IDs from the current ledger; each EP maps to acceptance criteria and ≥1 PE evaluation (EVAL-###) with explicit pass rules and evidence artifacts.
1) CAP-101 — Deterministic Intake → Deterministic Scenario Bundle
What it enables
•	Customer provides target/context intake once; AiGov deterministically compiles a bespoke scenario bundle with a stable bundle hash + manifest.
Acceptance criteria (must be testable)
•	AC-001: Intake output validates against the intake contract; missing required fields fails closed.
•	AC-002: Same intake + same scenario library version ⇒ same bundle_hash and identical bundle manifest (byte-for-byte or canonicalized equivalence).
•	AC-002a (expansion rule compliance): Scenario instances are generated per the expansion rules (multi-channel ⇒ multiple instances unless explicitly equivalent; one “violation concept” can yield multiple instances). (Contract-anchored; do not redefine here.)
PE eval links
•	EVAL-003, EVAL-014
Evidence artifacts (names/types, not paths)
•	EVID-003 “Scenario bundle artifact + manifest” (manifest includes bundle_hash, scenario IDs, instance IDs)
•	EVID-011 “PE test reports”
Runtime tier
•	Primary gate: PR-gate (fast determinism + schema checks).
________________________________________
2) CAP-102 — Stage A Runner (Execute + Capture Evidence)
What it enables
•	Executes scenario instances against the target (real or mock), capturing transcripts + raw artifacts without any judging.
Acceptance criteria
•	AC-004: Given a scenario bundle + target config, Stage A produces transcripts + raw artifacts per scenario instance plus a run manifest; exits 0 on success.
•	AC-005: If target is unreachable/errors, instances are marked execution_error with error class; partial artifacts still written; non-zero exit if error threshold exceeded.
•	AC-006: Stage A is “judge-free”: no judge/scoring logic executes during Stage A.
PE eval links
•	EVAL-004, EVAL-013
Evidence artifacts
•	EVID-004 “Stage A transcripts + raw artifacts”
•	EVID-011 “PE test reports”
Runtime tier
•	Primary gate: Nightly (can involve model calls / target adapters; keep PR-gate small).
________________________________________
3) CAP-103 — Evidence Pack Builder (Admissible + Portable)
What it enables
•	Converts Stage A outputs into a portable, schema-driven evidence pack with a manifest and integrity hashes, suitable for offline judging and external audit review.
Acceptance criteria
•	AC-007: Evidence pack validates against the evidence-pack schema and includes manifest + cryptographic hashes.
•	AC-008: Evidence vs telemetry separation is enforced (only whitelisted evidence enters the admissible pack).
•	AC-009: Evidence pack is portable: Stage B can run offline using only the evidence pack (no network calls).
PE eval links
•	EVAL-004, EVAL-005, EVAL-015
Evidence artifacts
•	EVID-005 “Evidence pack (admissible) + manifest”
•	EVID-011 “PE test reports”
Runtime tier
•	Primary gate: Nightly (build + validate packs at scale)
________________________________________
4) CAP-104 — Stage B Judge Harness (Offline + Normalized)
What it enables
•	Runs a governed judge process on frozen evidence packs to produce normalized findings, verdicts, and citations.
Acceptance criteria
•	AC-010: Stage B reads evidence pack and produces judgments.json (or equivalent) with normalized verdicts and citations to evidence IDs.
•	AC-011: Judge output passes schema validation; unknown verdict enum fails closed.
•	AC-012: Re-running Stage B on the same evidence pack yields identical normalized output (within defined tolerances).
PE eval links
•	EVAL-005, EVAL-006, EVAL-009, EVAL-011
Evidence artifacts
•	EVID-006 “Stage B judgments (schema-valid)”
•	EVID-011 “PE test reports”
Runtime tier
•	Primary gate: Nightly (golden-case correctness + determinism checks)
________________________________________
5) CAP-105 — Layered Reports (L1 EXEC / L2 COMPLIANCE / L3 SECURITY)
What it enables
•	Generates layered reports that summarize findings and allow drill-down to raw evidence + judgments. Reports must be regenerable without rerunning Stage A.
Acceptance criteria
•	AC-013: Reports validate against the report-fields contract; required sections present.
•	AC-014: Report evidence links resolve to evidence-pack artifact IDs; link-checker passes.
PE eval links
•	EVAL-007, EVAL-015
Evidence artifacts
•	EVID-007 “L1 report artifact”
•	EVID-008 “L2 report artifact”
•	EVID-009 “L3 trace/evidence export”
•	EVID-014 “Dashboards” (optional for MVP demo)
Runtime tier
•	Primary gate: Nightly (report regen + link integrity)
________________________________________
6) CAP-106 — Exports (GDPR-GR)
What it enables
•	Produces export packs aligned to the existing GDPR-GR reporting requirements and the authoritative report-fields crosswalk (contract-defined).
Acceptance criteria
•	AC-015: GDPR-GR export includes required fields per crosswalk; validates against export schema.
•	AC-016: Export pack includes manifest + hashed evidence pointers; shareable without leaking non-whitelisted telemetry.
PE eval links
•	EVAL-008, EVAL-015
Evidence artifacts
•	EVID-010 “GRC export files”
•	EVID-005 “Evidence pack (admissible) + manifest”
Runtime tier
•	Primary gate: Release (schema + crosswalk validation)
________________________________________
7) CAP-108 — CI Gates + Drift Prevention (Eval-first enforcement)
What it enables
•	Prevents drift and enforces eval-first: PRs fail if contracts drift without versioning, schemas don’t validate, or required evidence artifacts aren’t produced.
Acceptance criteria
•	AC-017: PR gate runs required evalset and publishes artifacts; fails if missing artifacts.
•	AC-018: Contract changes require version bump and updated crosswalk/mappings or CI fails closed.
PE eval links
•	EVAL-002, EVAL-017 (and any PR-gate evals)
Evidence artifacts
•	EVID-011 “PE test reports”
•	EVID-002 “Vendored contract snapshot (with commit SHA)” (or equivalent provenance artifact in monorepo)
Runtime tier
•	Primary gate: PR-gate (must stay short).
________________________________________
Core pipeline (modules, plain English)
1.	Scenario library (GDPR canonical set)
2.	Client intake + target preflight (contract output; fail-closed on missing required data)
3.	Bespoke scenario bundle compilation (deterministic; bundle hash + manifest)
4.	Stage A execution runner (target adapter; transcripts + raw artifacts; no judging)
5.	Evidence pack builder (admissible pack; manifest + hashes; evidence/telemetry separation)
6.	Stage B offline judge (governed, normalized outputs; citations to evidence IDs)
7.	Stage C reporting (EXEC/COMPLIANCE/SECURITY; drill-down to evidence)
8.	Exports (GDPR-GR)
9.	PE eval harness + runtime tiers (PR-gate short; heavier suites nightly/release/audit)
Single-source bespoke scenario spec rule (contract): auditor instructions and judge instructions must be generated from the same bespoke scenario spec (no divergent instruction sources).
Tier A controls (minimal enterprise defensibility)
Tier A controls are separate from EPs and must map to PE evals with evidence.
•	CO-001 Audit logging & traceability
•	CO-002 Role-based access controls
•	CO-003 DSAR/erasure procedure evidence
•	CO-004 Data retention & deletion controls
•	CO-005 Model/prompt change management
•	CO-006 Monitoring & incident response readiness
•	CO-007 Privacy notice + lawful basis disclosure
•	CO-008 Security controls (PII leakage / prompt injection evidence)
•	CO-009 Vendor/subprocessor list + contracts evidence
•	CO-010 Audit-ready reporting & export integrity
(Full mapping is in tier_a_coverage_report.md.)
Non-goals / out of scope (anti-bloat)
•	Non-GDPR jurisdictions and full multi-regime governance platform
•	Real-time monitoring/continuous compliance scanning as a product line
•	Full DSAR case management automation (beyond routing + evidence capture)
•	Full vulnerability management / pen-test platform (only scenario-driven evidence and minimal Tier A readiness)
•	Heavy UI/console work (MVP can be CLI-driven with report outputs)
Open variables (must be resolved, not handwaved)
•	Q-001: Scope boundary: evaluation product vs broader governance platform (what Tier A controls must ship in v1 vs deferred).
•	Q-002: Does a Stage B runner already exist (or is it a gap)?
•	Additional MVP questions:
o	What counts as “deterministic equivalence” for bundles and judge outputs (byte-for-byte vs canonical JSON)?
o	How to represent obligations that require timeline/process evidence in MVP exports (route + disclosure verifiable; completion may be document-verifiable). (EUR-Lex)
