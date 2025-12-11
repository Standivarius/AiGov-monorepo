# Judge - Research Findings

## LLM Testing Results
**Status**: Pending  
**Date**: TBD

### Test Scenario
- **Input**: Same RO transcript (email leak violation)
- **Expected**: Detect GDPR Art 5(1)(f), Art 32 violation
- **Models**: Gemini 2.0, Mistral Large 3, Claude Sonnet 4.5, GPT-4.5.1

### Results

| Model | Translation Accuracy | Pattern Detection | Consistency (5 runs) | Latency | Cost |
|-------|---------------------|-------------------|---------------------|---------|------|
| Gemini 2.0 Flash Thinking | TBD | TBD | TBD | TBD | TBD |
| Mistral Large 3 | TBD | TBD | TBD | TBD | TBD |
| Claude Sonnet 4.5 | TBD | TBD | TBD | TBD | TBD |
| GPT-4.5.1 | TBD | TBD | TBD | TBD | TBD |

### Winner
**Decision**: TBD after testing

---

## Inspect AI LLM Abstraction Research
**Status**: Pending

### Questions
- Does Inspect AI provide LLM abstraction layer?
- Supported providers: OpenRouter, Anthropic, OpenAI?
- Retry logic built-in?
- Cost tracking?
- Parameter control (temperature, top-p)?

### Findings
[TBD after documentation review]

---

## LLM Council Research
**Status**: Pending

### Existing Implementations
- Karpathy's llm-council: [TBD - find repo/implementation]
- Other patterns: [TBD]

### Implementation Strategy
**Option A**: Use existing library (if quality sufficient)  
**Option B**: Build custom (parallel API calls, vote aggregation)

**Decision**: TBD after review

---

## Translation Fidelity Testing
**Status**: Pending

### Test Protocol
- RO legal text → Judge (think in EN) → RO report
- Measure: Terminology preservation (GDPR terms, legal phrases)
- Test cases: 10 RO transcripts with known violations

### Results
[TBD]

---

**Links to GDrive**: [Will add after Gemini research]