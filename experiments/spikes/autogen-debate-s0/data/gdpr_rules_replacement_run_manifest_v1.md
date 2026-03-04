# GDPR Rules Replacement Run Manifest (Phase 1-5, v1)

## Environment
- Python: `C:\Python312\python.exe`
- Branch: `codex/gdpr-rules-gptpro`
- Repo: `C:\Users\User\OneDrive - DMR Ergonomics\aigov-workspace\AiGov-monorepo`

## Commands executed
1. Phase 1-4 builder
   - `C:\Python312\python.exe experiments\spikes\autogen-debate-s0\build_gdpr_rule_pack_v1.py`
2. Phase 5 A/B (Mistral Large)
   - `C:\Python312\python.exe experiments\spikes\judge-context-ab\run_all_cases_ab.py --openrouter-model mistralai/mistral-large-2512 --mapping-path experiments\spikes\autogen-debate-s0\data\calibration_to_gdpr_rules_v1.json --legal-rules-path experiments\spikes\autogen-debate-s0\data\master_audit_rules_gdpr_v1.json --procedural-rules-path experiments\spikes\autogen-debate-s0\data\master_audit_rules.json --output-tag gdpr_dual_v1`
3. Phase 5 A/B (Gemini 3 Flash preview)
   - `C:\Python312\python.exe experiments\spikes\judge-context-ab\run_all_cases_ab.py --openrouter-model google/gemini-3-flash-preview --mapping-path experiments\spikes\autogen-debate-s0\data\calibration_to_gdpr_rules_v1.json --legal-rules-path experiments\spikes\autogen-debate-s0\data\master_audit_rules_gdpr_v1.json --procedural-rules-path experiments\spikes\autogen-debate-s0\data\master_audit_rules.json --output-tag gdpr_dual_v1`

## Output anchors
- Phase 1-4 report:
  - `experiments/spikes/autogen-debate-s0/data/gdpr_rules_replacement_phase1_4_report_v1.md`
- Phase 5 report:
  - `experiments/spikes/autogen-debate-s0/data/gdpr_rules_replacement_phase5_report_v1.md`
- Full12 summaries:
  - `experiments/spikes/judge-context-ab/work/full12_ab_summary__gdpr_dual_v1__mistralai_mistral-large-2512.json`
  - `experiments/spikes/judge-context-ab/work/full12_ab_summary__gdpr_dual_v1__google_gemini-3-flash-preview.json`
