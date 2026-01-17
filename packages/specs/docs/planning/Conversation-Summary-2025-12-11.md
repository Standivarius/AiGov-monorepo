# AIGov Planning Session Summary (Dec 11, 2025)

**Purpose**: This document summarizes the organizational skeleton setup for AIGov. Upload to Claude Project Knowledge for context in future chats.

---

## WHAT WAS ACCOMPLISHED

### 1. Repository Structure Initialized
- **Aigov-specs**: Master planning repo (architecture, specs, tasks)
  - URL: https://github.com/Standivarius/AiGov-specs
  - Structure: docs/planning, docs/architecture, projects/
- **Aigov-eval**: Separate evaluation system repo
  - URL: https://github.com/Standivarius/Aigov-eval

### 2. Master Planning Documents Created
- **Master-Plan-v3.md**: Complete project plan (phases, architecture, decisions)
- **Phase-0-Detailed.md**: Detailed Phase 0 deliverables with timelines
- **Decision-Log.md**: Chronological decision history
- **README.md**: Entry point with quick links

### 3. Sub-Project Skeletons Created (7 total)
Each project has: README.md, TASKS.md, RESEARCH.md

- **IntakeAgent**: AI-dynamic onboarding questionnaire
- **ScenarioForge**: Scenario pipeline creation
- **Judge**: Multilingual transcript analysis
- **ReportGen**: L1/L2/L3 report generation
- **Dashboard**: Central control panel
- **AKG**: Knowledge graph (Codex-Petri)
- **RAG**: Legal corpus (CC-Petri)

### 4. Dashboard Mockup Built
- **Location**: `projects/dashboard/static/dashboard-mockup.html`
- **Tech**: Single HTML file + Tailwind CSS (no build)
- **Tabs**: 7 tabs covering all configurable variables
- **Usage**: Double-click to open, visual reference during development

---

## KEY ARCHITECTURAL DECISIONS

### Translation Architecture (ADR-0001)
- **Canonical English pipeline**: All reasoning in EN
- **Translation at edges**: RO transcript → EN (Judge internal) → RO reports
- **Single LLM**: No separate translator (avoid context loss)
- **Candidate**: Gemini 2.0 Flash Thinking (1M context, top multilingual)

### Scenario Storage (ADR-0004)
- **NOT in AKG**: Scenarios stored as file structure
- **Location**: `scenarios/scenario-001-email-leak/` folders
- **Rationale**: Scenarios = test definitions, AKG = legal knowledge (separation)

### Dashboard Technology
- **Phase 1**: HTML + Tailwind (static mockup) ✅ DONE
- **Phase 2**: Streamlit or Next.js (functional, later)

### IntakeAgent Pattern
- **Approach**: Claude Skill pattern (AI-dynamic)
- **NOT using**: Deterministic form platforms (Typeform, Fillout)
- **Phases**: Initial questions → Doc extraction → Output generation

### Synthetic Target LLM
- **Approach**: Standard LLM + instructional layer
- **Prompt**: "You are Target in Petri test, simulate violations"
- **NOT using**: Fine-tuned model (Phase 0 too complex)

---

## TOOL ECOSYSTEM ORGANIZATION

### GitHub (Engineering Truth)
- **Purpose**: Plans, specs, code, decision log
- **Structure**: Aigov-specs (master), Aigov-eval (separate)
- **Why**: Version control, co-located with code, single source of truth

### Google Drive (Deep Research)
- **Purpose**: Gemini research reports (auto-export)
- **Location**: AIGov-Research/ folder structure
- **Link**: https://drive.google.com/drive/folders/1CHKXcmgKRpieDUDC2TmKchHCvPgSBgeCc

### GitHub Projects (Task Tracking)
- **Purpose**: Kanban board (Backlog → Research → In Progress → Done → Blocked)
- **Why**: Native integration, least friction for solo founder
- **NOT using**: Linear (extra tool overhead)

### Notion (Business Strategy Only)
- **Purpose**: Revenue tracking, pilot pipeline, partnerships
- **Links to**: GitHub for engineering details
- **NOT duplicated**: Technical specs live in GitHub only

### Workflow
Notion (business) → GitHub (engineering) → GitHub Projects (tasks) → GDrive (research) → summarized back to GitHub

---

## PHASE 0 PRIORITIES (UPDATED ORDER)

### Priority 1: Report Templates (3-5 days)
- **Why first**: Reports are starting point for discovery calls
- **Scope**: L1/L2/L3 + Annexes + Audit Prep Docs + GRC Exports
- **Tool research**: Jinja2 vs Docxtpl vs Carbone.io
- **Output**: 3 example reports (EN + RO)

### Priority 2: Dashboard Static Mockup ✅ DONE
- Already complete (HTML + Tailwind)

### Priority 3: IntakeAgent (1 week)
- AI-dynamic questionnaire + doc extraction
- Claude Skill pattern (not form platform)

### Priority 4: Mock Target LLM (2-3 days)
- Standard LLM + instructional layer
- Simulates violations for testing

### Priority 5: OpenRouter Wrapper (2-3 days)
- Platform-agnostic LLM client
- Test: Gemini 2.0 vs others

---

## CRITICAL CORRECTIONS FROM THIS SESSION

### 1. Client Onboarding = Single Tool
- **NOT**: Separate questionnaire + audit prep docs
- **YES**: IntakeAgent with 3 phases (questions → docs → outputs)

### 2. Reports BEFORE Questionnaire
- **Old priority**: IntakeAgent first
- **New priority**: Reports first (needed for discovery calls)

### 3. Reporting = Starting Point
- **NOT**: Reports as end product
- **YES**: Reports as conversation starter for discovery calls

### 4. Framework Taxonomy BEFORE Scenarios
- Build GDPR infringement groups (2-3 days)
- Validate with Ally (CISO partner)
- THEN create scenario pipeline

### 5. Dashboard Code → GitHub
- **Location**: `projects/dashboard/static/dashboard-mockup.html`
- **Format**: Single HTML file (no separate CSS/JS)

### 6. Scenarios NOT in AKG
- **Storage**: File structure (`scenarios/scenario-001-email-leak/`)
- **AKG role**: Validation only ("Does X violate Y?")

### 7. Translation = Single LLM
- **NO**: Separate translation service
- **YES**: Judge handles RO↔EN internally

---

## NEXT ACTIONS (IMMEDIATE)

### WEEK 1: Report Template Research & Design
- Day 1: Research template tools (Jinja2, Docxtpl, Carbone)
- Days 2-3: Design L1/L2/L3 structures
- Days 4-5: Build template skeletons

### WEEK 2: Report Content Generation
- Create 3 example scenarios (fake data)
- Generate complete reports (L1/L2/L3)
- Review with Ally (CISO partner)

### WEEK 3: Annexes & IntakeAgent
- Build framework annexes (GDPR, ISO 27001)
- Start IntakeAgent implementation (parallel)

### Buffer: 1 week for iteration

---

## SUCCESS CRITERIA (PHASE 0 COMPLETE)

✅ 3 complete example reports (EN) + 1 (RO)  
✅ Dashboard static mockup (all 7 tabs)  
✅ IntakeAgent working (3 test runs)  
✅ Mock Target LLM (80%+ violation rate)  
✅ OpenRouter wrapper (4 models tested)

**GO/NO-GO**: If all 5 deliverables → Proceed to Phase 1 (First Tracer Bullet)

---

## IMPORTANT PRINCIPLES

### 1. GitHub = Single Source of Truth
- Plans, specs, decisions in GitHub (not duplicated in Notion or Project Knowledge)
- Claude reads directly from GitHub
- Project Knowledge: Only conversation summaries (like this doc)

### 2. Least Friction for Solo Founder
- Tools: HTML+Tailwind (no build), GitHub Projects (not Linear), Claude Skill (not form platforms)
- Speed: Use Codex/Claude Code for generation, focus on design/validation
- Simplicity: Bash scripts over orchestration frameworks (unless complexity demands it)

### 3. Validation Before Expansion
- Test existing systems (CC-Petri, Codex-Petri) before building new
- Manual creation before automation (2 scenarios by hand → then pipeline)
- Framework taxonomy before scenario pipeline

### 4. Reports = Discovery Tool
- Reports start conversations (not end them)
- 3 complete examples needed for client discovery calls
- Quality matters more than quantity

---

## FILE LOCATIONS (QUICK REFERENCE)

- **Master Plan**: `docs/planning/Master-Plan-v3.md`
- **Phase 0 Details**: `docs/planning/Phase-0-Detailed.md`
- **Decision Log**: `docs/planning/Decision-Log.md`
- **Dashboard Mockup**: `projects/dashboard/static/dashboard-mockup.html`
- **Sub-Projects**: `projects/{name}/README.md`

---

## PENDING RESEARCH TASKS

### Tools
- Report templates: Jinja2, Docxtpl, Carbone.io
- Questionnaire platforms: Typeform, Fillout, Tally (likely none fit)
- Scenario pipeline: Prefect, Dagster, Kestra, n8n, bash scripts
- LLM council: Karpathy's implementation?

### Technical
- Inspect AI: LLM abstraction layer (does it exist?)
- Petri: Multilingual capabilities (Slavic/Hindi seeds?)
- CC-Petri & Codex-Petri: Validate installations, query performance

### Legal
- GDPR infringement taxonomy (5 groups, subgroups)
- EDPB cases: Real-world violation patterns
- RO Law 190/2018: Integration with GDPR

---

**Document Purpose**: Context for future Claude sessions  
**Upload to**: Claude Project Knowledge (Settings → Knowledge)  
**Last Updated**: 2025-12-11
