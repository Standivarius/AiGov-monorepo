# GitHub Execution Board v1

Date: `2026-02-20`  
Board: `AiGov_Factory_Execution_Board`  
URL: `https://github.com/users/Standivarius/projects/5`

## Purpose

Use one canonical board for method execution so gate state does not drift across chats, docs, and local notes.

## Gate mapping

- G0 Method lock and workflow contract: issue `#194`
- G1 Pre-PRD discovery pack complete: issue `#195`
- G2 PRD-P and PRD-M approval: issue `#196`
- G3 PRD-E truth pack gate: issue `#197`
- G4 Build readiness decision only: issue `#198`

## Discovery task mapping

- M_Intake dossier extraction: issue `#199`
- M_Judge dossier extraction: issue `#200`
- Retrieval index and conflict policy: issue `#201`
- GPT Pro deep run and ingestion: issue `#202`

## Status labels

- `status:ready` means executable now.
- `status:blocked` means waiting on upstream gate approval.
- `factory:blocker` marks issues that block gate closure.

## Ownership labels

- `owner:codex` for agent-executed tasks.
- `owner:marius` for approval and decision tasks.

## Board discipline

1. Every method-stage action must map to an issue on this board.
2. Gate issues are only closed when exit evidence is linked in the issue body or comments.
3. PR links, artifact links, and validation outputs are mandatory for gate-closing comments.
4. If a gate criterion changes, update this file and the corresponding issue in the same PR.
5. Every gate-changing PR must link its issue, and that issue must link back to the PR.

## Exit evidence expectations per gate

- G0: method memo + contract update merged.
- G1: discovery pack + checklist completed with no blocker questions.
- G2: PRD-P and all PRD-M approved.
- G3: PRD-E baseline approved with validator set.
- G4: explicit go/no-go decision and first EX slice boundary.
