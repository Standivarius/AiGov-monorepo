# AIGov Decision Log

**Purpose**: Chronological record of all major technical and business decisions

---

## ADR-0005: Evaluation Framework Selection

**Date**: 2025-12-12  
**Status**: Accepted  
**Deciders**: Marius (technical/business), Claude (research synthesis)

### Context
Need evaluation framework for LLM security/compliance testing. Options: Inspect AI (UK AISI), DeepEval (Confident AI), or custom build.

### Decision
Use **Inspect AI + Petri** (not DeepEval, not custom).

### Rationale
1. **Agent compatibility**: Future market (3-4 years) moving toward agentic systems; Inspect built for agent evaluation
2. **Petri scenario library**: 111 ready scenarios (GDPR-mapped) = months of work saved
3. **OpenRouter native**: Multi-provider testing built-in (GPT, Claude, Gemini, Mistral)
4. **UK AISI backing**: Government support = long-term stability (critical for solo founder)
5. **Production security**: Docker + gVisor sandboxing essential for red-teaming

### Consequences
✅ **Positive**:
- Faster Phase 0 (no custom orchestration needed)
- Production security built-in (sandboxing, retries, logging)
- Free scenario content (111 scenarios vs building from scratch)
- Agent-ready (future-proof for market evolution)

⚠️ **Neutral**:
- VerifyWise export requires adapter (Inspect logs → DeepEval format)
- Learning curve for Inspect async patterns

❌ **Negative**: None significant

### Alternatives Considered
1. **DeepEval** (Confident AI)
   - ✅ Pytest-like familiarity
   - ✅ RAG metrics built-in
   - ❌ RAG-focused (not our use case)
   - ❌ No built-in sandboxing
   - ❌ Weaker agent support

2. **Custom Build**
   - ✅ Maximum control
   - ❌ 6+ months work
   - ❌ Solo founder risk
   - ❌ No free scenarios

### Implementation Impact
- **Phase 0**: Add "Inspect + Petri Setup" (1-2 days)
- **Phase 0**: Replace "Mock Target" with Inspect solver pattern
- **Phase 0**: Replace "OpenRouter Wrapper" with native Inspect support
- **Phase 1**: Use Petri scenarios directly (select 10 from 111)

### Related Documents
- Master Plan v3: Section 3.5 (Evaluation Engine)
- research/inspect-analysis/ (Codex repo analysis)
- research/petri-analysis/ (111 scenarios catalog)
- research/deepeval-analysis/ (comparative analysis)

---

## ADR-0004: Scenario Storage Architecture

**Date**: 2025-12-11  
**Status**: Accepted

### Decision
Scenarios stored as **file structure** (NOT in AKG).

### Structure
```
scenarios/scenario-001-email-leak/
├── scenario.json (Inspect dataset format)
├── scenario_interpretation.md
├── gdpr-articles.md
├── iso27001-controls.md
└── test-transcripts/
```

### Rationale
- Scenarios = test definitions (what we're testing)
- AKG = legal knowledge (what law says)
- Separation prevents coupling
- Enables independent evolution

---

## ADR-0003: Client Onboarding Architecture

**Date**: 2025-12-11  
**Status**: Accepted

### Decision
Single integrated tool: **IntakeAgent** (NOT separate questionnaire + audit prep docs).

### Three-Phase Structure
1. Initial questions (5-7 only)
2. Document upload & extraction (Claude Skill → Agent SDK pattern)
3. Output generation (Inspect config, report data, dashboard params)

### Tool Selection
AI-enabled dynamic questionnaire (Claude Skill pattern), NOT deterministic branched forms.

---

## ADR-0002: Reporting as Starting Point

**Date**: 2025-12-11  
**Status**: Accepted

### Decision
Reports are **client discovery tool**, not just output.

### Complete Report Structure
- L1 (Board/Executive): 5 pages
- L2 (Compliance/Legal): 15-20 pages with IMMEDIATE/SHORT-TERM/LONG-TERM recommendations
- L3 (Technical/CISO): 40-60 pages with code fixes
- Framework annexes: GDPR article-by-article, ISO control gaps
- Audit prep docs: Required documents (30-40 items), evidence timeline, interview scripts
- GRC exports: OneTrust CSV, Vanta JSON, VeriifyWise API

### Recommendations Section
Each finding includes:
- What happened (evidence)
- Why violation (article + interpretation)
- Severity
- Root cause (CONFIRMED vs INFERRED)
- Remediation (IMMEDIATE/SHORT-TERM/LONG-TERM)

---

## ADR-0001: Translation Architecture

**Date**: 2025-12-11  
**Status**: Accepted

### Decision
**Canonical English pipeline**: All reasoning in EN, translation at I/O edges only.

### Details
- AKG nodes: EN only
- Judge logic: Thinks in EN
- Translation: RO transcript → EN (Judge internal) → RO reports (output)
- Single multilingual LLM: No separate translator (context loss risk)
- Candidate: Gemini 2.0 Flash Thinking

### National Law Storage
- `National_Provision` nodes: `title_en` + `text_original` + `language_code`
- Romanian Law 190/2018: EN summary + original RO text
- Report exports: Reference actual RO law text (avoid double translation)

---

## Pre-ADR Decisions (Informal)

### 2025-12-11: Eval-app as Separate Repo
- Rationale: Systematic testing priority
- Repo: https://github.com/Standivarius/Aigov-eval

### 2025-12-11: Dashboard HTML+Tailwind
- Rationale: Least friction, visual reference
- Location: projects/dashboard/static/dashboard-mockup.html

### 2025-12-11: GitHub as Truth
- Master planning location: GitHub (not Notion)
- Notion: Business strategy only (revenue, partnerships)
- Google Drive: Deep research (Gemini exports)

---

**Document Conventions**:
- ADR format: Context, Decision, Rationale, Consequences, Alternatives
- Status: Proposed, Accepted, Deprecated, Superseded
- Chronological order (newest first)