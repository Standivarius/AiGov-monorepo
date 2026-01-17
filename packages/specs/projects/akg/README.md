# AKG - Autonomous Knowledge Graph

## Overview
Structured knowledge graph for legal reasoning and article validation. Based on **Codex-Petri** implementation.

## Purpose
- Store regulatory frameworks as graph nodes
- Answer: "Does behavior X violate Article Y?"
- Provide article text + interpretation
- Support national law overlays (Romanian Law 190/2018)

## Status
🟢 **Existing** (Codex-Petri deployed locally)

## Architecture

### Graph Structure
```
Framework (GDPR, ISO 27001, etc.)
  ↓ HAS_ARTICLE
Article (GDPR Art 5, Art 32, etc.)
  ↓ IMPLEMENTS
National_Provision (RO Law 190/2018)
  ↓ VIOLATES
ViolationPattern (email leak, RTBF failure, etc.)
```

### Node Types
- **Framework**: GDPR, ISO 27001, ISO 42001, EU AI Act
- **Article**: Individual articles/sections (with text_en, text_original)
- **National_Provision**: Country-specific implementations
- **ViolationPattern**: Common violation types (deterministic mapping)

### Edge Types
- **HAS_ARTICLE**: Framework → Article
- **IMPLEMENTS**: Article → National_Provision
- **SUPPLEMENTS**: National law adds to EU law
- **VIOLATES**: Behavior pattern → Article

### Database Options
- **Neo4j Aura** (cloud, managed)
- **FalkorDB** (Redis-based, fast)
- **Neo4j Local** (self-hosted)

**Current**: TBD (check Codex-Petri)

## Key Decisions
- **Canonical English**: All reasoning in EN (ADR-0001)
- **National overlays**: Stored with EN summary + original text
- **No scenarios**: Scenarios in file structure, not graph (ADR-0004)
- **Violation patterns**: Pre-computed CSV (not runtime reasoning)

## Current Data
- **GDPR**: 88 articles parsed
- **ISO 27001**: 93 controls parsed
- **ISO 42001**: TBD
- **EU AI Act**: 113 articles parsed
- **RO Law 190/2018**: TBD

**Total nodes**: ~2000-3000 (from memory, verify)

## Links
- [TASKS.md](TASKS.md) - Validation & expansion tasks
- [RESEARCH.md](RESEARCH.md) - Query optimization findings
- **Codex-Petri repo**: [Local path TBD]
