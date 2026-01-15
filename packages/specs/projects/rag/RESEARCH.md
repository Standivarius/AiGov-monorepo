# RAG - Research Findings

## CC-Petri Validation
**Status**: Pending  
**Date**: TBD

### Installation Check
- Location: [TBD - local path]
- Vector Database: [TBD - Pinecone? Weaviate?]
- Status: [TBD - running? needs setup?]

### Document Count
- EDPB Guidelines: [TBD - verify count]
- EDPB Enforcement Decisions: [TBD]
- CJEU Rulings: [TBD]
- ENISA Reports: [TBD]
- ANSPDCP (RO DPA): [TBD]
- Total documents: [TBD]

### Retrieval Quality
- Sample query relevance: [TBD]
- Top-K precision: [TBD]
- Latency: [TBD]

---

## Vector Database Comparison
**Status**: Deferred (use existing CC-Petri)

### If Migration Needed Later
| Database | Pros | Cons |
|----------|------|------|
| Pinecone | Managed, fast | Cost, vendor lock-in |
| Weaviate | Open source, hybrid search | Hosting complexity |
| Qdrant | Fast, Rust-based | Smaller ecosystem |

---

## Retrieval Optimization Research
**Status**: Pending

### Reranking
- **Purpose**: Improve Top-5 precision (80% → 90%)
- **Options**: Cohere Rerank, cross-encoder models
- **Trade-off**: +latency, +cost, +precision

### Query Enhancement
- **HyDE**: Generate hypothetical document, use for search
- **Query expansion**: Add synonyms, legal terms
- **Multi-query**: Generate 3 variations, merge results

**Decision**: TBD after baseline established

---

**Links to GDrive**: [Will add after validation complete]