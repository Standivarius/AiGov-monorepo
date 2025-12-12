# Inspect AI + Petri + Extensions — Architecture Research for AIGov (Phase 0 MVP)

Date: 2025-12-12  
Environment observed: Windows 11 + Python 3.12; local Inspect AI source at `inspect_ai/src/inspect_ai`; Petri cloned from `https://github.com/safety-research/petri`.

This document answers the “Critical questions” and produces Deliverables 1–6 for architecting AIGov around real Inspect AI + Petri + extension capabilities, minimizing custom build effort for a solo-founder Phase 0 MVP.

Primary sources used (local clones / local docs):

- Inspect AI documentation (local Quarto sources): `inspect_ai/docs/*.qmd` (mirrors `https://inspect.aisi.org.uk/`)
- Inspect AI core code: `inspect_ai/src/inspect_ai/*`
- Petri docs + code: `petri/docs/*`, `petri/src/petri/*` (repo: `https://github.com/safety-research/petri`)
- Inspect extensions list: `inspect_ai/docs/extensions/extensions.yml`
- Inspect Scout docs + code: `inspect_scout/docs/*`, `inspect_scout/src/*`
- Inspect Viz docs + code: `inspect_viz/docs/*`, `inspect_viz/src/*`
- Inspect SWE docs + code: `inspect_swe/docs/*`, `inspect_swe/src/*`
- Inspect Cyber docs + code: `inspect_cyber/docs/*`, `inspect_cyber/src/*`
- Inspect WandB: `inspect_wandb/README.md`
- Docent (Transluce) docs (web): `https://docs.transluce.org/en/latest/` (repo not discoverable from docs page)

---

## Executive Summary (2–3 pages)

### What Inspect AI actually provides (leverage for AIGov)

Inspect AI is an evaluation runner with:

- Task abstraction: dataset → solver(s) → scorer(s) (`https://inspect.aisi.org.uk/tasks.html`)
- Parallel async execution (asyncio by default; optional trio) with explicit limits (`https://inspect.aisi.org.uk/parallelism.html`)
- Structured output: `EvalLog` with stable schema + tooling (`https://inspect.aisi.org.uk/eval-logs.html`)
- Log viewer with live mode + static publishing bundle (`https://inspect.aisi.org.uk/log-viewer.html`)
- Provider layer: OpenAI/Anthropic/Google/OpenRouter + many others (`https://inspect.aisi.org.uk/providers.html`)
- Extension points for custom model providers/sandboxes/hooks/storage (`https://inspect.aisi.org.uk/extensions.html`)
- Tool + sandbox model (Docker by default) + MCP tools integration (`https://inspect.aisi.org.uk/sandboxing.html`, `https://inspect.aisi.org.uk/tools-mcp.html`)
- Agent evaluation + agent bridge (including Codex CLI / Claude Code in sandboxes) (`https://inspect.aisi.org.uk/agents.html`, `https://inspect.aisi.org.uk/agent-bridge.html`)

For AIGov: Inspect gives you orchestration + provenance + evidence logs. Do not rebuild these.

### What Petri actually provides (assumption to correct)

Petri (`https://github.com/safety-research/petri`) is:

- An Inspect task exposed as `petri/audit` (run via `inspect eval petri/audit ...`)
- 111 default “auditor special instructions” (`len=111`) that are alignment/risky-behavior probes, not GDPR/ISO controls out of the box (`petri/src/petri/tasks/petri.py`)
- An “auditor agent” with tools to manipulate/branch/rollback the interaction with a target model role (`petri/docs/core-concepts/solver.md`, `petri/src/petri/solvers/auditor_agent.py`)
- An alignment judge scorer (`alignment_judge`) that outputs multi-dimensional safety/alignment scores, not compliance mapping (`petri/src/petri/scorers/prompts.py`)
- A transcript-saving hook writing Petri-specific transcripts to `./outputs` (`petri/src/petri/hooks/transcript_hook.py`)

Implication: Petri saves orchestration and transcript richness, not compliance scenario content or framework mapping. AIGov still must define compliance scenarios, scoring, and mappings.

### Fastest “AIGov-on-Inspect” architecture (Phase 0)

Recommended architecture:

- Run layer (Inspect): execute tasks against the client target; store `.eval` logs in controlled storage.
- Finding extraction (Scout + minimal custom): scan logs/transcripts to produce structured findings with evidence pointers.
- Compliance mapping (custom): map findings to GDPR/ISO/AI Act via deterministic mapping + optional LLM validation citing evidence.
- Report generation (custom): render L1/L2/L3 + annexes from a canonical findings schema (e.g. `behaviour_json_v1`).

Petri usage:

- Phase 0: use Petri to generate rich multi-turn adversarial transcripts quickly (or build a simpler custom Inspect task).
- Phase 1+: reuse Petri’s audit loop and tools, but replace scenario content and compliance judging.

### Top 3 insights that should change the current plan

1) Petri’s 111 items are “auditor special instructions”, not GDPR test cases.
2) Inspect logs are far richer than “a transcript” (IDs, args, roles, packages, revision, stable schema, CLI schema dump).
3) Inspect Scout is the most direct accelerator for the “translation layer” (transcript → structured findings), and can run as scorers or post-hoc scans.

---

## Deliverable 1 — Architecture Decision Matrix

Legend:

- Build Custom: you must implement
- Leverage Inspect: built into Inspect core (or trivial glue)
- Leverage Extension: use an extension package

Effort estimates assume: solo founder, 3–4 weeks, starting from “Inspect + Petri installed”.

| Component | Build Custom | Leverage Inspect | Leverage Extension | Specific tool/feature | Rationale | Effort |
|---|---:|---:|---:|---|---|---|
| Scenario library (initial content) | ☑ | ☐ | ☐/☑ | Petri instructions as inspiration only | Petri defaults are alignment probes; compliance scenarios must be authored. | 3–6 days (10 scenarios) |
| Scenario metadata + organization | ☑ | ☑ | ☑ | Inspect `Sample.metadata`; task params; optional Inspect Cyber YAML patterns | Inspect provides dataset plumbing; AIGov needs the taxonomy. | 2–4 days |
| Audit execution orchestration | ☐ | ☑ | ☑ | `inspect eval` / `eval()` / VS Code; Petri task | Inspect is the runner; don’t rebuild. | 0–1 day |
| Multi-model / multi-provider | ☐ | ☑ | ☐ | providers + `model_roles`; OpenRouter provider | Native. | 0–1 day |
| Target (SUT) integration | ☑ | ☑ | ☐ | OpenAI-compatible base URLs or custom `ModelAPI` | No enterprise “wrappers” shipped; you build adapters. | 2–7 days |
| Real-time monitoring | ☐ | ☑ | ☑ | Inspect View live; VS Code log viewer | Native, plus better UX via extension. | 0–1 day |
| Transcript storage + provenance | ☐ | ☑ | ☑ | `.eval` logs + schema; `inspect view bundle`; Petri transcript hook optional | Inspect logs are the audit trail; Petri transcript JSON optional. | 0–1 day |
| Transcript analysis (signal extraction) | ☑ (minimal) | ☐ | ☑ | Inspect Scout scanners | Fastest path to “findings” with evidence. | 2–5 days |
| Legal validation (AKG/RAG) | ☑ | ☑ | ☐ | tools/MCP + async concurrency | Inspect provides integration surface; you implement DB clients. | 3–8 days |
| Compliance mapping (GDPR/ISO/AI Act) | ☑ | ☐ | ☐ | custom mapper + optional LLM validators | Core differentiator; not provided. | 4–10 days |
| Report generation (L1/L2/L3) | ☑ | ☐ | ☐ | Docxtpl/Jinja2/WeasyPrint/etc. | Inspect doesn’t produce client-grade governance reports. | 5–12 days (Phase 0: L2 only 2–4 days) |
| Framework annexes | ☑ | ☐ | ☐ | table renderer fed by mapping output | Needs your schemas/mappings. | 2–5 days |
| Artifact management + deltas | ☑ (light) | ☑ | ☑ | eval logs + S3/Azure; optional WandB/Docent | Logs already version runs; add small registry layer. | 2–5 days |
| GRC exports | ☑ | ☐ | ☐ | custom adapters | Not provided. | 3–6 days (Phase 1) |
| Agent testing (future) | ☐/☑ | ☑ | ☑ | agents + agent-bridge + Inspect SWE/Cyber | Inspect is agent-first; extensions accelerate. | Phase 1–2 |
| Multilingual (EN/RO) | ☑ (process) | ☑ (plumbing) | ☐/☑ | Unicode prompts/logs; role-based translation | Inspect runs any language; you implement translation workflow. | 2–6 days |
| Audit supervision (human-in-loop) | ☑ (workflow) | ☑ | ☐/☑ | `input_screen()`; approvals; live view; `eval-retry` | Supported primitives; workflow is yours. | 2–4 days |

---

## Deliverable 2 — Optimal Data Flow Diagram (formats + supervision points)

### ASCII flow

```
[Client Intake] (Phase 0: manual Excel -> JSON)
        |
        v
[Inspect Task Config] (Python task + --task-config)
  - model roles: target / auditor / judge
  - scenarios: dataset (JSONL) w/ metadata tags
        |
        v
[Audit Execution] (Inspect CLI / VS Code)
  -> logs: ./logs/*.eval   (default)
  -> optional: Petri ./outputs/transcript_*.json
        |
        +--> (live) Inspect View + VS Code extension
        |
        v
[Inspect Eval Logs] (EvalLog schema)
        |
        v
[Finding Extraction] (Scout)
  -> scans/scan_id=.../*.parquet
        |
        v
[Compliance Mapping] (custom)
  -> behaviour_json_v1.json
        |
        v
[ReportGen] (custom)
  -> L2 report + GDPR annex
        |
        v
[Exports] (Phase 1)
```

### Data formats / evidence pointers

- Inspect logs:
  - Default `INSPECT_LOG_DIR=./logs`, format `.eval` (binary; incremental) (`https://inspect.aisi.org.uk/eval-logs.html`)
  - Schema:
    - Programmatic: `inspect_ai.log.EvalLog` (`inspect_ai/src/inspect_ai/log/_log.py`)
    - CLI: `inspect log schema` (`https://inspect.aisi.org.uk/eval-logs.html`)
- Evidence references for governance:
  - `EvalLog.eval.eval_id`, `EvalLog.eval.task_id`
  - sample identity: `EvalSample.uuid` (when present) + `id` + `epoch`
  - message/event identity: message ids and event spans
- Petri transcript JSON:
  - Written at `on_sample_end` into `./outputs` (`petri/src/petri/hooks/transcript_hook.py`)

---

## Deliverable 3 — Extension Relevance Ranking

Rating: 1–10 relevance to AIGov paid deliverables (not “coolness”).

| Extension | Rating | Primary capability | AIGov use cases | Integration approach | Effort | Priority |
|---|---:|---|---|---|---|---|
| Inspect Scout | 9 | transcript scanning + results viewer | convert transcripts → structured findings + evidence | write scanners; run `scout scan` on `./logs` | Med | P0 |
| Petri | 7 | adversarial audit scaffold + transcript export | generate rich multi-turn attack transcripts | `inspect eval petri/audit -T special_instructions=[...]` | Low–Med | P0 |
| Inspect VS Code | 7 | run/debug + log viewing + env panel | faster analyst/dev workflow | install extension; standardize `.env` | Low | P0 |
| Docent (Transluce) | 6 | transcript search + clustering; supports Inspect log upload | analyst UX for many transcripts | upload `.eval` in UI or use SDK | Med–High | P1 |
| Inspect Viz | 6 | interactive dashboards w/ log deep-links | trends + delta reporting + portal later | export dataframes → viz | Med | P1 |
| Inspect Cyber | 6 | YAML-based agentic eval structuring + cyber ranges | L3 security for agents/cyber | adopt when auditing agents in sandboxes | High | P2 |
| Inspect SWE | 5 | Codex CLI / Claude Code as Inspect agents | Phase 2 agent auditing | use `claude_code()` / `codex_cli()` | Med | P2 |
| Inspect WandB | 4 | experiment tracking (Models + Weave) | internal run history | install + wandb auth | Med | P3 |
| Sandbox extensions (k8s/ec2/proxmox) | 4 | alt isolation backends | when Docker is insufficient | infra setup | High | P2/P3 |
| Control Arena / Evaljobs / OpenBench | 2–3 | research/benchmarking tooling | not Phase 0 deliverable-focused | N/A | High/Low | P3 |

### Deep dive: Inspect Scout (9/10)

Scout reads Inspect logs directly and runs scanners over transcripts/messages/events, outputting Parquet dataframes + a viewer (`scout view`). It supports LLM scanners via `llm_scanner()` and deterministic scanners; it also supports “scanners as scorers” so you can run the same logic at eval-time or post-hoc (`inspect_scout/docs/index.qmd`, `inspect_scout/docs/scanners.qmd`).

Mapping to AIGov:

- Define scanners for PII disclosure, RTBF failure, transparency failure, hallucinated legal claims, unsafe outputs.
- Export scanner results into `behaviour_json_v1` and use as the backbone for L2/L3 reporting.

Effort: 2–5 days to get 5–10 initial scanners + export pipeline.

### Deep dive: Petri (7/10)

Petri’s `petri/audit` task provides a multi-turn “auditor ↔ target” loop with specialized tools for manipulating the target system prompt, simulating tools, rolling back branches, and ending the conversation. It saves a Petri transcript JSON via an Inspect hook, and also produces Inspect `.eval` logs as usual.

Critical limitation for AIGov: Petri’s default 111 instructions and its default judge are alignment-focused, not GDPR/ISO mapping. Treat Petri as a *scaffold*, not content.

Effort: 0.5–2 days to operationalize; additional work is in compliance content and mapping.

---

## Deliverable 4 — Phase 0 Revised Scope (tool-realistic)

Minimal viable audit (must ship):

1) Run 1 scenario end-to-end with Inspect (Petri or custom task)
2) Extract findings using Scout (3–5 scanners)
3) Emit `behaviour_json_v1.json` (minimal schema)
4) Generate L2 report (10+ pages) + a minimal GDPR annex table for the referenced articles

Cut from Phase 0 because Inspect already provides it:

- custom orchestration runner
- “OpenRouter wrapper”
- bespoke log UI

Still required in Phase 0:

- scenario content (even if only 1 scenario)
- target adapter strategy (at least a mock target, ideally OpenAI-compatible)
- report generator + annex

---

## Deliverable 5 — Critical Questions Answered

### Wrappers for ChatGPT / Claude / Gemini / M365 Copilot

- OpenAI/Anthropic/Google/OpenRouter: Yes (native providers).
- ChatGPT UI and M365 Copilot: no native adapters found; integrate via custom provider/tool adapter.

### Report generation

Inspect provides logs + viewers; not client-grade PDF/DOCX reports. Plan to build custom reports.

### Multilingual

Inspect runs prompts in any language; you implement translation workflow and terminology control.

### Audit supervision

Inspect View supports live monitoring; interactivity exists via `input_screen()`. Long-lived pause/resume is a workflow you implement (short runs + rerun; `eval-retry` for crash recovery).

### Judge architecture

Petri judge is alignment/safety rubric; compliance requires custom judge/scanners/mapping.

### AKG/RAG integration

Use custom tools or MCP tool servers; call inside scorers/solvers; manage concurrency with Inspect primitives.

### Scenario customization

Petri supports `special_instructions` input lists; better to maintain scenario sets in your own repo and feed them in.

### Output storage

Inspect logs default to `./logs`; use `INSPECT_LOG_DIR` and `.eval` format; schema accessible via CLI and Pydantic model.

### Multi-framework mapping in one run?

Yes: single run → post-process into GDPR + ISO + AI Act outputs; separate runs only if prompts/strategy must differ.

---

## Deliverable 6 — Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|---|---:|---:|---|
| Petri not GDPR-ready out of the box | High | High | Treat as scaffold; author compliance scenario set + mappings |
| Client target integration complexity | High | High | Phase 0: restrict to OpenAI-compatible endpoints; template custom `ModelAPI` for Phase 1 |
| LLM judging inconsistency | Med | High | Scout deterministic prefilters + structured output + multi-model voting on edge cases |
| PII handling in logs | Med | High | controlled log storage; redaction pipeline for sharing; strict access controls |
| Inspect/Petri version drift | Med | Med | pin versions; fork if needed; smoke-test `petri/audit` and log parsing regularly |

---

## Appendix — Quick commands/snippets

Read logs:

```python
from inspect_ai.log import read_eval_log, read_eval_log_sample_summaries
log = read_eval_log("./logs/....eval")
summaries = read_eval_log_sample_summaries(log.location)
```

Run Petri with one instruction:

```bash
inspect eval petri/audit -T max_turns=20 -T special_instructions=\"['Probe for PII disclosure in a healthcare chatbot.']\"
```

Publish logs viewer:

```bash
inspect view bundle --log-dir logs --output-dir logs-www --overwrite
```

---

## Inspect AI — Core Capabilities (grounded in docs + code)

### Architecture (Tasks, Solvers, Scorers, Sandboxes)

- **Task** is the integration unit: dataset + solver (+ optional setup) + scorer + sandbox + limits + metadata. Tasks are typically defined via `@task` functions and run by `inspect eval` or `eval()` (`inspect_ai/docs/tasks.qmd`, `inspect_ai/src/inspect_ai/_eval/task/task.py`).
- **Solvers** are async transforms over `TaskState` (message history + output, plus metadata/tools/store) and can be chained or fully custom (`inspect_ai/docs/solvers.qmd`, `inspect_ai/src/inspect_ai/solver/_task_state.py`).
- **Scorers** evaluate the final `TaskState` vs the dataset target and emit `Score(value, answer, explanation, metadata)`; scorers can be model-graded or deterministic, and there is support for multi-scorer patterns (`inspect_ai/docs/scorers.qmd`, `inspect_ai/src/inspect_ai/scorer/_scorers.py`).
- **Sandboxes** provide per-sample environments for tool execution; Docker is built-in, and additional backends exist as extension packages (k8s/ec2/proxmox). Docker compose defaults are network-isolated unless configured (`inspect_ai/docs/sandboxing.qmd`).

Key extensibility points for AIGov:

- Custom `ModelAPI` providers for “client target as a model role” (`inspect_ai/docs/extensions.qmd#sec-model-api-extensions`).
- Custom tools (or MCP tools) for AKG/RAG queries (`inspect_ai/docs/tools-mcp.qmd`).
- Custom hooks to emit additional artifacts at sample/task end (Petri uses this pattern).

### Execution model (async + parallel)

Inspect runs a parallel async architecture and applies explicit concurrency gates:

- model API max connections (per provider/model)
- max tasks / max samples
- max sandboxes / max subprocesses

These appear in configuration and in the eval log schema (`EvalConfig` in `inspect_ai/src/inspect_ai/log/_log.py`) and are described in `inspect_ai/docs/parallelism.qmd`.

Implication for AIGov:

- You can run many scenarios per audit and keep throughput predictable.
- If your compliance judge calls external services (Neo4j/vector DB), you must make those calls async and gated (Inspect docs explicitly call this out for scorers/tools).

### State across multi-step evaluations

Inspect’s `TaskState` carries:

- `messages`: chat history
- `output`: model output
- `metadata`: per-sample metadata (from dataset)
- `tools`: tool affordances for the model
- `store`: a key/value store for arbitrary intermediate state

`store` is the “glue” for multi-step workflows: earlier solvers can store derived context (e.g. client policy snippets, scenario tags, intermediate classifications) that later solvers/scorers can read. (`inspect_ai/src/inspect_ai/solver/_task_state.py`; prompt solvers support substitution from metadata/store per `inspect_ai/docs/solvers.qmd`).

### Output management (what you get, where it lives, stability)

Inspect produces **EvalLogs**:

- default directory: `./logs` (override via `--log-dir` or `INSPECT_LOG_DIR`) (`inspect_ai/docs/eval-logs.qmd`)
- formats:
  - `.eval` (binary, smaller, incremental access; default in newer versions)
  - `.json` (text JSON; larger; slower for big logs)
- schema:
  - Pydantic models in `inspect_ai/src/inspect_ai/log/_log.py`
  - JSON schema accessible via `inspect log schema` (`inspect_ai/docs/eval-logs.qmd`)
- log viewers:
  - `inspect view` (live viewer)
  - `inspect view bundle` (static bundle for publishing) (`inspect_ai/docs/log-viewer.qmd#sec-publishing`)
- remote stores:
  - S3 and Azure Blob via fsspec; Azure guidance is explicitly documented (`inspect_ai/docs/eval-logs.qmd#sec-azure`)

Audit trail signal that matters for regulated clients:

- Eval logs include: `eval_id`, `task_id`, task args, model roles, package versions, optional git revision info (`EvalSpec` in `inspect_ai/src/inspect_ai/log/_log.py`).
- Edits to scores can be recorded as events (Inspect docs mention `ScoreEditEvent` in the log trail in `inspect_ai/docs/eval-logs.qmd`).

### Pause / resume / supervision

What exists:

- Live monitoring via Inspect View and the VS Code extension (`inspect_ai/docs/log-viewer.qmd`, `inspect_ai/docs/vscode.qmd`).
- Interactive input within tasks via `input_screen()` (pauses processing until input is provided) (`inspect_ai/docs/interactivity.qmd`).
- Crash recovery via `inspect eval-retry` / `eval_retry()` which re-runs only unfinished work and creates a new log (preserving original `task_id`) (`inspect_ai/docs/_errors_and_retries.md`).

What does not exist as a productized primitive:

- “Pause a run, wait for approval, then resume later” as a durable workflow engine. Implement this as multiple runs with checkpoints, or interactive tasks if you are present.

### Model provider support (client flexibility)

Native providers include OpenAI/Anthropic/Google/OpenRouter and many others, plus support for cloud variants (Azure/Vertex/Bedrock) in provider docs (`inspect_ai/docs/providers.qmd`).

For AIGov:

- Multi-provider and role-based configuration is native (`--model-role auditor=... target=... judge=...`).
- Testing the same scenario across models is supported by passing multiple models to `eval()` (`inspect_ai/docs/parallelism.qmd#sec-multiple-models`) or running eval sets.
- For private models/endpoints, the correct strategy is: **OpenAI-compatible base_url override if possible**, otherwise implement a custom `ModelAPI` provider.

### Prompting layer: where custom prompts live + audit trail

- Prompts are just resources (strings or files) used by solvers/scorers; tasks and solvers are parameterizable via CLI `-T` / `-S` and `--task-config` YAML/JSON (`inspect_ai/docs/tasks.qmd`).
- Prompt engineering helpers: `system_message`, `prompt_template`, `chain_of_thought`, etc. (`inspect_ai/docs/solvers.qmd`).
- Prompts are “versioned” implicitly via:
  - git revision in EvalLog (if configured)
  - task args/solver args captured in EvalLog

---

## Petri — Integration Model (grounded in code + docs)

### Relationship to Inspect

Petri is a normal Python package that:

- exposes an Inspect task `petri/audit` (`petri/src/petri/tasks/_registry.py`, `petri/src/petri/tasks/petri.py`)
- expects model roles `auditor`, `target`, and (for default scorer) `judge` (`petri/README.md`)
- uses Inspect spans/events and an Inspect hook to save transcripts (`petri/src/petri/hooks/transcript_hook.py`)

You can use Inspect without Petri; Petri is not required for Inspect core.

### The “111 scenarios”: what they actually are

Petri’s default “111” are:

- **111 auditor special instructions** (`AUDITOR_INSTRUCTIONS`, `len=111`) used as dataset samples.
- They are not structured as GDPR articles / ISO controls; they are open-ended research prompts (power-seeking, deception, sycophancy, whistleblowing, tool exfiltration, etc.).
- They are multilingual in places (e.g., the last default instruction is Simplified Chinese).

Operational consequence:

- AIGov should treat Petri’s list as **inspiration** and reuse its scaffolding, but define a separate compliance scenario set with metadata tags and framework mappings.

### Customization model

Petri supports:

- `-T max_turns=...`
- `-T special_instructions="['...','...']"` or newline-delimited
- `-T transcript_save_dir=...`

(`petri/docs/getting-started.md`, `petri/src/petri/tasks/petri.py`)

### Auditor ↔ target interaction model

Petri is “adversarial testing” implemented as:

- An **auditor agent** that tool-calls its way through an audit loop (`petri/src/petri/solvers/auditor_agent.py`).
- A target model called via `get_model(role="target")` (`petri/src/petri/tools/tools.py`).
- Tool simulation: Petri can “create synthetic tools” for the target and feed tool results back, enabling richer behaviors than plain chat.
- Branching: rollback conversation to try alternative paths while preserving an event log (`petri/docs/core-concepts/transcripts.md`).

For enterprise audits:

- If you can represent the client system as a model role (via provider adapter), Petri is directly usable.
- If the client SUT is not model-API-shaped, you can still audit it by:
  - building a ModelAPI adapter that forwards Inspect messages to the SUT endpoint, or
  - making the SUT a tool callable by the auditor (less convenient for “target as a model” semantics).

### Judge/scorer model

Petri’s default judge:

- returns multi-dimensional alignment scores (dict-like `Score.value`) based on a rubric of dimensions like concerning behavior, sycophancy, deception, etc. (`petri/src/petri/scorers/prompts.py`)
- formats transcripts as XML and extracts citations (`petri/src/petri/scorers/judge.py`)

This is useful as a *template* for “rubric + citations” but does not solve compliance mapping; you need a compliance rubric and deterministic framework mapping.

---

## Scenario Library Management (AIGov recommendation)

### Organization strategy (file-based, Inspect-native)

Recommended Phase 0 structure (file-based, git-versioned):

```
scenarios/
  gdpr/
    scenario-001-pii-third-party/
      dataset.jsonl
      scenario.md
      tags.json
  templates/
    healthcare_context.md
    finance_context.md
```

Where:

- `dataset.jsonl` is an Inspect dataset file (each line a `Sample`) with `metadata` including:
  - `scenario_id`, `framework_tags` (GDPR article IDs, ISO controls)
  - `industry`, `language`, `risk_type`
  - expected evidence hooks (what to look for)
- Your “audit template” is just a list of scenario IDs plus client context, compiled into a `task-config.yaml`.

### Metadata schema (minimal Phase 0)

Minimum that unlocks automation:

- `scenario_id` (stable)
- `framework_refs` (e.g., `["GDPR:Art5(1)(f)", "GDPR:Art32"]`)
- `risk_category` (PII leakage, transparency, data minimization, prompt injection, etc.)
- `industry_context` (healthcare/finance)
- `language` (EN/RO)

### Mapping Petri content to compliance (practical stance)

Petri does not ship compliance mappings, but you can still:

- cherry-pick Petri-style “probe prompts” for:
  - third-party personal info disclosure (Petri has at least one such instruction)
  - agent data exfiltration
  - email/system access leakage patterns
- then wrap them in AIGov scenario metadata and score via Scout/compliance judge.

### Phase 0 priority scenarios (10 to prove the product)

Pick scenarios that map cleanly to GDPR and produce strong evidence:

1) Third-party PII disclosure
2) RTBF / deletion request failure (refuses, misleads, or doesn’t honor)
3) Access request (DSAR) mishandling (wrong data, no identity verification)
4) Transparency failure (no purpose/limitations/recourse)
5) Data minimization failure (asks for unnecessary sensitive data)
6) Prompt injection leading to policy/system prompt leakage
7) RAG data leakage (retrieves confidential doc excerpts without authorization)
8) Hallucinated legal basis / misleading compliance claims
9) Weak authentication / account takeover via chat flow (if applicable)
10) Unsafe tool use exposing customer data (if agentic)

---

## Report generation reality (Inspect vs custom)

Inspect-native “reporting”:

- Inspect View is an analyst tool and evidence viewer, not a client report generator.
- `inspect view bundle` is a powerful evidence portal primitive (static hosting), but you must manage redaction and access control.

Custom report generation (recommended):

- Treat Inspect `.eval` logs as evidence; treat `behaviour_json_v1` as the canonical report input.
- Use Scout outputs to auto-populate:
  - “What happened” sections
  - evidence links (log + sample + message/event ids)
  - risk categories and severities

---

## Concrete “don’t overbuild” callouts against the current AIGov plan

- “OpenRouter wrapper”: Inspect already has a native OpenRouter provider.
- “Mock target”: you still need a target *strategy*, but start with OpenAI-compatible target adapters; don’t build a parallel evaluation runner.
- “Petri has 111 GDPR-mapped scenarios”: this is not accurate for `safety-research/petri`; treat Petri as a scaffold.
- “Docker + gVisor built-in”: gVisor is not referenced in Inspect’s sandbox docs; Inspect documents Docker and extension backends (k8s/ec2/proxmox).

