# AKG - Research Findings

## Codex-Petri Validation
**Status**: Pending  
**Date**: TBD

### Installation Check
- Location: [TBD - local path]
- Database: [TBD - Neo4j? FalkorDB?]
- Status: [TBD - running? needs setup?]

### Node Count
- GDPR articles: [TBD - verify actual count]
- ISO 27001 controls: [TBD]
- ISO 42001: [TBD - present?]
- EU AI Act: [TBD]
- RO Law 190/2018: [TBD]
- Total nodes: [TBD]

### Query Performance
- Sample query latency: [TBD]
- Concurrent query handling: [TBD]
- Cache effectiveness: [TBD]

---

## Graph Database Comparison
**Status**: Deferred (use existing Codex-Petri)

### If Migration Needed Later
| Database | Pros | Cons |
|----------|------|------|
| Neo4j Aura | Managed, scalable | Cost |
| FalkorDB | Fast (Redis), open source | Less mature |
| Neo4j Local | Full control | Maintenance burden |

---

## National Law Overlay Strategy
**Status**: Pending

### Storage Format
```cypher
CREATE (p:National_Provision {
  id: "ro-law-190-art-5",
  title_en: "Data Protection Officer duties",
  text_original: "[Romanian text]",
  language_code: "ro",
  implements: "gdpr-art-37"
})
```

### Translation Strategy
- Store: EN summary + RO original
- Judge uses: EN for reasoning
- Reports reference: RO original (avoid double translation)

---

**Links to GDrive**: [Will add after validation complete]