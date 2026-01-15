# DeepEval vs Inspect (VerifyWise Context)

## Feature Matrix
| Area | DeepEval (repo docs) | Inspect (UK AISI docs) |
| --- | --- | --- |
| Core abstraction | Pytest-like `assert_test` on `LLMTestCase` objects plus metrics; supports black-box end-to-end and component-level spans via tracing (`@observe`) | Three-part pipeline: Datasets -> Solvers (prompt/agent/tool chains) -> Scorers; tasks orchestrated with `inspect eval` |
| Metrics & scoring | Large library of LLM-based metrics (G-Eval, DAG, RAG metrics, agent metrics, hallucination, toxicity, conversation, summarization) and custom metric hooks | Scorers can be string matching, model-graded, or custom; fewer built-in RAG-specific metrics but flexible scoring functions |
| Safety & red teaming | Built-in red-teaming suite (40+ vulnerabilities, attack strategies) and safety metrics | No first-class red-team library; relies on writing eval tasks or external packages for adversarial probes |
| Dataset tooling | Synthetic dataset generation, dataset management/sharing through Confident AI platform | Dataset loaders from tabular/JSON, dataset caching, eval sets packaged as `inspect_evals` (100+ ready-made benchmarks) |
| Benchmarking | CLI helpers to run standard LLM benchmarks (MMLU, HellaSwag, DROP, BBH, TruthfulQA, HumanEval, GSM8K) | Inspect Evals catalogue covers popular academic/agent benchmarks; integrates with Inspect pipeline |
| Observability | Tracing plus span-level evals; Confident AI UI for test runs, comparisons, and iteration tracking | Inspect View web app plus VS Code extension for live logs, traces, and debugging |
| Agents & tools | Measures agent behaviors (task completion, tool correctness) and can evaluate traced spans; less focus on executing agent tools inside the eval harness | Rich agent framework (ReAct agent, custom agents, multi-agent), extensive tool calling (bash/python/edit/web/MCP), optional sandboxing for untrusted tool code |
| Execution model | Runs locally with any chosen LLM or local NLP models; minimal infra; CI-friendly (`deepeval test run`) | Supports many providers (OpenAI, Anthropic, Google, Mistral, HF, Bedrock, Azure, TogetherAI, Groq, vLLM/Ollama/llama-cpp); sandbox/docker for tool runs; CLI `inspect eval` |
| Platform tie-in | Tight integration with Confident AI for dataset curation, reporting, finetuning metrics, monitoring in production | Standalone OSS; plugins/extensions for tools, sandboxes, agents; no hosted platform by default |
| Integration surface | Examples for LangChain, LlamaIndex, HuggingFace; metrics can wrap any LLM call | Extension points for solvers, scorers, tools, sandboxes, and agents; agent bridge for external frameworks |

## Why VerifyWise Likely Picked DeepEval
- RAG- and safety-centric metrics out of the box (answer relevancy, faithfulness, contextual recall/precision, hallucination) reduce custom judging code.
- Pytest-like ergonomics for regression testing LLM outputs and CI gating.
- Component-level span evaluation matches traced pipelines without rewriting app logic.
- Built-in red teaming provides a ready-made safety harness without building adversarial datasets.
- Optional Confident AI platform gives shareable reports/iteration tracking, useful for stakeholder visibility.

## Overlap
- Both are Python OSS frameworks for LLM evaluation with CLI runners and custom scoring hooks.
- Support multiple model providers and local models; can run model-graded evaluations.
- Provide logging/tracing views (DeepEval via Confident AI; Inspect via Inspect View/VS Code).
- Allow building bespoke metrics/scorers to fit domain tasks.

## Feature Gaps
- Only DeepEval: rich RAG metric suite, DAG metric, safety/red-teaming harness, synthetic dataset generation, Confident AI platform integration, span-level assertions via tracing.
- Only Inspect: extensive agent/tool scaffolding (ReAct, multi-agent), built-in tool sandboxing for untrusted code, large catalogue of prebuilt evals (`inspect_evals`), VS Code authoring/debugging helpers, agent bridge for external frameworks.

## Compatibility & Interop
- Both run in Python; datasets can be shared (e.g., export DeepEval `LLMTestCase`s to CSV/JSON and load into Inspect datasets).
- Scorers/metrics are not drop-in interchangeable, but model-graded prompts can be ported between frameworks with minimal refactoring.
- No direct adapter layer today; running both in parallel is feasible (DeepEval for CI regression metrics, Inspect for benchmark/agent tasks) using the same model endpoints.

## Recommendation for AIGov
- Primary choice: keep DeepEval for CI-style regression, RAG quality, and safety/red-team coverage; it matches VerifyWise's likely needs.
- Add Inspect selectively when you need: (1) to run public benchmark suites via `inspect_evals`, (2) to evaluate complex agent/tool workflows with sandboxed execution, or (3) to leverage its agent bridge/VS Code tooling.
- If you want a single stack, prefer DeepEval for RAG-heavy apps; layer Inspect alongside (not instead of) when agentic or tool-execution evals become a priority.
