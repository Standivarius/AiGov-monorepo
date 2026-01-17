# Judge - Transcript Analysis & Violation Mapping

## Overview
Multilingual LLM system that analyzes Petri transcripts, queries AKG/RAG, and generates structured violation findings.

## Purpose
- Receive RO/EN transcripts from Petri
- Detect violation patterns (email leak, RTBF failure, etc.)
- Query AKG for article confirmation
- Query RAG for supporting evidence
- Generate behaviour_json_v1 output
- Translate reports to client language

## Status
🔴 **Not Started**

## Architecture

### Translation Layer (ADR-0001)
**Canonical English Pipeline**:
```
Input: RO transcript
  ↓
Judge (multilingual LLM): Think in EN internally
  ↓
Query AKG/RAG: EN queries
  ↓
Generate findings: EN
  ↓
Translate reports: EN → RO
```

**NO separate translation LLM** (avoid context loss)

### LLM Candidates
- **Gemini 2.0 Flash Thinking** (1M context, top multilingual benchmark)
- Mistral Large 3 (256k, EU-focused)
- Claude Sonnet 4.5 (200k, reasoning depth)
- GPT-4.5.1 (latest)

**Test Protocol**: Same RO transcript → 5 LLMs → measure accuracy, consistency, cost, latency

### Council Pattern
**Use for**: Ambiguous cases (e.g., borderline violations)
**Models**: GPT-4.5.1, Claude Sonnet 4.5, Mistral Large 3, Gemini 2.0
**Threshold**: 3/4 agreement
**Output**: Consensus vote + individual reasoning

### Output Format
**behaviour_json_v1** (schema TBD):
```json
{
  "scenario_id": "scenario-001-email-leak",
  "violation_detected": true,
  "gdpr_articles": ["5(1)(f)", "32"],
  "iso27001_controls": ["A.5.33", "A.8.9"],
  "confidence": 0.95,
  "evidence": "...",
  "supporting_cases": ["EDPB-2023-01"],
  "ambiguous": false
}
```

## Key Decisions
- **Single LLM** handles translation + context (not separate translator)
- **Gemini 2.0** likely winner (1M context, multilingual benchmark leader)
- **Platform-agnostic wrapper** (easy model swapping)
- **Temperature adjustable** per query type (pattern detection vs report generation)

## Links
- [TASKS.md](TASKS.md) - Implementation checklist
- [RESEARCH.md](RESEARCH.md) - LLM testing results
