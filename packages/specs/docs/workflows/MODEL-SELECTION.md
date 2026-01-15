# AIGov Model Selection Guide

**Purpose**: Choose the right AI tool for each task based on benchmark performance and use case fit.

**Date**: 2025-12-12  
**Models**: GPT-5.2 (Codex), Gemini 3.0 (Antigravity), Claude Opus 4.5 (Claude Code)

---

## BENCHMARK SUMMARY

| Benchmark | GPT-5.2 | Gemini 3.0 | Opus 4.5 | What It Measures |
|-----------|---------|------------|----------|------------------|
| **ARC-AGI-2** | **53%** | 45% | 37% | Original thinking, novel problem solving |
| **SWE-bench** | **Leader** | Good | Good | Coding (real-world repo tasks) |
| **MMLU-Pro** | 94%+ | **96%** | 92% | Knowledge breadth |
| **Multilingual** | Good | **Best** | Good | Translation accuracy |
| **Context** | 128k | **2M** | 200k | Long document handling |

---

## TASK ASSIGNMENTS

### 1. ORIGINAL THINKING & NEW APPROACHES
**Use**: **GPT-5.2** (Codex)  
**Why**: 53% ARC-AGI-2 (highest), best at novel problem solving  
**Tasks**:
- Architecture alternatives (when stuck)
- Novel scenario designs (compliance test patterns)
- Framework integration strategies
- "How might we...?" questions

---

### 2. CODING & TECHNICAL IMPLEMENTATION
**Use**: **GPT-5.2** (Codex)  
**Why**: SWE-bench leader, direct repo access  
**Tasks**:
- All Python code (scenarios, configs, Judge, pipelines)
- Inspect/Petri integration
- Template generation (Jinja2, JSON schemas)
- OpenRouter wrapper
- IntakeAgent implementation
- File operations (install, config, testing)

---

### 3. STRATEGY & COMPREHENSIVE PLANNING
**Use**: **Gemini 3.0** (Antigravity)  
**Why**: 2M context = sees entire project in one view  
**Tasks**:
- Deep research (competitive analysis, market intel)
- Long-form planning (Phase 2-3 detailed specs)
- Multi-document synthesis (GDPR + ISO + AI Act cross-mapping)
- Framework comparison (when evaluating 3+ options)
- Scenario gap analysis (reviewing all 111 Petri scenarios)

---

### 4. LEGAL REASONING & COMPLIANCE
**Use**: **Claude Opus 4.5** (Claude Code)  
**Why**: Nuanced reasoning, GDPR interpretation depth  
**Tasks**:
- GDPR article interpretation (ambiguous cases)
- Violation severity assessment
- Legal language validation (L2 reports)
- Framework mapping logic (scenario → article)
- Compliance recommendations (what clients must do)

---

### 5. TRANSLATION (RO ↔ EN)
**Use**: **Gemini 3.0** (Antigravity) or **GPT-5.2** (Codex)  
**Why**: Both top multilingual benchmarks  
**Tasks**:
- RO transcript → EN (for Judge input)
- EN reports → RO (for Romanian clients)
- Legal term preservation (GDPR terminology)
- Validation: Does translation maintain legal meaning?

**Backup**: Opus 4.5 (if Gemini/GPT fail on legal nuance)

---

### 6. REPORT WRITING (L1/L2/L3)
**Use**: **Claude Opus 4.5** (Claude Code)  
**Why**: Natural prose, audience adaptation, concise executive summaries  
**Tasks**:
- L1 reports (Board/Executive - 5 pages)
- L2 reports (Compliance/Legal - 15-20 pages)
- L3 reports (Technical/CISO - 40-60 pages)
- Recommendations sections (IMMEDIATE/SHORT-TERM/LONG-TERM)
- Audit prep documents (interview scripts, timelines)

---

### 7. ARCHITECTURE DECISIONS
**Use**: **Claude Opus 4.5** (Claude Code)  
**Why**: Tradeoff analysis, challenge assumptions, long-term thinking  
**Tasks**:
- Technical choices (Inspect vs DeepEval vs Custom)
- Data architecture (AKG vs RAG vs hybrid)
- Translation architecture (edges vs throughout)
- Framework stacking (GDPR → ISO → AI Act order)
- ADR documentation (Context/Decision/Rationale/Consequences)

---

## WORKFLOW PATTERNS

### Pattern 1: Research → Decision → Implementation
1. **Gemini 3.0**: Deep research (competitive analysis, options evaluation)
2. **Opus 4.5**: Strategic decision (tradeoffs, ADR)
3. **GPT-5.2**: Technical implementation (code)

**Example**: Choosing evaluation framework
- Gemini: Research Inspect vs DeepEval (38KB analysis)
- Opus: Decide based on criteria (ADR-0005)
- Codex: Install Inspect, integrate Petri

---

### Pattern 2: Code → Review → Refine
1. **GPT-5.2**: Generate code (fast, SWE-bench optimized)
2. **Opus 4.5**: Code review (architecture, edge cases)
3. **GPT-5.2**: Refine based on feedback

**Example**: IntakeAgent implementation
- Codex: Build Claude Skill pattern
- Opus: Review prompts, logic flow
- Codex: Refine based on review

---

### Pattern 3: Multi-Document Synthesis
1. **Gemini 3.0**: Read all documents (2M context)
2. **Opus 4.5**: Synthesize findings (nuanced interpretation)
3. **GPT-5.2**: Generate structured output (JSON, tables)

**Example**: Scenario gap analysis
- Gemini: Read all 111 Petri scenarios + GDPR taxonomy
- Opus: Map scenarios → GDPR groups, identify gaps
- Codex: Generate scenario-catalog.json

---

## WHEN TO SWITCH MODELS

### Switch from Codex to Opus if:
- Code works but architecture feels wrong
- Need to challenge approach (bias check)
- Legal interpretation required (GDPR nuance)
- Report writing (L1/L2/L3)

### Switch from Opus to Gemini if:
- Need to review 50+ documents
- Multi-framework cross-mapping (GDPR + ISO + AI Act)
- Deep competitive research (VerifyWise + Confident AI + CISO Assistant)

### Switch from Gemini to Codex if:
- Research done, need to implement
- Code generation from specs
- File operations (install, config, testing)

---

## CURRENT PHASE ASSIGNMENTS

### Phase 0 (Foundation)
- **Codex** (GPT-5.2): Inspect install, Petri integration, template generation
- **Opus 4.5**: Report structure design, ADR documentation, architecture decisions
- **Gemini 3.0**: Deep research (if needed for Phase 1 planning)

### Phase 1 (Prototype)
- **Codex**: IntakeAgent, Judge pipeline, AKG/RAG integration
- **Opus**: GDPR interpretation, scenario mapping, report writing
- **Gemini**: Scenario gap analysis (111 Petri → GDPR groups)

### Phase 2 (Evaluation)
- **Codex**: Eval-app test harness, automated testing
- **Opus**: Evaluation metrics design, consistency analysis
- **Gemini**: EDPB case synthesis (ground truth dataset)

---

## ANTI-PATTERNS (Don't Do This)

❌ **Codex for legal interpretation** (use Opus)  
❌ **Opus for bulk code generation** (use Codex)  
❌ **Gemini for short code tasks** (overkill, use Codex)  
❌ **Single model for everything** (leverage each strength)  
❌ **Switching models mid-task** (context loss, finish first)

---

## QUICK DECISION TREE

```
START: What's the task?
│
├─ Code? → GPT-5.2 (Codex)
├─ Legal reasoning? → Opus 4.5 (Claude Code)
├─ Read 50+ docs? → Gemini 3.0 (Antigravity)
├─ Novel approach? → GPT-5.2 (Codex) - highest ARC-AGI-2
├─ Write report? → Opus 4.5 (Claude Code)
├─ Translate RO↔EN? → Gemini 3.0 or GPT-5.2
└─ Architecture decision? → Opus 4.5 (Claude Code)
```

---

**Last Updated**: 2025-12-12  
**Review**: After each phase (update based on actual performance)