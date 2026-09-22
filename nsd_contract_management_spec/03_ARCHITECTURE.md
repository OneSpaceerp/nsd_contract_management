# Technical Architecture

## 1. Architecture style
Use an application-domain architecture inside Frappe, not a separate microservice maze for core transactions.

```text
Browser / Desk / Portal / Mobile / External Systems
                     |
                 Frappe HTTP
                     |
           API / Service Layer
                     |
     +---------------+----------------+
     |               |                |
 Contract Domain  Workflow Domain  Integration Domain
     |               |                |
     +---------------+----------------+
                     |
             Frappe DocTypes / ORM
                     |
             MariaDB / Files / Redis
                     |
          Background Jobs / Scheduler
                     |
      AI Provider Adapter / eSignature
```

Frappe's DocType model should remain the source of truth for core transactional records. Frappe already provides CRUD REST endpoints and RPC methods; use app-owned whitelisted methods for higher-level actions. See official REST documentation: https://docs.frappe.io/framework/user/en/guides/integration/rest_api

## 2. Application package
```text
nsd_contract_management/
├── hooks.py
├── modules.txt
├── api/
├── config/
├── contract_management/
│   ├── doctype/
│   ├── services/
│   ├── workflows/
│   ├── integrations/
│   ├── ai/
│   ├── reports/
│   ├── utils/
│   └── tests/
├── public/
├── templates/
├── www/
└── fixtures/
```

Keep each domain's business logic in service modules, while DocType controllers enforce record-level invariants. Use hooks.py for scheduler, assets, document events, permission query conditions, and other framework extensions. Official hook reference: https://docs.frappe.io/framework/user/en/python-api/hooks

## 3. Main domain modules
1. `contracts`
2. `intake`
3. `templates`
4. `clauses`
5. `negotiation`
6. `approvals`
7. `signatures`
8. `obligations`
9. `renewals`
10. `performance`
11. `disputes`
12. `repository`
13. `ai`
14. `integrations`
15. `security`
16. `analytics`

## 4. Core DocTypes
### Master
- Contract
- Contract Type
- Contract Party
- Party Role
- Legal Entity
- Contract Classification
- Contract Version
- Contract Relationship
- Contract Tag
- Contract Request
- Contract Intake Question
- Contract Intake Answer

### Drafting
- Contract Template
- Template Clause
- Clause
- Clause Version
- Clause Playbook
- Clause Playbook Rule
- Contract Generation Job

### Review/negotiation
- Contract Review
- Review Assignment
- Negotiation Round
- Negotiation Issue
- Contract Redline
- Contract Comment
- External Review Session

### Approval
- Approval Matrix
- Approval Rule
- Contract Approval
- Contract Approval Step
- Approval Delegation

### Signature
- Signature Request
- Signature Request Signer
- Signature Event
- Signature Provider
- Signature Evidence
- Identity Verification Request
- Notary Request

### Post-signature
- Contract Obligation
- Obligation Evidence
- Obligation Event
- Contract Milestone
- Contract Renewal
- Renewal Notice
- Contract Amendment
- Contract Termination
- Contract Performance Metric
- Contract Performance Period
- Contract Claim / Dispute
- Contract Legal Hold

### AI
- AI Extraction Job
- AI Extracted Field
- AI Extracted Clause
- AI Risk Finding
- AI Review
- AI Agent
- AI Agent Run
- AI Agent Action
- AI Prompt Policy
- AI Model Provider
- AI Knowledge Chunk
- AI Evidence Reference
- AI Relationship Brief

### Integration/ops
- Contract Integration Mapping
- External System Connection
- Contract Webhook Event
- Contract Import Job
- Contract Export Job
- Contract Automation Rule
- Contract Notification Rule
- Contract Data Retention Policy

## 5. Service layer
Create explicit service classes/functions rather than putting all logic in controllers.

```text
contract_service.py
contract_version_service.py
intake_service.py
template_service.py
clause_service.py
workflow_service.py
approval_service.py
negotiation_service.py
signature_service.py
obligation_service.py
renewal_service.py
amendment_service.py
termination_service.py
performance_service.py
risk_service.py
search_service.py
ai_service.py
agent_service.py
integration_service.py
retention_service.py
```

## 6. AI architecture
Do not bind business objects directly to a single model vendor.

```text
AI Service
   |
Provider Adapter
   +-- OpenAI
   +-- Gemini
   +-- Anthropic
   +-- Azure OpenAI
   +-- Local / self-hosted
```

Every AI operation must return:
- provider
- model
- model version when supplied
- prompt policy/version
- input document(s)
- evidence references
- confidence
- structured output
- latency
- token/cost metadata when available
- reviewer/approval status when applicable

## 7. File architecture
Use Frappe File records and document attachments for primary document storage. Respect document permissions. For very large files, use an object-storage adapter while preserving a File record and signed access URL. Official attachment behavior: https://docs.frappe.io/framework/user/en/desk/attachments

## 8. Background jobs
Long-running OCR, AI extraction, bulk analysis, document rendering, imports, exports and integration syncs must be queued using Frappe background jobs rather than executed in request/response transactions. Official reference: https://docs.frappe.io/framework/user/en/api/background_jobs

Recommended queues:
- `short`: status updates, small rule evaluation
- `default`: ordinary AI and integration tasks
- `long`: OCR, large batch extraction, bulk imports/exports, re-indexing

## 9. Scheduler
Use `scheduler_events` for standard hourly/daily tasks. Use configurable Scheduled Job Type for tenant-configurable schedules. Frappe documents both approaches. https://docs.frappe.io/framework/user/en/python-api/hooks

Required jobs:
- renewal deadline scan
- obligation due scan
- overdue escalation
- approval SLA escalation
- signature reminder
- AI extraction retry
- failed integration retry
- retention/legal hold enforcement
- semantic index refresh
- AI usage aggregation

## 10. Realtime
Use Frappe realtime for progress indicators, review updates, approval state changes, signature status and background-job progress only. Avoid chatty events and permission leaks. https://docs.frappe.io/framework/user/en/api/realtime

## 11. Database rules
- Use standard Frappe ORM.
- Add indexes only after query patterns are known and justified.
- Avoid JSON blobs for fields that must be filtered/reportable.
- JSON may be used for provider-specific payloads, AI raw outputs and flexible metadata, but maintain normalized canonical fields.
- Avoid foreign-key assumptions outside Frappe's Link fields.
- Keep audit/history in dedicated DocTypes where business significance exists.

## 12. Upgrade safety
Never patch ERPNext/Frappe core code. Use:
- custom DocTypes
- hooks
- extend_doctype_class where appropriate
- custom permission types
- app-owned services
- fixtures
- custom scripts only where necessary

Frappe's customization hooks and v16 permission types are designed for this pattern. https://docs.frappe.io/framework/user/en/permission-types

## 13. Error handling
All service functions must:
- validate input
- raise meaningful Frappe exceptions
- never leave partially-created business state after a synchronous failure
- use transactions for multi-record critical transitions
- enqueue noncritical side effects after commit when appropriate
- log integration/AI failures without logging secrets or sensitive document content unnecessarily

## 14. Idempotency
External-facing actions must accept an idempotency key where repeated calls can create side effects.
Example keys:
- signature_request_id
- import_job_id
- webhook_event_id
- contract_action_request_id

## 15. Observability
Record:
- API error rates
- background job failures
- integration retry counts
- AI latency/error/cost
- OCR failures
- eSignature failures
- contract transition anomalies
- renewal processing failures

## 16. Performance targets
Baseline target for production deployment:
- ordinary list views < 2.5s at p95 for indexed queries
- ordinary form save < 2.0s at p95 excluding external provider calls
- AI/OCR always asynchronous when > a few seconds
- no synchronous request should wait on an external AI provider for an interactive list page
- bulk jobs must expose progress and retry state
