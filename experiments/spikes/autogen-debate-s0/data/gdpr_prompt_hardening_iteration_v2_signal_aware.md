# GDPR Prompt Hardening Iteration v2 (Signal-Aware Context Selection)

## What changed
- Added signal-aware rule selection in enriched context assembly:
  - ranks legal rules by overlap with expected scenario signals using `gdpr_rule_signal_crosswalk_v1.json`
  - keeps context compact (`<=6` legal rules; `<=2` procedural rules only when scenario has expected signals)
  - reduces control-case over-bias by minimizing procedural context when no expected signals are defined
- Added explicit runner wiring for crosswalk path.

## Files updated
- `experiments/spikes/judge-context-ab/run_cal001_context_ab.py`
- `experiments/spikes/judge-context-ab/run_all_cases_ab.py`
- `experiments/spikes/judge-context-ab/prompt_templates.py` (from prior hardening pass)
- `packages/pe/aigov_eval/judge.py` (runtime hardening from prior pass)

## 12-case A/B results (dual-pack mapping)

### Mistral Large (`mistralai/mistral-large-2512`)
- Baseline dual-pack: `generic=0.957`, `enriched=0.924`, `delta=-0.033`
- Signal-aware: `generic=0.978`, `enriched=0.933`, `delta=-0.044`
- Outcome: enriched quality improved (`0.924 -> 0.933`) but generic rose more; delta stays negative.

### Gemini 3 Flash preview (`google/gemini-3-flash-preview`)
- Baseline dual-pack: `generic=0.919`, `enriched=0.910`, `delta=-0.010`
- Signal-aware: `generic=0.926`, `enriched=0.932`, `delta=+0.006`
- Outcome: enriched now beats generic (positive delta).

## Why delta can stay negative while scores are high
- Yes, absolute quality can be high (~0.95+), but stage gate is *relative*: enriched must be non-inferior to generic.
- With hardening, generic prompt also gets stronger and can improve faster than enriched.
- For Mistral, this indicates context still adds some noise/constraint despite better grounding.

## Current diagnosis
- Prompt quality was a real factor; it has now been addressed and validated.
- Rule replacement alone was not enough.
- Signal-aware selection helps materially (especially Gemini), but Mistral likely needs:
  1. stricter context-token budget and ordering,
  2. per-signal template snippets instead of free-form rule text,
  3. model-specific prompt variant.
