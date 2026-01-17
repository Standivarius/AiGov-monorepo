# RAG - Retrieval-Augmented Generation Corpus

## Overview
Vector search over legal corpus (EDPB cases, CJEU rulings, ENISA guidance). Based on **CC-Petri** implementation.

## Purpose
- Provide supporting evidence for violations
- Retrieve relevant case law (EDPB enforcement decisions)
- Find regulatory guidance (ENISA, EDPB guidelines)
- Support report annexes (citations)

## Status
🟢 **Existing** (CC-Petri deployed locally)

## Architecture

### Vector Database Options
- **Pinecone** (managed, fast)
- **Weaviate** (open source, hybrid search)
- **Qdrant** (Rust-based, performant)

**Current**: TBD (check CC-Petri)

### Document Sources
- **EDPB Guidelines**: Interpretation guidance
- **EDPB Enforcement Decisions**: Real violation cases
- **CJEU Rulings**: EU court precedents
- **ENISA Reports**: Security best practices
- **ANSPDCP**: Romanian DPA decisions

### Retrieval Strategy
- **Top-K**: 5 results (configurable)
- **Similarity threshold**: 0.7+ (configurable)
- **Reranking**: Optional (improve precision)

## Key Decisions
- **RAG complements AKG**: AKG for article confirmation, RAG for evidence
- **Canonical English**: All queries in EN (ADR-0001)
- **Fallback strategy**: If AKG fails, use RAG (vice versa)

## Current Data
- **EDPB cases**: ~150 parsed (estimate, verify)
- **CJEU rulings**: TBD
- **ENISA reports**: TBD
- **Total documents**: ~500-1000 (estimate, verify)

## Links
- [TASKS.md](TASKS.md) - Validation & expansion tasks
- [RESEARCH.md](RESEARCH.md) - Retrieval optimization findings
- **CC-Petri repo**: [Local path TBD]
