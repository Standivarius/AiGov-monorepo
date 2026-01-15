# IntakeAgent - AI-Dynamic Onboarding

## Overview
AI-powered client onboarding system combining dynamic questionnaire with intelligent document extraction.

## Purpose
- Minimize client friction (auto-extract from uploaded docs)
- Generate outputs for Petri, Reports, Dashboard
- Claude Skill pattern → Agent SDK migration path

## Status
🔴 **Not Started**

## Architecture
```
Phase 1: Initial Questions (5-7 quick questions)
  ↓
Phase 2: Document Upload & Extraction
  - Policies, technical docs, Target LLM docs
  - Claude Skill extracts: Controls, gaps, stakeholders
  ↓
Phase 3: Output Generation
  - Petri config (scenarios, Target params)
  - Report data (framework annexes, audit prep)
  - Dashboard params (client profile JSON)
```

## Key Decisions
- **NOT using**: Typeform/Fillout/Tally (no LLM integration)
- **Using**: Claude Skill pattern (AI-dynamic branching)
- **Migration path**: Agent SDK later if needed

## Links
- [TASKS.md](TASKS.md) - Implementation checklist
- [RESEARCH.md](RESEARCH.md) - Tool research findings
- [STATUS.md](STATUS.md) - Current state & blockers