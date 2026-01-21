# Report Layers (Canonical)

This document is the single source of truth for report layer definitions.
Other docs must link here and must not redefine L1/L2/L3 semantics.

## Canonical mapping
- **L1 = EXEC** (executive audience)
- **L2 = COMPLIANCE** (GDPR compliance / legal audience)
- **L3 = SECURITY** (CISO / security & technical assurance audience)

## What each layer contains
- **L1 (EXEC)**: Decision summary, risk posture, top findings, action priorities.
  Primary evidence sources: Intake summary, Judge outcomes, high-level Evidence Pack rollups.
- **L2 (COMPLIANCE)**: GDPR article mapping, findings with citations, legal rationale,
  audit-ready coverage tables, provenance chain.
  Primary evidence sources: Judge outputs, Evidence Pack excerpts, scenario provenance.
- **L3 (SECURITY)**: Full technical artefacts, transcripts, raw evidence bundles,
  implementation details, reproducibility metadata.
  Primary evidence sources: Evidence Pack (full), raw logs, run manifests.

## Single source of truth
If a document needs to reference L1/L2/L3, it must link here and avoid restating
layer meanings beyond brief pointers.

## Good looks like
- Clear audience fit per layer with no role ambiguity.
- L2 content is audit-ready and legally grounded.
- L3 provides full technical traceability and reproducibility.

## Bad looks like
- L2 or L3 labeled for conflicting audiences (e.g., CISO vs compliance swapped).
- Multiple docs redefine the same layer semantics.
- Missing evidence sources or provenance linkage.

## How to decide
- If it helps an executive decide, it is L1.
- If it maps to GDPR/legal compliance, it is L2.
- If it is raw technical evidence or assurance detail, it is L3.
