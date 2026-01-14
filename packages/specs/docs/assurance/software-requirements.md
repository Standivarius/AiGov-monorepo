# Software requirements (AIGov) — v0.x

Purpose: a stable set of **requirement IDs** referenced by ADRs/architecture decisions.

## SR-00 Evidence integrity and auditability
- **SR-001** Every run MUST produce `run_manifest` (intent) and `result_manifest` (outputs).
- **SR-002** Every artefact referenced by `result_manifest` MUST have a cryptographic hash recorded (sha256 minimum).
- **SR-003** Manifests MUST be immutable once written; changes create new manifests (append-only).
- **SR-004** Exports MUST reference evidence by `run_id` + artefact refs/hashes (no “free text” claims).
- **SR-005** If manifests/hashes cannot be produced, the run MUST fail as non-auditable.

## SR-10 Data minimisation (default)
- **SR-101** Default mode MUST avoid storing raw prompts/responses at rest unless explicitly enabled.
- **SR-102** When redaction/anonymisation is applied, the system MUST record the method/version used.
- **SR-103** Retention configuration MUST be explicit, versioned, and captured in `run_manifest`.

## SR-20 Deterministic judgement and replay
- **SR-201** Offline judgement MUST be deterministic given fixed inputs and fixed model parameters.
- **SR-202** Replays MUST detect drift and record deltas (new `result_manifest`).
- **SR-203** Judgement outputs MUST be attach-by-reference; no mutation-in-place.

## SR-30 Contract validation
- **SR-301** Schema validation MUST be fail-closed at ingest and export boundaries.
- **SR-302** Schema namespaces MUST be explicit (specs vs eval harness flexibility).

## SR-40 Storage backends
- **SR-401** Filesystem backend MUST preserve artefact identity (stable paths/refs) and hashes.
- **SR-402** CAS backend is OPTIONAL in v0.x; design MUST remain CAS-ready by keeping content hashes canonical.

## SR-50 Scout vs Judge consistency
- **SR-501** Judge outputs are canonical verdict artefacts.
- **SR-502** Scout MAY add non-canonical signals but MUST NOT overwrite judge artefacts.
- **SR-503** Scout view MUST surface `judge_verdict_hash` and compare to `result_manifest` for integrity.
