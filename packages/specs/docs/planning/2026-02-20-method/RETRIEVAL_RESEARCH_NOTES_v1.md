# Retrieval Research Notes v1

Date: `2026-02-20`  
Purpose: reference patterns used to design retrieval for Pre-PRD dossiers.

## Pattern 1: context-aware chunk retrieval

Signal:
- Retrieval quality improves when chunk context is preserved instead of isolated snippets.

Reference:
- Anthropic, "Introducing Contextual Retrieval"  
  `https://www.anthropic.com/engineering/contextual-retrieval`

## Pattern 2: graph plus vector hybrid retrieval

Signal:
- Combining graph structure with semantic retrieval improves multi-hop and relationship-heavy queries.

References:
- Microsoft Research, "From Local to Global GraphRAG"  
  `https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/`
- Microsoft GraphRAG project  
  `https://github.com/microsoft/graphrag`

## Pattern 3: retrieval quality must be evaluated as a first-class artifact

Signal:
- Treat retrieval quality and data quality as measurable pipeline outputs, not ad hoc behavior.

Reference:
- NVIDIA AI Blueprint, "Retriever Evaluation"  
  `https://docs.nvidia.com/ai-blueprints/latest/information-extraction/retriever-eval.html`

## Pattern 4: last-mile enterprise data alignment is usually the blocker

Signal:
- Most failures are from data capture, normalization, and governance gaps, not model capability.

Reference:
- VentureBeat analysis on enterprise agentic AI data bottlenecks  
  `https://venturebeat.com/data/the-last-mile-data-problem-is-stalling-enterprise-agentic-ai-golden/`

## Applied decision for AiGov

For current scope, use Factory-Lite retrieval discipline:

1. deterministic source list
2. explicit claim schema
3. explicit conflict policy
4. dossier artifacts as gate evidence

No orchestrator build is required at this stage.

