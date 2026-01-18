# Legacy repos mapping (deprecated)

This program is **monorepo-only** now.

The following repos are **deprecated** and should be treated as historical references only:

- Standivarius/AiGov-specs
- Standivarius/AiGov-mvp
- Standivarius/Aigov-eval

**Canonical source of truth:** Standivarius/AiGov-monorepo

## Policy

- Do not add new content to legacy repos.
- Do not run CI from legacy repos (monorepo CI is the gate).
- If you find a reference to a legacy repo in documentation, update it to point to the monorepo path listed below.
- If something appears to exist only in a legacy repo, treat it as a migration-closeout bug.

## Mapping tables (FROM → TO)

### AiGov-specs → monorepo (packages/specs)

| Legacy (FROM) | Monorepo (TO) |
|---|---|
| `AiGov-specs/schemas/` | `packages/specs/schemas/` |
| `AiGov-specs/scenarios/` | `packages/specs/scenarios/` |
| `AiGov-specs/legal/eu/gdpr/` | `packages/specs/legal/eu/gdpr/` |
| `AiGov-specs/docs/` | `packages/specs/docs/` |

### AiGov-mvp → monorepo (packages/ep) [EP = product capabilities]

| Legacy (FROM) | Monorepo (TO) |
|---|---|
| `AiGov-mvp/aigov_ep/` | `packages/ep/aigov_ep/` |
| `AiGov-mvp/targets/compose/` | `packages/ep/targets/compose/` |
| `AiGov-mvp/services/targetlab_rag/` | `packages/ep/services/targetlab_rag/` |
| `AiGov-mvp/runs/` | `packages/ep/runs/` |
| `AiGov-mvp/tools/` | `packages/ep/tools/` |
| `AiGov-mvp/pyproject.toml` | `packages/ep/pyproject.toml` |

### Aigov-eval → monorepo (packages/pe + evalsets) [PE = acceptance criteria + evals]

| Legacy (FROM) | Monorepo (TO) |
|---|---|
| `Aigov-eval/aigov_eval/` | `packages/pe/aigov_eval/` |
| `Aigov-eval/tests/` | `packages/pe/tests/` |
| `Aigov-eval/tools/` | `packages/pe/tools/` |
| `Aigov-eval/requirements*.txt` | `packages/pe/requirements*.txt` |
| `Aigov-eval/conftest.py` | `packages/pe/conftest.py` |
| `Aigov-eval/{cases,golden_set,sources,taxonomy,reports}/` | `evalsets/aigov-eval/{cases,golden_set,sources,taxonomy,reports}/` |

## Notes

- EP vs PE is intentional:
  - **EP** = the product capabilities/features customers pay for.
  - **PE** = acceptance criteria + evaluations that prove EP claims, plus enterprise auditability/security controls.
- If you need to define eval groupings, use evalsets (PR gate / nightly / release / audit pack) and keep PR gate runtime short.
