# Alpha Workflow: Client Intake → Compiled GDPR Bundles

**Date**: 2026-01-29
**Status**: Alpha (GDPR-only, fixture-based)
**Scope**: Deterministic compilation from client intake to runnable scenario bundles

---

## Workflow Overview

```
intake.json                   (client policy/target profiles)
    ↓
compile_bundle() API          (deterministic compiler)
    ↓
manifest.json + scenarios/    (compiled bundle ready for Stage A)
```

**Determinism guarantee**: Identical inputs → stable `bundle_hash` across runs

**Note on determinism**: The `bundle_hash` is computed from sorted scenario checksums and is stable for identical inputs. The manifest may include output directory paths (e.g., `bundle_dir` field), so compare `bundle_hash` values to verify determinism rather than byte-comparing entire manifests.

**Fail-closed principle**: Missing overrides directory, empty overrides, or unknown `base_scenario_id` references → hard error (no silent fallback)

---

## Available Today: Python API

The compiler is available as a Python API in `packages/ep/aigov_ep/scenario/compiler.py`.

### Basic Usage (No Client Overrides)

```python
from packages.ep.aigov_ep.scenario.compiler import compile_bundle

manifest = compile_bundle(
    base_dir="packages/specs/scenarios/library/base/gdpr",
    overrides_dir=None,
    output_dir="/tmp/bundles/default_client"
)

print(f"Bundle hash: {manifest['bundle_hash']}")
```

**Output**:
- `/tmp/bundles/default_client/manifest.json`
- `/tmp/bundles/default_client/scenarios/*.json`

### With Client Overrides

```python
from packages.ep.aigov_ep.scenario.compiler import compile_bundle

manifest = compile_bundle(
    base_dir="packages/specs/scenarios/library/base/gdpr",
    overrides_dir="packages/specs/scenarios/overrides/acme_hospital",
    output_dir="/tmp/bundles/acme_hospital"
)
```

**Override sources**:
- `overrides/acme_hospital/*.json` files reference `base_scenario_id` from base library
- Each override contains `policy_profile` (DSAR channels, verification constraints)
- Compiler merges base scenario + override → compiled instance

---

## Planned: CLI Tooling (Milestone 2)

A command-line wrapper is planned for future milestones:

```bash
# Planned syntax (not yet available)
python3 tools/build_client_bundle.py \
  --base-dir packages/specs/scenarios/library/base/gdpr \
  --overrides-dir packages/specs/scenarios/overrides/acme_hospital \
  --output-dir /tmp/bundles/acme_hospital
```

For now, use the Python API directly (see above).

---

## Expected Outputs

### manifest.json Structure

```json
{
  "schema_version": "0.1.0",
  "bundle_dir": "/tmp/bundles/acme_hospital",
  "scenarios": [
    {
      "path": "scenarios/GDPR-001__acme_hospital.json",
      "sha256": "abc123...",
      "scenario_id": "GDPR-001",
      "scenario_instance_id": "GDPR-001__acme_hospital"
    }
  ],
  "bundle_hash": "def456..."
}
```

**Key fields**:
- `bundle_hash`: SHA256 of sorted `path:sha256` pairs (stable for identical inputs)
- `scenarios[]`: Sorted by `path` (determinism guarantee)
- `scenario_instance_id`: Base scenario ID + client suffix (if override applied)

### Compiled Scenario Structure

```json
{
  "scenario_id": "GDPR-001",
  "scenario_instance_id": "GDPR-001__acme_hospital",
  "title": "Third-party PII leak via account lookup",
  "framework": "GDPR",
  "turns": [...],
  "override": {
    "client_id": "acme_hospital",
    "override_type": "partial_patch",
    "base_scenario_id": "GDPR-001"
  },
  "policy_profile": {
    "supported_dsar_channels": ["email", "portal"],
    "right_to_erasure_handling": {...}
  }
}
```

---

## Common Failure Modes (Fail-Closed)

All failures raise `ValueError` with descriptive messages. Representative failure conditions:

### 1. Overrides Directory Missing

**Condition**: `overrides_dir` provided but path does not exist

**Behavior**: Raises `ValueError` indicating the directory path does not exist

**Fix**: Correct path typo or remove `overrides_dir` parameter if no overrides needed

---

### 2. No Base Scenarios Found

**Condition**: `base_dir` contains no `*.json` files

**Behavior**: Raises `ValueError` indicating no base scenarios found

**Fix**: Verify `base_dir` path and ensure it contains scenario JSON files

---

### 3. Unknown base_scenario_id in Override

**Condition**: Override references `base_scenario_id` not present in base library

**Example override**:
```json
{
  "base_scenario_id": "GDPR-999",
  "client_id": "client_x",
  "policy_profile": {...}
}
```

**Behavior**: Raises `ValueError` listing the unknown scenario IDs

**Fix**: Remove stale override or update `base_scenario_id` to valid scenario

---

### 4. Duplicate Override Files

**Condition**: Multiple override files reference the same `base_scenario_id`

**Behavior**: Raises `ValueError` indicating duplicate override

**Fix**: Remove duplicate override files (only one override per base scenario)

---

### 5. Missing Required Fields

**Condition**: Base scenario or override missing required fields (e.g., `scenario_id`, `base_scenario_id`)

**Behavior**: Raises `ValueError` indicating which file and field are missing

**Fix**: Add required field to JSON file

---

## Out of Scope (Alpha)

### Not Supported Yet

- **Non-GDPR frameworks**: ISO27001, ISO42001, AI_ACT scenarios (base library empty)
- **Scenario subset selection**: Compiler processes all `*.json` in `base_dir` (no filtering by role/tags)
- **Multi-channel expansion**: Override `channel_variants` not yet implemented (single instance per override)
- **LLM-assisted authoring**: Base scenarios hand-authored only

### Future Enhancements

- CLI wrapper tool (`tools/build_client_bundle.py`)
- Scenario filtering by `role`, `applies_to`, `tags` (e.g., only `role=customer_service`)
- Channel variant expansion (email vs in_chat vs portal)
- Provenance tracking: `base_scenario_checksum` + `override_checksum` in compiled instance
- Validation: `canonical_signal_ids` exist in `signals.json` (currently unchecked)

---

## CI Fixture Setup

**Base scenarios**: `tools/fixtures/scenario_compile/base/` (1-2 minimal GDPR scenarios)
**Overrides**: `tools/fixtures/scenario_compile/overrides/` (1 override file)

**Why fixtures?**: Full GDPR-253 library not yet available; CI validates compiler mechanics with tiny dataset

**Tests**:
- `packages/pe/tests/scenario/test_bundle_compiler.py::test_compile_bundle_manifest` (pass)
- `packages/pe/tests/scenario/test_bundle_compiler.py::test_compile_bundle_missing_overrides_dir` (fail-closed)
- `packages/pe/tests/scenario/test_bundle_compiler.py::test_compile_bundle_unknown_override_base_id` (fail-closed)

---

## Determinism Validation

Run compilation twice with identical inputs and verify stable `bundle_hash`:

```python
from packages.ep.aigov_ep.scenario.compiler import compile_bundle

# Compile bundle 1
manifest1 = compile_bundle(
    base_dir="tools/fixtures/scenario_compile/base",
    overrides_dir="tools/fixtures/scenario_compile/overrides",
    output_dir="/tmp/bundle1"
)

# Compile bundle 2 (same inputs)
manifest2 = compile_bundle(
    base_dir="tools/fixtures/scenario_compile/base",
    overrides_dir="tools/fixtures/scenario_compile/overrides",
    output_dir="/tmp/bundle2"
)

# Verify identical bundle_hash
assert manifest1["bundle_hash"] == manifest2["bundle_hash"]
print(f"✅ Determinism verified: {manifest1['bundle_hash']}")
```

**Expected**: Identical `bundle_hash` values across runs

**Note**: Output directory paths in manifest may differ (`/tmp/bundle1` vs `/tmp/bundle2`), but `bundle_hash` is path-independent and remains stable.

---

## Next Steps (Post-Alpha)

1. **CLI wrapper**: Add `tools/build_client_bundle.py` for command-line usage
2. **Expand base library**: Add 20-30 GDPR scenarios (coverage for PII_DISCLOSURE, CONSENT, ERASURE, etc.)
3. **Implement channel expansion**: Override with `channel_variants: ["email", "in_chat"]` → 2 compiled instances
4. **Add signal validation**: Fail closed if `canonical_signal_ids` reference unknown signals
5. **Automated determinism test**: CI test verifying stable `bundle_hash` across runs
6. **Integration with Stage A**: Wire compiled bundles into `packages/ep/aigov_ep/execute/runner.py`

---

## References

- Scenario card schema: `packages/specs/schemas/scenario_card/scenario-card-schema-v1.2.md`
- Client intake contract (v0.1): `packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md`
- Client intake schema (v0.2): `packages/specs/schemas/client_intake_v0_2.schema.json`
- Override schema: (TBD - `client_scenario_override_v0.schema.json`)
- Compiler implementation: `packages/ep/aigov_ep/scenario/compiler.py`
