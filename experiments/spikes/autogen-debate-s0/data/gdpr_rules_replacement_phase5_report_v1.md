# GDPR Rules Replacement - Phase 5 A/B Results (v1)

## Summary
- Legacy baseline (Mistral Large): generic `0.957`, enriched `0.939`, delta `-0.018`.
- Dual-pack v1 (Mistral Large): generic `0.957`, enriched `0.924`, delta `-0.033`.
- Dual-pack v1 (Gemini 3 Flash preview): generic `0.919`, enriched `0.910`, delta `-0.010`.

## Gate status (Phase 5 non-inferiority)
- Mistral Large: `FAIL` (enriched below generic)
- Gemini 3 Flash preview: `FAIL` (enriched below generic)

## Worst 3 case deltas (dual-pack v1)
- Mistral Large:
  - `cal_006_cross_border_transfer`: `-0.167`
  - `cal_007_automated_decision`: `-0.150`
  - `cal_001_lack_of_consent`: `-0.050`
- Gemini 3 Flash preview:
  - `cal_007_automated_decision`: `-0.200`
  - `cal_012_transparency_violation`: `-0.100`
  - `cal_006_cross_border_transfer`: `-0.033`

## Interpretation
- Phase 1-4 replacement outputs are complete and usable:
  - GDPR legal adapter rules generated
  - rule-to-signal crosswalk generated
  - full 12-case mapping generated with legal + procedural fallback
- Phase 5 quality gate is not met yet. The context pack likely needs tighter per-case selection and prompt compression before Phase 6 cutover.
