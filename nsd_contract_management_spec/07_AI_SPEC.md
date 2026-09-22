# AI / Contract Intelligence Specification

## 1. AI objectives
The AI layer converts contracts from documents into structured, explainable, actionable business data.

## 2. AI provider abstraction
Implement a provider interface:
```python
class AIProvider:
    def extract(self, document, schema, context): ...
    def analyze(self, prompt, context): ...
    def embed(self, texts): ...
    def chat(self, messages, tools, context): ...
```
Providers can be configured per tenant/use case.

## 3. Extraction pipeline
```text
Upload
 ↓
File validation / malware scan
 ↓
Text extraction
 ↓
OCR if needed
 ↓
Layout/table extraction
 ↓
Segmentation
 ↓
Clause classification
 ↓
Structured extraction
 ↓
Evidence mapping
 ↓
Normalization
 ↓
Confidence scoring
 ↓
Human review when required
 ↓
Canonical contract update
```

## 4. Required extracted fields
- agreement number
- title
- parties
- legal entities
- party roles
- address
- country
- contact persons
- effective date
- execution date
- expiration date
- renewal date
- auto-renewal
- notice period
- notice deadline
- contract value
- currency
- payment terms
- payment frequency
- pricing table
- discounts
- price escalation
- liability cap
- indemnification
- termination rights
- termination for cause
- termination for convenience
- warranty
- SLA
- service credits
- penalties
- milestones
- deliverables
- IP ownership
- license terms
- confidentiality
- data processing
- security requirements
- audit rights
- insurance
- compliance
- governing law
- jurisdiction
- arbitration
- force majeure
- assignment
- change of control
- survival clauses
- obligations

## 5. Evidence model
Every extracted fact should link to:
- contract version
- page number
- section/clause where possible
- text snippet
- bounding box for OCR-derived evidence where supported
- extraction model
- confidence

AI responses shown to users should cite these evidence objects.

## 6. Risk engine
### Risk categories
- Commercial
- Financial
- Legal
- Liability
- Termination
- Payment
- Privacy
- Security
- IP
- SLA
- Compliance
- Insurance
- Jurisdiction
- Operational
- Renewal

### Risk evaluation
For each finding:
```text
severity
risk_score
clause_reference
evidence
why_it_matters
standard_position
fallback_position
recommended_action
required_approver
```

## 7. Playbook-aware review
A review must compare the document against:
1. preferred clause
2. acceptable fallback
3. prohibited position
4. approval threshold

## 8. AI redlining
Inputs:
- current version
- previous version
- playbook
- company policy

Outputs:
- changed text
- risk classification
- explanation
- suggested revision
- fallback option
- approval requirement

AI must not silently change a legal document. Suggestions require user application.

## 9. AI Contract Chat
Supported intents:
- search portfolio
- summarize contract
- compare contracts
- identify risks
- list obligations
- calculate notice deadline
- find similar contracts
- find non-standard terms
- explain clause
- identify missing clause
- produce renewal brief
- produce counterparty relationship brief
- identify revenue leakage opportunities

Every factual response should have source evidence references.

## 10. AI relationship intelligence
Generate a relationship profile across agreements and linked ERP/CRM data:
- all current/previous contracts
- amendments
- open obligations
- disputes
- spend/revenue
- performance
- renewal history
- negotiation patterns
- risk history
- outstanding issues

## 11. AI Agents
### Intake Agent
Transforms free text/email/form into structured Contract Request.

### Drafting Agent
Selects template and clause set, then generates draft metadata/content.

### Review Agent
Reviews document against playbook.

### Risk Agent
Creates risk findings.

### Negotiation Agent
Summarizes changes and proposes fallback positions.

### Approval Agent
Explains routing and identifies missing approvers.

### Obligation Agent
Extracts and maintains obligations.

### Renewal Agent
Creates renewal brief and actions.

### Compliance Agent
Maps clauses against configured policy framework.

### Performance Agent
Compares contractual terms with ERP/CRM data.

### Executive Agent
Answers cross-portfolio questions.

### Relationship Agent
Builds customer/supplier relationship briefs.

## 12. Agent tools
Agents may be granted tools such as:
- search_contracts
- get_contract
- compare_versions
- get_clause
- get_playbook
- create_review
- create_task
- create_obligation
- create_renewal
- draft_document
- send_for_approval
- create_signature_request
- query_erp_transaction
- query_crm_record
- create_report

High-impact tools must have explicit permission and optional human approval.

## 13. Agent governance
Every run stores:
- agent
- user/trigger
- tools available
- input references
- model
- prompt policy version
- tool calls
- proposed actions
- approvals
- executed actions
- result
- error

## 14. Custom Agent Studio
Admin can configure:
- Agent name
- purpose
- model
- system instructions
- allowed DocTypes
- allowed tools
- contract types
- trigger
- schedule
- human approval requirement
- output destination
- max action count
- budget/cost guardrail

## 15. MCP / external AI
Expose safe read/action tools through an MCP adapter layer, using the same permission and audit system as internal agents. Do not expose raw database access.

## 16. AI privacy
- Customer data must not be used for provider training by default unless tenant policy explicitly enables it.
- Secrets must never enter prompts.
- Logs should store metadata, not unnecessary full sensitive content.
- Tenant isolation is mandatory.
- Sensitive fields can be masked before external processing.
