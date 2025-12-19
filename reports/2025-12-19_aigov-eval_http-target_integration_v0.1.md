# AiGov-eval HTTP Target Integration Report

**Date**: 2025-12-19

## Files Changed
- `aigov_eval/targets/http_target.py`
- `aigov_eval/targets/__init__.py`
- `aigov_eval/runner.py`
- `aigov_eval/evidence.py`
- `aigov_eval/cli.py`
- `tests/minimal_loop/test_http_target.py`
- `README_MINIMAL_LOOP.md`

## How the HTTP Target Works
- The new `http` target POSTs to `{base_url}/chat` with the last user message, session id, and leak controls.
- The response JSON is parsed as `{ "reply": "...", "server_audit": {...} }`.
- The assistant text is stored verbatim in the transcript; `server_audit` is attached to metadata.

## Evidence Pack Capture
- Each assistant turn for the HTTP target appends the `server_audit` payload to `evidence_pack.http_audit`.
- The list is aligned by assistant turn order so leaks map directly to transcript turns.

## Local TargetLab Commands (Expected PASS/FAIL)
PII strict (PASS):
```bash
python -m aigov_eval run --scenario examples/scenarios/pii_disclosure_positive_control.yaml --target http --target-config-json '{"base_url":"http://localhost:8000","leak_mode":"strict","leak_profile":"pii","use_llm":false}' --out runs/
```

PII leaky (FAIL):
```bash
python -m aigov_eval run --scenario examples/scenarios/pii_disclosure_positive_control.yaml --target http --target-config-json '{"base_url":"http://localhost:8000","leak_mode":"leaky","leak_profile":"pii","use_llm":false}' --out runs/
```

Special category strict (PASS):
```bash
python -m aigov_eval run --scenario examples/scenarios/special_category_leak_positive_control.yaml --target http --target-config-json '{"base_url":"http://localhost:8000","leak_mode":"strict","leak_profile":"special_category","use_llm":false}' --out runs/
```

Special category leaky (FAIL):
```bash
python -m aigov_eval run --scenario examples/scenarios/special_category_leak_positive_control.yaml --target http --target-config-json '{"base_url":"http://localhost:8000","leak_mode":"leaky","leak_profile":"special_category","use_llm":false}' --out runs/
```
