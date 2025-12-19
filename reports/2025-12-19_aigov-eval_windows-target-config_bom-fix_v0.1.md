# AiGov-eval Windows Target Config BOM Fix Report

**Date**: 2025-12-19

## What Changed
- Target config file loading now uses UTF-8 BOM-tolerant decoding.
- Added example HTTP target config JSON and tests for BOM and example parsing.
- Documented file-based PowerShell invocation to avoid quoting issues.

## Why
- Windows editors often add BOM; PowerShell JSON quoting is fragile.

## Recommended PowerShell Commands
```bash
python -m aigov_eval.cli run --scenario examples/scenarios/pii_disclosure_positive_control.yaml --target http --target-config-file examples/target_config_http.json --out runs/
```

## Test Command + Output
```bash
python -m pytest tests/minimal_loop -q
```
Output summary:
```
19 passed in 0.30s
```
