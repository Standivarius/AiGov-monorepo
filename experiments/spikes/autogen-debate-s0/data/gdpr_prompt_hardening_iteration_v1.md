# GDPR Prompt Hardening Iteration v1 (Claude feedback integration)

## Scope
Integrated prompt-level improvements inspired by Petri analysis into both:
- Runtime Judge path (`packages/pe/aigov_eval/judge.py`)
- Spike A/B prompt path (`experiments/spikes/judge-context-ab/prompt_templates.py`, `run_cal001_context_ab.py`)

## Implemented changes
1. Evidence citation discipline in prompt contract:
   - Turn-index + exact quote + GDPR article format in `citations`.
2. Transcript structure:
   - Indexed transcript format (`[T001][ROLE] ...`) used in prompt inputs.
3. Uncertainty handling:
   - Explicit `UNDECIDED` instruction for missing/ambiguous evidence.
4. Correction rule:
   - Prompt rule that later apology/correction does not erase earlier violation evidence.
5. Parser hardening:
   - JSON extraction fallback.
   - Validation for required keys.
   - Retry loop (up to 3 attempts) before fail-closed fallback.
6. Enriched-context compaction:
   - Rule context capped to reduce prompt overload (`6 legal + 3 procedural` in spike path).

## 12-case A/B results (dual-pack mapping)

### Mistral Large (`mistralai/mistral-large-2512`)
- Baseline dual-pack (pre-hardening): `generic=0.957`, `enriched=0.924`, `delta=-0.033`
- Hardening (full context): `generic=0.981`, `enriched=0.924`, `delta=-0.057`
- Hardening + compact context: `generic=0.971`, `enriched=0.926`, `delta=-0.044`

### Gemini 3 Flash preview (`google/gemini-3-flash-preview`)
- Baseline dual-pack (pre-hardening): `generic=0.919`, `enriched=0.910`, `delta=-0.010`
- Hardening (full context): `generic=0.932`, `enriched=0.910`, `delta=-0.022`
- Hardening + compact context: `generic=0.932`, `enriched=0.929`, `delta=-0.003`

## Interpretation
- The Claude-driven prompt hardening was implemented and verified.
- Parser robustness improved substantially (runtime + spike).
- Enriched-vs-generic gap is reduced for Gemini with context compaction (near parity).
- Mistral still shows negative enriched delta; context selection/routing needs another tuning pass.

## Next suggested step
- Move from static caps to signal-aware context assembly per case family (top-N legal rules by expected signal overlap), then rerun 12-case A/B.
