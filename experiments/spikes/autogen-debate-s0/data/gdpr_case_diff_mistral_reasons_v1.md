# Mistral Negative Delta Diagnosis (3-case deep dive)

Scope: `cal_001_lack_of_consent`, `cal_006_cross_border_transfer`, `cal_007_automated_decision`  
Model: `mistralai/mistral-large-2512`  
Context mode: signal-aware enriched prompt (legal-first GPT rules + procedural fallback)

## Case-level reasons

### 1) `cal_001_lack_of_consent`
- Generic: `q=0.967`, verdict `INFRINGEMENT`, signals:
  - `inadequate_transparency`
  - `lack_of_consent`
  - `purpose_limitation_breach`
- Enriched: `q=0.917`, verdict `INFRINGEMENT`, signals:
  - generic signals above + extra `unlawful_processing`
- Dominant regression: **signal_precision_drop**
- Why:
  - Expected signal set in this case does not include `unlawful_processing` as allowed extra.
  - Enriched prompt pushed one additional legal-true but case-scoring-disallowed signal, reducing precision.

### 2) `cal_006_cross_border_transfer`
- Generic: `q=1.000`, verdict `INFRINGEMENT`
- Enriched: `q=1.000`, verdict `INFRINGEMENT`
- Dominant regression: **none** (no delta)
- Why:
  - Context pack was aligned with transfer obligations; enriched did not harm this case.

### 3) `cal_007_automated_decision`
- Generic: `q=1.000`, verdict `INFRINGEMENT`, signals:
  - `inadequate_transparency`
  - `profiling_without_safeguards`
  - `rights_violation`
- Enriched: `q=0.850`, verdict `INFRINGEMENT`, signals:
  - `profiling_without_safeguards`
  - `rights_violation`
- Dominant regression: **required_signal_miss**
- Why:
  - Enriched output dropped `inadequate_transparency`, which is required/expected in this calibration case.
  - Verdict stayed correct, but recall loss drove the quality drop.

## Rules payload shape used (signal-aware run)
- `cal_001`: 8 rules (6 legal + 2 procedural)
- `cal_006`: 7 rules
- `cal_007`: 7 rules

Observed pattern:
- The remaining negative delta on Mistral is no longer from verdict collapse.
- It is now mostly a **signal calibration mismatch**:
  - over-including a legal-but-unexpected extra signal (`cal_001`)
  - under-including one required signal (`cal_007`)

## Cross-model check on the same 3 cases
From `gdpr_case_diff_matrix_3cases_4models_v1`:
- `mistralai/mistral-large-2512`: avg delta `-0.067`
- `qwen/qwen3.5-plus-02-15`: avg delta `-0.033`
- `openai/gpt-5.3-chat`: avg delta `-0.094`
- `anthropic/claude-opus-4.6`: avg delta `-0.260`

Interpretation:
- This is not only a Mistral issue; all tested models show some regression pressure on this strict 3-case slice.
- Mistral regression is moderate and concentrated in signal-level scoring behavior, not verdict-level failure.
