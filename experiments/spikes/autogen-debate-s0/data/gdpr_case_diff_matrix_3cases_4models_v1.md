# GDPR Case Diff Matrix (3 cases x 4 models) v1

Cases: `cal_001`, `cal_006`, `cal_007`

## Model Summary (avg enriched-generic delta)
- `mistralai/mistral-large-2512`: `-0.067` | reasons: `{'signal_precision_drop': 1, 'no_regression_or_improved': 1, 'required_signal_miss': 1}`
- `qwen/qwen3.5-plus-02-15`: `-0.033` | reasons: `{'no_regression_or_improved': 1, 'citation_recall_drop': 1, 'signal_precision_drop': 1}`
- `openai/gpt-5.3-chat`: `-0.094` | reasons: `{'citation_recall_drop': 1, 'no_regression_or_improved': 1, 'required_signal_miss': 1}`
- `anthropic/claude-opus-4.6`: `-0.260` | reasons: `{'citation_recall_drop': 1, 'verdict_regression': 1, 'signal_precision_drop': 1}`

## Per-case rows
| Model | Case | Delta | GQ | EQ | G Verdict | E Verdict | Dominant Reason | Rules |
|---|---|---:|---:|---:|---|---|---|---:|
| mistralai/mistral-large-2512 | cal_001_lack_of_consent | -0.050 | 0.967 | 0.917 | INFRINGEMENT | INFRINGEMENT | signal_precision_drop | 8 |
| mistralai/mistral-large-2512 | cal_006_cross_border_transfer | +0.000 | 1.000 | 1.000 | INFRINGEMENT | INFRINGEMENT | no_regression_or_improved | 7 |
| mistralai/mistral-large-2512 | cal_007_automated_decision | -0.150 | 1.000 | 0.850 | INFRINGEMENT | INFRINGEMENT | required_signal_miss | 7 |
| qwen/qwen3.5-plus-02-15 | cal_001_lack_of_consent | +0.000 | 0.967 | 0.967 | INFRINGEMENT | INFRINGEMENT | no_regression_or_improved | 8 |
| qwen/qwen3.5-plus-02-15 | cal_006_cross_border_transfer | -0.033 | 0.967 | 0.933 | INFRINGEMENT | INFRINGEMENT | citation_recall_drop | 7 |
| qwen/qwen3.5-plus-02-15 | cal_007_automated_decision | -0.067 | 1.000 | 0.933 | INFRINGEMENT | INFRINGEMENT | signal_precision_drop | 7 |
| openai/gpt-5.3-chat | cal_001_lack_of_consent | -0.033 | 0.950 | 0.917 | INFRINGEMENT | INFRINGEMENT | citation_recall_drop | 8 |
| openai/gpt-5.3-chat | cal_006_cross_border_transfer | +0.000 | 0.867 | 0.867 | INFRINGEMENT | INFRINGEMENT | no_regression_or_improved | 7 |
| openai/gpt-5.3-chat | cal_007_automated_decision | -0.250 | 1.000 | 0.750 | INFRINGEMENT | INFRINGEMENT | required_signal_miss | 7 |
| anthropic/claude-opus-4.6 | cal_001_lack_of_consent | -0.033 | 0.950 | 0.917 | INFRINGEMENT | INFRINGEMENT | citation_recall_drop | 8 |
| anthropic/claude-opus-4.6 | cal_006_cross_border_transfer | -0.667 | 0.867 | 0.200 | INFRINGEMENT | UNDECIDED | verdict_regression | 7 |
| anthropic/claude-opus-4.6 | cal_007_automated_decision | -0.080 | 1.000 | 0.920 | INFRINGEMENT | INFRINGEMENT | signal_precision_drop | 7 |
