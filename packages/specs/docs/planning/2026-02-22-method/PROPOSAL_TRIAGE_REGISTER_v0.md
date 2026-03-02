# Proposal Triage Register (v0)

Date opened: `2026-02-25`
Status: `Active`

Purpose: durable capture of PM proposals so they do not disappear between turns/threads.

## Entries

### PTR-001
- Date: `2026-02-25`
- Title: `AiGov-wide component built end-to-end as reusable methodology block`
- Category: `EXPLORE`
- Source: `User`
- Why it matters: validates a repeatable "build one component properly" pattern (tasks/prompt/input-output/evals/architecture/storage) for later v0.1 work.
- Next action / trigger: evaluate candidate components and choose one bounded scope after dashboard/taxonomy control surface is stable enough.
- Owner: `Codex`
- Status: `Open`

### PTR-002
- Date: `2026-02-25`
- Title: `Parallel spec-only exploration lab (Lab1) in separate window/worktree`
- Category: `EXPLORE`
- Source: `User + Codex`
- Why it matters: allows method experimentation (shell-first spec derivation) without destabilizing current spike/dashboard track.
- Next action / trigger: finalize method contract and subordinate task packet; then launch Lab1 in isolated folder/worktree.
- Owner: `Codex`
- Status: `Open`

### PTR-003
- Date: `2026-02-25`
- Title: `Direct Codex parent/subagent orchestration strategy (app vs CLI multi-agent)`
- Category: `EXPLORE`
- Source: `User`
- Why it matters: determines how to run parallel work without forcing Marius to manually align two streams.
- Next action / trigger: lock one practical operating mode (app-window mailbox now, CLI experimental later if worth setup cost).
- Owner: `Codex`
- Status: `Open`

### PTR-004
- Date: `2026-02-25`
- Title: `External agent consistency review of current spike logic and architecture`
- Category: `PARK`
- Source: `User + Codex`
- Why it matters: can catch hidden coupling and drift, but generates noise if done before dashboard/taxonomy structure stabilizes.
- Next action / trigger: revisit after next stable checkpoint (dashboard v2 + intake taxonomy structure reviewed).
- Owner: `Codex`
- Status: `Open`

### PTR-005
- Date: `2026-02-25`
- Title: `Observability stack options for AiGov (OpenTelemetry, W3C Trace Context, Langfuse)`
- Category: `PARK`
- Source: `User (via ChatGPT discussion summary)`
- Why it matters: provides future-ready tracing, LLM observability, and correlation standards for debugging/evidence trails once pipeline architecture stabilizes.
- Next action / trigger: defer until core app flow and two-task chain are stable; revisit only when telemetry extraction is an active implementation need.
- Owner: `Codex`
- Status: `Open`

### PTR-006
- Date: `2026-02-25`
- Title: `Treat manual handovers as reusable Codex-operated skills / task packs during spike and beyond`
- Category: `EXECUTE`
- Source: `User`
- Why it matters: may simplify development by standardizing repetitive manual orchestration steps (inputs/prompts/outputs/checks) without forcing deterministic code too early.
- Next action / trigger: produce v0 skill pattern proposal now (task contract + runtime envelopes + remedy mode hook), then pilot on one two-task chain.
- Owner: `Codex`
- Status: `In progress`

### PTR-007
- Date: `2026-02-25`
- Title: `Extract useful architecture guidance from Anthropic Claude Skills guide for AiGov task/skill pattern`
- Category: `EXPLORE`
- Source: `User`
- Why it matters: AiGov is increasingly relying on repeatable task packs/skills; external skill design patterns can improve packaging, reuse, and testing discipline.
- Next action / trigger: summarize actionable patterns for AiGov (progressive disclosure, composability, testing criteria, packaging) and map them to current task packets; park source link afterward.
- Owner: `Codex`
- Status: `Open`

### PTR-008
- Date: `2026-02-25`
- Title: `Inspect ecosystem extensions research (Inspect SWE / Flow / Evals / VS Code extension) for AiGov architecture reuse`
- Category: `EXECUTE`
- Source: `User`
- Why it matters: may reduce custom build effort by reusing Inspect-aligned execution/orchestration/eval patterns and agent integration seams.
- Next action / trigger: complete scoped research memo with concrete adopt/defer matrix focused on `inspect_swe` (Codex CLI agent), `inspect_flow` (orchestration/log reuse), and VS Code operational workflow.
- Owner: `Codex`
- Status: `In progress`

### PTR-009
- Date: `2026-02-25`
- Title: `Source realistic GDPR client docs (public/synthetic) for M_Intake testing`
- Category: `EXPLORE`
- Source: `User`
- Why it matters: improves M_Intake testing realism beyond synthetic-only bundles and supports reconciliation/sufficiency experiments.
- Next action / trigger: compile source options (public notices/policies/process docs/templates), usage constraints, and fixture strategy.
- Owner: `Codex`
- Status: `Open`

### PTR-010
- Date: `2026-02-25`
- Title: `Use LAB1_SHELLSPEC_EXPLORER as command center to spawn/coordinate Inspect extensions research sub-agent`
- Category: `EXPLORE`
- Source: `User`
- Why it matters: enables delegated architecture research (Inspect extensions reuse patterns) without contaminating main AiGov implementation thread.
- Next action / trigger: define research-agent identity, scope, deliverables, and mailbox protocol for Inspect ecosystem extension analysis.
- Owner: `Codex`
- Status: `Open`

### PTR-011
- Date: `2026-02-26`
- Title: `Dashboard v3 UX refinement for M_Intake (vertical flow, tooltips, clearer component/task separation, Legislation tab)`
- Category: `EXECUTE`
- Source: `User`
- Why it matters: current dashboard is too high-entropy for human control; visual clarity is now a project safety requirement.
- Next action / trigger: implement next dashboard pass focused on `M_Intake` clarity and cross-cutting tabs (Taxonomy + Legislation) without adding backend controls.
- Owner: `Codex`
- Status: `Open`

### PTR-012
- Date: `2026-02-26`
- Title: `Clarify GDPR obligation families vs standard scenario branching scope and likely library size`
- Category: `EXPLORE`
- Source: `User`
- Why it matters: scenario-library size and branching strategy will affect taxonomy mapping design, M_Bespoke selection logic, and M_Intake normalization scope.
- Next action / trigger: produce a bounded PM model (obligation families -> chatbot/agent-relevant subset -> scenario families -> use-case overlays) with rough size ranges.
- Owner: `Codex`
- Status: `Open`

### PTR-013
- Date: `2026-02-26`
- Title: `Decide M_Intake document parsing approach for early versions (simple LLM parse vs agentic RAG, up to ~200k tokens)`
- Category: `EXPLORE`
- Source: `User`
- Why it matters: influences document repository seam, extraction task design, provenance strategy, and cost/latency assumptions without needing premature infrastructure build-out.
- Next action / trigger: compare options against current spike/Lab1 constraints and define a default early-version path plus upgrade seam.
- Owner: `Codex`
- Status: `Open`

### PTR-014
- Date: `2026-02-26`
- Title: `App-native subordinate thread feasibility via LAB1_SHELLSPEC_EXPLORER_CODEXAPP direct coordination`
- Category: `EXPLORE`
- Source: `User`
- Why it matters: if workable, reduces friction versus CLI-only subordinate workers and simplifies parallel exploration management.
- Next action / trigger: attempt a bounded connection/protocol test with `LAB1_SHELLSPEC_EXPLORER_CODEXAPP`; keep CLI mailbox path as fallback.
- Owner: `Codex`
- Status: `Open`

### PTR-015
- Date: `2026-02-27`
- Title: `Implement Codex app-server adapter using bidirectional JSON-RPC 2.0 framing`
- Category: `EXPLORE`
- Source: `User`
- Why it matters: enables app-level orchestration and tool bridging using the Codex app-server contract (MCP-like, bidirectional messages), which can support multi-agent and control-plane workflows for AiGov.
- Next action / trigger: define target package boundary and transport/runtime choice in PM; execute implementation only after explicit mode switch command `Switch to EX MODE for Codex app-server adapter implementation`.
- Owner: `Codex`
- Status: `Open`

### PTR-016
- Date: `2026-02-27`
- Title: `Direct cross-thread context carryover by thread ID in Codex app`
- Category: `REJECT`
- Source: `User`
- Why it matters: user wants ChatGPT-like branch chat behavior while preserving current thread context exactly.
- Next action / trigger: use context-pack file handoff pattern instead; direct guaranteed thread-ID replay is not supported/reliable in current app setup.
- Owner: `Codex`
- Status: `Closed`

### PTR-017
- Date: `2026-02-27`
- Title: `Orchestrator remedy mode for LLM-task failure points with operator guidance`
- Category: `EXECUTE`
- Source: `User`
- Why it matters: allows non-expert operators to recover runs using guided remediation steps instead of requiring deep app internals knowledge.
- Next action / trigger: define remedy-mode spec now in PM; implement first working version immediately after two consecutive LLM tasks are active, then validate on one end-to-end failure path.
- Owner: `Codex`
- Status: `Open`

### PTR-018
- Date: `2026-02-27`
- Title: `Evaluate whether any agentic/evals framework is a better local-first fit than Inspect for AiGov`
- Category: `EXPLORE`
- Source: `User`
- Why it matters: avoids accidental lock-in and verifies whether Inspect should be core infrastructure or only one component.
- Next action / trigger: compare candidate frameworks against AiGov constraints (local-first, evalsets, logs, retries, agent integration, VS Code workflow), then issue keep/switch recommendation.
- Owner: `Codex`
- Status: `Open`

### PTR-019
- Date: `2026-02-27`
- Title: `Inspect-first eval library for LLM tasks with explicit flexibility gate`
- Category: `EXECUTE`
- Source: `User + Codex`
- Why it matters: keeps evals centralized in Inspect while preventing lock-in if task-level evaluation needs exceed Inspect flexibility.
- Next action / trigger: define evaluation gate criteria and perform documentation/code capability comparison first (Inspect vs alternatives), before any runtime eval execution.
- Owner: `Codex`
- Status: `In progress`

### PTR-020
- Date: `2026-02-27`
- Title: `Codex-in-VSCode operating model for running Inspect flows and AiGov skill chains`
- Category: `EXECUTE`
- Source: `User`
- Why it matters: this is the practical day-to-day operator path for AiGov build/test loops, and should minimize custom orchestration code in early phases.
- Next action / trigger: define the concrete command-level workflow (author task/skill packs -> run Inspect/Flow from terminal -> inspect logs/viewer -> apply remedy actions) and map each step to artifacts.
- Owner: `Codex`
- Status: `In progress`

### PTR-021
- Date: `2026-02-27`
- Title: `Cross-check protocol for EN GDPR terminology source list after first discovery pass`
- Category: `EXPLORE`
- Source: `User + Codex`
- Why it matters: source quality controls reduce glossary drift and avoid using low-authority references as canonical inputs.
- Next action / trigger: after first source-list pass is complete, run a lightweight authority and overlap check before extraction/normalization.
- Owner: `Codex`
- Status: `Open`

### PTR-022
- Date: `2026-03-02`
- Title: `De-risk oversized PR by splitting into thematic micro-PRs from current branch snapshot`
- Category: `EXECUTE`
- Source: `User + Codex`
- Why it matters: a ~68k-line PR is unauditable and increases merge/regression risk; splitting preserves useful work while restoring reviewability.
- Next action / trigger: freeze current branch as parking baseline, create clean integration branch, and promote only approved file groups (legal research docs, judge A/B spike scripts, selected tests) in separate PRs.
- Owner: `Codex`
- Status: `Open`

### PTR-023
- Date: `2026-03-02`
- Title: `Create concise PM checkpoint artifact for Dutch UAVG/AP + Judge context-engineering experiment outcomes`
- Category: `EXECUTE`
- Source: `User`
- Why it matters: keeps decision history durable before branch cleanup and avoids re-deriving research outcomes later.
- Next action / trigger: write one compact checkpoint with completed tasks, artifacts, and key findings/deltas before starting PR split operations.
- Owner: `Codex`
- Status: `Closed`
