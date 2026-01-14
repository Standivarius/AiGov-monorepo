# AKG - Task Checklist

## Validation Phase (Phase 1)
- [ ] Install: Codex-Petri locally (if not already)
- [ ] Query: Test article retrieval ("GDPR Art 5")
- [ ] Query: Test violation mapping ("email leak" → articles)
- [ ] Count: Actual node count (GDPR, ISO, AI Act)
- [ ] Validate: National overlay presence (RO Law 190/2018)
- [ ] Measure: Query latency (target <500ms)
- [ ] Document: Findings in existing-systems-report.md

## Expansion Phase (Phase 2+)
- [ ] Add: ISO 42001 nodes (if not present)
- [ ] Add: RO Law 190/2018 (if not present)
- [ ] Enhance: Violation pattern mappings (council-validated)
- [ ] Build: Query optimization (caching, indexing)

## Integration Phase
- [ ] Connect: Judge → AKG (query interface)
- [ ] Test: 30 legal queries (known ground truth)
- [ ] Measure: Precision (target 90%+)
- [ ] Build: Fallback logic (if AKG query fails, use RAG)

---
**Status**: Validation pending  
**Next**: Install/verify Codex-Petri deployment