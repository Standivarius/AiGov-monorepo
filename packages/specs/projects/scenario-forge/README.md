# ScenarioForge

**Purpose**: Scenario pipeline creation and management

---

## Overview

ScenarioForge manages the creation, validation, and organization of security/compliance test scenarios for AIGov audits.

## Scenario Sources

### 1. Petri Library (111 scenarios, GDPR-mapped)
- **Source**: Anthropic's Petri extension for Inspect AI
- **Coverage**: System prompt probing, PII handling, self-preservation, censorship, violence, illicit chemistry
- **GDPR Mapping**: Already mapped by Codex analysis (see research/petri-analysis/)
- **Usage**: Select relevant scenarios for GDPR compliance testing
- **Location**: Anthropic's Petri repo (referenced, not copied)

### 2. Custom GDPR Scenarios
- **Source**: AIGov-created scenarios for articles not covered by Petri
- **Focus**: Compliance-specific tests (transparency, legal basis, data minimization)
- **Storage**: scenarios/ directory (see ADR-0004)

### 3. ISO 27001 Scenarios
- **Source**: Control-specific tests
- **Focus**: Annex A controls (e.g., Access Control, Cryptography, Physical Security)

### 4. EU AI Act Scenarios
- **Source**: High-risk system requirements
- **Focus**: Transparency, human oversight, robustness

## Scenario Format

**Standard**: Inspect AI dataset format (JSONL with FieldSpec)

**Structure**:
```json
{
  "id": "scenario-001-email-leak",
  "input": "Adversarial prompt (Auditor question)",
  "target": "Expected behavior (compliant response)",
  "metadata": {
    "category": "PII disclosure",
    "gdpr_articles": ["Art 5(1)(f)", "Art 32"],
    "iso_controls": ["A.5.33", "A.8.10"],
    "difficulty": "medium",
    "language": "ro"
  }
}
```

**Compatible with**: Petri execution model, Inspect scorers

## Scenario Lifecycle

### 1. Discovery
- Review Petri catalog (111 scenarios)
- Identify gaps (GDPR articles not covered)
- Research EDPB enforcement cases (real-world examples)

### 2. Creation
```
scenarios/scenario-001-email-leak/
├── scenario.json (Inspect dataset format)
├── scenario_interpretation.md (human analysis)
├── gdpr-articles.md (relevant GDPR text)
├── iso27001-controls.md
├── ai-act-articles.md
├── ro-law-190.md (national overlay)
└── test-transcripts/ (validation examples)
```

### 3. Validation
- Run scenario with Mock Target (synthetic violations)
- Judge analysis (violation detection accuracy)
- AKG/RAG queries (correct article retrieval)
- Eval-app testing (consistency, precision)

### 4. Cataloging
- Add to scenario-catalog.md (master index)
- Tag: GDPR articles, ISO controls, difficulty, language
- Link: To test results (Eval-app)

## Taxonomy

### GDPR Groups (Phase 1)
1. **Group 1**: Lawfulness & Transparency (Art 5, 6, 13, 14)
2. **Group 2**: Data Subject Rights (Art 15-22)
3. **Group 3**: Security & Breach (Art 32, 33, 34)
4. **Group 4**: Special Categories (Art 9, 10)
5. **Group 5**: Third-Party & Transfer (Art 44-49, 28)

### Coverage Analysis
- Petri scenarios: Map to GDPR groups
- Gaps identified: Create custom scenarios
- Target: 80%+ article coverage for Phase 1

## Phase 0 Tasks

### Immediate (Week 1)
- [ ] Review Petri catalog (111 scenarios)
- [ ] Select 10 GDPR-relevant scenarios
- [ ] Map to GDPR Groups 1-5
- [ ] Document gaps (articles not covered)

### Near-term (Weeks 2-4)
- [ ] Create 5 custom GDPR scenarios (fill gaps)
- [ ] Validate scenarios with Inspect + Judge
- [ ] Build scenario-catalog.md (master index)

### Phase 1
- [ ] Complete GDPR coverage (all 5 groups)
- [ ] Add ISO 27001 scenarios (20 controls)
- [ ] Build automated scenario pipeline

## Integration

### With Inspect AI
- Scenarios loaded as Inspect datasets
- Executed via Inspect solvers
- Results logged in Inspect format

### With Judge
- Judge consumes Inspect transcripts
- Queries AKG/RAG for violation detection
- Outputs behaviour_json_v1

### With ReportGen
- Scenario results feed into L2/L3 reports
- Framework annexes auto-populated
- Evidence links maintained

## Tools

**Current**: Manual creation (text editor + JSON)

**Future** (Phase 2+):
- Scenario generator (LLM-assisted)
- Automated validation pipeline
- Version control integration
- Scenario marketplace (community-contributed)

## Research

See: `RESEARCH.md` for:
- Petri scenario analysis
- GDPR article mapping
- EDPB case examples
- Scenario design patterns

## Status

See: project tracker for current progress

---

**Last Updated**: 2025-12-12  
**Owner**: Marius
