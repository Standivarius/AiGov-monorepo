# Evidence ID Format v0.1 (Deterministic)

Purpose: define a deterministic, contract-level evidence_id format so
judgments/reports can resolve evidence references to the evidence pack manifest.

## Canonical format

Evidence IDs MUST follow:

`EVID-###:<relpath>[#<json_pointer>]`

Where:
- `EVID-###` is an existing evidence artifact prefix from the planning registry.
- `relpath` MUST match `manifest.files[].relpath` in
  `packages/specs/schemas/evidence_pack_manifest_v1.json`.
- `#<json_pointer>` is optional and, if present, refers to a JSON Pointer within
  the referenced file.

The manifest entry with the matching `evidence_id` provides the canonical
`sha256` for integrity checks.

## Deterministic resolution

1) Parse the `evidence_id` into prefix + relpath (+ optional json_pointer).
2) Look up a matching `manifest.files[].evidence_id`.
3) Use `manifest.files[].sha256` as the integrity hash for that evidence_id.
4) If `json_pointer` is present, it scopes the reference within the file; the
   hash still applies to the full file recorded in the manifest.

## Examples

- Transcript: `EVID-004:transcript.json`
- Run manifest v0: `EVID-004:run_manifest_v0.json`
- Judgments: `EVID-006:judgments.json`
- Evidence pack signal item: `EVID-005:evidence_pack.json#/signals/0`
