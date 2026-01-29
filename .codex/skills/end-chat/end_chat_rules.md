# End Chat Rules (Repo Standard)

## Canonical paths (exact patterns)
- State object JSON: `packages/specs/docs/planning/YYYY-MM-DD/state_object_v0_3__YYYY-MM-DD.json`
- Chat transcript artifact: `packages/specs/docs/artifacts/YYYY-MM-DD__chat__<topic>.md`
- Handoff primer (optional but recommended): `packages/specs/docs/artifacts/YYYY-MM-DD__handoff__new-chat-primer.md`

## Wrap-up checklist
1) ChatGPT drafts the next state_object JSON content (updated milestones + next module queue).
2) User saves full chat transcript to the artifacts path above.
3) ChatGPT produces a self-contained “New Chat Prompt Template” that includes:
   - GDPR-only scope lock.
   - Allowed verification commands list.
   - “Auditor/enterprise scrutiny, but minimal sufficient process; don’t overdo it”.
   - Must-read context file paths (AGENTS + latest state object + latest transcript + any relevant artifacts).
