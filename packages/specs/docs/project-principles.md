# AIGov Project Principles

**Purpose**: Foundational philosophy and quality standards guiding all development decisions  
**Status**: Living document - read at start of EVERY new chat  
**Last Updated**: 2025-12-16

---

## Core Mission

**AIGov enables EU organizations to deploy AI with confidence, not liability.**

We bridge the gap between technical LLM security testing and regulatory compliance frameworks, delivering integrated audits that serve both CISOs (security findings) and Compliance Officers (regulatory documentation) with a single engagement.

---

## Design Philosophy

### 1. Validation Before Infrastructure

**Principle**: Prove demand before building platforms.

**Application**:
- Phase 0: Manual PDF reports via email validate business model
- SaaS platform development deferred to Phase 1+
- €8k-15k audits delivered without custom infrastructure
- Speed over perfection - leverage existing tools (Inspect, Petri) rather than building from scratch

**Anti-pattern**: Building complex orchestration before proving customers will pay.

---

### 2. Evidence-Based Technical Decisions

**Principle**: Use empirical validation over expert opinions.

**Application**:
- Real-world GDPR violations from enforcement databases (not invented scenarios)
- MITRE ATLAS and OWASP taxonomies for LLM attacks
- Official supervisory authority audit criteria (Art.24, Art.32)
- Documented attack scenarios from security research papers

**Anti-pattern**: Expensive expert reviews or statistical approaches without proven grounding.

---

### 3. LLM as Amplifier, Not Root Cause

**Principle**: LLMs democratize access to sensitive information users shouldn't reach.

**Core Insight**: Traditional permission controls fail because LLMs bypass them through natural language queries. Latent data governance problems become exploitable vulnerabilities.

**Application**:
- Test for confidential data leakage through conversational context
- Validate authentication checks before PII disclosure
- Assess RAG systems for unauthorized document access
- Measure prompt injection resilience

**Positioning**: "Your AI tools work too well - they expose data your users shouldn't see."

---

### 4. Dual-Audience Value Proposition

**Principle**: Serve both security and compliance with single audit.

**Differentiation**:
- **vs Security vendors**: We map technical findings to GDPR/ISO articles
- **vs Compliance consultants**: We provide actual exploit evidence, not checkboxes
- **Unique value**: €15k integrated audit replaces €8k security + €12k compliance

**Report Structure**:
- **L1 (Executive)**: Business risk summary, liability exposure, ROI of fixes
- **L2 (CISO)**: Technical vulnerability details, exploit evidence, remediation steps
- **L3 (CCO)**: Regulatory mapping, compliance gaps, audit-ready documentation

---

### 5. Governance Over Guesswork

**Principle**: Systematic schema management prevents technical debt.

**Application**:
- Variable registry: Single source of truth for all schema fields
- File registry: Dependency tracking, naming conventions, lifecycle management
- Weekly consistency checks: Codex/ChatGPT audits for PM-level review
- ADRs (Architectural Decision Records): Document all non-trivial choices

**Anti-pattern**: Ad-hoc file creation, duplicate variables, orphaned schemas.

---

## Quality Standards

### Technical Quality

**Code**:
- Deterministic over probabilistic (CSV lookup tables, not runtime AI reasoning)
- Observable over opaque (logging, tracing, error transparency)
- Testable over theoretical (eval system validates Judge accuracy)

**Data**:
- Structured over unstructured (YAML schemas, JSON outputs, not free text)
- Versioned over volatile (semantic versioning for schemas, scenarios)
- Validated over trusted (Pydantic models in Phase 1+, manual YAML validation Phase 0)

### Business Quality

**Client-Facing**:
- Professional over polished (working audits before pretty dashboards)
- Evidence-based over claimed (cite sources: EDPB guidelines, CNIL cases)
- Actionable over exhaustive (prioritized recommendations, not 100-page dumps)

**Internal**:
- Documented over assumed (ADRs for decisions, registries for schemas)
- Measurable over subjective (Judge accuracy %, scenario coverage metrics)
- Iterative over perfect (Phase 0 MVP, Phase 1 refinement)

---

## Decision-Making Framework

### When to Build vs Buy

**Build if**:
- Core differentiator (scenario creation pipeline, compliance translation layer)
- No suitable tool exists (GDPR-to-Petri mapping)
- Integration overhead > build effort (custom orchestration vs existing tools)

**Buy/Use if**:
- Commodity functionality (Inspect for orchestration, PostgreSQL for storage)
- Well-tested solutions (Petri for LLM security, industry-standard tools)
- Time-to-value critical (Phase 0 focus on validation, not infrastructure)

---

### Complexity Guardrails

**Push back when**:
- Abstract frameworks without implementation path ("We should use microservices")
- Governance exceeding actual work (more process than product)
- Premature optimization ("Phase 1 might need X")
- Answer to "Why?" is "best practice" not "Without this, X broke"

**Implement when**:
- Solves active problem (file registry prevents naming conflicts we just had)
- Prevents rework (variable registry stops duplicate definitions)
- Catches bugs (eval system found Judge hallucinations in testing)
- Saves time (automated consistency checks faster than manual review)

**Test**: If uncertain, ask "Does this solve a problem we have, or prevent one we'll definitely hit?"

---

## Phase 0 Specific Principles

### Scope Discipline

**In Scope**:
- GDPR compliance only (no ISO27001, ISO42001, AI Act)
- Generic chatbots only (no MS365 Copilot, no agents)
- Romania national law only (no Poland, Germany)
- English + Romanian languages (Petri thinks EN, translates at edges)

**Out of Scope** (Phase 1+):
- Multi-framework audits
- Custom SaaS platform
- Subscription monitoring services (FlagWise integration)
- Fine-tuned target LLMs (use instructional layer instead)

### Success Metrics

**Phase 0 Complete When**:
- ✅ 3 complete example reports (EN) + 1 (RO)
- ✅ Dashboard static mockup (all 7 tabs)
- ✅ IntakeAgent working (3 test runs)
- ✅ Mock Target LLM (80%+ violation rate)
- ✅ OpenRouter wrapper (4 models tested)
- ✅ Judge accuracy: 80%+ on systematic tests (TEST-J01/J02/J03)

**Phase 0 Timeline**: 21-24 days (3-4 weeks)

---

## Anti-Patterns to Avoid

### Over-Engineering
- ❌ Building custom orchestration when Inspect works
- ❌ Fine-tuning LLMs when prompt engineering suffices
- ❌ Real-time monitoring in Phase 0 (audit = point-in-time)
- ❌ Complex knowledge graphs when CSV lookup tables work

### Under-Specification
- ❌ Vague scenario seeds ("test for PII" vs "test for email disclosure without auth")
- ❌ Missing legal text (Judge needs inline GDPR articles, not just numbers)
- ❌ Ambiguous evaluation criteria ("check compliance" vs "rate VIOLATED if X")

### Process Bloat
- ❌ Multiple approval layers for internal decisions (solo founder speed advantage)
- ❌ Extensive documentation before validation (write after proving demand)
- ❌ Theoretical frameworks without concrete implementation ("consider using X")

---

## Collaboration Patterns

### With Claude (AI Assistant)

**Effective**:
- "Search for official GDPR violation taxonomies and extract categories"
- "Update variable-registry.md to add national_law field, then update scenario-card-schema-v1.2.md"
- "Review Phase-0-Detailed.md and flag any tasks slipping timeline"

**Ineffective**:
- "Make it better" (no actionable direction)
- "Add best practices" (which ones? why?)
- "Research LLM security" (too broad, no specific question)

### With Ally (CISO Partner)

**Validation**:
- Review GDPR violation taxonomy (are categories realistic?)
- Validate scenario realism (would real auditors test this way?)
- Sanity-check technical findings (is this a genuine security issue?)

**Not for**: Detailed implementation decisions (that's AIGov's domain).

---

## Future-Proofing

### Extensibility Hooks

**Phase 0 designs for Phase 1+**:
- Framework-agnostic schema structure (evaluation_criteria per framework)
- Language-agnostic translation layer (Petri thinks EN, translates at edges)
- Multi-industry tags (not hardcoded industry field)

**But don't implement**:
- Multi-framework report templates (build when needed)
- ISO27001 evaluation criteria (not in scope)
- Subscription monitoring (defer to commercial validation)

### Learning Loops

**Capture learnings**:
- ADRs: Why we chose X over Y (Decision-Log.md)
- Eval results: Judge accuracy per scenario type (informs Phase 1 improvements)
- Client feedback: What reports are actually used (shapes Phase 1 priorities)

**Apply learnings**:
- Refine scenario templates based on Phase 0 creation friction
- Adjust evaluation criteria based on Judge failure modes
- Optimize report structure based on pilot client feedback

---

## Closing Thoughts

**This is a business, not a research project.**

Every decision should pass the "Can I explain this to a paying client?" test. If the answer involves "best practices" or "future-proofing" without concrete ROI, reconsider.

**Speed is a feature.**

The August 2026 EU AI Act deadline creates urgency. Organizations need audits now, not perfect platforms later. Phase 0 validates the business model. Phase 1+ builds sustainable infrastructure.

**Evidence over enthusiasm.**

Cite sources. Show real violations. Prove claims with data. Clients trust documented research (EDPB guidelines, CNIL cases, ENISA reports) more than confident assertions.

---

**Document Purpose**: Read by Claude at start of every new chat to align with AIGov philosophy  
**Upload to**: Claude Project Knowledge (Settings → Knowledge)  
**Review**: End of Phase 0 (evaluate alignment with actual development)
