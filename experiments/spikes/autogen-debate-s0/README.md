# AutoGen Debate Spike (EDPB Grounded)

This spike builds a courtroom-style multi-agent audit loop with:
- `Lead_Auditor` (retrieves only from `docs_auditor_manual/`)
- `Client_Defender` (retrieves only from `docs_client_evidence/`)
- `GDPR_Judge` (rules-driven JSON verdict)

It also includes an extraction pipeline that converts the EDPB D2 methodology PDF into a structured `MasterAuditCatalog` used at runtime.

## Files
- `extract_edpb_rules.py`: Parse -> map -> self-correct -> output JSON/YAML.
- `schemas.py`: Pydantic schema for master audit rules and judge verdict.
- `main.py`: AutoGen runtime that injects one testcase into Auditor/Judge prompts.
- `generate_dummy_docs.py`: Creates minimal local docs for smoke tests.

## Quick Start
1. Install dependencies:
   - `C:/Python312/python.exe -m pip install -r requirements.txt`
2. Create dummy docs:
   - `C:/Python312/python.exe generate_dummy_docs.py`
3. Extract EDPB rules:
   - `C:/Python312/python.exe extract_edpb_rules.py`
4. Run debate:
   - Set either `OPENROUTER_API_KEY` (recommended here) or `OPENAI_API_KEY`
   - `C:/Python312/python.exe main.py --test-case-id LEG_BASIS_1`

## Notes
- GDPR article mapping is strict-by-default: explicit references only.
- Missing mappings are retained with validation issues for manual legal review.
- Defender never gets access to the auditor-manual vector store.

