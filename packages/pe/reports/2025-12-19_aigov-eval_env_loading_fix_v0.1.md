# AiGov-eval .env Loading Fix Report

**Date**: 2025-12-19

## What Was Wrong
- The CLI guard could run before `.env` was loaded consistently, so `OPENROUTER_API_KEY` was missing even when present.
- Environment loading happened in multiple places, which made ordering unreliable.

## Fix
- Added a single bootstrap in `aigov_eval/env.py` using `python-dotenv` with `find_dotenv()` and `load_dotenv(..., override=False)`.
- CLI now initializes environment exactly once before any key checks.
- Mock LLM adapter relies on the already-bootstrapped environment.
- Added `--debug` flag to show whether `.env` was found and which keys were loaded (names only).
- Added a regression test that simulates a local `.env` and ensures CLI run does not fail.

## Files Touched
- `aigov_eval/env.py`
- `aigov_eval/cli.py`
- `aigov_eval/targets/mock_llm.py`
- `README_MINIMAL_LOOP.md`
- `tests/minimal_loop/test_cli_env_loading.py`
- `reports/2025-12-19_aigov-eval_env_loading_fix_v0.1.md`

## Safety
- `.env` remains ignored and is not tracked.
- No secret values are logged or stored.
