# Inspect-Petri Naming Map v1 (AiGov Alignment)

Date: 2026-03-04  
Scope: naming conventions and term mapping only (no runtime changes).

## 1) Source anchors

- Inspect repo: `UKGovernmentBEIS/inspect_ai` @ `ae06ec4a79936ffb3675c4010d3e04f7b6b39f8e`
- Petri repo: `safety-research/petri` @ `7fef276f63d0ff6b15396399b84d2366b488d62a`
- AiGov canonical terminology/taxonomy:
  - `packages/specs/docs/contracts/terminology.md`
  - `packages/specs/docs/contracts/modules/module_registry_v0.yaml`
  - `packages/specs/docs/contracts/taxonomy/verdicts.json`
  - `packages/specs/docs/contracts/taxonomy/signals.meta.json`

## 2) Concept naming map (Petri vs Inspect vs AiGov)

| Concept | Inspect term | Petri term | AiGov alignment |
|---|---|---|---|
| Execution unit | `Task` | `audit` task (`@task`) | Keep primitive `Task`; bind to module stages through `M_*` docs |
| Input set | `Dataset` | dataset built from seed instructions (`Sample` list) | Keep case/scenario dataset abstraction; avoid custom synonyms |
| Input item | `Sample` | `Sample` | Keep `Sample` semantics in PE/EP adapters |
| Runtime behavior unit | `Solver` | `auditor_agent` (solver) | Map to AiGov task-role units (`R_*`) |
| Evaluation behavior unit | `Scorer` | `alignment_judge` (scorer) | Map to `M_Judge` internal task(s) |
| Audit actor | model role (generic) | `auditor` | Keep role name `auditor` (runtime role) |
| System under test | model role (generic) | `target` | Keep AiGov canonical wording `Target System` with alias `target` |
| Decision actor | model role (generic) | `judge` | Keep role name `judge`; module remains `M_Judge` |
| Optional realism actor | model role (generic) | `realism` | Keep optional runtime role, not a module |
| Tool invocation | `tool` / tool calls | auditor tools | Keep term `tool/toolset` |
| Run output | eval/log APIs | transcript + log dir | Keep Stage A artifacts + logs pointer pattern |

## 3) Naming conventions (code-level)

## 3.1 Explicit conventions

- Inspect explicitly uses decorator/registry contracts:
  - `@task` + `Task` object
  - `@solver`
  - `@scorer`
- Petri explicitly uses Inspect runtime role names:
  - `auditor`
  - `target`
  - `judge`
  - optional `realism`

## 3.2 Implicit conventions

- Inspect:
  - singular primitive package names: `dataset`, `solver`, `scorer`, `tool`, `log`
  - internal/private module files prefixed with `_` (example: `_solver.py`)
- Petri:
  - plural implementation package names: `tasks`, `solvers`, `scorers`, `tools`
  - snake_case module files (example: `auditor_agent.py`)
  - task invocation namespace follows `package/task` pattern (example: `petri/audit`)

No standalone naming-style spec was found in reviewed files; conventions are mostly code-embedded.

## 4) AiGov alignment recommendations (bounded)

1. Keep three namespaces separate:
   - module namespace: `M_*` (product stages/modules)
   - runtime role namespace: `auditor`, `target`, `judge`, optional `realism`
   - primitive execution namespace: `task`, `dataset`, `sample`, `solver`, `scorer`, `tool`
2. Do not rename AiGov modules to Petri role names.
3. Keep `Target System` as the canonical business term; accept `target` as runtime alias only.
4. Keep verdict/signal canon in specs taxonomy (`verdicts.json`, `signals.meta.json`) and forbid role-local verdict labels.
5. Keep role-task IDs in `R_*` pattern for LLM-task orchestration, independent of `M_*`.

## 5) Alignment decision

Adopt Petri/Inspect role naming for runtime interoperability (`auditor`, `target`, `judge`) while preserving AiGov module taxonomy (`M_*`) as product architecture authority.
