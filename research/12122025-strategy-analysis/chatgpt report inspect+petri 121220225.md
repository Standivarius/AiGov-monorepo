# **AIGov × Inspect AI \+ Petri: Architecture & Execution Report (Dec 2025\)**

## **Executive summary**

**Three “tool reality” truths that should change your plan:**

1. **Inspect already *is* your orchestration \+ observability layer.**  
    It’s not “run eval, get transcript”. It gives you: composable multi-step workflows (solver chains), multi-scorer pipelines, tool/agent execution, sandboxing, live log streaming, and a first-class log viewer \+ VS Code workflow. [Inspect+5Inspect+5Inspect+5](https://inspect.aisi.org.uk/?utm_source=chatgpt.com)

2. **Your “Judge pipeline” belongs (mostly) inside Inspect scorers.**  
    You don’t need a separate orchestration engine to do Transcript → AKG/RAG → mapping → findings JSON. Inspect scorers can yield multiple structured scores, run in parallel, and store everything in the eval log. [Inspect+2Inspect+2](https://inspect.aisi.org.uk/scorers.html?utm_source=chatgpt.com)

3. **Petri is an *Inspect task* with explicit role separation.**  
    Petri’s built-in audit supports `model_roles` (auditor/target/judge), accepts `special_instructions` (path/string/list), and can save transcript JSON to a directory — that’s enough to run Phase 0 end-to-end without inventing your own adversarial runner. [safety-research.github.io](https://safety-research.github.io/petri/tutorials/running-petri-eval/)

---

## **DELIVERABLE 1 — Architecture decision matrix**

**Legend:**

* **Leverage Inspect** \= use core Inspect framework features

* **Leverage extension** \= use an official/known extension

* **Build custom** \= AIGov-specific code you must own

| Component | Build custom | Leverage Inspect | Leverage Extension | Specific feature / hook | Rationale | Solo effort |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| Scenario execution runner | ☐ | ✅ | ☐ | `inspect eval`, `eval()`; Task/Solver/Scorer model [Inspect+1](https://inspect.aisi.org.uk/?utm_source=chatgpt.com) | Don’t build orchestration; Inspect already runs tasks, handles retries, concurrency, logging. | 0–1 day (config) |
| Live monitoring / run UX | ☐ | ✅ | ✅ | Inspect View \+ VS Code extension [Inspect+2Inspect+2](https://inspect.aisi.org.uk/log-viewer.html?utm_source=chatgpt.com) | You already get live progress, sample transcripts, history, log browsing (even remote dirs). | 0.5–1 day |
| Artifact storage / run history | ☐ | ✅ | ☐ | Default `./logs`; `.eval`/`.json`; list/read APIs; `inspect log schema` [Inspect+3Inspect+3Inspect+3](https://inspect.aisi.org.uk/?utm_source=chatgpt.com) | This is your evidence store. Build a thin indexer later if needed. | 0–2 days (optional) |
| Model provider integration | ☐ | ✅ | ☐ | Built-in providers \+ OpenAI-compatible endpoint \+ OpenRouter option [Inspect+1](https://inspect.aisi.org.uk/models.html?utm_source=chatgpt.com) | Avoid adapters for most client stacks; if it talks OpenAI-compatible, you’re done. | 0.5–2 days |
| “Target system” adapters (client chatbot/agent) | ✅ | ✅ | ☐ | Use OpenAI-compatible interface / custom Model API extensions [Inspect+1](https://inspect.aisi.org.uk/models.html?utm_source=chatgpt.com) | If the client exposes an API endpoint: cheap. If not (e.g., Copilot UI): you’ll need custom harnessing. | 2–10 days depending |
| Adversarial scenario library | ☐ | ✅ | ✅ | Petri task (`petri/audit`) \+ `special_instructions` [safety-research.github.io+1](https://safety-research.github.io/petri/tutorials/running-petri-eval/) | Petri gives you the attacker/target/judge scaffolding and a big prompt bank. | 0–2 days to start |
| Scenario organisation \+ metadata (GDPR/ISO/AI Act tags) | ✅ | ☐ | ☐ | Your own YAML/JSON “scenario card” layer | Petri gives prompts; it doesn’t give your compliance ontology. | 2–5 days (Phase 0 minimal) |
| Transcript analysis → finding extraction | ✅ | ✅ | ☐ | Custom scorer(s) returning structured dict score values [Inspect+1](https://inspect.aisi.org.uk/scorers.html?utm_source=chatgpt.com) | Inspect won’t create “behaviour\_json\_v1” for you; but it gives the slot to do it cleanly. | 3–7 days |
| AKG/RAG legal validation | ✅ | ✅ | ☐ | Scorer calls Neo4j/vector DB \+ attaches evidence to score | Inspect supports arbitrary code in solvers/scorers; add your connectors here. [Inspect+1](https://inspect.aisi.org.uk/solvers.html?utm_source=chatgpt.com) | 3–10 days |
| Multi-framework mapping (GDPR+ISO+AI Act) | ✅ | ✅ | ☐ | Multiple scorers or one scorer yielding multiple values [Inspect+1](https://inspect.aisi.org.uk/scorers.html?utm_source=chatgpt.com) | One run can produce multiple framework outputs (store separately). | 2–5 days |
| Human-in-the-loop supervision | ✅ | ✅ | ☐ | Tool approval policies (human/auto/custom) [Inspect+1](https://inspect.aisi.org.uk/approval.html?utm_source=chatgpt.com) | You can force approvals on tool calls (useful for agent evals \+ safety), but this is not a “pause whole pipeline” workflow engine. | 1–3 days |
| Report generation (L1/L2/L3) | ✅ | ☐ | ☐ | Build templates (docx/pdf) from findings JSON | Inspect gives logs \+ viewer, not €15k-grade client reports. [Inspect+1](https://inspect.aisi.org.uk/log-viewer.html?utm_source=chatgpt.com) | 5–15 days |
| Annex generation (GDPR article table etc.) | ✅ | ☐ | ☐ | Generate from findings \+ mappings | Needs your mapping layer \+ template system. | 2–7 days |
| GRC exports (OneTrust/Vanta/VerifyWise) | ✅ | ☐ | ☐ | Custom export adapters | Inspect isn’t a GRC exporter. | 3–10 days |
| Agent testing (Phase 2+) | ☐ | ✅ | ✅ | Inspect Agents \+ external agents (Claude Code/Codex CLI via Inspect SWE) [GitHub+3Inspect+3Inspect+3](https://inspect.aisi.org.uk/?utm_source=chatgpt.com) | Inspect is unusually strong here; don’t fight it. | Later |
| Cyber-style sandboxed environments (optional) | ☐ | ✅ | ✅ | Docker/K8s/EC2/Proxmox sandboxes; Inspect Cyber [Inspect+2Inspect Cyber+2](https://inspect.aisi.org.uk/sandboxing.html?utm_source=chatgpt.com) | For AIGov, valuable mainly if you test tool-using agents in realistic infra. | Later |

**Uncomfortable conclusion:** your “Phase 0 MVP” critical path is **NOT** Inspect/Petri. It’s:  
 (1) compliance findings schema \+ mapping, and (2) report production quality.

---

## **DELIVERABLE 2 — Optimal data flow diagram (formats \+ intervention points)**

`[Client Context Intake]  (Phase 0: manual Excel/JSON)`  
        `|`  
        `|  (AIGov config JSON)`  
        `v`  
`[Inspect Task Config]`  
  `- model(s): provider/model name or OpenAI-compatible endpoint`  
  `- task: petri/audit (or your task)`  
  `- task_args: max_turns, special_instructions, transcript_save_dir`  
        `|`  
        `|  inspect eval ...  (CLI or Python eval())`  
        `v`  
`[Audit Execution in Inspect]`  
  `- Roles: auditor / target / (optional) judge`  
  `- Tools/sandbox if agentic (docker recommended)`  
  `- Live logs to ./logs (or INSPECT_LOG_DIR)`  
        `|`  
        `|  outputs:`  
        `|   A) Inspect eval log: .eval (default) or .json`  
        `|   B) Petri transcript JSONs in transcript_save_dir`  
        `v`  
`[Evidence Store]`  
  `- log files + transcript files`  
  `- viewable live in Inspect View / VS Code`  
        `|`  
        `|  (post-processing)`  
        `v`  
`[Custom Compliance Judge Scorers inside Inspect OR offline batch]`  
  `- Judge_Analyst: parse transcript → candidate issues`  
  `- Judge_Validator: query AKG (Neo4j) + RAG snippets`  
  `- Judge_Mapper: map to GDPR/ISO/AI Act controls`  
  `- Output: findings JSON (behaviour_json_v1)`  
        `|`  
        `v`  
`[ReportGen]`  
  `- Templates L1/L2/L3 → DOCX/PDF`  
  `- Annex tables generated from mapping layer`  
        `|`  
        `v`  
`[GRC Export Adapters]`  
  `- CSV/JSON per target platform`  
        `|`  
        `v`  
`[Client Deliverables]`

### **Concrete format notes (what’s real, not aspirational)**

* **Inspect logs**: stored by default in `./logs` [Inspect](https://inspect.aisi.org.uk/?utm_source=chatgpt.com), in either `.eval` (binary, default) or `.json` [Inspect+1](https://inspect.aisi.org.uk/eval-logs.html?utm_source=chatgpt.com).

* You can **dump/convert** logs and even print a **JSON schema** via `inspect log schema`. [Inspect](https://inspect.aisi.org.uk/reference/inspect_log.html?utm_source=chatgpt.com)

* You can build parsers using Inspect’s **log file API** (`list_eval_logs`, `read_eval_log`, incremental sample reads). [Inspect+1](https://inspect.aisi.org.uk/reference/inspect_ai.log.html?utm_source=chatgpt.com)

* **Live supervision**: Inspect View supports live view, log history, and bundling a static viewer site; VS Code extension can run/debug tasks and browse logs. [Inspect+1](https://inspect.aisi.org.uk/log-viewer.html?utm_source=chatgpt.com)

* **Intervention points** (realistic):

  * If you run agentic tasks with tools, you can require human approval for tool calls via approval policies. [Inspect+1](https://inspect.aisi.org.uk/approval.html?utm_source=chatgpt.com)

  * For “Codex intervenes mid-run”, you typically do it by: (a) stopping/re-running with changed `task_args`, or (b) using approval mode to block tool calls until reviewed. (Inspect is not a workflow engine with arbitrary pause/resume checkpoints; it’s an eval runner.)

---

## **DELIVERABLE 3 — Extension relevance ranking (and what to actually do with them)**

### **Ranking table (AIGov relevance)**

| Extension / tool | Rating (1–10) | Primary capability | AIGov use cases | Integration effort | Priority |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **Petri** | 10 | Adversarial audit task: auditor/target/judge roles; special instruction prompts; transcript export [safety-research.github.io+1](https://safety-research.github.io/petri/tutorials/running-petri-eval/) | Fastest path to reproducible red-teaming transcripts | Low | **Phase 0** |
| **Inspect View \+ VS Code extension** | 9 | Live monitoring, log browsing, run/debug from IDE [Inspect+2Inspect+2](https://inspect.aisi.org.uk/vscode.html?utm_source=chatgpt.com) | Solo-founder productivity; audit evidence review; demo UX | Low | **Phase 0** |
| **Inspect core** | 9 | Tasks/solvers/scorers, tools, agents, sandboxes, log APIs [Inspect+4Inspect+4Inspect+4](https://inspect.aisi.org.uk/tasks.html?utm_source=chatgpt.com) | Your execution platform \+ evidence store | Medium | **Phase 0** |
| **Inspect SWE** | 6 | Run external SWE agents (Claude Code, Codex CLI) as Inspect agents [meridianlabs.ai+2GitHub+2](https://meridianlabs.ai/) | Later: auditing coding agents; internal “agent-as-a-solver” for automation | Med | Phase 1–2 |
| **Inspect Cyber** | 5 (Phase0: 2\) | Standardised agentic cyber eval scaffolding; infra configs \+ solvability checks [Inspect Cyber+2Inspect Cyber+2](https://inspect.cyber.aisi.org.uk/?utm_source=chatgpt.com) | If you audit tool-using agents in realistic infra (CTFs, internal networks) | Med–High | Phase 2+ |
| **Inspect Viz** | 4 | Visualisation library for Inspect eval data [meridianlabs.ai](https://meridianlabs.ai/) | Nice client dashboards later; not required for Phase 0 | Med | Later |
| **Inspect Scout** | 6 (speculative but promising) | Transcript scanning \+ visualisation (per Meridian description) [meridianlabs.ai](https://meridianlabs.ai/) | Could accelerate finding extraction / pattern analysis later | Unknown | Phase 1–2 |
| **Control Arena** | 3 | Control/monitoring experiments framework (not core to compliance deliverables) [Inspect](https://inspect.aisi.org.uk/extensions/?utm_source=chatgpt.com) | Research interest, not MVP revenue | High | Later/never |

### **Deep dives (extensions ≥5)**

**Petri (10/10)**  
 Petri gives you a ready-made adversarial audit harness as an Inspect task (`petri/audit`) with explicit **role separation** (auditor vs target, optional judge) and practical knobs (`max_turns`, `max_connections`, retries, and `transcript_save_dir`). It also accepts `special_instructions` as a path, newline string, or JSON list — which is the clean “scenario injection” interface you want for compliance scenario packs. [safety-research.github.io](https://safety-research.github.io/petri/tutorials/running-petri-eval/)  
 **Implication:** treat Petri as your Phase 0 execution engine; do *not* build your own “Auditor vs Target” runner.

**Inspect Cyber (5/10)**  
 Inspect Cyber standardises the creation of agentic cyber evaluations using “two config files” (evaluation \+ sandbox config) and provides a recommended project structure, variants, and solvability checks. [Inspect Cyber+2Inspect Cyber+2](https://inspect.cyber.aisi.org.uk/?utm_source=chatgpt.com)  
 **Implication:** only pull it in if your client audits include agents operating in infra (e.g., RAG agent \+ internal tools \+ network). Otherwise it’s a distraction in Phase 0\.

**Inspect SWE (6/10)**  
 Inspect supports external agents and Inspect SWE makes “Claude Code and Codex CLI available as standard Inspect Agents” (Meridian’s own phrasing). [meridianlabs.ai+2GitHub+2](https://meridianlabs.ai/)  
 **Implication:** this is strategically aligned with your “AI-assisted solo founder” setup — but it’s not the MVP bottleneck.

---

## **DELIVERABLE 4 — Phase 0 revised scope (3–4 weeks, solo founder reality)**

### **Phase 0 MVP (must ship)**

1. **Run Petri end-to-end on 1–3 scenarios**

   * Use `petri/audit` with `special_instructions` and `transcript_save_dir`. [safety-research.github.io](https://safety-research.github.io/petri/tutorials/running-petri-eval/)

2. **Define `behaviour_json_v1`** (your canonical findings format)

   * Include: scenario id, transcript references, evidence snippets, severity, impacted frameworks, recommended remediation.

3. **Implement 1 custom compliance scorer**

   * It reads the transcript/log and emits `behaviour_json_v1` as a structured score value (dict). Inspect supports multi-value scores. [Inspect+1](https://inspect.aisi.org.uk/scorers.html?utm_source=chatgpt.com)

4. **Generate a credible L2 report (10+ pages)**

   * From `behaviour_json_v1` \+ scenario metadata.

5. **Generate one annex table**

   * GDPR article mapping for those findings.

### **Phase 0 stretch (only if ahead of schedule)**

* L1 \+ L3 report templates

* Run 5–10 scenarios (same pipeline)

* Romanian output (translate report), but do **not** try to “translate the whole pipeline” yet.

### **What you are *not* building in Phase 0 (because Inspect already does it)**

* A runner/orchestrator for multi-turn evals and retries

* A log viewer/dashboard for internal review (Inspect View \+ VS Code already) [Inspect+1](https://inspect.aisi.org.uk/log-viewer.html?utm_source=chatgpt.com)

* Agent/tool sandbox lifecycle (use docker sandbox) [Inspect](https://inspect.aisi.org.uk/sandboxing.html?utm_source=chatgpt.com)

### **A blunt feasibility note**

Your plan says “Inspect setup 1–2 days”. That part is fine. The **real time sink is the compliance judgement data model \+ report production**. If you don’t lock those down early, you’ll burn the whole month “running scenarios” without something you can sell.

---

## **DELIVERABLE 5 — Critical questions answered (definitively where possible)**

### **1\) Chatbot/Agent wrappers: OpenAI / Claude / Gemini / M365 Copilot?**

* **OpenAI / Anthropic / Gemini**: **Yes, natively** (Inspect has built-in model provider support). [Inspect+1](https://inspect.aisi.org.uk/models.html?utm_source=chatgpt.com)

* **Anything with an OpenAI-compatible endpoint**: **Yes** (use Inspect’s OpenAI-compatible interface). [Inspect](https://inspect.aisi.org.uk/models.html?utm_source=chatgpt.com)

* **OpenRouter**: **Yes** (Inspect supports using OpenRouter as a bridge). [Inspect](https://inspect.aisi.org.uk/models.html?utm_source=chatgpt.com)

* **Microsoft 365 Copilot**: **No “Inspect-native wrapper” is documented**; you’ll likely need a bespoke harness depending on how the client exposes their system (Graph/Copilot Studio/Teams/UI). I didn’t find an official Inspect adapter for “Copilot as a product”.

### **2\) Report generation: does Inspect generate professional client reports?**

* **No**. Inspect provides logs \+ a viewer (and can bundle a static viewer site), but it’s not a €15k audit report generator. [Inspect+1](https://inspect.aisi.org.uk/log-viewer.html?utm_source=chatgpt.com)  
   **So you must build** templates (DOCX/PDF) fed from a stable findings schema.

### **3\) Multilingual: can Inspect run Romanian/German/French evals?**

* **Yes in practice, but not as a special “feature”.** Inspect is language-agnostic: prompts/messages are just text; you run the eval in whatever language your task/prompt uses, assuming the target/auditor/judge models support it. [Inspect+1](https://inspect.aisi.org.uk/solvers.html?utm_source=chatgpt.com)  
   **Caveat:** scoring quality depends on judge model language capability; don’t assume your LLM grader is equally strong in RO as EN.

### **4\) Audit supervision: can Codex monitor logs and intervene mid-audit?**

* **Monitoring:** Yes — Inspect View is live, and VS Code integrates log viewing. [Inspect+1](https://inspect.aisi.org.uk/log-viewer.html?utm_source=chatgpt.com)

* **Intervening mid-run:** Only in constrained ways:

  * You can require **tool call approvals** (human/auto/custom) which blocks tool execution until approved. [Inspect+1](https://inspect.aisi.org.uk/approval.html?utm_source=chatgpt.com)

  * Otherwise, the typical pattern is stop → tweak `task_args`/prompts → re-run (Inspect is an eval framework, not a long-lived workflow engine with arbitrary checkpoints).

### **5\) Judge architecture: can Petri’s judge be used for compliance?**

* Petri has a built-in judge role and scorer workflow, but it’s designed for **alignment/safety audit outcomes**, not “GDPR Art 5(1)(f) \+ ISO 27001 A.8.2 mapping”. [safety-research.github.io](https://safety-research.github.io/petri/tutorials/running-petri-eval/)  
   **Conclusion:** you must implement a **custom compliance scorer** (you can still *use* Petri’s scaffolding for transcript generation).

### **6\) Extension integration: drop-in vs heavy**

* **Drop-in**: VS Code extension \+ Inspect View (built-in) [Inspect+1](https://inspect.aisi.org.uk/vscode.html?utm_source=chatgpt.com)

* **Drop-in**: Petri (`petri/audit`) with task args \+ roles [safety-research.github.io](https://safety-research.github.io/petri/tutorials/running-petri-eval/)

* **Moderate**: Inspect SWE (if you truly need SWE agents inside evals) [meridianlabs.ai+1](https://meridianlabs.ai/)

* **Heavier**: Inspect Cyber (infra configs, sandbox topologies, etc.) [Inspect Cyber+1](https://inspect.cyber.aisi.org.uk/evaluation-configuration.html?utm_source=chatgpt.com)

### **7\) AKG/RAG integration: how to connect external knowledge sources to Inspect?**

* Put it in a **scorer** (or solver) as normal Python code: parse transcript, call Neo4j/vector DB, then produce structured scores. This is exactly what Inspect scorers are for. [Inspect+2Inspect+2](https://inspect.aisi.org.uk/scorers.html?utm_source=chatgpt.com)

### **8\) Scenario customisation: can we modify Petri scenarios?**

* Yes at the interface level: Petri accepts custom `special_instructions` (string/path/list), and exports transcripts. [safety-research.github.io](https://safety-research.github.io/petri/tutorials/running-petri-eval/)  
   This is sufficient to build “Audit templates” as curated instruction packs without forking Petri.

### **9\) Output storage: where do artifacts go?**

* Inspect logs: default `./logs` [Inspect](https://inspect.aisi.org.uk/?utm_source=chatgpt.com); `.eval` default format; `.json` supported [Inspect+1](https://inspect.aisi.org.uk/eval-logs.html?utm_source=chatgpt.com)

* Petri transcripts: written to `transcript_save_dir` as JSON files [safety-research.github.io](https://safety-research.github.io/petri/tutorials/running-petri-eval/)

* Logs are queryable via Python API and convertible/dumpable via CLI. [Inspect+1](https://inspect.aisi.org.uk/reference/inspect_ai.log.html?utm_source=chatgpt.com)

### **10\) Multi-framework evaluation: one run or separate runs?**

* **One run is feasible**: use multiple scorers (or a scorer yielding a dict of outputs) and store outputs separately. [Inspect+1](https://inspect.aisi.org.uk/scorers.html?utm_source=chatgpt.com)  
   Trade-off: a single “mega-judge” prompt can get messy; separate scorers keep logic isolated.

---

## **DELIVERABLE 6 — Top 5 risks & mitigations**

| Risk | Probability | Impact | Mitigation | Validation method |
| ----- | ----- | ----- | ----- | ----- |
| You overbuild orchestration that Inspect already provides | High | High | Freeze custom runner work; adopt Inspect View \+ VS Code as default workflow [Inspect+1](https://inspect.aisi.org.uk/vscode.html?utm_source=chatgpt.com) | Demo: run Petri \+ view logs live in VS Code |
| Compliance “judge” outputs are inconsistent / not auditable | High | High | Define `behaviour_json_v1` early; require evidence pointers (transcript spans) | Human spot-check 10 findings vs transcripts |
| “Client target integration” is harder than expected (non-API systems) | Med | High | Standardise on OpenAI-compatible endpoint requirement for Phase 0; document exceptions [Inspect](https://inspect.aisi.org.uk/models.html?utm_source=chatgpt.com) | Run against 2 different providers successfully |
| Multilingual scoring quality (RO) collapses | Med | Med/High | Keep Phase 0 scoring in EN; translate reports after; later test RO judge models | Compare judge agreement EN vs RO |
| Report generation eats the schedule | High | High | Start report templates Week 1; don’t wait for “perfect pipeline” | Produce a “good enough” L2 report by end of Week 2 |

---

## **Practical “do this next” checklist (no fluff)**

**Week 1**

* Lock `behaviour_json_v1` (fields \+ evidence linking).

* Run `inspect eval petri/audit ...` and review in Inspect View/VS Code. [safety-research.github.io+1](https://safety-research.github.io/petri/tutorials/running-petri-eval/)

**Week 2**

* Implement one compliance scorer that emits `behaviour_json_v1` into the Inspect log.

* Generate a rough L2 report from that JSON.

**Week 3**

* Add AKG/RAG validation calls inside the scorer.

* Add GDPR annex generator.

**Week 4**

* Polish templates; run 5 scenarios; produce a sales-grade sample pack.

