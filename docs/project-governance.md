# AIGov Project Governance

**Purpose**: Persistent rules and checklists Claude reads EVERY session  
**Status**: Living document - Claude updates when governance changes  
**Last Updated**: 2025-12-15

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
- [ ] `/docs/specs/scenario-card-schema.md` - Currently v1.2
- [ ] `/schemas/behaviour_json_v0_phase0.schema.json` - Currently v0

---

## Consistency Checks

### Weekly (During Active Development)
- [ ] Variable-registry vs actual schema usage
- [ ] File-registry vs actual repo files
- [ ] Phase 0 plan vs completed deliverables

### Monthly (Or End-of-Phase)
- [ ] **Codex Analysis**: File structure, naming conventions, orphaned files
- [ ] **ChatGPT Analysis**: Schema consistency, redundancy detection, documentation gaps
- [ ] **Manual Review**: Variable registry completeness, cross-schema alignment

### Audit Prompts

**Codex (Claude Code)**:
```
Analyze /Aigov-specs repository structure:
1. Check all YAML files validate against declared schemas
2. Detect duplicate variable definitions across schemas
3. Flag inconsistent naming conventions (compare vs file-registry.md)
4. Report orphaned files (exist in repo but not in file-registry.md)
5. Check cross-references (scenario_id usage, framework consistency)

Generate report: findings + recommendations
```

**ChatGPT**:
```
Review AIGov project at https://github.com/Standivarius/AiGov-specs:
1. Schema redundancy: Are variables defined multiple times?
2. File organization: Does structure match file-registry.md?
3. Documentation gaps: Missing specs for implemented features?
4. Naming inconsistencies: Violations of naming conventions?
5. Dependency conflicts: Circular dependencies or broken references?

Generate report: issues + priority ranking
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
- **kebab-case**: File names only (`scenario-card-schema.md`)

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
1. This file (`/docs/project-governance.md`) - governance rules
2. `/docs/specs/file-registry.md` - current project files
3. `/docs/planning/Phase-0-Detailed.md` - current phase status

**Then Claude checks**:
- Are registries out of sync? (flag for update)
- Are there pending "TODO: update X" items? (remind Marius)
- Has it been >10 messages? (suggest consistency check)

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
- Run consistency audit at end of each phase
- Update custom instructions when governance patterns emerge

### For Claude
- Read project-governance.md FIRST every session
- Flag registry drift within 3 messages
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