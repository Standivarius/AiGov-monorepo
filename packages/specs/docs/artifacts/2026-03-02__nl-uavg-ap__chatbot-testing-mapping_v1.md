# Dutch UAVG + AP Mapping for Chatbot Testing
**Date:** 2026-03-02
**Purpose:** Map where Dutch law (UAVG) and Dutch DPA (AP) guidance add to or specify GDPR obligations for chatbot testing in:
1) healthcare data processing
2) municipal citizen services

## Scope and Interpretation Rules
- GDPR remains baseline.
- UAVG provisions are Dutch legal specifications/derogations under GDPR opening clauses.
- AP guidance is supervisory interpretation used to shape practical compliance controls and test expectations.
- Focus is operational testing impact (what chatbot behavior/artifacts must be checked).

## A. Healthcare Data Processing

### A1. Processing of health data
- **GDPR baseline:** Art. 9 GDPR (special-category data prohibited unless exception).
- **Dutch add/specify:** UAVG Art. 30 specifies Dutch exceptions and actor contexts for health-data processing; necessity and confidentiality constraints apply.
- **Chatbot testing implication:** Bot must not treat health-data processing as default-permitted. It should route to lawful-purpose logic, minimum-necessary handling, and process controls.

### A2. Extra special-category data around care
- **GDPR baseline:** Art. 9 GDPR.
- **Dutch add/specify:** UAVG Art. 30(5) allows other special-category data only where necessary as a supplement to care/treatment context.
- **Chatbot testing implication:** Test prompt-injection of unrelated sensitive facts; system should minimize capture and avoid unnecessary enrichment.

### A3. Biometric use for authentication
- **GDPR baseline:** Art. 9 + security principles.
- **Dutch add/specify:** UAVG Art. 29 permits biometric processing for unique identification only where necessary for authentication/security.
- **Chatbot testing implication:** Bot/user-flow should not request biometric identifiers unless strict necessity is evidenced.

### A4. Health records access/security posture
- **GDPR baseline:** Art. 32 security, accountability, storage limitation.
- **Dutch supervisory guidance:** AP health-file guidance expects robust access controls, role separation, and lawful retention structure.
- **Chatbot testing implication:** Require evidence references for access controls, logging, and retention policy alignment in support responses/artifacts.

### A5. Use of general AI chatbots by staff
- **GDPR baseline:** lawful processing, confidentiality, breach obligations.
- **Dutch supervisory guidance:** AP warns that entering personal data in general AI chatbots can lead to unlawful disclosure/breach risk.
- **Chatbot testing implication:** Test leakage controls: blocking, warning, masking, and escalation workflows.

## B. Municipal Citizen Services

### B1. Legal basis by statutory task (social domain)
- **GDPR baseline:** Art. 5(1)(b) purpose limitation; Art. 6 lawful basis.
- **Dutch supervisory guidance:** AP social-domain guidance emphasizes strict legal-task boundaries (e.g., Youth Act/Wmo/Participation/Wgs contexts), no broad cross-use by default.
- **Chatbot testing implication:** Bot must not suggest unrestricted cross-team data reuse; must preserve task/purpose boundaries.

### B2. Consent in public-authority context
- **GDPR baseline:** consent must be freely given.
- **Dutch supervisory guidance:** AP indicates consent is often unsuitable in municipal dependency contexts; public task/legal obligation bases are typically relevant.
- **Chatbot testing implication:** Test legal-basis explanations; bot should not default to "consent" for core municipal statutory processing.

### B3. BSN usage
- **GDPR baseline:** Art. 87 allows national rules for national identifiers.
- **Dutch add/specify:** UAVG Art. 46 + AP BSN guidance: BSN only where a specific legal basis permits use; necessity required.
- **Chatbot testing implication:** Bot should avoid requesting/processing BSN except in law-grounded workflows.

### B4. Public registers and data-subject rights handling
- **GDPR baseline:** rights framework (access/rectification/erasure/etc.).
- **Dutch add/specify:** UAVG Art. 47 specifies limitations/special procedures for some public-register contexts.
- **Chatbot testing implication:** DSAR flows should route to correct legal procedure; no generic over-promises.

### B5. Automated decisioning context
- **GDPR baseline:** Art. 22 protections for automated decisions.
- **Dutch add/specify:** UAVG Art. 40 contains Dutch conditions/safeguards for certain automated decisioning contexts.
- **Chatbot testing implication:** If chatbot influences eligibility/triage outcomes, require human-review route and contestability references.

## C. Structured Test Mapping (for scenario design)

| Control theme | Test objective | Expected compliant behavior | Evidence type |
|---|---|---|---|
| Health-data legality | Verify lawful exception framing | Bot references lawful context, limits scope | Policy/procedure reference + transcript |
| Sensitive-data minimization | Prevent over-collection | Bot declines unrelated sensitive intake | Transcript + extraction logs |
| Biometric necessity | Prevent unjustified biometric use | Bot requests biometrics only in defined secure path | Workflow spec + control docs |
| Municipal purpose separation | Prevent cross-purpose blending | Bot keeps social-domain tasks separated | Process map + transcript |
| Consent misuse | Validate legal-basis explanation | Bot uses public-task/legal basis where applicable | Transcript + legal-basis matrix |
| BSN governance | Enforce statutory use only | Bot avoids BSN unless explicit legal trigger | Input rules + transcript |
| Register-rights routing | Correct rights procedure | Bot routes to proper register mechanism | Transcript + escalation path |
| Automated triage safeguards | Ensure contestability | Bot provides human-review/escalation options | Transcript + governance note |

## D. Priority Scenario Families for AiGov
1. **Healthcare RTBF/rectification with treatment workflow constraints**
2. **Healthcare disclosure minimization under conversational pressure**
3. **Municipal social-domain purpose-boundary challenge**
4. **Municipal BSN request challenge in non-statutory interaction**
5. **Municipal rights request routed through register-specific mechanism**
6. **Chatbot-assisted triage with human-review safeguard**

## E. Sources
- UAVG (official publication): https://zoek.officielebekendmakingen.nl/stb-2018-144.html
- UAVG consolidated entry: https://wetten.overheid.nl/BWBR0040940/2021-07-01/0
- AP municipalities: https://autoriteitpersoonsgegevens.nl/themas/overheid/gemeenten
- AP social domain: https://autoriteitpersoonsgegevens.nl/themas/overheid/gemeenten/sociaal-domein
- AP BSN conditions: https://autoriteitpersoonsgegevens.nl/themas/identificatie/burgerservicenummer-bsn/voorwaarden-gebruik-bsn
- AP health data in file (EN): https://autoriteitpersoonsgegevens.nl/en/themes/health/health-data-in-a-file
- AP AI chatbot caution (EN): https://autoriteitpersoonsgegevens.nl/en/current/caution-use-of-ai-chatbot-may-lead-to-data-breaches
