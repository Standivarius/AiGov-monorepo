# AiGov-eval Windows Config File Hardening Report

**Date**: 2025-12-19

## What Changed
- Added Windows-safe TargetLab config example and HTTP payload examples.
- Updated README to recommend `--target-config-file` and provided a PowerShell 5.1-safe no-BOM snippet.
- Ignored root-level throwaway `target_config_*.json` and `targetlab_*.json` files.

## Commands
Create a UTF-8 no-BOM config (PowerShell 5.1 safe):
```powershell
[System.IO.File]::WriteAllText("target_config_http.json", '{"base_url":"http://localhost:8000","chat_path":"/chat","leak_mode":"strict","leak_profile":"special_category","use_llm":false}', (New-Object System.Text.UTF8Encoding($false)))
```

Run TargetLab HTTP:
```bash
python -m aigov_eval.cli run --scenario examples/scenarios/special_category_leak.yaml --target http --target-config-file examples/target_configs/target_config_http_localhost.json --out runs/ --debug
```

Tests:
```bash
python -m pytest tests/minimal_loop -q
```
Output summary:
```
22 passed, 1 skipped in 0.49s
```
