# AiGov-eval OpenRouter Local Secrets Handling Report

**Date**: 2025-12-19

## Changes
- Added a minimal `.env` loader in `aigov_eval/env.py` and wired it into the CLI.
- Enforced a guard that fails fast when `OPENROUTER_API_KEY` is missing for the `mock-llm` target.
- Documented local setup steps in `README_MINIMAL_LOOP.md`.
- Added `.env.example` with required and optional OpenRouter variables.
- Updated `.gitignore` to ignore `.env` files (including nested `.env`).

## Files Updated/Added
- `aigov_eval/env.py`
- `aigov_eval/cli.py`
- `aigov_eval/targets/mock_llm.py`
- `README_MINIMAL_LOOP.md`
- `.env.example`
- `.gitignore`
- `reports/2025-12-19_aigov-eval_openrouter_env_handling_v0.1.md`

## Confirmation
- `.env` is ignored by git and not tracked.
- No secrets were written to disk or committed.
