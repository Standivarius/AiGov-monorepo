# Phase 0 Integration Summary: Eval System

**Date**: 2025-12-15  
**Purpose**: Document integration of Aigov-eval into Phase 0 plan

---

## What Changed

### Before (Dec 11)
- Phase 0 plan: Scenarios → Judge → Reports
- Judge validation: Subjective Ally review ("looks professional")
- Timeline: 21 days (3 weeks)
- Success criteria: "80%+ Judge accuracy" (but no way to measure)

### After (Dec 15)
- Phase 0 plan: Scenarios → Judge → **Eval validation** → Reports
- Judge validation: **Systematic tests** (TEST-J01, J02, J03)
- Timeline: 21-24 days (add 2-3 days for eval in Week 2)
- Success criteria: **Measurable** (95% consistency, 100% schema, 80%+ accuracy)

---

## Why This Matters

### Problem Identified
You caught a critical gap: **"How do we know the Judge works?"**

Without eval:
- Ally's review becomes subjective ("it looks good")
- No defensible accuracy claims for client discovery
- Potential rework if Judge fails under systematic testing
- Missing foundation for AIGov's core value prop: "We validate our audit tool"

### Solution Implemented
**Minimal eval in Phase 0** (Option A):
- TEST-J01: Consistency check (same transcript → same violations, 95%+)
- TEST-J02: Schema validation (behaviour_json_v0 compliance, 100%)
- TEST-J03: Accuracy measurement (Judge vs MOCK_LOG, 80%+ precision/recall)

**Impact**:
- Ally review becomes technical: "Judge validated to 87% accuracy"
- Discovery calls: "Our Judge is validated against documented metrics"
- Foundation for Phase 1 expanded testing (AKG, RAG, reports, council)
- Only 2-3 days added to timeline

---

## Key Decisions (ADRs)

### ADR-0006: Inline Legal Text
**Decision**: Embed GDPR articles + EDPB guidance in scenario_card `legal_context`  
**Why**: No AKG/RAG dependency Phase 0, self-contained scenario_cards, faster execution  
**Transition**: Keep inline text Phase 1+, use AKG/RAG for additional context  

### ADR-0007: MOCK_LOG Format
**Decision**: Test_target outputs structured log of intentional violations  
**Why**: Enables objective Judge accuracy measurement (precision/recall)  
**Format**: JSON with scenario_id, turn, violation_intent, gdpr_article  

### ADR-0008: Minimal Eval Phase 0
**Decision**: Implement TEST-J01, J02, J03 only (not full 25-test suite)  
**Why**: Necessary for Phase 0 success criteria, defensible results, 2-3 days effort  
**Defer**: Dashboard, council tests, AKG/RAG tests, report tests (Phase 1+)  

### ADR-0009: Simplified Schema
**Decision**: Create behaviour_json_v0_phase0 without confidence, AKG/RAG, redaction  
**Why**: Complexity reduction, focus on core fields, clear upgrade path Phase 1  

### ADR-0010: Real-World GDPR Violations
**Decision**: Base scenarios on EDPB enforcement decisions, not Petri's 111 mapping  
**Why**: Realistic scenarios, documented evidence, credible test coverage  

---

## Updated Timeline

### Week 1 (Days 1-7): Scenarios + Example Report
- Day 1: GDPR research (1h) + 5 scenarios
- Day 2: 5 more scenarios + template setup
- Day 3-4: Example report (fake data)
- Day 5: Test target configuration + MOCK_LOG

### Week 2 (Days 8-14): Judge + **Validation** ⭐ NEW
- Day 6: Inspect configuration
- Days 7-9: Judge implementation
- Days 10-11: Judge refinement
- **Days 12-14: Judge validation (TEST-J01, J02, J03)** ⭐

### Week 3 (Days 15-21): Pipeline Integration
- Days 15-16: Report aggregation
- Day 17: GDPR annex
- Days 18-19: Buffer/iteration
- Day 20: Romanian translation
- Day 21: Final validation

---

## Deliverables Added

### Deliverable 7: Judge Validation (NEW)
**Priority**: CRITICAL  
**Time**: 2-3 days  
**Location**: `Aigov-eval/tests/judge/`  

**Tests**:
- `test_j01_consistency.py` - 95%+ consistency target
- `test_j02_schema.py` - 100% schema compliance
- `test_j03_accuracy.py` - 80%+ precision/recall vs MOCK_LOG

**Output**: Test report with objective metrics for Ally review

---

## Files Updated

### Aigov-specs Repo
1. `/docs/planning/Phase-0-Detailed.md` - Add Deliverable 7, update timeline
2. `/schemas/scenario_card/scenario-card-schema-v1.2.md` - Add `legal_context` and `test_target_instructions`
3. `/schemas/behaviour_json_v0_phase0.schema.json` - NEW simplified schema
4. `/docs/planning/Decision-Log.md` - Add ADR-0006 through ADR-0010
5. `/docs/planning/Phase-0-Integration-Summary.md` - This document

### Aigov-eval Repo
1. `/tests/judge/README.md` - Test suite overview
2. `/tests/judge/test_j01_consistency.py` - Consistency test
3. `/tests/judge/test_j02_schema.py` - Schema validation test
4. `/tests/judge/test_j03_accuracy.py` - Accuracy test vs MOCK_LOG

---

## Success Criteria (Updated)

**Phase 0 Complete When**:
✅ 10 GDPR scenario_cards with inline legal_context  
✅ Example L2 report (fake data) for discovery calls  
✅ Test_target configured with MOCK_LOG format  
✅ Inspect + Petri running custom scenarios  
✅ Judge implemented (reads inline legal_context)  
✅ **TEST-J01: 95%+ consistency** ⭐  
✅ **TEST-J02: 100% schema compliance** ⭐  
✅ **TEST-J03: 80%+ detection accuracy** ⭐  
✅ Pipeline report generated (real data)  
✅ Romanian translation validated  
✅ **Ally approval: "Technically defensible with validated metrics"** ⭐

**GO/NO-GO**: All criteria met + documented accuracy metrics → Phase 1

---

## What's Deferred to Phase 1+

### From Full Eval System (25 tests)
- AKG Tests (TEST-A01-A04) - requires Neo4j implementation
- RAG Tests (TEST-R01-R03) - requires vector DB implementation
- Report Tests (TEST-RE01-RE03) - requires GRC export formats
- Council Tests (TEST-C01-C02) - requires multi-model setup
- Scenario Tests (TEST-S01-S03) - expanded coverage Phase 1
- Dashboard/metrics visualization - test runner sufficient Phase 0

### From behaviour_json_v1 (Full Schema)
- Confidence scoring
- AKG context fields
- RAG citations fields
- Redaction logic and metadata
- PII type granularity in evidence

---

## Next Steps

### Immediate (Week 1, Day 1)
1. Start GDPR violation research (1h)
2. Create first 5 scenario_cards with `legal_context`
3. Begin example L2 report template

### Week 2 Focus
1. Implement Judge scorer
2. Run TEST-J01, J02, J03
3. Generate test report with metrics

### Week 3 Validation
1. Show Ally test results: "Judge validated to X% accuracy"
2. Use metrics in client discovery calls
3. Document learnings for Phase 1 expansion

---

## Questions Resolved

**Q1**: Example report (Week 1) OR pipeline-generated report (Week 4) as priority?  
**A1**: BOTH. Example report Week 1 (discovery calls), real report Week 3 (technical proof).

**Q2**: Inline legal text in scenario_card OR wait for AKG/RAG?  
**A2**: Inline text Phase 0. Keep it Phase 1+, use AKG/RAG for additional context.

**Q3**: Simplified behaviour_json_v0 for Phase 0 OR full schema now?  
**A3**: Simplified v0 Phase 0. Upgrade to v1 when AKG/RAG implemented.

**Q4**: MOCK_LOG purpose and format?  
**A4**: Test_target self-documents violations → Judge accuracy measurement (precision/recall).

**Q5**: Evidence indexing (turn vs message_index)?  
**A5**: Turn-level only Phase 0. Add message_index Phase 1 if Inspect supports it.

---

**Document Status**: Integration summary  
**Last Updated**: 2025-12-15  
**Ready to Execute**: YES ✅
