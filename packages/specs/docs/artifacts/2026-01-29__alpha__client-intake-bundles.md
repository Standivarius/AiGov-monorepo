# Alpha Workflow: Client Intake → Compiled GDPR Bundles

**Date**: 2026-01-29
**Status**: Alpha (GDPR-only, fixture-based)
**Scope**: Deterministic compilation from client intake to runnable scenario bundles

---

## Workflow Overview

```
intake.json                   (client policy/target profiles)
    ↓
build_client_bundle.py        (deterministic compiler)
    ↓
manifest.json + scenarios/    (compiled bundle ready for Stage A)
```

**Determinism guarantee**: Identical inputs → byte-identical outputs (same bundle_hash, same scenario checksums)

**Fail-closed principle**: Missing overrides directory, empty overrides, or unknown base_scenario_id references → hard error (no silent fallback)

---

## CLI Invocation

### Basic Usage (No Client Overrides)

```bash
python3 -m packages.ep.aigov_ep.scenario.compiler \
  --base-dir packages/specs/scenarios/library/base/gdpr \
  --output-dir /tmp/bundles/default_client
```

**Output**:
- `/tmp/bundles/default_client/manifest.json`
- `/tmp/bundles/default_client/scenarios/*.json`

### With Client Overrides

```bash
python3 -m packages.ep.aigov_ep.scenario.compiler \
  --base-dir packages/specs/scenarios/library/base/gdpr \
  --overrides-dir packages/specs/scenarios/overrides/acme_hospital \
  --output-dir /tmp/bundles/acme_hospital
```

**Override sources**:
- `overrides/acme_hospital/*.json` files reference `base_scenario_id` from base library
- Each override contains `policy_profile` (DSAR channels, verification constraints)
- Compiler merges base scenario + override → compiled instance

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
- `bundle_hash`: SHA256 of sorted `path:sha256` pairs (deterministic across runs)
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

### 1. Overrides Directory Missing

```bash
# User typo: "overides" instead of "overrides"
python3 -m ... --overrides-dir packages/specs/scenarios/overides/client_x
```

**Error**: `ValueError: Overrides directory does not exist: .../overides/client_x`

**Fix**: Correct path to `overrides/client_x`

---

### 2. Empty Overrides Directory

```bash
# Directory exists but contains no *.json files
mkdir -p /tmp/empty_overrides
python3 -m ... --overrides-dir /tmp/empty_overrides
```

**Error**: `ValueError: overrides_dir provided (/tmp/empty_overrides) but no *.json files found. Check path or use overrides_dir=None for no overrides.`

**Fix**: Add override files or remove `--overrides-dir` flag

---

### 3. Empty String Overrides Directory

```bash
# Accidental empty string (shell variable not set)
python3 -m ... --overrides-dir ""
```

**Error**: `ValueError: overrides_dir cannot be empty string`

**Fix**: Remove flag or provide valid path

---

### 4. Unknown base_scenario_id in Override

```json
// overrides/client_x/stale.json
{
  "base_scenario_id": "GDPR-999",  // Scenario removed from base library
  "client_id": "client_x",
  "policy_profile": {...}
}
```

**Error**: `ValueError: Overrides reference unknown base_scenario_id(s): ['GDPR-999']`

**Fix**: Remove stale override or update `base_scenario_id` to valid scenario

---

### 5. Missing policy_profile in Override

```json
// overrides/client_x/incomplete.json
{
  "base_scenario_id": "GDPR-001",
  "client_id": "client_x"
  // Missing "policy_profile"
}
```

**Error**: `ValueError: Override for GDPR-001 missing 'policy_profile'`

**Fix**: Add required `policy_profile` object with `supported_dsar_channels`, `right_to_erasure_handling`, etc.

---

## Out of Scope (Alpha)

### Not Supported Yet

- **Non-GDPR frameworks**: ISO27001, ISO42001, AI_ACT scenarios (base library empty)
- **Scenario subset selection**: Compiler processes all `*.json` in `base_dir` (no filtering by role/tags)
- **Multi-channel expansion**: Override `channel_variants` not yet implemented (single instance per override)
- **LLM-assisted authoring**: Base scenarios hand-authored only

### Future Enhancements

- Scenario filtering by `role`, `applies_to`, `tags` (e.g., only `role=customer_service`)
- Channel variant expansion (email vs in_chat vs portal)
- Provenance tracking: base_scenario_checksum + override_checksum in compiled instance
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

Run compilation twice and verify byte-identical output:

```bash
# Compile bundle 1
python3 -m packages.ep.aigov_ep.scenario.compiler \
  --base-dir tools/fixtures/scenario_compile/base \
  --overrides-dir tools/fixtures/scenario_compile/overrides \
  --output-dir /tmp/bundle1

# Compile bundle 2 (same inputs)
python3 -m packages.ep.aigov_ep.scenario.compiler \
  --base-dir tools/fixtures/scenario_compile/base \
  --overrides-dir tools/fixtures/scenario_compile/overrides \
  --output-dir /tmp/bundle2

# Verify identical bundle_hash
diff /tmp/bundle1/manifest.json /tmp/bundle2/manifest.json
# Should show no differences

# Verify byte-identical manifest
sha256sum /tmp/bundle1/manifest.json /tmp/bundle2/manifest.json
# Both checksums should match
```

**Expected**: Zero diff, identical SHA256 checksums for `manifest.json` and all `scenarios/*.json` files

---

## Next Steps (Post-Alpha)

1. **Expand base library**: Add 20-30 GDPR scenarios (coverage for PII_DISCLOSURE, CONSENT, ERASURE, etc.)
2. **Implement channel expansion**: Override with `channel_variants: ["email", "in_chat"]` → 2 compiled instances
3. **Add signal validation**: Fail closed if `canonical_signal_ids` reference unknown signals
4. **Determinism test in CI**: Automated test verifying byte-identical compilation
5. **Integration with Stage A**: Wire compiled bundles into `packages/ep/aigov_ep/execute/runner.py`

---

## References

- Scenario card schema: `packages/specs/schemas/scenario_card/scenario-card-schema-v1.2.md`
- Client intake contract: `packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md`
- Override schema: (TBD - `client_scenario_override_v0.schema.json`)
- Compiler implementation: `packages/ep/aigov_ep/scenario/compiler.py`
