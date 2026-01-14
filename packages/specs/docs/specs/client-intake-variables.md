# Client Intake Variables

**Purpose**: Required inputs for client onboarding and audit configuration  
**Status**: Living document - update when intake process changes  
**Last Updated**: 2025-12-16

---

## Overview

Client intake captures information needed to:
1. Configure Petri auditor and judge
2. Select appropriate test scenarios
3. Generate client-specific reports
4. Scope the audit engagement

**Process**: IntakeAgent (AI-dynamic questionnaire) → Doc extraction → Output generation

---

## Core Variables

### 1. Chatbot Language

| Field | Type | Mandatory | Used By |
|-------|------|-----------|----------|
| `chatbot_language` | string | YES | Auditor, Judge |

**Values**: ISO 639-1 codes (RO, EN, DE, FR)  
**Purpose**: Auditor speaks this language to target, Judge translates internally  
**Example**: `chatbot_language: "RO"` → Auditor probes in Romanian, Judge thinks in English

**Validation**: Must be supported by Petri multilingual capabilities

---

### 2. Industry

| Field | Type | Mandatory | Used By |
|-------|------|-----------|----------|
| `industry` | enum | YES | Scenario selection |

**Values**: `healthcare | finance | telco | tech | retail | all`  
**Purpose**: Filter scenarios relevant to client's sector  
**Example**: `industry: "healthcare"` → Select scenarios with healthcare context

**Note**: Industry becomes a `tag` in scenario_card, not a top-level field.

---

### 3. Role

| Field | Type | Mandatory | Used By |
|-------|------|-----------|----------|
| `role` | enum | YES | Scenario selection, Auditor config |

**Values**: `hr | logistics | customer_service | admin | general`  
**Purpose**: Defines chatbot's operational context  
**Example**: `role: "customer_service"` → Test appointment scheduling, complaint handling

---

### 4. Chatbot Scope

| Field | Type | Mandatory | Used By |
|-------|------|-----------|----------|
| `chatbot_scope` | text | YES | Auditor seed, Judge context |

**Format**: 2-3 sentence functional description  
**Purpose**: What the chatbot is supposed to do  
**Example**:
```yaml
chatbot_scope: |
  Healthcare appointment scheduling chatbot. 
  Handles patient inquiries about available slots, doctor specialties, and location.
  Should not disclose other patients' information or medical records.
```

---

### 5. Target Frameworks

| Field | Type | Mandatory | Used By |
|-------|------|-----------|----------|
| `target_frameworks` | list[enum] | YES | Scenario selection, Report generation |

**Values**: `GDPR | ISO27001 | ISO42001 | AI_ACT`  
**Phase 0**: GDPR only  
**Phase 1+**: Multi-framework support

**Example**:
```yaml
target_frameworks:
  - GDPR
  - ISO27001
```

---

### 6. Company Name

| Field | Type | Mandatory | Used By |
|-------|------|-----------|----------|
| `company_name` | string | YES | Report generation |

**Format**: Full legal name  
**Purpose**: Appears on all report headers  
**Example**: `company_name: "MedTech Solutions SRL"`

---

### 7. Audit Date

| Field | Type | Mandatory | Used By |
|-------|------|-----------|----------|
| `audit_date` | string | YES | Report generation, Timestamp |

**Format**: ISO 8601 (YYYY-MM-DD)  
**Purpose**: Establishes point-in-time for compliance assessment  
**Example**: `audit_date: "2025-12-20"`

**Note**: Audits are snapshots, not continuous monitoring (Phase 0).

---

### 8. National Law (Optional)

| Field | Type | Mandatory | Used By |
|-------|------|-----------|----------|
| `national_law_applies` | string | NO | Scenario selection, Legal context |

**Values**: ISO country codes (RO, PL, DE)  
**Phase 0**: Romania (RO) only  
**Purpose**: Include country-specific legislation (e.g., RO Law 190/2018)

**Example**:
```yaml
national_law_applies: "RO"  # Romanian GDPR implementation
```

---

## Document Inputs (Optional)

IntakeAgent can extract information from uploaded documents:

### Privacy Policy
- **Purpose**: Understand stated data practices
- **Extraction**: Legal basis claims, retention periods, third-party disclosures

### System Architecture Diagram
- **Purpose**: Identify data flows, storage locations
- **Extraction**: RAG systems, authentication layers, data pipelines

### Existing DPIA (Data Protection Impact Assessment)
- **Purpose**: Leverage prior risk analysis
- **Extraction**: Identified risks, mitigation measures, residual concerns

---

## Derived Variables

**Not directly asked, but computed during intake**:

### Scenario Selection
```yaml
selected_scenarios:
  - GDPR-007  # Healthcare + PII disclosure
  - GDPR-015  # Customer service + RTBF
  - GDPR-023  # General + Authentication bypass
```

**Logic**:
1. Filter by `target_frameworks` (GDPR only Phase 0)
2. Filter by `industry` tag match
3. Filter by `role` match
4. If `national_law_applies`, prioritize scenarios with national_law context

### Report Configuration
```yaml
report_config:
  language: "RO"  # Report language matches chatbot_language
  formats: ["L1_Executive", "L2_CISO", "L3_CCO"]
  annexes: ["GDPR_Articles", "RO_Law_190_2018"]
```

---

## Validation Rules

### Required Field Check
```python
required_fields = [
    'chatbot_language',
    'industry',
    'role',
    'chatbot_scope',
    'target_frameworks',
    'company_name',
    'audit_date'
]

for field in required_fields:
    assert field in client_intake, f"Missing required field: {field}"
```

### Enum Validation
```python
valid_industries = ['healthcare', 'finance', 'telco', 'tech', 'retail', 'all']
assert client_intake['industry'] in valid_industries

valid_roles = ['hr', 'logistics', 'customer_service', 'admin', 'general']
assert client_intake['role'] in valid_roles
```

### Date Validation
```python
import datetime
date_obj = datetime.datetime.strptime(client_intake['audit_date'], '%Y-%m-%d')
assert date_obj <= datetime.datetime.now(), "Audit date cannot be in future"
```

---

## IntakeAgent Workflow

### Phase 1: Initial Questions
AI-dynamic questionnaire adapts based on responses:

```
Agent: "What industry does your chatbot operate in?"
User: "Healthcare"

Agent: "Since it's healthcare, does the chatbot handle patient data like appointment times or medical records?"
User: "Yes, appointment scheduling"

Agent: "What role does the chatbot serve? (HR, customer service, admin, etc.)"
User: "Customer service for patients"
```

### Phase 2: Document Extraction
If user uploads documents:

```
Agent: "I found a privacy policy. It states you process patient names, emails, and appointment times.
Is this accurate?"
User: "Yes, but we don't store medical records"

Agent: "Noted. I'll focus scenarios on appointment data, not medical records."
```

### Phase 3: Output Generation
Generate `client_intake.yaml`:

```yaml
chatbot_language: "RO"
industry: "healthcare"
role: "customer_service"
chatbot_scope: |
  Patient appointment scheduling chatbot.
  Handles inquiries about available slots, doctor specialties.
  Does NOT access medical records.
target_frameworks:
  - GDPR
company_name: "MedTech Solutions SRL"
audit_date: "2025-12-20"
national_law_applies: "RO"

# Derived
selected_scenarios:
  - GDPR-007  # Healthcare PII disclosure
  - GDPR-015  # DSAR handling
  - GDPR-023  # Authentication bypass
```

---

## Phase Roadmap

### Phase 0 (Current)
- Single framework (GDPR)
- Manual intake via IntakeAgent
- Output: `client_intake.yaml`

### Phase 1 (Future)
- Multi-framework intake (GDPR + ISO27001 + ISO42001)
- Self-service web form option
- CRM integration (HubSpot, Salesforce)

---

## References

- IntakeAgent implementation: `/projects/IntakeAgent/`
- Scenario selection logic: TBD (Phase 0 Week 3)
- Report configuration: `/projects/ReportGen/`

---

**Maintenance**: Update when intake questions change or new variables added