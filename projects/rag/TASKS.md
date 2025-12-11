# RAG - Task Checklist

## Validation Phase (Phase 1)
- [ ] Install: CC-Petri locally (if not already)
- [ ] Query: Test case retrieval ("email leak GDPR violation")
- [ ] Query: Test guidance retrieval ("ENISA LLM security")
- [ ] Count: Actual document count (EDPB, CJEU, ENISA)
- [ ] Validate: Retrieval relevance (Top-5 quality)
- [ ] Measure: Query latency (target <1s)
- [ ] Document: Findings in existing-systems-report.md

## Expansion Phase (Phase 2+)
- [ ] Add: Missing EDPB cases (2024 decisions)
- [ ] Add: Romanian DPA (ANSPDCP) decisions
- [ ] Add: AI Act guidance (when available)
- [ ] Enhance: Reranking (improve Top-5 precision)

## Integration Phase
- [ ] Connect: Judge → RAG (query interface)
- [ ] Test: 30 evidence queries (known relevant cases)
- [ ] Measure: Relevance (target 80%+ in Top-5)
- [ ] Build: Fallback logic (if RAG fails, note in report)

---
**Status**: Validation pending  
**Next**: Install/verify CC-Petri deployment