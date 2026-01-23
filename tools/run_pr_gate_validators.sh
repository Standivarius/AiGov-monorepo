#!/usr/bin/env bash
set -euo pipefail

python3 tools/validate_verdict_strictness.py \
  --fixture tools/fixtures/validators/verdict_strictness_pass.json

python3 tools/validate_doc_mode_operational_evidence.py \
  --judgments tools/fixtures/validators/doc_mode_judgments.json \
  --limitations tools/fixtures/validators/doc_mode_limitations_pass.json

python3 tools/validate_equivalence_labeling.py \
  --fixture tools/fixtures/validators/equivalence_labeling_pass.json

python3 tools/validate_golden_contamination.py \
  --citations tools/fixtures/validators/retrieval_citations_pass.json
