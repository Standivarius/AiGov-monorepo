# AIGov Project Governance

**Purpose**: Persistent rules and checklists Claude reads EVERY session  
**Status**: Living document - Claude updates when governance changes  
**Last Updated**: 2025-12-16

---

## Living Documents (Update on Change)

### Registries (Critical - Keep Synchronized)
- [ ] `/docs/specs/variable-registry.md` - When schemas change
- [ ] `/docs/specs/file-registry.md` - When files added/removed
- [ ] `/docs/planning/Decision-Log.md` - When ADRs made

### Plans (Update Weekly)
- [ ] `/docs/planning/Phase-0-Detailed.md` - Weekly timeline updates
- [ ] `/docs/planning/Master-Plan-v3.md` - Monthly roadmap updates

### Schemas (Version on Breaking Change)
- [ ] `/schemas/scenario_card/scenario-card-schema-v1.2.md` - Currently v1.2
- [ ] `/schemas/behaviour_json_v0_phase0.schema.json` - Currently v0

---

## Consistency Checks

### Every Project Week (End of Week 1, 2, 3, etc.)
**"Weekly" = Every week of active project work, not calendar weeks**

Run these checks at end of each project week:
- [ ] Variable-registry vs actual schema usage
- [ ] File-registry vs actual repo files  
- [ ] Phase 0 plan vs completed deliverables
- [ ] Run Codex comprehensive audit (see below)

### Monthly or End-of-Phase
- [ ] Full ChatGPT analysis (comprehensive PM review)
- [ ] Manual governance review
- [ ] Evaluate governance effectiveness

---

## Comprehensive Project Audit

### Codex Analysis (Every Project Week)
**Technical Health + Business Logic + Documentation Quality**

```
Analyze /Aigov-specs repository from Expert Product Manager perspective:

TECHNICAL HEALTH
1. Schema consistency (variables defined once, used consistently)
2. File organization (matches file-registry, no orphans)
3. Naming conventions (violations flagged)
4. Cross-references (scenario_id usage, framework alignment)
5. Dependency graph (circular dependencies, broken references)

BUSINESS LOGIC
6. Feature completeness (do scenarios cover stated scope?)
7. Framework coverage (GDPR articles vs scenarios - gaps?)
8. Value proposition coherence (does architecture support claims?)
9. Scaling assumptions (will current design support 100 scenarios?)
10. Automation opportunities (manual steps that could be scripted?)

DOCUMENTATION QUALITY
11. Specification clarity (ambiguous requirements?)
12. Decision rationale (ADRs documented for key choices?)
13. Implementation gaps (missing specs for built features?)
14. Onboarding readiness (can new contributor understand system?)

RISK ASSESSMENT
15. Single points of failure (bus factor concerns?)
16. Technical debt accumulation (shortcuts that need addressing?)
17. Scope creep indicators (feature bloat vs core value?)
18. Timeline realism (Phase 0 estimate vs actual progress?)

RECOMMENDATIONS
- Priority ranking (P0/P1/P2)
- Quick wins (< 1 hour fixes)
- Strategic improvements (architectural changes)
- Defer/drop candidates (overengineering to remove)

Generate comprehensive report with actionable findings.
```

### ChatGPT Analysis (Monthly)
**Deep PM Review**

```
Review AIGov project at https://github.com/Standivarius/AiGov-specs:

Perform comprehensive Product Manager analysis covering:
- Technical health (schemas, files, naming, dependencies)
- Business logic (feature completeness, value proposition coherence)
- Documentation quality (clarity, gaps, onboarding)
- Risk assessment (single points of failure, technical debt, timeline)

Provide:
1. Executive summary (top 3 concerns, top 3 wins)
2. Detailed findings by category
3. Prioritized recommendations (P0/P1/P2)
4. Quick wins vs strategic improvements

Format: Professional PM audit report
```

---

## Naming Conventions

### Files
- **Scenarios**: `scenario_NNN_descriptive_name.yaml`
- **Research**: `topic-research-YYYY-MM-DD.md`
- **Schemas**: `schema_name_vX.Y.format`
- **Tests**: `test_component_name.py`
- **Plans**: `Phase-N-Detailed.md` or `topic-plan.md`

### Variables
- **snake_case**: `scenario_id`, `gdpr_articles`, `mock_log_entry`
- **SCREAMING_SNAKE**: `PII_DISCLOSURE`, `VIOLATED`, `COMPLIANT`
- **kebab-case**: File names only (`scenario-card-schema-v1.2.md`)

### Git Commits
- **Format**: `[Type] Brief description`
- **Types**: Add, Update, Remove, Fix, Refactor, Document
- **Examples**:
  - `Add scenario_007: Healthcare email leak test`
  - `Update Phase-0-Detailed: Add Week 2 eval tasks`
  - `Fix variable-registry: Correct risk_category enum`

---

## Change Protocol

### Schema Changes
1. **Propose change** (in conversation)
2. **Impact assessment** (check file-registry dependencies)
3. **Update variable-registry** (add/modify/remove variables)
4. **Update affected schemas** (scenario-card, behaviour_json, etc.)
5. **Update file-registry** (increment version)
6. **Commit with ADR** (if architectural decision)

### File Addition
1. **Check file-registry** (naming conflicts?)
2. **Follow naming conventions**
3. **Add to file-registry** (appropriate section)
4. **Update dependencies** (if applicable)
5. **Commit**: `Add [file]: [purpose]`

### ADR (Architectural Decision Record)
1. **Trigger**: Any decision affecting >1 component or future phases
2. **Document in**: `/docs/planning/Decision-Log.md`
3. **Format**: Date, Decision, Rationale, Alternatives, Impact, References
4. **Numbering**: ADR-NNNN (sequential)

---

## Claude Session Startup Protocol

**EVERY SESSION, Claude reads**:
1. `/docs/project-principles.md` - Development philosophy
2. This file (`/docs/project-governance.md`) - Governance rules
3. `/docs/specs/file-registry.md` - Current project files
4. `/docs/planning/Phase-0-Detailed.md` - Current phase status

**Then Claude checks**:
- Are registries out of sync? (flag for update)
- Are there pending "TODO: update X" items? (remind Marius)
- Has it been >10 messages? (suggest work summary)
- Has it been >15 messages? (suggest consistency audit)

---

## Claude Memory Clarification

**How Claude's memory works**:
- **Within same chat**: I remember EVERYTHING from start to current message
- **New chat**: I only see Project Knowledge docs + userPreferences
- **After 3-week pause**: If you return to THIS chat, I still have full context
- **Project-principles.md**: In Project Knowledge → I read it EVERY new chat

**So**: If you pause this chat for 3 weeks and return, I'll remember our whole conversation. But if you start a NEW chat in 3 weeks, I'll only know what's in Project Knowledge (principles, governance, file-registry).

---

## Escalation Rules

### When Claude Should Stop and Ask
1. **Schema conflict detected** (variable defined differently in 2 places)
2. **Circular dependency found** (A depends on B depends on A)
3. **Breaking change proposed** (would require rewriting existing scenarios)
4. **Governance violation** (new file doesn't follow conventions)

### When Claude Should Auto-Fix
1. **Typos in documentation**
2. **Formatting inconsistencies** (spacing, capitalization)
3. **Minor registry updates** (adding clearly defined file)

---

## Best Practices Reminders

### For Marius
- Use file-registry.md before creating files (avoid duplicates)
- Run consistency audit at end of each project week
- Update custom instructions when governance patterns emerge

### For Claude
- Read project-principles.md + project-governance.md FIRST every session
- Flag registry drift within 3 messages
- Suggest work summary after 10+ messages
- Suggest consistency audit after 15+ messages
- Never propose files without checking file-registry
- Always update registries when schemas/files change

---

## Complexity Guardrails

**Marius's rule**: *"Push back when I add too much theory and complexity"*

### Red Flags (Push Back)
- Abstract frameworks without concrete implementation path
- Governance layers that don't solve active problems
- Premature optimization ("Phase 1 might need...")
- Process overhead exceeding actual work

### Green Lights (Implement)
- Registry systems solving actual confusion ("Where is X defined?")
- Naming conventions preventing real conflicts
- Consistency checks catching real bugs
- Protocols preventing rework

**Test**: If Marius asks "Why do we need this?", and answer is "Best practice" → push back. If answer is "Without this, X broke" → implement.

---

**Next Review**: End of Phase 0 (evaluate governance effectiveness)  
**Maintenance**: Claude updates when governance rules change
