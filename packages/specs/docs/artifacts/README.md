# Research & Pro-Run Artifacts

This folder stores **raw, dated outputs** from Deep Research runs and Pro runs (PDF/DOCX/MD).
These files are **inputs and references** for planning and contract work, but they are **not**
the canonical source-of-truth contracts.

## Naming convention (required)
Use date-first filenames:

`YYYY-MM-DD__<type>__<short-name>.<ext>`

Where `<type>` is one of:
- `deep-research`
- `pro-run`
- `notes`

Examples:
- `2026-01-20__deep-research__gdpr-gr-requirements.pdf`
- `2026-01-20__pro-run__pre2.2-taxonomy.md`

## What belongs here
- Deep research exports (PDF/DOCX)
- Pro run outputs (MD/DOCX)
- One-off notes that should be preserved as historical context

## What does NOT belong here
- Canonical contracts, schemas, or “source of truth” docs.
  Those live under: `packages/specs/docs/contracts/`

## Windows metadata warning
Do not commit `*:Zone.Identifier` files (Windows ADS metadata). They are ignored via `.gitignore`.
