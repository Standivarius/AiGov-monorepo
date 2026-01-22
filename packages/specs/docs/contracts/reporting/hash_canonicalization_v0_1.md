# Hash Canonicalization v0.1 (JCS/RFC8785)

Defines canonicalization for hashing JSON artifacts used in determinism and
reporting integrity checks.

## Scope
Applies to:
- Evidence pack manifests
- Judgments output (`judgments.json`)
- Report export manifests

## Rule
- Canonicalize JSON using JCS (RFC8785) before hashing.
- Hash over the canonicalized UTF-8 byte stream.

## Required behavior
- Object keys MUST be lexicographically sorted.
- Numbers MUST use the shortest round-trippable representation (per RFC8785).
- No insignificant whitespace is preserved.

## Good looks like
- Hashes match across implementations when inputs are semantically identical.

## Bad looks like
- Hashes change due to JSON key ordering or whitespace differences.

## How to decide
- If the artifact is JSON and used for integrity/determinism, apply JCS.
