# AiGov-eval HTTP Target Messages Contract Fix Report

**Date**: 2025-12-19

## What Changed
- HTTP target now sends `messages` list (role/content) instead of single `message`.
- Preserves all turns and maps leak profiles (`pii_basic` -> `pii`, `special_category_basic` -> `special_category`).
- Non-2xx errors now include status, body, endpoint, and payload keys.

## Why
- TargetLab /chat expects `messages`, and 422 errors reported missing `body.messages`.

## CLI Command
```bash
python -m aigov_eval.cli run --scenario examples/scenarios/pii_disclosure_positive_control.yaml --target http --target-config-file examples/target_config_http.json --out runs/
```
