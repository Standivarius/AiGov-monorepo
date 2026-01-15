# Runbook — Batch Calibration (GDPR Phase 0)

## Preconditions
- Python env available
- For LIVE judge runs: relevant API keys / config present in environment

## 1) Always-run checks (cement baseline)
### A) Unit tests
```bash
python -m pytest -q
