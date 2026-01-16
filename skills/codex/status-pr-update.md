# status-pr-update

Generate a paste-ready STATUS.md snippet without conflicts.

## Inputs (read in order)
1) `STATUS.md`
2) `AGENTS.md`
3) PR diff summary (changed files + intent)

## Output (required)
Return exactly two sections:

1) **STATUS Snippet** (append-only)
- Plain English, 2–4 bullets max.
- Must not contradict existing Phase/Proof/Next-PR facts.
- Must not rename past PR labels.
- If the next PR label is ambiguous/reused, choose the next unused label (PR-D, PR-E, etc.) and state it.
- Include: what changed, why it matters, what to run to verify.

2) **Conflict Check**
- Output one line:
  - "No conflicts detected" OR
  - "Potential conflict: … Proposed fix: …"
