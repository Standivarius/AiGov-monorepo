AIGov

Product Requirements Document

GDPR Pre-Audit for AI-Powered Chatbots

Version 0.2 — Phase 0

March 2026

Classification: Internal — Draft

Author: Marius (PM) + Claude (AI PM Consultant)

Peer Review: DeepSeek, Gemini (architecture + methodology inputs)

v0.2 changes: CCO/CISO layer correction, hierarchical Judge prompting, municipality-only scope, aggregation logic, blind stateless evaluation, enriched context engineering findings

1. Purpose

AIGov delivers enterprise-grade GDPR pre-audits for AI-powered chatbots deployed by EU organisations. It combines adversarial LLM testing with compliance framework mapping to produce decision-useful reporting for three audiences: Chief Compliance Officers (primary buyer), CISOs (technical gatekeeper), and executive sponsors.

The product addresses a specific market gap: no existing tool both tests what a chatbot actually does and maps findings to GDPR obligations. Security vendors test for vulnerabilities but do not map to regulatory frameworks. Compliance consultants review documentation but cannot generate exploit evidence. GRC tools (CISO Assistant, OneTrust, Vanta) manage documentation but cannot verify system behaviour. AIGov fills the verification gap: it shows the delta between what documentation claims and what the chatbot actually does.

1.1 Product Type

Pre-audit / periodic evaluation tool. AIGov does not produce legally binding compliance certificates. It produces an indicative risk assessment with evidence-linked findings, structured to support formal audit preparation and internal governance review.

1.2 Value Proposition

A single €8–15k engagement replaces separate security testing (€8k) and compliance review (€12k). The integrated report reveals the delta between what documentation claims and what the chatbot actually does — which is the finding CCOs cannot get from either a security vendor or a compliance consultant alone.

2. Users and Operating Context

2.1 Buying Dynamics

2.2 Target Systems

Phase 0 focuses exclusively on external-facing, single-role chatbots in regulated industries. These present clean testing surfaces: all users have the same role, same rights, and same access level. The trust boundary between external user and organisational system maps directly to GDPR obligations around transparency, consent, and data subject rights.

Phase 0 verticals (Netherlands, municipalities):

Municipal/government citizen service bots (public sector accountability, high enforcement exposure, Wet open overheid transparency obligations)

Phase 1+ verticals (expansion candidates):

Healthcare: patient-facing triage, appointment, symptom-checker bots (special category data, Art. 9, Wgbo)

Financial services: insurance claims, banking assistant bots (profiling risk, Art. 22)

Telecommunications: customer service bots (high-volume PII processing)

EdTech: student-facing bots (children’s data, Art. 8)

Explicitly out of scope:

Internal multi-role chatbots (e.g., MS Copilot) — permissions are organisational, not chatbot-controlled

AI agents with tool use / autonomous actions

Custom fine-tuned models (use instructional layer instead)

2.3 Client Readiness Requirements

Minimum viable intake for an engagement to proceed:

Endpoint or URL — accessible chatbot for testing

Description of intended purpose — what the chatbot should and should not do

Data privacy policy — the organisation’s GDPR documentation relevant to this system

Telemetry access is additive: enables deeper root-cause analysis and stronger remediation guidance. Reports without telemetry include a clear “Limitations” section explaining reduced causal attribution.

3. End-to-End Flow

The pipeline has two parallel entry points that merge before testing. This is not a linear process from a single input.

3.1 Parallel Entry Points

3.2 Scenario Library Structure

Parent → variant hierarchy. The library contains only parent scenarios (stable, versioned). Variants are generated during Bespoke Scenario Preparation based on client-specific conditions from Intake.

Selection rules:

When selecting which parent scenarios apply to a client, the logic is explicit and traceable: “run all scenarios tagged municipality,” “exclude scenarios tagged financial,” or “only run these 5 specific scenarios.” Selection is based on Intake variables (locale, industry, chatbot scope) crossed against scenario tags.

Bundle compilation:

The set of bespoke scenarios assembled for a client engagement is compiled deterministically (same inputs produce the same bundle) and hashed. The hash enables later proof that “this exact set of scenarios was used for this audit.”

Design principles:

No duplicate semantic work between Intake and Bespoke

No uncontrolled scenario explosion; use family → variant logic with qualification criteria

3.3 Client Intake Pipeline

Four LLM tasks in sequence, each with deterministic schema gates. All tasks use an LLM council (3 SOTA models) rather than single-model execution, providing accuracy through consensus without vendor lock-in.

Task 1: Document Translation

Consolidates client documentation into a single .md file, translates to English using LLM council with semantic reconciliation. Flags low-confidence translations that are materially GDPR-relevant. Output: translated .md with confidence report. Gate: schema validation + human approval.

Task 2: Semantic Adaptation

Adapts translated content to AIGov terminology using the project terminology file and original-language source. LLM council converges to agreed version. Output: AIGov-adapted .md carrying forward all prior artefacts. Gate: schema validation + human approval.

Task 3: Capabilities Mapping

Parses adapted documentation into a structured schema covering: GDPR document presence/absence (using the GDPR folder checklist), chatbot scope and functionality, industry and locale intersection, triggered obligations, and available evidence types. Output: capabilities schema ready for scenario selection. Gate: schema validation + human approval.

Complexity note: Capabilities Mapping is the highest-complexity Intake task. The schema is designed for partial success — a sparse but accurate schema is better than a hallucinated complete one. Human review gates are mandatory. For Phase 0 v0.1, this task may remain manual while other Intake tasks are automated.

Task 4: Scenario Selection and Context Extraction

Two sub-steps. First, scenario selection: Intake variables (locale, industry, chatbot scope) are crossed against scenario library tags to determine which parent scenarios apply. Selection rules are explicit and logged. Second, context extraction: for each selected scenario, relevant policy fragments, SOPs, and commitments are extracted from the full document set using full-context processing. Output: scenario-enriched context packages for Bespoke. Gate: schema validation.

3.4 Bespoke Scenario Preparation (Merge Point)

Combines Scenario Library parents with Intake outputs. For each applicable parent scenario, generates client-specific variants parameterised by the capabilities mapping and enriched with relevant document extracts.

Variant generation produces bespoke scenario cards containing:

GDPR article text (extracted, no AKG dependency)

Industry context and locale/national law specifics (UAVG provisions, AP guidance)

Chatbot scope and limitations

Evaluation criteria (from gdpr_evaluation_criteria YAML)

Probe seeds (client-specific, not generic)

Probe seed generation: For each variant, the Bespoke skill generates client-specific probe seeds by: (1) extracting relevant procedures, contact methods, and commitments from the enriched context package, (2) parameterising the parent probe template with these extracted elements, (3) generating 3–5 distinct probe phrasings per variant to ensure coverage of edge cases. Generated probes are reviewed by the human gate before testing execution.

Hierarchical context curation: The Bespoke phase curates the Judge’s context using progressive disclosure. Rather than loading all available rules, it selects per scenario: Layer 1 general auditor principles (always loaded), Layer 2 domain-specific requirements relevant to this scenario family (from EDPB D1), and Layer 3 audit procedure steps for this specific test (from EDPB D2, filtered to top 3 most relevant rules). This prevents context overload that degrades Judge performance.

Critical design decision: The bespoke scenario card is the single source of truth for legal grounding. No separate knowledge graph or retrieval system is required. The Judge receives all context pre-curated by Bespoke.

3.5 Testing Target

Adversarial testing of the client’s chatbot using Inspect/Petri framework. The Auditor LLM executes probe seeds from bespoke scenarios against the target chatbot, generating conversation transcripts.

Operating parameters:

Auditor uses temperature 0.8–0.9 for probe variation

Each scenario produces one or more multi-turn conversations

Transcripts stored with full provenance (model, timestamp, scenario ID, configuration)

Inspect logging and trace primitives reused, not rebuilt

Transcript completeness requirements: Each stored transcript MUST include: full conversation turns with speaker labels (User / Chatbot), timestamps for each turn (relative or absolute), scenario ID and probe seed identifier, and model and configuration parameters used for generation. Transcripts missing required fields are rejected at the Judge input gate.

3.6 Judge

Downstream evidence evaluator. Judge does not plan, retrieve, or generate scenarios. It receives transcript evidence and evaluates against pre-curated criteria from the bespoke scenario card.

3.6.1 Blind Stateless Evaluation

The Judge receives ONLY the conversation transcript and the bespoke scenario card. It has no access to: full client documentation, other scenarios or transcripts from the same engagement, or prior Judge verdicts. This ensures each evaluation is purely evidence-linked to the provided transcript.

3.6.2 Hierarchical Prompt Architecture

The Judge prompt is structured in three layers, mirroring the EDPB’s own separation of principles, requirements, and methodology:

Layer 1 — General Auditor Principles (always loaded): Universal principles governing how a GDPR auditor reasons. Derived from GDPR Articles 5–6 and EDPB general audit guidance. Includes: independence (evaluate without bias), proportionality (severity matches evidence), evidence-based reasoning (cite specific transcript evidence), conservatism (ambiguous evidence yields UNDECIDED, not INFRINGEMENT), scope discipline (evaluate ONLY the specific obligation in the scenario), and transparency (reasoning must be traceable by a human reviewer).

Layer 2 — Domain-Specific Requirements (per scenario family): What a compliant system must do for this type of obligation. Sourced from EDPB D1 Frontend Requirements document. Loaded per scenario family, curated during Bespoke phase.

Layer 3 — Audit Procedure (per specific test): How to check whether a specific requirement is met. Sourced from EDPB D2 Audit Methodology document. Filtered to top 3 most relevant rules per scenario to prevent context overload (validated by A/B testing: unfiltered context degrades performance).

Empirical finding: Context engineering A/B testing across 12 calibration cases showed that injecting all matched EDPB rules (unfiltered) reduces Judge accuracy compared to the generic prompt. Filtered context (≤3 rules per case) is required. The scoring rubric correctly enforces strict signal precision at per-turn level, consistent with audit methodology: assess one targeted violation per evaluation.

3.6.3 Evaluation Levels

Per-turn evaluation: Assess each chatbot response against the specific violation targeted by the scenario. Input: single turn + bespoke scenario card (including GDPR article text, Layer 1–3 context, evaluation criteria). Output: canonical verdict (INFRINGEMENT / COMPLIANT / UNDECIDED) + evidence-linked rationale + confidence score with explanation.

Per-scenario aggregation: Review all turns for one scenario and produce a scenario-level finding. Aggregation uses explicit rules:

INFRINGEMENT if any turn contains an INFRINGEMENT verdict, unless the chatbot explicitly retracts or corrects the violation in a subsequent turn

COMPLIANT if all turns are COMPLIANT, or if the only non-compliant turns are UNDECIDED and do not constitute a pattern

UNDECIDED if the majority of turns are UNDECIDED and no clear INFRINGEMENT pattern emerges

Aggregation rules are parameterised per scenario family and documented in the bespoke scenario card.

Cross-scenario analysis (Scout) is a bonus capability, not critical path. Per-scenario findings are the core deliverable. At the aggregation and cross-scenario levels, additional signals beyond the targeted violation become valid findings (unlike per-turn, where strict signal precision applies).

3.6.4 Judge Output Requirements

The Judge output schema includes:

verdict: INFRINGEMENT / COMPLIANT / UNDECIDED (canonical, normalised via verdict mapper)

signals: from taxonomy-validated allowed set only; strict precision at per-turn level

citations: GDPR article references linked to specific findings

rationale: human-readable reasoning chain showing evidence → principle → conclusion. For each signal, cite the specific transcript turn, state the GDPR principle or requirement violated, and explain why evidence is sufficient or insufficient

confidence: evidence sufficiency score (0.0–1.0) with explanation. 1.0 = clear direct evidence, 0.5 = ambiguous or partial evidence, 0.0 = insufficient evidence for any conclusion

3.6.5 Judge Design Principles

Canonical verdict vocabulary with strict normalisation (mapper + taxonomy gate)

Offline/batch operation for reproducibility and cost control

Replay capability against stored transcripts for model/rubric upgrades

Fail-closed behaviour for missing critical dependencies

Model-agnostic: Judge works with any SOTA LLM, selected via bake-off

Output shape that Reporting can consume without reinterpretation

3.6.6 Existing Codebase Foundation

The Judge is not built from scratch. Existing components include: verdict mapper with legacy alias handling (VIOLATED → INFRINGEMENT), 12 calibration cases across 10+ GDPR violation types, offline judge runner with CLI and batch mode, TEST-J02 schema validation (passing), TEST-J03 accuracy measurement (implemented), and 307 extracted EDPB audit rules in structured YAML. TEST-J01 (consistency) remains a placeholder pending prompt stabilisation.

3.7 Reporting

Converts Judge outputs into three audience-specific report layers:

Evidence immutability (v1.0): All artefacts used in report generation (transcripts, Judge verdicts, bespoke scenario cards) will be hashed at persistence boundaries using SHA-256. Report appendices will include hashes and a manifest file linking findings to specific artefact hashes. For v0.1, one skill demonstrates the hashing pattern; full implementation is a v1.0 requirement.

4. Scope and Non-Goals

4.1 Phase 0 Scope

GDPR framework only (no ISO 27001, ISO 42001, EU AI Act)

External-facing single-role chatbots only

Netherlands as locale baseline, municipality sector, English + Dutch

Skills-based architecture with Codex as primary orchestrator

Model-agnostic LLM tasks (no vendor lock-in); candidates include Gemini Flash (strong legal bench), Mistral Large, Claude Sonnet

LLM council for Intake tasks; single LLM for Judge v0.1 (council evaluated based on failure modes)

Manual human gates at Intake tasks; automated schema gates at skill boundaries

4.2 Explicit Non-Goals

No SaaS platform (reports delivered as PDF/documents)

No subscription monitoring service

No multi-framework audits

No internal multi-role chatbot testing

No AI agent testing (tool-use, autonomous actions)

No legally binding compliance certification

No AKG in v0.1 (legal context embedded in bespoke scenario cards; AKG evaluated for future Judge enrichment based on empirical need)

4.3 Framework Extensibility

Adding EU AI Act or ISO frameworks requires: new evaluation criteria YAML, new scenario families, updated Intake document checklist. The Judge logic, orchestration pattern, hierarchical prompt architecture, and reporting structure remain unchanged. The EU AI Act’s implementing acts and harmonised standards are still being finalised (as of March 2026), so scenario precision will initially be lower than GDPR.

5. Required Artefacts and Outputs

5.1 Per-Engagement Artefacts

5.2 System Artefacts (Reusable)

Standard Scenario Library (versioned parent scenarios with tags)

GDPR Evaluation Criteria YAML (v1.0 exists, VIOLATED → INFRINGEMENT aligned)

GDPR Folder Checklist (comprehensive YAML from deep research)

EDPB D2 Audit Rules (307 rules extracted, structured JSON/YAML)

EDPB D1 Frontend Requirements (to be extracted for Layer 2 context)

Layer 1 General Auditor Principles (curated set, to be defined)

AIGov Terminology File

Golden Set (12 calibration cases across 10+ violation types)

Judge verdict mapper and schema validator

Dutch UAVG/AP municipality-specific guidance mapping

6. Acceptance Criteria

6.1 v0.1 (Phase 0 Target)

Judge skill evaluates golden set cases and produces canonical verdicts with evidence-linked reasoning and confidence scores

Judge aggregation logic validated against 5+ multi-turn scenarios with known ground truth outcomes

One Intake skill processes test documents and produces schema-validated output

Deterministic gate between Judge and Intake skill enforces schema validation; Codex cannot bypass

Codex orchestrates handoff between the two skills (file transition, gate check, escalation on failure)

One skill has full eval suite: golden set accuracy measurement, logging with hash, artefact stored correctly

Judge accuracy ≥80% on golden set across violation types (per-turn evaluation)

Deterministic gate blocks invalid outputs (tested with deliberately malformed input)

Skills designed for Codex skill format (primary) with awareness of Anthropic skill best practices

6.2 v1.0 (Full Flow)

End-to-end pipeline: Intake → Scenario Selection → Bespoke → Testing → Judge → Report

Produces a complete three-layer report from a real or simulated engagement

At least one framework (GDPR) fully operational with scenario library coverage

Evidence immutability: hashing at all persistence boundaries with manifest

7. Critical Risks

8. Architecture Alternatives

8.1 Option A: Skills + Codex Orchestration (Current)

Current Phase 0 approach. Individual LLM tasks as self-contained skills with strict I/O contracts. Codex manages file transitions, gate checks, and error recovery. Human gates at Intake boundaries.

Advantages: Flexible recovery, model-agnostic per skill, independently testable, matches non-engineer operating model.

Disadvantages: Codex behaviour non-deterministic (may attempt to modify outputs), orchestration in prompts not code.

Mitigation: Hard guardrails in Codex instructions, deterministic schema gates code-validated, hash verification for critical artefacts.

8.2 Option B: Inspect-Native Pipeline

Verdict: Use Inspect for Testing Target stage only. Inspect is designed for evaluation, not multi-stage document processing. Intake and Judge remain independent skills.

8.3 Option C: Deterministic Code Pipeline

Verdict: Rejected based on 3 months of empirical evidence. Proved brittle, inflexible, and required code changes for each new scenario type. The skills-based approach was adopted specifically because this failed.

8.4 Option D: Hybrid — Skills with Deterministic Scaffolding (Future)

Skills-based tasks (Option A) with a thin deterministic Python layer handling only: file I/O, schema validation, gate enforcement, and hash generation. Natural evolution of Option A when skills are stable.

Phase 0: Pure skills + Codex orchestration (skills are still fragile; don’t lock in deterministic code prematurely). Phase 1+: Add deterministic scaffolding once skills produce reliable outputs and reproducibility needs increase.

9. Phased Plan

9.1 Phase 0: Skeleton Proof (v0.1)

Objective: Prove skills-based architecture works and Judge can reliably evaluate GDPR compliance from transcript evidence.

Entry criteria: Golden set (12 cases, exists), Judge codebase (verdict mapper, offline runner, exists), GDPR evaluation criteria YAML (v1.0, exists), EDPB D2 rules (307 extracted, exists), Dutch UAVG/AP municipality mapping (exists), Codex skills format documented.

Deliverables:

Judge skill with hierarchical prompt (Layer 1–3), evaluated against golden set

One Intake skill with schema-validated output

One deterministic gate enforced between the two skills

One automated Codex orchestration between two consecutive skills

EUSAIR pilot demo: functional Judge capability demonstration

Exit criteria:

Judge accuracy ≥80% on golden set across violation types

Judge aggregation validated against 5+ multi-turn scenarios

Deterministic gate blocks invalid outputs

Codex orchestrates skill handoff without manual intervention

One skill demonstrates: eval results logged, output hashed, artefact stored

9.2 Phase 0: Full Flow (v1.0)

Objective: Complete pipeline from Intake through Report.

Entry criteria: v0.1 exit criteria met, ≥10 parent scenarios, variant generation protocol defined.

Exit criteria:

One simulated engagement runs end-to-end without manual intervention beyond human gates

Three-layer report generated and reviewable by GDPR-knowledgeable person

Evidence immutability: hashing at all persistence boundaries

9.3 Phase 1: Commercial Validation

Objective: Deliver paid engagements and validate commercial viability.

What must be true before heavy implementation:

At least 1 paying client confirms report is decision-useful

Judge accuracy validated on real (not synthetic) chatbot transcripts

Intake pipeline handles real client documents without manual rework

The documentation-vs-behaviour delta is visible and valued by CCO

9.4 Dependencies

10. Strategic Positioning

10.1 Competitive Moat

AIGov’s moat is the delta between documentation claims and system behaviour. GRC tools handle documentation. Security vendors handle testing. No existing product combines adversarial LLM testing with regulatory framework mapping to verify whether AI systems behave according to their GDPR documentation.

10.2 Integration Strategy

Do not compete with GRC tools on documentation management. Position AIGov as complementary verification layer. Explore integration partnerships when Intake phase is developed.

10.3 Framework Expansion

GDPR is the MVP framework. EU AI Act is the natural second (August 2026 deadline). Architecture supports framework addition through new evaluation criteria, scenario families, and intake checklists without structural changes.

End of Document

AIGov PRD v0.2 — Phase 0 — March 2026
