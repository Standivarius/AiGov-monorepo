# M_Intake OSS Eval — OPA (v2026-02-06)

## Task 2R — OPA Deep Evaluation for M_Intake (code-grounded + runnable)

### Objective
Run a minimal OPA experiment and document a deterministic, code-grounded integration plan for policy_profile/readiness gating without implementing M_Intake.

### Inputs (code-grounded)
- Constitution: `packages/specs/docs/planning/2026-02-06/m_intake_constitution_2026-02-06.md`.
- Runbook: `packages/specs/docs/planning/2026-02-06/m_intake_codex_runbook_2026-02-06.md`.
- Codebase map: `packages/specs/docs/planning/2026-02-06/m_intake_codebase_map_2026-02-06.md`.
- Intake contract + runtime validation:
  - `packages/specs/docs/contracts/intake/client_intake_output_contract_v0_1.md`
  - `packages/specs/schemas/client_intake_v0_2.schema.json`
  - `packages/ep/aigov_ep/intake/validate.py`
- Scenario pipeline:
  - `packages/ep/aigov_ep/scenario/override.py`
  - `packages/ep/aigov_ep/scenario/compiler.py`
- PE tests + fixtures:
  - `packages/pe/tests/intake/test_intake_validation.py`
  - `tools/fixtures/validators/client_intake_v0_2_pass.json`
  - `tools/fixtures/validators/client_intake_v0_2_fail.json`
  - `tools/fixtures/validators/intake_output_context_fail_pack_order.json`

### Fit matrix status
- **Missing**: `packages/specs/docs/planning/2026-02-06/m_intake_monorepo_fit_matrix_2026-02-06.md` was not present in the repo at the provided path. Seam mapping below is grounded in the codebase map and runtime locations; confirm once the fit matrix is available.

---

## A) Monorepo seam mapping (exact paths)
OPA must sit **after** intake schema/contract validation and **before** scenario override generation to preserve fail-closed, contract-first behavior.

**Primary seam (intake validation gate):**
- `packages/ep/aigov_ep/intake/validate.py` — deterministic validation of policy_profile/context_profile; OPA should be invoked after this passes.
- `packages/ep/aigov_ep/cli.py` — CLI entrypoint for intake validation; should surface OPA deny as validation failure.

**Secondary seam (scenario pipeline gate):**
- `packages/ep/aigov_ep/scenario/override.py` — block override generation if OPA denies policy readiness.
- `packages/ep/aigov_ep/scenario/compiler.py` — block scenario bundle compilation if OPA denies policy readiness.

**PE evidence + fixtures:**
- `packages/pe/tests/intake/test_intake_validation.py` — extend with deterministic OPA decision cases once adapter is specified.
- `tools/fixtures/validators/client_intake_v0_2_pass.json` — baseline payload to derive OPA input.
- `tools/fixtures/validators/client_intake_v0_2_fail.json` — baseline payload to test deny path.
- `tools/fixtures/validators/intake_output_context_fail_pack_order.json` — ensures policy_pack_stack determinism pre-OPA.

---

## B) OPA runnable experiment (commands + verbatim output)

### Install (binary)
Downloaded OPA from GitHub release:
```
curl -L -o /tmp/opa https://github.com/open-policy-agent/opa/releases/download/v0.63.0/opa_linux_amd64_static
chmod +x /tmp/opa
```

### Version
Command:
```
/tmp/opa version
```
Output (verbatim):
```
Version: 0.63.0
Build Commit: bb30b153692aa77738b982e29424c8b24a1ad14a
Build Timestamp: 2024-03-28T15:50:15Z
Build Hostname: e0fc7320a0f2
Go Version: go1.22.1
Platform: linux/amd64
WebAssembly: unavailable
```

### Minimal eval (policy_profile/context_profile shape)
Policy file:
```
package aigov

# Allow if policy_pack_stack matches expected deterministic order
# and DSAR channels include email.

allow {
  input.context_profile.policy_pack_stack == ["GDPR_EU", input.context_profile.jurisdiction, input.context_profile.sector, "client"]
  input.policy_profile.supported_dsar_channels[_] == "email"
}

policy_result := {
  "decision": "allow",
  "reasons": ["policy_pack_stack_valid", "email_channel_supported"],
} {
  allow
}

policy_result := {
  "decision": "deny",
  "reasons": ["policy_pack_stack_invalid_or_missing_email"],
} {
  not allow
}
```
Input file:
```
{
  "policy_profile": {
    "supported_dsar_channels": ["email", "portal"],
    "right_to_erasure_handling": {
      "primary_channel": "email",
      "fallback_channels": ["portal"],
      "constraints": []
    },
    "known_client_constraints": []
  },
  "context_profile": {
    "jurisdiction": "NL",
    "sector": "public",
    "policy_pack_stack": ["GDPR_EU", "NL", "public", "client"]
  }
}
```
Command:
```
/tmp/opa eval -i /tmp/opa_input.json -d /tmp/opa_policy.rego "data.aigov.policy_result"
```
Output (verbatim):
```
{
  "result": [
    {
      "expressions": [
        {
          "value": {
            "decision": "allow",
            "reasons": [
              "policy_pack_stack_valid",
              "email_channel_supported"
            ]
          },
          "text": "data.aigov.policy_result",
          "location": {
            "row": 1,
            "col": 1
          }
        }
      ]
    }
  ]
}
```

---

## C) Adapter boundary (names only; no schema)
- **Input name:** `policy_input` (derived from intake payload).
- **Output name:** `policy_result` (OPA decision object).

**policy_input** should include only:
- `policy_profile` (supported_dsar_channels, right_to_erasure_handling, known_client_constraints)
- `context_profile` (jurisdiction, sector, policy_pack_stack)

**policy_result** should include only:
- `decision` (allow|deny)
- `reasons` (deterministically ordered strings)
- `policy_bundle_digest` (string)
- `input_digest` (string)

---

## D) Determinism + audit (decision logs + evidence refs)
- **Determinism controls:**
  - Pin OPA bundle (policy + data) by digest and store alongside artifacts.
  - Forbid Rego builtins that introduce nondeterminism (`time.now_ns`, `uuid`, `rand`, external HTTP calls).
  - Normalize any unordered collections before emitting `reasons` (sort lexicographically).
- **Audit/evidence handling (Model B compatible):**
  - Store a **policy decision artifact** as JSON with ordered keys.
  - Include `input_digest` (hash of `policy_input`) and `policy_bundle_digest` (hash of bundle).
  - If a timestamp is required for ops, record it outside the canonical artifact and **never** use it for policy decisions.

---

## E) License + operational modes (recommendation)
- **License:** OPA is **Apache 2.0** (compatible; must be registered in OSS tracking if adopted).
- **Operational modes:**
  - **Sidecar (HTTP API):** adds network dependency and runtime complexity; risks nondeterminism via remote policy updates.
  - **Embedded CLI (local binary):** deterministic when binary + bundle are pinned; simpler to sandbox; no network in runtime path.
  - **Wasm (in-process):** deterministic if wasm module + bundle are pinned; requires build pipeline to generate wasm.
- **Recommendation:** **Embedded CLI** with pinned binary + local bundle for initial AiGov integration, because it keeps the runtime path offline and deterministic while minimizing build-system changes. Consider **Wasm** later if in-process speed or tighter sandboxing is required.

---

## F) Integration implications (paths only; no edits)
- `packages/ep/aigov_ep/intake/validate.py`
- `packages/ep/aigov_ep/cli.py`
- `packages/ep/aigov_ep/scenario/override.py`
- `packages/ep/aigov_ep/scenario/compiler.py`
- `packages/pe/tests/intake/test_intake_validation.py`
- `tools/fixtures/validators/client_intake_v0_2_pass.json`
- `tools/fixtures/validators/client_intake_v0_2_fail.json`
- `tools/fixtures/validators/intake_output_context_fail_pack_order.json`

---

## Summary
- Ran a minimal OPA eval with an input shaped like AiGov’s policy_profile/context_profile and documented the exact output for deterministic gating.
- Mapped seams to existing intake validation + scenario override paths, aligned with contract-first intake validation.
- Recommended an embedded CLI mode with pinned bundles for deterministic, offline policy gating.

## Work performed
- Read constitution, runbook, and codebase map to preserve non-negotiable invariants.
- Installed OPA binary from GitHub release and executed `opa version` and a minimal `opa eval`.
- Documented adapter boundary, determinism controls, audit artifact handling, and integration touchpoints.

## Findings
- OPA can serve as a deterministic policy gate if bundles + inputs are pinned and evaluation is offline.
- Sidecar operation increases nondeterminism risk (remote policy drift); embedded CLI avoids network dependence.
- Fit matrix file was missing at the provided path; mapping is based on runtime + test files and should be confirmed once the fit matrix exists.

## Checkpoint
- Files changed:
  - `packages/specs/docs/planning/2026-02-06/m_intake_oss_eval_opa_2026-02-06.md`
- Commands run:
  - `ls packages/specs/docs/planning/2026-02-06`
  - `rg -n "m_intake_monorepo_fit_matrix_2026-02-06" -S`
  - `find packages -name "*fit_matrix*" -print`
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_constitution_2026-02-06.md`
  - `sed -n '1,200p' packages/specs/docs/planning/2026-02-06/m_intake_codex_runbook_2026-02-06.md`
  - `curl -L -o /tmp/opa https://open-policy-agent.org/downloads/latest/opa_linux_amd64_static` (failed: 403)
  - `which opa`
  - `apt-get update`
  - `apt-cache search openpolicyagent`
  - `apt-cache search "^opa"`
  - `curl -L -o /tmp/opa https://github.com/open-policy-agent/opa/releases/download/v0.63.0/opa_linux_amd64_static`
  - `chmod +x /tmp/opa`
  - `/tmp/opa version`
  - `cat <<'EOF' > /tmp/opa_policy.rego` (create policy file)
  - `cat <<'EOF' > /tmp/opa_input.json` (create input file)
  - `/tmp/opa eval -i /tmp/opa_input.json -d /tmp/opa_policy.rego "data.aigov.policy_result"` (first attempt failed: rego compile error)
  - `cat <<'EOF' > /tmp/opa_policy.rego` (fix policy file)
  - `/tmp/opa eval -i /tmp/opa_input.json -d /tmp/opa_policy.rego "data.aigov.policy_result"` (success)
- Results:
  - OPA install via open-policy-agent.org blocked (403); GitHub release download succeeded.
  - `opa version` and minimal `opa eval` executed successfully; outputs captured above.
- Risks/unknowns:
  - Fit matrix file missing at specified path; seam mapping needs confirmation once available.
- Next task:
  - Confirm seam mapping against the monorepo fit matrix when provided.
  - Draft eval-first fixtures for OPA adapter once integration decision is approved.
