# GDPR Rules Replacement Plan v1 (D2 -> GPT-Pro Legal Pack)
Date: 2026-03-04
Scope: PM plan only (no runtime code changes in this artifact).

## 1) Objective
Replace D2-extracted rules as the primary legal context source for Judge enrichment with the GPT-Pro GDPR legal pack, while keeping compatibility with current spike scripts and preserving rollback safety.

## 2) Current Inputs
- New pack:
  - `C:/Users/User/AppData/Local/Temp/gdprpack/gdpr_audit_pack.yaml`
  - `C:/Users/User/AppData/Local/Temp/gdprpack/sources_register.csv`
- Current D2 assets:
  - `C:/Users/User/OneDrive - DMR Ergonomics/aigov-workspace/AiGov-monorepo/experiments/spikes/autogen-debate-s0/data/master_audit_rules.yaml`
  - `C:/Users/User/OneDrive - DMR Ergonomics/aigov-workspace/AiGov-monorepo/experiments/spikes/autogen-debate-s0/data/master_audit_rules.json`
  - `C:/Users/User/OneDrive - DMR Ergonomics/aigov-workspace/AiGov-monorepo/experiments/spikes/autogen-debate-s0/data/calibration_to_edpb_rules.json`
- Judge context AB scripts:
  - `C:/Users/User/OneDrive - DMR Ergonomics/aigov-workspace/AiGov-monorepo/experiments/spikes/judge-context-ab/run_cal001_context_ab.py`
  - `C:/Users/User/OneDrive - DMR Ergonomics/aigov-workspace/AiGov-monorepo/experiments/spikes/judge-context-ab/run_all_cases_ab.py`

## 3) Key Findings from New Pack
- Strong baseline quality:
  - 255 rules
  - no duplicate `rule_id`
  - full core fields present on all rules
  - article coverage aligns with declared scope
- Better legal fit for calibration-style GDPR judging than messenger-specific D2 rules.
- Not drop-in compatible with current D2 schema consumers.
- Contains non-testable governance/authority items (`duty_holder: n/a`) that must be excluded from org-compliance judge contexts.
- Includes one draft interpretive source (EDPB 1/2024 public consultation), which must be marked as non-final authority.

## 4) Non-Goals
- No immediate replacement of all old files in one step.
- No full architecture refactor.
- No legal-policy change in verdict taxonomy.

## 5) Canonical Replacement Strategy
Use dual-track context:
- P1 Legal Requirements Pack -> GPT-Pro legal pack (new primary legal source)
- P2 Procedure Pack -> D2 procedural method (kept, but no longer primary legal grounding)

This avoids breaking existing flows while shifting legal grounding to GDPR-native rules.

## 6) Migration Phases and Acceptance Gates

### Phase 0 - Baseline Freeze
Actions:
- Snapshot current D2 artifacts and current A/B baseline outputs.
- Record file hashes and counts before changes.

Acceptance gate:
- Baseline manifest exists with:
  - rules file names + counts
  - current calibration mapping file
  - current A/B summary references

### Phase 1 - Source Pack Validation
Actions:
- Validate GPT-Pro pack structure and required fields.
- Exclude `duty_holder: n/a` rules from testable pool.
- Flag draft-source-derived rules for metadata warning.

Acceptance gate:
- Validation report produced with:
  - rule count (raw vs testable)
  - missing field count
  - duplicate ID count
  - list of excluded non-testable rules
  - list of draft/low-authority markers

### Phase 2 - Adapter to Existing Consumer Shape
Actions:
- Build adapter output in D2-compatible shape for existing scripts.
- Emit:
  - `master_audit_rules_gdpr_v1.yaml`
  - `master_audit_rules_gdpr_v1.json`
- Include source provenance in mapped output.

Mapping contract:
- `id <- rule_id`
- `title <- canonical obligation label (short form)`
- `requirement <- canonical_obligation_text`
- `audit_procedure <- derived from trigger_condition + procedural expectation`
- `evidence_requirements <- minimum_evidence_expectation`
- `finding_criteria <- deterministic_failure_test`
- `gdpr_article_mappings <- article + related_articles`

Acceptance gate:
- Adapter outputs parse in all existing consumers without schema break.

### Phase 3 - Rule-to-Signal Crosswalk
Actions:
- Create explicit rule->AiGov signal mapping.
- Mark mapping mode per rule: `direct`, `derived`, `manual_required`.

Acceptance gate:
- Crosswalk coverage threshold met:
  - 100% of rules have mapping status
  - unresolved `manual_required` list is explicit and bounded

### Phase 4 - Rebuild Calibration Rule Mapping
Actions:
- Rebuild case->rule mapping from new legal pack:
  - step A: article prefilter
  - step B: signal-aware narrowing
  - step C: per-case cap policy
- Emit:
  - `calibration_to_gdpr_rules_v1.json`

Acceptance gate:
- For 12-case set:
  - all infringement/uncertain cases have non-empty rule sets
  - compliant control case may remain empty by policy
  - no case exceeds cap

### Phase 5 - Judge Context A/B Re-run
Actions:
- Run full A/B with updated mapping/context pack on selected models.
- Compare against current baseline:
  - verdict correctness
  - required signal recall
  - allowed precision
  - citation recall

Acceptance gate:
- Enriched mode is non-inferior overall and improves at least one high-value metric (or has explicit justified tradeoff).

### Phase 6 - Cutover Decision
Actions:
- If Phase 5 passes: set new pack as legal default for enrichment.
- Keep D2 as procedural-only context source.
- If Phase 5 fails: retain dual mode and open corrective iteration.

Acceptance gate:
- One explicit decision log entry:
  - `adopted` or `deferred`
  - reasons
  - next corrective step

## 7) Missing Pieces to Resolve Before Full Cutover
1. Rule->signal crosswalk does not exist yet.
2. T0/T1/T2 evidence tier classification is missing for new rules.
3. Scenario-family tags for Bespoke routing are missing in new pack.
4. Locale/industry overlay links are not embedded at rule level.
5. Citation-grade source quote anchors are not embedded (article locator exists, direct quote anchors mostly absent).

## 8) Risk Controls
- Keep old D2 files intact until Phase 6 decision.
- Do not overwrite current mapping files in place during validation.
- Run parallel outputs with `_gdpr_v1` suffix first.

## 9) Execution Readiness
This plan is ready for EX execution in one batch:
- adapter artifacts
- crosswalk
- remapping
- A/B rerun
- cutover recommendation
