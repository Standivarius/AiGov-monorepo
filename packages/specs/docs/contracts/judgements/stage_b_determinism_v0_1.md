# Stage B Determinism Tolerance v0.1

Defines normalization rules and determinism expectations for Stage B outputs.
This contract is doc-only and must not change verdict or signal taxonomies.

## Canonical references
- Verdict enum: `packages/specs/docs/contracts/taxonomy/verdicts.json`
- Signal IDs: `packages/specs/docs/contracts/taxonomy/signals.json`
- Judgments schema: `packages/specs/docs/contracts/judgements/judgments_v0.schema.json`
- Hash canonicalization: `packages/specs/docs/contracts/reporting/hash_canonicalization_v0_1.md`

## Normalization (required)
- Verdicts MUST be normalized to the canonical enum via `verdicts.json`.
- Signal IDs MUST be canonicalized to `signals.json`.
- Evidence IDs MUST reference evidence pack artifact IDs (no free-form labels).

## Determinism modes
- **strict (default)**: byte-for-byte identical `judgments.json` when inputs
  (evidence pack + judge config) are unchanged.
- **tolerant**: allowed only if explicitly declared; differences must be limited
  to whitespace or ordering that is erased by JCS canonicalization.

## Canonical hashing
- Determinism comparisons MUST use JCS/RFC8785 canonicalization before hashing.
- Hash inputs include: judgments output + judge manifest + evidence pack manifest.

## Material change (must be explicit)
A change is material if any of the following differ:
- `model_id`
- `base_model_version`
- `system_prompt_hash`
- `tools_schema_hash`
- `retrieval_corpus_hash`
- `verdicts_version` or `signals_version`
- `judge_instructions_template_ref`

If a material change occurs, determinism strictness resets and outputs must be
re-baselined with a new `judgement_id`.

## Good looks like
- Strict mode is the default and enforced in CI.
- Material changes are explicit and versioned.

## Bad looks like
- Silent judge config changes without new baselines.
- Verdict labels outside the canonical enum.

## How to decide
- If any input listed under material change differs, treat it as a new run.
- If differences are only ordering, rely on JCS canonicalization.
