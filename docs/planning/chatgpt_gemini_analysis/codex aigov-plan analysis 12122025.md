# AIGov Implementation Plan Review (Codex) — Material Issues & Integration Gaps

**Scope reviewed (AiGov-specs):**
- `docs/planning/Master-Plan-v3.md`
- `docs/planning/Phase-0-Detailed.md`
- `docs/planning/Decision-Log.md`
- `docs/progress-tracker.html`
- `docs/workflows/MODEL-SELECTION.md`
- `projects/scenario-forge/README.md`
- Sub-project READMEs: `projects/intake-agent/README.md`, `projects/report-gen/README.md`, `projects/dashboard/README.md`, `projects/judge/README.md`, `projects/akg/README.md`, `projects/rag/README.md`

**Important context applied:** ADR-0005 (2025-12-12) switches evaluation to **Inspect AI + Petri**, deprecating **Mock Target LLM** and **OpenRouter Wrapper**.

---

## Section 1: Critical Issues (Execution Blockers)

Issue: **Phase 0 deliverables are contradictory across “source-of-truth” docs (Mock Target/OpenRouter still treated as Phase 0 deliverables)**
Location: `docs/planning/Phase-0-Detailed.md` → “DELIVERABLE 4: Mock Target LLM (P2)” and “DELIVERABLE 5: OpenRouter Wrapper (P2)”; `docs/progress-tracker.html` → Phase 0 Deliverables shows items 4 and 5 as pending
Impact: Blocks execution planning because the team will build the *wrong things* in Week 4 (and the tracker will keep reinforcing that plan), directly contradicting ADR-0005 and the Master Plan’s Phase 0 deliverables list.
Recommendation: Update Phase 0 deliverables everywhere to match ADR-0005 + Master Plan:
- Replace Deliverable 4/5 with **“Inspect + Petri Setup (1–2 days)”** and either (a) move IntakeAgent into Phase 1, or (b) define a minimal “Wizard-of-Oz” Intake for Phase 0.

Issue: **Inspect + Petri setup is a Phase 0 deliverable in the Master Plan but is missing from the detailed plan and tracker**
Location: `docs/planning/Master-Plan-v3.md` → Phase 0 deliverables include “Inspect + Petri Setup”; `docs/planning/Phase-0-Detailed.md` has no corresponding deliverable; `docs/progress-tracker.html` Phase 0 Deliverables list has no “Inspect + Petri Setup”
Impact: Blocks “Phase 0 complete enables Phase 1 start” because Phase 1 depends on actually producing Inspect/Petri transcripts/logs. Without a written setup/runbook and a tracked deliverable, it’s easy to finish “templates” but still be unable to run an eval and generate real evidence.
Recommendation: Add a concrete Deliverable “Inspect + Petri Setup” with:
- prerequisites (Docker Desktop/gVisor expectations on Windows, where logs are written, how to run a single scenario)
- definition of “first test run” and how outputs feed Judge (file paths, formats)
- a short “day-by-day” 1–2 day plan.

Issue: **Core integration contracts are undefined (schemas/paths between Inspect → Judge → ReportGen → Dashboard)**
Location: `projects/judge/README.md` (“behaviour_json_v1 (schema TBD)”); `docs/planning/Master-Plan-v3.md` architecture diagram (“Outputs: Inspect config, Report data, Dashboard params”) without concrete schemas; `projects/intake-agent/README.md` (“Petri config … Dashboard params”) without formats
Impact: Blocks implementation because each sub-project can’t safely proceed in parallel without knowing the exact interface. ReportGen cannot reliably generate annex tables or evidence logs if Judge output is undefined; IntakeAgent can’t emit “Inspect config” if “Inspect config format” is not specified.
Recommendation: Create a minimal “data contracts” spec (even one page) defining:
- **Inspect run config** format (what file, what keys, how scenario selection is represented)
- **Judge input** (what constitutes a transcript; how to point to Inspect logs)
- **Judge output** `behaviour_json_v1` v0.1 schema (fields required for L2/L3 + annexes)
- **ReportGen input** “report_data” schema (maps to template placeholders)
- **Dashboard JSON** schema (what the UI needs to display/configure).

Issue: **Scenario storage format is internally inconsistent (JSON vs JSONL vs “Inspect dataset format”)**
Location: `docs/planning/Decision-Log.md` ADR-0004 shows `scenario.json (Inspect dataset format)`; `docs/planning/Master-Plan-v3.md` references `scenario.json (Inspect dataset format)`; `projects/scenario-forge/README.md` says “Inspect AI dataset format (JSONL with FieldSpec)” but provides a single JSON object example and stores it as `scenario.json`
Impact: Blocks writing the loader/tooling for ScenarioForge + Inspect because the on-disk format is unclear (and will cause avoidable rework once Inspect datasets are actually integrated).
Recommendation: Decide and document one canonical format (recommended: `dataset.jsonl` + optional `fields.json`/FieldSpec) and update ADR-0004 + ScenarioForge README accordingly.

Issue: **Phase 0 “Report Template Suite” scope is far larger than its estimate (3–5 days) and implicitly depends on missing contracts**
Location: `docs/planning/Phase-0-Detailed.md` Deliverable 1 scope includes L1/L2/L3 templates, annexes, audit prep docs, and multiple GRC exports; Master Plan Phase 0 lists the same broad scope
Impact: Blocks execution for a solo founder because the plan does not specify a “minimum viable report” subset. Without a strict cutline, Phase 0 will balloon and crowd out Inspect setup (the real Phase 1 enabler) and/or any Intake work.
Recommendation: Define Deliverable 1 as **two layers**:
- **P0 (Phase 0 must-have):** L1+L2 skeletons + 1 annex (GDPR) + evidence log table + PDF/DOCX generation
- **P1 (defer):** L3, ISO/AI Act annexes, OneTrust/Vanta/VeriifyWise exports (or implement as stub exporters with fixed schema and fake data).

Issue: **Credential/API key and environment prerequisites are not documented anywhere**
Location: Across reviewed docs (no mention of `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY`, `.env`, etc.)
Impact: Blocks repeatable execution (especially on a new machine or CI) and makes “Inspect + Petri setup” non-reproducible. It also prevents outsourcing work or future contributors from running the pipeline.
Recommendation: Add a short runbook for Phase 0 that lists required env vars, how to store them, and the minimal “smoke test” commands to validate provider access.

---

## Section 2: Consistency Gaps (Confusion Risks)

Gap: **Deprecated components still appear as current work (Mock Target LLM, OpenRouter Wrapper)**
Locations: `docs/planning/Phase-0-Detailed.md`, `docs/progress-tracker.html`, `docs/workflows/MODEL-SELECTION.md` (includes “OpenRouter wrapper” as a coding task), `projects/scenario-forge/README.md` (validation step: “Run scenario with Mock Target”)
Risk: Team wastes time building redundant infrastructure; confusion over whether OpenRouter is configured via Inspect or via a custom wrapper; poor prioritization in Week 4.
Recommendation: Replace mentions with “Inspect provider config (OpenRouter supported natively)” and “Synthetic violation generation via Inspect solver patterns”.

Gap: **“Petri transcripts” vs “Inspect logs/transcripts” terminology is inconsistent**
Locations: `projects/judge/README.md` (“analyzes Petri transcripts”) vs `docs/planning/Master-Plan-v3.md` (Judge consumes Inspect transcripts)
Risk: Implementation mismatches on where logs come from and what the Judge input should be (raw chat transcript vs Inspect eval log object).
Recommendation: Standardize wording: “Inspect eval logs (from Petri tasks)” and explicitly define the extraction step.

Gap: **AKG/RAG naming is clear in the Master Plan but not consistently carried into the tracker/UI language**
Locations: `docs/planning/Master-Plan-v3.md` (“Dual Knowledge Systems (RAG + AKG Hybrid)”) vs `docs/progress-tracker.html` (“Knowledge graph (Codex-Petri)” and “Legal corpus (CC-Petri)”)
Risk: Confusion for new contributors and for later productization (AKG/RAG are product concepts; Codex-Petri/CC-Petri are implementation ancestry).
Recommendation: Use both, consistently: “AKG (Codex-Petri)” and “RAG (CC-Petri)”.

Gap: **Deliverable numbering differs between Master Plan and Phase-0 Detailed**
Locations: `docs/planning/Master-Plan-v3.md` Phase 0 deliverables list vs `docs/planning/Phase-0-Detailed.md` deliverables table vs `docs/progress-tracker.html`
Risk: The tracker can’t be trusted; “Phase 0 complete” becomes ambiguous; links/anchors break when people attempt to reconcile.
Recommendation: Pick one canonical deliverable list (Master Plan + ADR-0005), then update the detailed plan and tracker to match.

Gap: **Encoding/character artifacts reduce readability and can cause copy/paste errors**
Locations: All reviewed docs include corrupted glyphs (e.g., “ƒo.”, “dY", “RO ƒ+' EN”)
Risk: Misread status (“DONE” vs “IN PROGRESS”), broken commands/snippets, and reduced professional polish when sharing docs externally.
Recommendation: Normalize files to UTF-8 (no BOM) and replace symbol-based status markers with plain text (e.g., DONE/IN PROGRESS/PENDING).

---

## Section 3: Architecture Validation

### Does the Inspect + Petri + Judge + AKG/RAG pipeline make sense?
Yes, at a high level the architecture is coherent:
- **Inspect + Petri**: generates standardized adversarial test runs and produces rich, structured logs.
- **Judge**: transforms logs/transcripts into **structured compliance findings** (GDPR/ISO mappings), using:
  - **AKG** for “what the law says” / deterministic confirmation and overlays
  - **RAG** for supporting evidence/citations (cases, guidance)
- **ReportGen**: renders findings into human-facing L1/L2/L3 outputs and annexes
- **Dashboard**: config + execution UX and visibility.

### Are integration points well-defined?
Partially. The *conceptual* integration points are described, but the **implementation contracts are missing**:
- What exactly is the “transcript” Judge consumes (raw text vs Inspect log JSON)?
- How are scenarios selected and configured (Inspect config schema; where stored; how Intake outputs map)?
- What is the minimum stable schema for findings (`behaviour_json_v1`) that ReportGen can depend on?

### Is the data flow clear (transcript → Judge → reports)?
The intended flow is clear in `docs/planning/Master-Plan-v3.md`, but the detailed execution plan does not operationalize it.

Recommended concrete flow to document (minimal v0.1):
1. **Inspect run** writes `eval-log.json` (or folder of logs) + extracted `transcript.txt/json`
2. **Judge** consumes `eval-log.json` (preferred) and outputs `behaviour_json_v1.json`
3. **ReportGen** consumes `behaviour_json_v1.json` + scenario metadata and outputs `L1.pdf`, `L2.pdf`, `annex_gdpr.pdf`, plus export stubs.

### Are tools properly scoped (what each does)?
Mostly, with two scope risks:
- “Synthetic Target LLM / Mock Target” should be reframed as **Inspect solver patterns** (not a separate Deliverable 4).
- “OpenRouter Wrapper” should be reframed as **Inspect provider configuration** (not a separate deliverable), unless you have a non-Inspect use case that truly requires it.

---

## Section 4: Timeline & Feasibility (Phase 0)

### Is 3–4 weeks realistic for 5 deliverables?
As currently written across docs: **not reliably**. The timeline is feasible only if Phase 0 is re-scoped to match ADR-0005 and if Deliverable 1 is narrowed.

Primary feasibility problems:
- `docs/planning/Phase-0-Detailed.md` Week 4 allocates time to deprecated Deliverables (Mock Target + OpenRouter Wrapper) instead of Inspect+Petri setup.
- Deliverable 1 (reports) includes too many outputs (multiple report levels + annexes + audit prep docs + multiple GRC exports + bilingual output) for 3–5 days, especially without fixed schemas.

### Are parallel tasks feasible for a solo founder?
Parallel tasks are listed (“IntakeAgent … parallel”), but for a solo founder, true parallelization is limited. Without stable contracts, “parallel” work increases rework risk.

### Are dependencies properly sequenced?
Key dependency missing: **Inspect+Petri setup should precede** any work that relies on real transcripts/logs (even if Phase 0 uses fake data, Phase 0 success criteria explicitly includes a working eval setup in the Master Plan).

### Does Phase 0 end enable Phase 1 start?
Not guaranteed until:
- Inspect+Petri setup is completed and documented, and
- the Judge/ReportGen contract is stabilized (even a minimal v0.1 schema).

---

## Section 5: Recommendations (Prioritized)

### 1) Immediate (before starting Phase 0 execution)
1. **Synchronize Phase 0 deliverables across all docs**: update `docs/planning/Phase-0-Detailed.md` and `docs/progress-tracker.html` to remove Mock Target/OpenRouter Wrapper and add “Inspect + Petri Setup (1–2 days)”.
2. **Write v0.1 data contracts**: define the minimal JSON schemas and file paths that connect Inspect → Judge → ReportGen (+ Dashboard config surfaces).
3. **Decide scenario storage format**: choose JSON vs JSONL (and file naming) and update ADR-0004 + ScenarioForge README.
4. **Add a credentials/prereqs runbook**: minimal env vars + smoke tests for Inspect providers on Windows.

### 2) Short-term (fix during Phase 0)
1. **Rescope Deliverable 1** to a strict “minimum viable report” subset (L1/L2 + GDPR annex + evidence log) and treat the rest as Phase 1 backlog.
2. **Standardize terminology** across READMEs: “Inspect eval logs (from Petri)” and “AKG (Codex-Petri) / RAG (CC-Petri)”.
3. **Clean file encodings** to UTF-8 and replace symbol glyphs with plain status text.

### 3) Long-term (document for Phase 1+)
1. **Pin down AKG/RAG “existing locally” reality**: record the actual local paths/repos and DB choices (or explicitly mark as deferred with a plan).
2. **Define multilingual QA protocol** (RO→EN reasoning→RO outputs) tied to ADR-0001 and measurable acceptance criteria.
3. **Document exporter strategy** (OneTrust/Vanta/VeriifyWise): “real adapters” vs “spec-only stubs” per phase.

---

## Quick Answers to Your Specific Checks

- Inspect + Petri consistently referenced? **No** (Master Plan + ADR-0005 yes; Phase-0 Detailed + progress tracker + ScenarioForge validation steps still assume deprecated components).
- Mock Target LLM and OpenRouter Wrapper fully removed? **No** (`docs/planning/Phase-0-Detailed.md`, `docs/progress-tracker.html`, `docs/workflows/MODEL-SELECTION.md`, `projects/scenario-forge/README.md`).
- Phase 0 timeline reflect Inspect setup (1–2 days)? **Only in ADR-0005 and Master Plan**; not in Phase-0 Detailed or tracker.
- Petri’s 111 scenarios mentioned in ScenarioForge? **Yes** (`projects/scenario-forge/README.md`).

