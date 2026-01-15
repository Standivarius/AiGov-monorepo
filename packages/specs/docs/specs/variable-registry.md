# AIGov Variable Registry

**Purpose**: Single source of truth for ALL variables across ALL schemas  
**Status**: Living document - update when variables added/modified/removed  
**Last Updated**: 2025-12-16

---

## How to Use This Registry

**Before adding a variable**:
1. Search this document for similar variables
2. Check if existing variable can be reused
3. If new variable needed, add to appropriate section
4. Define clearly: name, type, mandatory status, used in

**When changing a variable**:
1. Update definition here
2. Update all schemas that use it
3. Update file-registry.md with version bump

---

## scenario_card Variables

### Core Identity

| Variable | Type | Mandatory | Used In | Definition |
|----------|------|-----------|---------|------------|
| scenario_id | string | YES | scenario_card, behaviour_json, mock_log | Unique identifier (format: FRAMEWORK-NNN, e.g., GDPR-007) |
| title | string | YES | scenario_card, reports | Human-readable scenario name |
| version | string | YES | scenario_card | Scenario version (semantic: 1.0, 1.1, 2.0) |

### Taxonomy

| Variable | Type | Mandatory | Used In | Definition |
|----------|------|-----------|---------|------------|
| applies_to | enum | YES | scenario_card, library structure | chatbot_general \| ms365_copilot \| agent |
| framework | enum | YES | scenario_card, behaviour_json, evaluation_criteria | GDPR \| ISO27001 \| ISO42001 \| AI_ACT |
| role | enum | YES | scenario_card, client_intake | hr \| logistics \| customer_service \| admin \| general |
| tags | list[string] | YES | scenario_card | Free-form tags (industry: healthcare/finance, violation type, context) |

### Compliance Mapping

| Variable | Type | Mandatory | Used In | Definition |
|----------|------|-----------|---------|------------|
| primary_violation.article | string | YES | scenario_card, behaviour_json | Primary article being tested (e.g., Art.5(1)(f)) |
| primary_violation.title | string | YES | scenario_card | Human-readable article title |
| articles | list[string] | YES | scenario_card, behaviour_json | All GDPR articles tested in scenario |
| risk_category | enum | YES | scenario_card, behaviour_json | See risk_category_taxonomy (11 categories) |

### Source Traceability

| Variable | Type | Mandatory | Used In | Definition |
|----------|------|-----------|---------|------------|
| source_case.authority | string | NO | scenario_card | Supervisory authority name (e.g., CNIL, ICO) |
| source_case.case_ref | string | NO | scenario_card | Official case number or reference |
| source_case.year | integer | NO | scenario_card | Year of enforcement action |
| source_case.url | string | NO | scenario_card | Link to official case documentation |
| source_case.summary | string | NO | scenario_card | 2-3 sentence case description |

### Audit Execution

| Variable | Type | Mandatory | Used In | Definition |
|----------|------|-----------|---------|------------|
| auditor_seed | text | YES | scenario_card, auditor config | Core scenario description for Petri auditor (1-2 paragraphs) |
| context | text | NO | scenario_card | Background explanation of legal/technical concepts (edge cases only) |
| insights | list[object] | NO | scenario_card | Research findings on violation patterns |
| insights[].source | string | NO | scenario_card | Research source (ENISA report, EDPB case, etc.) |
| insights[].finding | string | NO | scenario_card | Key finding from source |
| insights[].implication | string | NO | scenario_card | How finding affects scenario testing |

### Legal Context

| Variable | Type | Mandatory | Used In | Definition |
|----------|------|-----------|---------|------------|
| legal_context.gdpr_articles | list[object] | YES | scenario_card | Inline GDPR article text (Phase 0) |
| legal_context.gdpr_articles[].article | string | YES | scenario_card | Article number (Art.5(1)(f)) |
| legal_context.gdpr_articles[].text | text | YES | scenario_card | Full official article text |
| legal_context.edpb_guidance | list[object] | NO | scenario_card | EDPB guidelines relevant to scenario |
| legal_context.edpb_guidance[].source | string | NO | scenario_card | EDPB guideline title and number |
| legal_context.edpb_guidance[].section | string | NO | scenario_card | Specific section reference |
| legal_context.edpb_guidance[].url | string | NO | scenario_card | Link to guideline |
| legal_context.edpb_guidance[].excerpt | text | NO | scenario_card | Relevant text excerpt |
| legal_context.edpb_guidance[].relevance | string | NO | scenario_card | Why this guidance matters for scenario |
| national_law | list[object] | NO | scenario_card | Country-specific legislation (Phase 0: Romania only) |
| national_law[].country | string | NO | scenario_card | ISO country code (RO, PL, DE) |
| national_law[].legislation | list[object] | NO | scenario_card | National laws |
| national_law[].legislation[].law | string | NO | scenario_card | Law name (e.g., Law 190/2018) |
| national_law[].legislation[].article | string | NO | scenario_card | Article number |
| national_law[].legislation[].text | text | NO | scenario_card | Article text |

### Expected Outcome

| Variable | Type | Mandatory | Used In | Definition |
|----------|------|-----------|---------|------------|
| expected_violation_behavior | string | YES | scenario_card | What violation should occur (1 sentence) |

### Metadata

| Variable | Type | Mandatory | Used In | Definition |
|----------|------|-----------|---------|------------|
| author | string | YES | scenario_card | Marius \| Claude \| Generated |
| created_date | string | YES | scenario_card | ISO date (YYYY-MM-DD) |
| last_updated | string | YES | scenario_card | ISO date (YYYY-MM-DD) |
| notes | text | NO | scenario_card | Internal comments |

---

## behaviour_json Variables

| Variable | Type | Mandatory | Used In | Definition |
|----------|------|-----------|---------|------------|
| scenario_id | string | YES | behaviour_json, scenario_card | Must match scenario_card.scenario_id |
| framework | enum | YES | behaviour_json, scenario_card | Must match scenario_card.framework |
| rating | enum | YES | behaviour_json | VIOLATED \| COMPLIANT \| UNDECIDED |
| reasoning | text | YES | behaviour_json | Natural language explanation of rating |
| violations | list[object] | CONDITIONAL | behaviour_json | Required if rating=VIOLATED |
| violations[].finding_id | string | YES | behaviour_json | Unique ID (format: scenario_id-F-NNN) |
| violations[].gdpr_article | string | YES | behaviour_json | Article violated (Art.5(1)(f)) |
| violations[].severity | enum | YES | behaviour_json | HIGH \| MEDIUM \| LOW |
| violations[].description | text | YES | behaviour_json | What violation occurred |
| violations[].evidence | list[object] | YES | behaviour_json | Transcript evidence |
| violations[].evidence[].turn | integer | YES | behaviour_json | Conversation turn number |
| violations[].evidence[].role | enum | YES | behaviour_json | user \| assistant \| system |
| violations[].evidence[].snippet | text | YES | behaviour_json | Verbatim quote from transcript |

---

## client_intake Variables

| Variable | Type | Mandatory | Used In | Definition |
|----------|------|-----------|---------|------------|
| chatbot_language | string | YES | client_intake, auditor_config, judge_config | ISO 639-1 code (RO/EN/DE/FR) |
| industry | enum | YES | client_intake, scenario_tags | healthcare \| finance \| telco \| tech \| all |
| role | enum | YES | client_intake, scenario_card | hr \| customer_service \| admin \| logistics |
| chatbot_scope | text | YES | client_intake, auditor_config | Functional description (e.g., "appointment scheduling") |
| target_frameworks | list[enum] | YES | client_intake, scenario_selection | GDPR \| ISO27001 \| ISO42001 \| AI_ACT |
| company_name | string | YES | client_intake, reports | For report generation |
| audit_date | string | YES | client_intake, reports | ISO date (YYYY-MM-DD) |
| national_law_applies | string | NO | client_intake, scenario_selection | ISO country code (RO/PL/DE) if applicable |

---

## risk_category_taxonomy (Enum)

**Phase 0 Categories** (11 total):

```yaml
PII_DISCLOSURE              # Art.5(1)(f) - confidentiality breach
DATA_MINIMIZATION_FAILURE   # Art.5(1)(c) - excessive collection
PURPOSE_LIMITATION_FAILURE  # Art.5(1)(b) - use beyond stated purpose
CONSENT_FAILURE            # Art.6 - no/invalid consent
LEGAL_BASIS_MISSING        # Art.6 - no legal basis claimed
DSAR_FAILURE               # Art.15 - access request mishandled
RTBF_FAILURE               # Art.17 - erasure request ignored
AUTH_BYPASS                # Art.32 - inadequate authentication
TRANSPARENCY_FAILURE       # Art.13 - no/inadequate privacy info
PROMPT_INJECTION           # Art.32 - security vulnerability
RAG_LEAK                   # Art.5(1)(f) + Art.32 - unauthorized doc access
```

---

## Cross-Schema Variables (Must Match)

| Variable | Appears In | Must Match | Validation Rule |
|----------|------------|------------|----------------|
| scenario_id | scenario_card, behaviour_json, mock_log | YES | Exact string match |
| framework | scenario_card, behaviour_json, evaluation_criteria | YES | Same enum value |
| articles | scenario_card, behaviour_json | YES | behaviour_json violations must reference articles in scenario_card |

---

## Enum Definitions

### applies_to
```yaml
chatbot_general    # Generic chatbot (web, mobile)
ms365_copilot      # Microsoft 365 Copilot
agent              # Autonomous AI agent
```

### framework
```yaml
GDPR        # EU General Data Protection Regulation
ISO27001    # Information security management (Phase 1)
ISO42001    # AI management system (Phase 1)
AI_ACT      # EU AI Act (Phase 2)
```

### role
```yaml
hr                 # Human Resources
logistics          # Supply chain, warehouse
customer_service   # Support, helpdesk
admin              # General administration
general            # No specific role
```

### rating
```yaml
VIOLATED      # Compliance violation detected
COMPLIANT     # No violation, system behaves correctly
UNDECIDED     # Insufficient evidence or edge case
```

### severity
```yaml
HIGH      # Significant risk to rights and freedoms
MEDIUM    # Moderate risk, single principle violation
LOW       # Minor risk, procedural violation
```

---

## Naming Conventions

### Variable Naming
- **snake_case**: All variables (`scenario_id`, `gdpr_articles`, `mock_log_entry`)
- **SCREAMING_SNAKE**: Enum values (`PII_DISCLOSURE`, `VIOLATED`, `COMPLIANT`)
- **kebab-case**: File names only (`scenario-card-schema-v1.2.md`)

### ID Formats
- **Scenario ID**: `FRAMEWORK-NNN` (e.g., `GDPR-007`, `ISO-042`)
- **Finding ID**: `scenario_id-F-NNN` (e.g., `GDPR-007-F-001`)
- **Turn numbers**: 1-indexed integers (turn 1, turn 2, ...)

---

## Validation Rules

### Required Field Validation
```python
# scenario_card mandatory fields
required_fields = [
    'scenario_id',
    'title',
    'version',
    'applies_to',
    'framework',
    'role',
    'tags',
    'primary_violation',
    'articles',
    'risk_category',
    'auditor_seed',
    'legal_context.gdpr_articles',
    'expected_violation_behavior',
    'author',
    'created_date',
    'last_updated'
]
```

### Cross-Schema Validation
```python
# behaviour_json must reference scenario_card
assert behaviour_json['scenario_id'] == scenario_card['scenario_id']
assert behaviour_json['framework'] == scenario_card['framework']

# All violations must reference scenario articles
for violation in behaviour_json['violations']:
    assert violation['gdpr_article'] in scenario_card['articles']
```

---

## Phase Roadmap

### Phase 0 (Current)
- **Frameworks**: GDPR only
- **Applies to**: chatbot_general only
- **National law**: Romania (RO) only
- **Risk categories**: 11 categories (PII_DISCLOSURE through RAG_LEAK)

### Phase 1 (Future)
- Add ISO27001, ISO42001 frameworks
- Add ms365_copilot, agent to applies_to
- Expand national_law to Poland (PL), Germany (DE)
- Refine risk_category taxonomy based on Phase 0 learnings

---

## Change Log

| Date | Version | Changes | Impact |
|------|---------|---------|--------|
| 2025-12-16 | 1.0 | Initial registry created | All schemas |

---

**Maintenance**: Update when variables added/changed, increment version in Change Log
