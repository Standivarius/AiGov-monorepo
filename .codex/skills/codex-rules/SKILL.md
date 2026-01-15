---
name: codex-rules
description: "Enforce repo execution discipline: keep PRs small; always update STATUS.md; run migration-smoke when invariants change; never hand-edit vendored contracts."
---

## Always
- Keep PRs small and auditable; avoid drive-by refactors.
- Update /STATUS.md (what changed, why, what's next).
- If invariants/plumbing are touched: run the canonical proof command listed in /STATUS.md (once PR-0 lands this is typically `npx nx run evalsets:migration-smoke`).
- Never hand-edit vendored contracts; use sync scripts + drift gates.
