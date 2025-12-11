# Judge - Task Checklist

## Research Phase
- [ ] Research: Inspect AI LLM abstraction (does it exist?)
- [ ] If not, design: Platform-agnostic wrapper (OpenRouter, Anthropic, OpenAI)
- [ ] Test: Gemini 2.0 Flash Thinking (RO transcript → EN analysis)
- [ ] Test: Mistral Large 3 (same transcript)
- [ ] Test: Claude Sonnet 4.5 (same transcript)
- [ ] Test: GPT-4.5.1 (same transcript)
- [ ] Compare: Translation accuracy, pattern detection, cost, latency
- [ ] Research: LLM Council implementations (Karpathy's llm-council?)
- [ ] Document: Test results in RESEARCH.md

## Design Phase
- [ ] Define: behaviour_json_v1 schema (output format)
- [ ] Design: Prompt templates (pattern detection, article confirmation)
- [ ] Design: Council voting logic (3/4 threshold, divergence handling)
- [ ] Design: Ambiguity flagging (when to escalate to human)
- [ ] Spec: AKG query format (how Judge asks "Does X violate Y?")
- [ ] Spec: RAG query format (how Judge requests supporting cases)

## Implementation Phase
- [ ] Build: LLM wrapper (if Inspect AI doesn't have one)
- [ ] Build: Judge core (transcript → pattern detection)
- [ ] Build: AKG integration (query legal knowledge)
- [ ] Build: RAG integration (retrieve supporting evidence)
- [ ] Build: Council system (multi-model voting)
- [ ] Build: Output generator (behaviour_json_v1)
- [ ] Build: Report translator (EN → RO)

## Validation Phase
- [ ] Test: Email leak scenario (5 runs, measure consistency)
- [ ] Test: RTBF failure scenario (5 runs)
- [ ] Test: Ambiguous case (council divergence)
- [ ] Test: Translation fidelity (RO → EN → RO round-trip)
- [ ] Measure: Latency (target <5s per transcript)
- [ ] Iterate: Based on accuracy/performance

---
**Status**: Not started  
**Next**: Research Inspect AI LLM abstraction