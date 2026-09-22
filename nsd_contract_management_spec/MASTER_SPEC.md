# NSD Contract Management & Contract Intelligence — MASTER BUILD SPEC

This is the consolidated source-of-truth specification for the ERPNext v16 custom application `nsd_contract_management`.


---

## SOURCE FILE: 00_MASTER_README.md

# NSD Contract Management & Contract Intelligence — ERPNext v16 Custom App

## Purpose
Build a production-grade Contract Lifecycle Management (CLM) and Contract Intelligence application for ERPNext v16 / Frappe Framework v16.

The application is intended to exceed the baseline feature set of Zoho Contracts and combine advanced capabilities observed across modern enterprise CLM / Intelligent Agreement Management platforms: lifecycle management, workflow, negotiation, eSignature, obligations, performance/value realization, AI review/redlining/extraction, contract knowledge graph, configurable automation, enterprise integrations, security, and AI-agent orchestration.

## Target application
- App name: `nsd_contract_management`
- Python package: `nsd_contract_management`
- Display name: `NSD Contract Management`
- Target: ERPNext v16 / Frappe Framework v16
- Database: use Frappe-supported site database only; do not introduce a second transactional database for core CLM records.
- UI: native Frappe Desk first; custom Vue/React-like SPA only where a specialized workspace is required, and package it as a Frappe asset rather than bypassing the framework.

## Non-negotiable principles
1. Upgrade-safe: do not modify ERPNext/Frappe core files.
2. Standard DocTypes for domain entities, Child Tables for line-level structures, Single DocTypes for singleton configuration.
3. Use native Frappe permissions plus v16 Custom Permission Types for action-level controls.
4. Use standard Workflow where appropriate; implement complex dynamic routing in an app-owned workflow service that persists decisions in auditable DocTypes.
5. All AI outputs must be traceable to source evidence and model metadata.
6. High-impact AI actions require human approval unless a tenant policy explicitly permits automation.
7. All dates/times that drive notice, renewal, and obligation deadlines must be timezone-aware.
8. Files must use Frappe File/attachment mechanisms and preserve document-level permissions.
9. APIs must be idempotent where they create business objects or trigger external side effects.
10. Tests are required for every domain service, critical workflow, permission boundary, and API contract.

## Specification set
| File | Purpose |
|---|---|
| `01_PRD.md` | Complete product requirements and business scope |
| `02_FEATURE_MATRIX.md` | Feature-by-feature scope, priority, and acceptance criteria |
| `03_ARCHITECTURE.md` | Technical architecture and Frappe v16 implementation rules |
| `04_DOCTYPES_ERD.md` | Domain model, ERD, relationships, naming, lifecycle |
| `05_DOCTYPE_FIELD_SPEC.md` | Field-level data dictionary for core DocTypes |
| `06_WORKFLOWS_AND_AUTOMATIONS.md` | Workflow, rules, scheduler, escalation, automation |
| `07_AI_SPEC.md` | AI extraction, review, risk, agents, knowledge graph, governance |
| `08_API_SPEC.md` | REST v2 / RPC contracts, webhooks and idempotency |
| `09_PERMISSIONS_SECURITY.md` | Roles, permission matrix, security and compliance |
| `10_UI_UX_SPEC.md` | Desk workspace, forms, workspaces, portals, interaction rules |
| `11_INTEGRATIONS.md` | ERPNext, CRM, email, Microsoft 365, eSignature, external AI/MCP |
| `12_REPORTS.md` | Reports, dashboards, KPIs and analytics |
| `13_TESTING_QA.md` | Unit/integration/E2E/security/performance acceptance tests |
| `14_DEPLOYMENT.md` | Install, migration, CI/CD, observability, backups |
| `15_BUILD_ROADMAP.md` | Implementation phases and Definition of Done |
| `16_ANTIGRAVITY_BUILD_PROMPT.md` | Master prompt for Google Antigravity coding agent |
| `17_ERPNext_INTEGRATION_MATRIX.md` | Deep ERPNext v16 integration matrix and transaction rules |
| `erd.mmd` | Standalone Mermaid ERD source |

## Recommended implementation order
1. App skeleton and domains
2. Parties / Contract Type / Templates / Clauses
3. Contract Request + Contract + versioning + files
4. Workflow / approvals / permissions
5. Negotiation + external review
6. eSignature adapters
7. Obligations + renewals + notices
8. AI extraction + review + risk
9. Performance / ERP linkage / leakage
10. AI Agents / knowledge graph / MCP
11. Portals / mobile-ready APIs / integrations
12. ERPNext transaction integration hardening and end-to-end financial testing
13. Analytics / hardening / enterprise packaging

## Official Frappe references used by this specification
- DocTypes: https://docs.frappe.io/erpnext/doctype
- DocType fundamentals: https://docs.frappe.io/framework/user/en/basics/doctypes
- Permissions: https://docs.frappe.io/framework/user/en/basics/users-and-permissions
- v16 Custom Permission Types: https://docs.frappe.io/framework/user/en/permission-types
- REST API v1/v2: https://docs.frappe.io/framework/user/en/guides/integration/rest_api
- REST API reference: https://docs.frappe.io/framework/user/en/api/rest
- Hooks and scheduler: https://docs.frappe.io/framework/user/en/python-api/hooks
- Background jobs: https://docs.frappe.io/framework/user/en/api/background_jobs
- Notifications: https://docs.frappe.io/framework/notifications
- Workflow: https://docs.frappe.io/erpnext/workflows
- v16 Workflow Transition Tasks: https://docs.frappe.io/erpnext/workflow-transition-tasks
- Attachments: https://docs.frappe.io/framework/user/en/desk/attachments
- Field types: https://docs.frappe.io/framework/user/en/basics/doctypes/fieldtypes
- Custom app structure: https://github.com/frappe/frappe_docker/blob/main/docs/09-concepts/01-custom-app.md

The official docs confirm that DocTypes are Frappe's core data model, Frappe provides REST v2, background jobs, scheduler hooks, standard workflows, document attachments, and v16 Custom Permission Types. Use these framework primitives rather than duplicating them in the app. 


---

## SOURCE FILE: 01_PRD.md

# Product Requirements Document (PRD)
# NSD Contract Management & Contract Intelligence

## 1. Product vision
Create an enterprise Contract Operating System inside ERPNext that manages a contract from intake to drafting, review, negotiation, approval, signature, execution, obligations, performance, renewal/amendment/termination, dispute handling, and archival — while turning unstructured agreements into structured, queryable, explainable business intelligence.

## 2. Problem statement
Organizations commonly manage contracts across Word files, PDFs, email threads, spreadsheets, CRM, procurement, ERP, shared drives, and eSignature platforms. The result is slow legal review, poor visibility into obligations, missed notice dates, non-standard clauses, revenue/cost leakage, and weak auditability.

The app centralizes the lifecycle and connects contract language to execution data.

## 3. Goals
- Single source of truth for agreements and related data.
- Reduce contract cycle time.
- Detect risk and non-standard terms earlier.
- Automate approvals and deadline management.
- Convert contractual obligations into owned, trackable work.
- Measure contract performance and value realization.
- Enable natural-language contract intelligence.
- Support AI agents with strong governance.
- Integrate with ERPNext and external enterprise platforms.
- Support multiple companies, jurisdictions, languages, currencies and time zones.
- Provide a foundation for future SaaS / multi-tenant deployment.

## 4. Non-goals for the first production release
- Replace a full ERP/accounting system.
- Build a proprietary cryptographic eSignature scheme.
- Build a general-purpose BPM suite unrelated to contracts.
- Replace Word as the primary legal drafting editor.
- Automatically provide legal advice or make binding legal decisions without human governance.

## 5. Personas
### Executive
Wants portfolio risk, value, renewals, exposure, performance and exceptions.

### Legal Counsel
Wants intake, playbooks, clauses, review, negotiation, approvals, evidence and auditability.

### Contract Manager
Owns lifecycle, metadata, obligations, renewals and operational follow-up.

### Sales User
Creates customer agreement requests, tracks negotiation/signature, and connects contracts to opportunities/orders.

### Procurement User
Manages supplier agreements, commercial terms, renewals and performance.

### Finance User
Sees value, spend, pricing, payment terms, rebates, penalties, credits and revenue leakage.

### Compliance User
Reviews regulatory/security/privacy terms and evidence.

### Counterparty
Reviews, comments, redlines, uploads evidence and signs through a secure external workspace.

### System Administrator
Configures types, templates, clauses, workflows, rules, permissions, integrations and AI policies.

## 6. Core lifecycle
```text
Request → Intake → AI Classification → Draft → Internal Review → Negotiation
→ Approval → Signature → Effective/Executed → Obligations → Performance
→ Renewal/Amendment/Termination → Archive/Retention
```

## 7. Functional domains
### 7.1 Contract Intake
- New contract request
- NDA request
- Supplier request
- Customer request
- SOW request
- Amendment request
- Renewal request
- Termination request
- Upload/import existing agreement
- Counterparty-initiated import
- API intake
- Email-to-contract
- Web form intake
- Dynamic conditional intake questions
- Intake validation and duplicate detection
- SLA and queue assignment

### 7.2 Contract authoring
- Template-driven generation
- DOCX generation
- PDF generation
- Dynamic fields
- Conditional clauses
- Repeating sections
- Schedules / appendices
- Clause library and fallback clauses
- Contract numbering
- Version control
- Draft comparison
- Source contract relation

### 7.3 Clause management
- Approved clause library
- Clause versions
- Clause categories
- Jurisdiction mapping
- Risk rating
- Preferred wording
- Fallback wording
- Prohibited wording
- Required approver
- Playbook position
- Applicable contract types
- Effective/retired dates
- Semantic matching

### 7.4 Review and negotiation
- Internal review workspace
- External counterparty workspace
- Track changes
- Comments and mentions
- Redline upload
- Side-by-side comparison
- Version history
- Negotiation rounds
- Negotiation summary
- AI deviation detection
- AI redline recommendations
- Approved fallback suggestions
- Negotiation issue register

### 7.5 Approval
- Serial approvals
- Parallel approvals
- Conditional approvals
- Value-based approval
- Risk-based approval
- Clause-deviation approval
- Country/legal-entity based approval
- Delegation
- Escalation
- SLA
- Approval groups
- Dynamic approver rules
- Transition tasks

### 7.6 eSignature
- Native eSignature adapter abstraction
- DocuSign adapter
- Adobe Sign adapter
- Zoho Sign adapter where licensed
- Signer order
- Parallel/serial signatures
- OTP / identity verification
- Signature reminders
- Certificate/audit evidence
- Wet/offline signature tracking
- Notary workflow extension

### 7.7 Obligation management
- Obligations extracted by AI or entered manually
- Owner
- Beneficiary
- Trigger
- Due date
- Recurrence
- SLA
- Evidence
- Completion
- Escalation
- Penalty / credit impact
- Linked task
- Linked contract clause

### 7.8 Renewal and notice management
- Expiration
- Renewal date
- Auto-renewal
- Notice period
- Last notice date
- Renewal decision
- Renewal pipeline
- Renewal brief
- Escalation
- Calendar

### 7.9 Amendment/termination
- Amendment generation
- Parent-child hierarchy
- Changed terms tracking
- Effective date
- Termination request
- Notice requirement
- Exit obligations
- Financial impact
- Data return
- Survival clauses

### 7.10 Contract performance
- Contracted value
- Actual value
- Spend
- Revenue
- Utilization
- SLA KPIs
- Penalties
- Credits
- Rebates
- Savings
- Supplier performance
- Customer performance
- Commitment utilization
- Revenue leakage detection

### 7.11 Disputes and claims
- Claim/dispute register
- Related contract/clause
- Amount
- Evidence
- Responsible legal owner
- Milestones
- Settlement
- Resolution
- Legal hold

### 7.12 Repository
- Metadata
- Full-text search
- Semantic search
- AI search
- Structured filtering
- Saved views
- Favorites
- Archives
- Bulk import
- Duplicate detection
- Relationship graph
- Document permissions
- Retention/legal hold

### 7.13 AI contract intelligence
- OCR
- PDF/DOCX/image extraction
- Arabic + English mixed-language understanding
- Table extraction
- Field extraction
- Clause extraction
- Obligation extraction
- Risk analysis
- Compliance analysis
- Redline analysis
- Summary
- Comparison
- Contract chat
- Portfolio Q&A
- Renewal brief
- Relationship brief
- Performance brief
- Explainability with source evidence

### 7.14 AI agents
- Intake Agent
- Drafting Agent
- Review Agent
- Risk Agent
- Negotiation Agent
- Approval Agent
- Obligation Agent
- Renewal Agent
- Compliance Agent
- Performance Agent
- Executive Agent
- Relationship Agent
- Custom Agent Studio
- Human-in-the-loop policies
- Action permissions
- Agent audit trail

### 7.15 Enterprise integrations
- ERPNext Customer/Supplier/Sales/Purchase/Opportunity/Quotation/Sales Order/Purchase Order/Project/Invoice
- CRM
- Microsoft 365 / Word / Outlook / Teams
- Google Workspace
- Salesforce
- HubSpot
- SAP
- Oracle
- Workday
- Procurement platforms
- eSignature providers
- Slack
- SMS/WhatsApp gateways
- External AI providers
- MCP gateway

## 8. Business rules
1. A Contract cannot reach `Executed` until all mandatory approvals are completed.
2. A Contract cannot become `Effective` unless signature/evidence requirements are satisfied or an authorized offline-signature path is selected.
3. A contract with `Auto Renewal = Yes` must have a computed notice deadline.
4. Notice deadline calculations must use the contract's jurisdiction/timezone policy.
5. Non-standard clauses must be compared against the configured playbook.
6. Critical risk findings must create a review or approval requirement according to policy.
7. AI extracted data must store source evidence and confidence.
8. AI cannot delete/terminate/approve/sign/create external financial commitments without the required permission or configured approval policy.
9. Every external side effect must be idempotent.
10. Superseded versions are immutable except through controlled amendment/versioning actions.
11. Documents under legal hold cannot be deleted or purged by ordinary users.
12. Access to contracts must respect entity, company, department, role, and document-level rules.

## 9. Contract lifecycle statuses
`Draft`, `Intake`, `In Review`, `Legal Review`, `Commercial Review`, `Negotiation`, `Approval Pending`, `Approved`, `Signature Pending`, `Executed`, `Effective`, `On Hold`, `Expiring`, `Renewal In Progress`, `Amendment In Progress`, `Terminated`, `Expired`, `Archived`, `Rejected`, `Cancelled`.

## 10. KPIs
- Request-to-draft time
- Draft-to-approval time
- Approval cycle time
- Negotiation cycle time
- Number of negotiation rounds
- Signature cycle time
- End-to-end cycle time
- % contracts on standard template
- % non-standard clauses
- High-risk contract count
- Obligation completion rate
- Overdue obligations
- Renewal completion rate
- Missed notice count
- Contracted value
- Realized value
- Savings
- Revenue leakage detected/recovered
- SLA breaches
- AI extraction confidence
- AI review acceptance rate

## 11. MVP vs Phase 2
### MVP
Repository, Contract, Contract Request, Contract Type, Template, Clause, Contract Version, Approval Matrix, Workflow integration, Negotiation, Signature adapter abstraction, Obligations, Renewals, Roles/permissions, Audit, baseline AI extraction/review/risk, reports, ERPNext integration.

### Phase 2
Knowledge graph, performance/value realization, leakage engine, custom agent studio, MCP, advanced portals, electronic notarization, relationship intelligence, advanced external integrations.

## 12. Acceptance criteria
A production build is acceptable only when:
- all mandatory DocTypes exist with fixtures and permissions;
- lifecycle state transitions are deterministic and auditable;
- permissions are enforced server-side;
- all critical APIs have automated tests;
- AI outputs include evidence and confidence;
- scheduled jobs cover renewal/notice/obligation processing;
- external webhooks are idempotent;
- migration/install/uninstall is documented and tested;
- no core Frappe/ERPNext source is modified;
- test site can be seeded with demo contracts and complete an end-to-end lifecycle.


## 13. ERPNext-first integration requirement

This application is incomplete unless it is deeply integrated with the relevant ERPNext transactional modules. The system must connect Contract lifecycle to native ERPNext CRM, Selling, Buying, Accounts, Payments, Projects, Support, Subscriptions, HR, Assets, Stock and other relevant modules.

The application must not merely store external document IDs. It must support governed creation of approved downstream transactions, bidirectional status synchronization, permission enforcement, transactional event handling, contractual-vs-actual financial analysis, and traceability from agreement terms to invoices, payments, projects, service activity, assets and HR records.

A dedicated integration matrix is maintained in `17_ERPNext_INTEGRATION_MATRIX.md` and is part of the build source of truth.


---

## SOURCE FILE: 02_FEATURE_MATRIX.md

# Feature Matrix

Priority: `P0` = mandatory foundation, `P1` = first production wave, `P2` = advanced enterprise, `P3` = future extension.

| Domain | Feature | Priority | Notes |
|---|---|---|---|
| Intake | Contract Request | P0 | Core intake object |
| Intake | Dynamic web intake forms | P1 | Conditional fields |
| Intake | Duplicate/related-contract detection | P1 | AI + deterministic matching |
| Lifecycle | Contract master | P0 | Main domain object |
| Lifecycle | Contract versions | P0 | Immutable superseded versions |
| Lifecycle | Contract hierarchy | P0 | MSA/SOW/amendment/order form |
| Templates | Template library | P0 | DOCX/Jinja-first |
| Templates | Conditional clauses | P1 | Rules-driven |
| Clauses | Clause library | P0 | Versioned |
| Clauses | Fallback / prohibited clauses | P1 | Playbook |
| Drafting | Document assembly | P1 | DOCX/PDF |
| Review | Internal review | P0 | Comments, assignments |
| Negotiation | Redline management | P0 | Upload + compare |
| Negotiation | AI redline | P1 | Recommendations + evidence |
| Approval | Multi-level approval | P0 | Frappe Workflow + app service |
| Approval | Dynamic routing | P1 | Rules engine |
| Approval | Custom v16 permission types | P0 | approve/download/execute |
| Signature | eSignature adapter | P0 | Provider-agnostic |
| Signature | Identity verification | P1 | Provider dependent |
| Signature | Notarization extension | P2 | External provider |
| Obligations | Obligation master | P0 | Linked to clause |
| Obligations | Evidence | P0 | Files/links |
| Renewal | Notice calculator | P0 | Timezone-aware |
| Renewal | Renewal workspace | P1 | AI renewal brief |
| Amendments | Amendment lifecycle | P0 | Parent/child |
| Termination | Termination lifecycle | P1 | Exit checklist |
| Performance | SLA/KPI | P1 | Contract performance |
| Performance | ERP transaction matching | P1 | PO/SO/invoice |
| Performance | Leakage detection | P2 | AI/rule based |
| Repository | Full text search | P0 | Frappe search baseline |
| Repository | Semantic/AI search | P1 | Embeddings/vector service abstraction |
| Repository | Saved views | P0 | User/team |
| Repository | Legal hold | P1 | Retention |
| AI | OCR | P1 | External/local provider adapter |
| AI | Field extraction | P1 | Evidence anchored |
| AI | Clause extraction | P1 | Evidence anchored |
| AI | Risk analysis | P1 | Playbook-aware |
| AI | Contract chat | P1 | Citation-based answers |
| AI | AI agents | P2 | Guardrailed |
| AI | Agent Studio | P2 | No-code agent definition |
| AI | Knowledge graph | P2 | Relationship intelligence |
| AI | MCP | P2 | External AI tools |
| Integrations | ERPNext core integration | P0 | Native ERPNext-first architecture |
| Integrations | CRM: Lead/Opportunity/Quotation/Communication | P0 | Bidirectional context + controlled actions |
| Integrations | Selling: Sales Order/Delivery Note/Sales Invoice | P0 | Full O2C linkage and performance |
| Integrations | Payments: Payment Request/Payment Entry/Dunning | P0 | Payment traceability + allocation |
| Integrations | Buying: RFQ/Supplier Quotation/Purchase Order | P0 | Full procure-to-pay context |
| Integrations | Purchase Receipt/Purchase Invoice | P0 | Supplier performance + cost leakage |
| Integrations | Accounts: Cost Center/Payment Terms/Tax/GL analytics | P0 | Native accounting source of truth |
| Integrations | Projects: Project/Task/Timesheet/Expense Claim | P0 | Obligation execution + cost |
| Integrations | Subscription / recurring billing | P1 | Contract-to-recurring-invoice |
| Integrations | Support: Issue/SLA/Maintenance/Warranty | P1 | Service contract execution |
| Integrations | HR/Frappe HR: Employee lifecycle | P1 | Employment/consulting contracts |
| Integrations | Asset management | P1 | Lease/AMC/warranty coverage |
| Integrations | Stock | P1 | Item/warehouse/serial/batch/fulfillment |
| Integrations | Manufacturing/Subcontracting | P2 | Contract-driven production |
| Integrations | Quality | P2 | Acceptance/quality obligations |
| Integrations | Microsoft 365 | P1 | Word/Outlook/Teams |
| Integrations | eSignature | P0 | Adapter layer |
| Integrations | CRM | P1 | Generic adapter + specific connectors |
| Security | RBAC | P0 | Frappe |
| Security | ABAC / business rules | P1 | App-owned restrictions |
| Security | Audit trail | P0 | Immutable business audit |
| Security | AI audit | P1 | Model/prompt/evidence |
| Reporting | Contract dashboard | P0 | KPIs |
| Reporting | Legal dashboard | P1 | SLA/risk |
| Reporting | Executive dashboard | P1 | Value/risk |
| Reporting | Leakage dashboard | P2 | Performance |
| Portals | Counterparty review portal | P1 | Secure tokenized access |
| Mobile | Mobile-ready REST | P1 | Frappe API |
| Admin | Configuration center | P0 | Types/templates/rules |
| Admin | Custom fields | P0 | Frappe Customize Form |
| Admin | Custom objects | P2 | App framework extension |


---

## SOURCE FILE: 03_ARCHITECTURE.md

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


---

## SOURCE FILE: 04_DOCTYPES_ERD.md

# DocTypes and ERD

## 1. Core entity model

### Contract
The central agreement record.

### Contract Version
Immutable business version of a contract document / terms snapshot.

### Contract Relationship
Generic relation between contracts: parent/child, amendment, renewal, SOW, order form, addendum, supersedes, related.

### Contract Party
Party participation in a contract, linked to ERPNext Customer, Supplier, Employee, Contact, or generic Organization/Person representation.

### Contract Obligation
Post-signature commitment tied to a clause or section.

### Contract Renewal
Renewal process for a contract.

### Contract Amendment
Change process linked to a parent contract.

### Contract Performance Metric
Defines what should be measured.

### Contract Performance Period
Stores actual vs target for a metric and contract period.

## 2. ERD (logical)
```text
Company ───────────────┐
Legal Entity ───────────┤
Customer ───────────────┤
Supplier ───────────────┤
Contact ────────────────┤
Employee/User ──────────┤
                        ▼
                   CONTRACT
                     │ 1
        ┌────────────┼───────────────────────────────┐
        │            │                               │
        ▼            ▼                               ▼
 CONTRACT VERSION  PARTY                         RELATIONSHIP
        │            │                               │
        │            └─────────────┐                 │
        │                          ▼                 │
        │                    Party Role              │
        ▼                                            │
 Contract File/Attachment                           │
                                                     │
      ┌──────────────────────────────────────────────┘
      │
      ├──── Clause / Clause Version
      │
      ├──── Contract Review ─── Review Assignment
      │
      ├──── Negotiation Round ─ Negotiation Issue
      │
      ├──── Approval ─ Approval Step
      │
      ├──── Signature Request ─ Signer ─ Signature Event
      │
      ├──── Obligation ─ Obligation Evidence ─ Obligation Event
      │
      ├──── Renewal ─ Renewal Notice
      │
      ├──── Amendment
      │
      ├──── Termination
      │
      ├──── Performance Metric ─ Performance Period
      │
      ├──── Dispute/Claim ─ Legal Hold
      │
      ├──── AI Review ─ Risk Finding
      │               └─ Extracted Field / Extracted Clause
      │
      └──── ERPNext transactions
             ├─ Lead / Opportunity / Communication
             ├─ Quotation
             ├─ Sales Order
             ├─ Delivery Note
             ├─ Sales Invoice
             ├─ Payment Request / Payment Entry / Dunning
             ├─ Material Request / RFQ / Supplier Quotation
             ├─ Purchase Order
             ├─ Purchase Receipt
             ├─ Purchase Invoice / Payment Entry
             ├─ Project / Task / Timesheet / Expense Claim
             ├─ Subscription / Subscription Plan
             ├─ Issue / SLA / Maintenance Visit / Warranty Claim
             ├─ Employee / Onboarding / Separation (Frappe HR)
             ├─ Asset
             ├─ Item / Price List / Warehouse / Serial / Batch
             ├─ Work Order / Production Plan (optional)
             └─ Quality Inspection / Non Conformance (optional)
```

## 3. Contract relationships
Supported relationship types:
- `Parent Agreement`
- `Child Agreement`
- `Amendment Of`
- `Renewal Of`
- `SOW Of`
- `Order Form Of`
- `Addendum Of`
- `Supersedes`
- `Related`
- `Settlement Of`
- `Termination Of`

## 4. Naming conventions
Suggested autoname patterns:
- Contract Request: `CTR-REQ-.YYYY.-.#####`
- Contract: `CTR-.YYYY.-.#####`
- Contract Version: `CTV-.YYYY.-.#####`
- Clause: `CLA-.#####`
- Obligation: `OBL-.YYYY.-.#####`
- Renewal: `REN-.YYYY.-.#####`
- Amendment: `AMD-.YYYY.-.#####`
- Signature Request: `SIG-.YYYY.-.#####`
- Negotiation Round: `NEG-.YYYY.-.#####`
- AI Review: `AIR-.YYYY.-.#####`

Use naming series configurable by Contract Type where needed.


## 7. ERPNext integration entities

The ERD intentionally does not reproduce ERPNext master data. Native ERPNext records are referenced by Link fields and `Contract ERP Reference` rows.

High-value relationship chains:

```text
Contract
  ├─ Customer -> Opportunity -> Quotation -> Sales Order
  │                                  └-> Delivery Note -> Sales Invoice -> Payment Entry
  │                                                        └-> Dunning
  ├─ Supplier -> RFQ -> Supplier Quotation -> Purchase Order
  │                                      └-> Purchase Receipt -> Purchase Invoice -> Payment Entry
  ├─ Contract -> Project -> Task -> Timesheet / Expense Claim
  ├─ Contract -> Subscription -> Recurring Sales/Purchase Invoice -> Payment Entry
  ├─ Contract -> Issue / Maintenance Visit / Warranty Claim
  ├─ Contract -> Employee / HR lifecycle records
  └─ Contract -> Asset
```

Where one financial transaction spans multiple contracts, use explicit Contract Allocation child tables rather than forcing a single ambiguous Contract link.

## 8. Status model
### Contract
`Draft → Intake → In Review → Negotiation → Approval Pending → Signature Pending → Executed → Effective`
with side states `Rejected`, `Cancelled`, `On Hold`, `Expiring`, `Renewal In Progress`, `Amendment In Progress`, `Terminated`, `Expired`, `Archived`.

## 9. Child tables
Recommended child DocTypes:
- Contract Party Row
- Contract Term Row
- Contract Clause Row
- Contract Approval Step Row
- Contract Signer Row
- Contract Obligation Row
- Contract Metric Row
- Contract ERP Reference Row
- Contract AI Evidence Row
- Contract Tag Row
- Template Variable Row
- Workflow Rule Condition Row

Use child tables for true one-to-many line data that should travel with the parent; use standalone DocTypes where the child has its own lifecycle.


---

## SOURCE FILE: 05_DOCTYPE_FIELD_SPEC.md

# Core DocType Field Specification

This is the implementation-level field contract for the core DocTypes. Add `owner`, `creation`, `modified`, `modified_by`, `docstatus`, and other standard Frappe fields automatically rather than duplicating them as custom fields.

## 1. Contract Type
| Field | Type | Required | Notes |
|---|---|---:|---|
| contract_type_name | Data | Yes | Unique |
| code | Data | Yes | Unique short code |
| active | Check | Yes | Default 1 |
| description | Small Text | No | |
| default_template | Link: Contract Template | No | |
| default_playbook | Link: Clause Playbook | No | |
| default_workflow | Link: Workflow | No | Optional |
| default_contract_duration_days | Int | No | |
| default_notice_days | Int | No | |
| requires_legal_review | Check | Yes | |
| requires_finance_review | Check | Yes | |
| requires_compliance_review | Check | Yes | |
| allowed_companies | Table | No | Child company list |
| allowed_countries | Small Text | No | JSON-like list or child table |

## 2. Contract
| Field | Type | Required | Notes |
|---|---|---:|---|
| title | Data | Yes | Human title |
| contract_type | Link: Contract Type | Yes | |
| company | Link: Company | Yes | ERPNext |
| legal_entity | Link: Legal Entity | Yes | Executing entity |
| contract_number | Data | Yes | Usually autoname |
| external_reference | Data | No | Counterparty ref |
| status | Select | Yes | Lifecycle status |
| sub_status | Data | No | Configurable |
| source | Select | Yes | Internal/Imported/Email/API/Web Form/Counterparty |
| business_owner | Link: User | Yes | Primary owner |
| legal_owner | Link: User | No | Legal owner |
| procurement_owner | Link: User | No | |
| sales_owner | Link: User | No | |
| counterparty_primary | Dynamic Link/Link design | Yes | Use party row as source of truth |
| effective_date | Date | No | |
| expiration_date | Date | No | |
| renewal_date | Date | No | Calculated where possible |
| auto_renewal | Check | Yes | |
| notice_period_days | Int | No | |
| notice_deadline | Date | No | Calculated |
| governing_law | Data | No | |
| jurisdiction | Data | No | |
| contract_timezone | Link: Timezone / Data | Yes | Default company timezone |
| language | Select | Yes | English/Arabic/Bilingual/Other |
| currency | Link: Currency | No | |
| contract_value | Currency | No | |
| contract_value_type | Select | No | Fixed/Recurring/Usage/Unknown |
| payment_terms | Data | No | Canonical summarized field |
| confidentiality | Select | No | Standard/Enhanced/Strict |
| risk_level | Select | No | Low/Medium/High/Critical |
| risk_score | Float | No | AI/rule score |
| compliance_score | Float | No | |
| performance_score | Float | No | |
| renewal_score | Float | No | |
| current_version | Link: Contract Version | No | |
| parent_contract | Link: Contract | No | |
| executed | Check | Yes | |
| executed_on | Datetime | No | |
| signed_document | Attach | No | Final executed document |
| archive_date | Date | No | |
| legal_hold | Check | Yes | |
| description | Text Editor | No | Executive summary |
| ai_summary | Long Text | No | Cached AI summary; never source of truth |
| ai_last_reviewed_on | Datetime | No | |

### Contract child tables
- Contract Party Row
- Contract Clause Row
- Contract Term Row
- Contract ERP Reference Row
- Contract Tag Row

## 3. Contract Party Row
| Field | Type |
|---|---|
| party_type | Select: Customer/Supplier/Company/Contact/Employee/Other |
| party | Dynamic Link or Link according to implementation |
| role | Link: Party Role |
| legal_name | Data |
| display_name | Data |
| registration_no | Data |
| tax_id | Data |
| country | Link: Country |
| email | Data |
| phone | Data |
| address | Small Text |
| authorized_signer | Data |
| signer_email | Data |
| primary | Check |

## 4. Contract Version
| Field | Type |
|---|---|
| contract | Link: Contract |
| version_no | Int |
| version_label | Data |
| version_status | Select: Draft/Negotiation/Approved/Executed/Superseded |
| source_type | Select: Generated/Uploaded/Amended/Imported |
| document_file | Attach |
| source_document | Attach |
| change_summary | Text Editor |
| hash_sha256 | Data |
| created_from_version | Link: Contract Version |
| created_by_user | Link: User |
| generated_on | Datetime |
| approved_on | Datetime |
| executed_on | Datetime |
| immutable | Check |

## 5. Clause
| Field | Type |
|---|---|
| clause_name | Data |
| clause_code | Data |
| clause_category | Link: Clause Category |
| active | Check |
| preferred_version | Link: Clause Version |
| risk_level | Select |
| mandatory | Check |
| prohibited | Check |
| applicable_contract_types | Table MultiSelect or child table |
| applicable_jurisdictions | Table MultiSelect or child table |
| owner | Link: User |
| notes | Small Text |

## 6. Clause Version
| Field | Type |
|---|---|
| clause | Link: Clause |
| version_no | Int |
| effective_from | Date |
| effective_to | Date |
| language | Select |
| text | Text Editor |
| fallback_text | Text Editor |
| prohibited_text | Text Editor |
| risk_explanation | Text Editor |
| approved_by | Link: User |
| approval_date | Date |
| status | Select: Draft/Approved/Retired |

## 7. Contract Review
| Field | Type |
|---|---|
| contract | Link: Contract |
| review_type | Select: Legal/Commercial/Finance/Compliance/Security/AI |
| status | Select: Pending/In Progress/Completed/Rejected |
| assigned_to | Link: User |
| due_date | Date |
| started_on | Datetime |
| completed_on | Datetime |
| decision | Select |
| comments | Text Editor |
| risk_score | Float |
| source_version | Link: Contract Version |

## 8. Negotiation Round
| Field | Type |
|---|---|
| contract | Link: Contract |
| round_no | Int |
| participant_type | Select: Internal/Counterparty |
| participant | Link: User or Contact |
| submitted_by | Data |
| submitted_on | Datetime |
| version_in | Link: Contract Version |
| version_out | Link: Contract Version |
| change_count | Int |
| issue_count | Int |
| ai_summary | Long Text |
| status | Select: Open/Resolved/Cancelled |

## 9. Negotiation Issue
| Field | Type |
|---|---|
| negotiation_round | Link: Negotiation Round |
| clause | Link: Clause |
| issue_type | Select: Liability/Payment/Termination/IP/Privacy/SLA/Other |
| severity | Select: Low/Medium/High/Critical |
| counterparty_position | Text Editor |
| company_position | Text Editor |
| fallback_position | Text Editor |
| recommended_action | Text Editor |
| requires_approval | Check |
| status | Select: Open/Accepted/Rejected/Resolved |

## 10. Approval Matrix
| Field | Type |
|---|---|
| name | Data |
| active | Check |
| contract_type | Link: Contract Type |
| company | Link: Company |
| conditions | JSON / child rules |
| fallback_approver_role | Link: Role |

## 11. Contract Approval
| Field | Type |
|---|---|
| contract | Link: Contract |
| matrix | Link: Approval Matrix |
| approval_status | Select: Pending/Approved/Rejected/Cancelled |
| current_step | Int |
| requested_on | Datetime |
| completed_on | Datetime |
| final_decision | Select |
| comments | Text Editor |

## 12. Contract Approval Step
| Field | Type |
|---|---|
| contract_approval | Link: Contract Approval |
| step_no | Int |
| approver_type | Select: User/Role/Department/Rule |
| approver | Link: User |
| approver_role | Link: Role |
| status | Select: Pending/Approved/Rejected/Skipped |
| due_date | Date |
| acted_on | Datetime |
| comments | Text Editor |

## 13. Signature Request
| Field | Type |
|---|---|
| contract | Link: Contract |
| provider | Link: Signature Provider |
| provider_request_id | Data |
| status | Select: Draft/Sent/Viewed/Partially Signed/Completed/Declined/Expired/Cancelled |
| signing_url | Data |
| sent_on | Datetime |
| completed_on | Datetime |
| expires_on | Datetime |
| identity_verification_required | Check |
| notary_required | Check |
| idempotency_key | Data |
| raw_provider_response | Code/JSON |

## 14. Signature Request Signer
| Field | Type |
|---|---|
| signature_request | Link: Signature Request |
| order_no | Int |
| signer_type | Select: Internal/Counterparty/Witness/Notary |
| contact | Link: Contact |
| user | Link: User |
| email | Data |
| phone | Data |
| authentication_method | Select: Email/OTP/SMS/Identity Provider |
| required | Check |
| status | Select: Pending/Sent/Viewed/Signed/Declined |
| signed_on | Datetime |

## 15. Contract Obligation
| Field | Type |
|---|---|
| contract | Link: Contract |
| clause | Link: Clause |
| obligation_type | Select |
| title | Data |
| description | Text Editor |
| obligated_party | Data |
| beneficiary_party | Data |
| owner | Link: User |
| department | Link: Department |
| start_date | Date |
| due_date | Date |
| recurrence | Select/Duration |
| trigger_type | Select: Date/Delivery/Event/Payment/Manual |
| priority | Select |
| status | Select: Open/In Progress/Completed/Overdue/Cancelled/Waived |
| evidence_required | Check |
| evidence_file | Attach |
| penalty_value | Currency |
| currency | Link: Currency |
| escalation_days | Int |
| source_evidence | Link: AI Evidence Reference |

## 16. Contract Renewal
| Field | Type |
|---|---|
| contract | Link: Contract |
| renewal_type | Select: Auto/Manual/Extension |
| current_expiration_date | Date |
| notice_period_days | Int |
| notice_deadline | Date |
| renewal_start_date | Date |
| renewal_end_date | Date |
| status | Select: Not Started/In Progress/Renewed/Not Renewed/Expired |
| owner | Link: User |
| decision | Select: Renew/Negotiate/Terminate/Undecided |
| renewal_value | Currency |
| ai_brief | Long Text |

## 17. Contract Amendment
| Field | Type |
|---|---|
| parent_contract | Link: Contract |
| amendment_contract | Link: Contract |
| amendment_no | Data |
| reason | Text Editor |
| effective_date | Date |
| change_summary | Text Editor |
| financial_impact | Currency |
| status | Select: Draft/Review/Approved/Signed/Effective/Cancelled |

## 18. Contract Performance Metric
| Field | Type |
|---|---|
| contract | Link: Contract |
| metric_name | Data |
| metric_type | Select: SLA/KPI/Financial/Volume/Quality/Compliance |
| target | Float |
| unit | Data |
| direction | Select: Higher Better/Lower Better/Range |
| source_type | Select: Manual/ERPNext/API/AI |
| source_reference | Data |
| owner | Link: User |
| active | Check |

## 19. Contract Performance Period
| Field | Type |
|---|---|
| metric | Link: Contract Performance Metric |
| period_start | Date |
| period_end | Date |
| target_value | Float |
| actual_value | Float |
| score | Float |
| status | Select: On Track/At Risk/Breached |
| evidence | Attach |
| notes | Text Editor |

## 20. AI Review
| Field | Type |
|---|---|
| contract | Link: Contract |
| contract_version | Link: Contract Version |
| provider | Link: AI Model Provider |
| model | Data |
| prompt_policy | Link: AI Prompt Policy |
| status | Select: Queued/Running/Completed/Failed/Needs Review |
| started_on | Datetime |
| completed_on | Datetime |
| confidence | Float |
| token_input | Int |
| token_output | Int |
| estimated_cost | Currency |
| summary | Long Text |
| raw_result | Code/JSON |

## 21. AI Extracted Field
| Field | Type |
|---|---|
| ai_review | Link: AI Review |
| field_name | Data |
| value_text | Long Text |
| value_number | Float |
| value_date | Date |
| value_boolean | Check |
| confidence | Float |
| page_number | Int |
| evidence_text | Long Text |
| bounding_box | JSON |
| normalized_value | Long Text |
| accepted | Check |
| accepted_by | Link: User |

## 22. AI Risk Finding
| Field | Type |
|---|---|
| ai_review | Link: AI Review |
| risk_category | Select |
| severity | Select: Low/Medium/High/Critical |
| score | Float |
| clause_reference | Data |
| evidence | Long Text |
| rationale | Long Text |
| standard_position | Long Text |
| recommended_action | Long Text |
| required_approval | Check |
| status | Select: Open/Acknowledged/Resolved/Waived |
| owner | Link: User |

## 23. AI Agent / AI Agent Run / AI Agent Action
### AI Agent
- name
- code
- description
- active
- agent_type
- allowed_tools
- system_policy
- model_provider
- model
- requires_human_approval
- max_actions_per_run
- allowed_contract_types
- allowed_roles

### AI Agent Run
- agent
- initiated_by
- trigger_type
- input_reference
- status
- started_on
- completed_on
- summary
- trace_id
- cost

### AI Agent Action
- agent_run
- action_type
- target_doctype
- target_name
- proposed_change
- action_status
- approved_by
- approved_on
- executed_on
- result
- error

## 24. Legal Hold
| Field | Type |
|---|---|
| contract | Link: Contract |
| hold_reason | Text Editor |
| issued_by | Link: User |
| issued_on | Datetime |
| release_on | Datetime |
| status | Select: Active/Released |
| scope_description | Long Text |


---

## SOURCE FILE: 06_WORKFLOWS_AND_AUTOMATIONS.md

# Workflows, Rules and Automations

## 1. Contract Request workflow
```text
Draft
 → Submitted
 → Intake Validation
 → Classified
 → Accepted / Rejected
 → Contract Created
```

Rules:
- Missing mandatory business data blocks submission.
- Duplicate/related contract check runs before contract creation.
- High-value/high-risk intake automatically routes to Legal/Finance.

## 2. Contract workflow
```text
Draft
 → Internal Review
 → Legal Review
 → Commercial Review (conditional)
 → Negotiation (optional)
 → Approval Pending
 → Approved
 → Signature Pending
 → Executed
 → Effective
```

Alternative outcomes: `Rejected`, `Cancelled`, `On Hold`.

## 3. Dynamic approval examples
```text
IF contract_value >= 1000000 → CFO
IF contract_value >= 5000000 → CEO / delegated executive role
IF risk_level = Critical → General Counsel
IF data_processing = Yes → Privacy/Compliance
IF governing_law requires local review → Local Legal Role
IF non_standard_clause_count > 0 → Legal approval
IF payment_terms > company_policy_days → Finance approval
IF liability_cap below standard → General Counsel
```

Implement conditions as data, not hard-coded if a rule can reasonably be configured.

## 4. Negotiation workflow
1. Send secure review session.
2. Counterparty uploads or edits version.
3. Create Negotiation Round.
4. Parse changes.
5. Compare clauses against playbook.
6. Create Negotiation Issues.
7. AI proposes response/fallback.
8. Human accepts/edits/rejects AI suggestions.
9. Create next version.
10. Close round when all issues are resolved or escalated.

## 5. Signature workflow
```text
Approved
 → Build Signature Packet
 → Send
 → Viewed
 → Signed / Declined
 → Completed
 → Store certificate/evidence
 → Mark Contract Executed
```

External provider events must be idempotent.

## 6. Obligation automation
Daily job:
- identify due in 90/60/30/14/7/1 days;
- notify owner;
- escalate according to policy;
- mark overdue;
- update contract health where configured;
- create tasks where evidence is required.

## 7. Renewal automation
Daily job:
- recalculate notice deadline;
- identify contracts approaching notice window;
- generate Renewal records if not present;
- generate renewal task;
- produce AI renewal brief asynchronously;
- escalate missed deadlines.

## 8. AI review automation
On Contract Version upload/import:
- create AI Review job if policy enabled;
- extract metadata;
- extract clauses;
- extract dates/financial terms;
- identify risk;
- create obligations;
- update Contract canonical fields only where confidence/policy allows;
- otherwise create review tasks.

## 9. Post-signature automation
On executed:
- set executed flag/date;
- create or update effective lifecycle;
- create obligations;
- schedule renewal/notice;
- synchronize CRM/ERP references;
- notify owner and finance;
- generate immutable executed version;
- index document for search.

## 10. Retention automation
Scheduled task:
- identify records past retention date;
- skip legal hold;
- require retention-release permission;
- archive or purge only according to tenant policy;
- record audit evidence.

## 11. Webhook processing
Inbound external event pattern:
1. Authenticate signature.
2. Save raw event metadata.
3. Check idempotency/event ID.
4. Process.
5. Mark processed.
6. Retry failures safely.

## 12. Workflow transition tasks
Frappe v16 supports workflow transition tasks including app-defined actions, server scripts and webhooks. Use them for small transition-side effects, while keeping important domain logic inside the app service layer. https://docs.frappe.io/erpnext/workflow-transition-tasks


---

## SOURCE FILE: 07_AI_SPEC.md

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


---

## SOURCE FILE: 08_API_SPEC.md

# API Specification

Frappe automatically exposes CRUD APIs for DocTypes and supports custom whitelisted methods. Use REST v2 for new integration contracts where possible, with app-owned RPC methods for domain actions. Official docs: https://docs.frappe.io/framework/user/en/guides/integration/rest_api

## 1. Base URL
`https://{site}/api/v2`

Standard Frappe document resources:
```text
GET    /api/v2/document/Contract
GET    /api/v2/document/Contract/{name}
POST   /api/v2/document/Contract
PATCH  /api/v2/document/Contract/{name}
DELETE /api/v2/document/Contract/{name}
```

## 2. Domain RPC endpoints
Expose app-owned methods under:
`/api/method/nsd_contract_management.api.<module>.<method>`

### Contract actions
```text
contract.create_from_request
contract.submit_for_review
contract.start_negotiation
contract.create_version
contract.mark_approved
contract.send_for_signature
contract.mark_executed
contract.activate
contract.put_on_hold
contract.resume
contract.terminate
contract.archive
```

### Review
```text
review.start
review.complete
review.request_changes
review.create_ai_review
```

### Negotiation
```text
negotiation.create_round
negotiation.import_redline
negotiation.analyze_changes
negotiation.accept_change
negotiation.reject_change
negotiation.resolve_issue
```

### Obligations
```text
obligation.complete
obligation.waive
obligation.reopen
obligation.add_evidence
```

### Renewals
```text
renewal.create
renewal.start
renewal.approve
renewal.mark_not_renewed
renewal.generate_brief
```

### AI
```text
ai.extract_contract
ai.review_contract
ai.compare_versions
ai.ask_contract
ai.ask_portfolio
ai.run_agent
ai.approve_agent_action
```

## 3. Idempotency
Mutation endpoints that create an external or financial side effect must accept:
`Idempotency-Key: <uuid>`

Persist the key, target action, result and timestamp. Repeating a valid identical request should return the previous result rather than duplicate work.

## 4. Webhooks
### Outbound
Events:
- contract.created
- contract.updated
- contract.status_changed
- contract.approved
- contract.executed
- contract.expiring
- contract.renewal_due
- obligation.due
- obligation.overdue
- signature.sent
- signature.completed
- ai.review.completed
- ai.risk.created

### Inbound
Provider adapters should expose a single signed webhook endpoint, then route internally.

```text
POST /api/method/nsd_contract_management.api.webhooks.receive
```

## 5. Example create contract request
```json
{
  "title": "Enterprise Services Agreement",
  "contract_type": "MSA",
  "company": "My Company",
  "legal_entity": "My Company LLC",
  "currency": "USD",
  "contract_value": 250000,
  "effective_date": "2026-10-01",
  "expiration_date": "2027-09-30",
  "auto_renewal": true,
  "notice_period_days": 60,
  "language": "Bilingual",
  "parties": [
    {
      "party_type": "Customer",
      "party": "CUST-0001",
      "role": "Customer"
    }
  ]
}
```

## 6. AI answer response
```json
{
  "answer": "The agreement allows termination for convenience with 60 days notice.",
  "confidence": 0.96,
  "evidence": [
    {
      "contract": "CTR-2026-00001",
      "version": "CTV-2026-00004",
      "page": 18,
      "clause": "Termination",
      "quote": "..."
    }
  ]
}
```

## 7. Error model
Use Frappe exceptions plus structured API messages where appropriate:
```json
{
  "error": {
    "code": "CONTRACT_APPROVAL_REQUIRED",
    "message": "The contract cannot be sent for signature until the Legal approval is completed.",
    "details": {
      "contract": "CTR-2026-00001",
      "missing_step": "Legal Review"
    }
  }
}
```

## 8. Authentication
Use Frappe's standard auth/session/token mechanisms for internal APIs; use OAuth/service accounts or signed tokens for controlled machine-to-machine integrations. Never embed privileged API secrets in client JavaScript.

## 9. Pagination/filtering
Support standard Frappe filters and pagination. Domain endpoints must document filter fields and maximum page sizes.

## 10. API versioning
Internal domain endpoints should be published under `/api/v1/...` and `/api/v2/...` when a breaking contract is introduced. Preserve backward compatibility for at least one documented deprecation window.

## 11. ERPNext integration endpoints

Domain actions must exist for controlled transaction integration:

```text
erp.get_related_transactions
erp.resolve_contract_context
erp.create_sales_order
erp.create_purchase_order
erp.create_project
erp.create_subscription
erp.create_payment_request
erp.sync_transaction
erp.sync_payment
erp.allocate_payment
erp.recalculate_contract_financials
erp.detect_leakage
erp.get_contract_statement
erp.get_contract_profitability
```

Read endpoints must enforce the underlying ERPNext document permissions.

Transaction-creation endpoints must require explicit permission and configuration flags.

## 12. ERPNext integration webhook events

Support controlled hooks for:

```text
selling.opportunity.submitted
selling.quotation.submitted
selling.sales_order.submitted
selling.delivery_note.submitted
selling.sales_invoice.submitted
accounts.payment_request.submitted
accounts.payment_entry.submitted
accounts.dunning.submitted
buying.purchase_order.submitted
buying.purchase_receipt.submitted
buying.purchase_invoice.submitted
projects.task.updated
projects.timesheet.submitted
projects.expense_claim.submitted
subscription.updated
support.issue.updated
support.maintenance_visit.submitted
support.warranty_claim.updated
assets.asset.updated
hr.employee_updated
```

## 13. ERPNext integration payload requirement

Every synchronization record must store:
- source_doctype
- source_name
- source_company
- source_status
- source_docstatus
- source_modified_on
- contract
- sync_direction
- sync_idempotency_key
- sync_hash
- last_success_on
- last_error


---

## SOURCE FILE: 09_PERMISSIONS_SECURITY.md

# Permissions, Security and Compliance

## 1. Roles
### System/Platform
- Contract System Manager
- Contract System Administrator

### Business
- Contract Requester
- Contract Manager
- Contract Owner
- Legal Counsel
- Legal Manager
- Procurement User
- Procurement Manager
- Sales User
- Sales Manager
- Finance User
- Finance Manager
- Compliance User
- Compliance Manager
- Executive Viewer

### AI
- AI Administrator
- AI Reviewer
- AI Agent Operator

### External
- Counterparty Reviewer
- Counterparty Signer

## 2. Permission strategy
Use standard Frappe DocType permissions for base CRUD and v16 Custom Permission Types for action-level operations such as:
- approve_contract
- reject_contract
- send_for_signature
- execute_contract
- download_contract
- export_contract_data
- release_legal_hold
- run_ai_review
- run_ai_agent
- execute_ai_action
- manage_playbook
- manage_clause
- manage_workflow

Frappe v16 explicitly supports custom permission types beyond read/write/create/delete/submit. https://docs.frappe.io/framework/user/en/permission-types

## 3. Data scope
A user may be restricted by:
- Company
- Legal Entity
- Department
- Territory
- Contract Type
- Contract Owner
- Role
- User Permission records
- Document-specific sharing

## 4. Server-side enforcement
Never rely only on UI hiding. Every sensitive operation must re-check permissions server-side.

## 5. Document access
Attachments inherit document read permission in Frappe. Keep executed documents private unless a controlled portal/signature path explicitly creates a secure external access mechanism. https://docs.frappe.io/framework/user/en/desk/attachments

## 6. External review security
Counterparty sessions should use:
- random high-entropy token
- expiration
- one-time or scoped access
- optional password/OTP
- IP/device audit where allowed
- contract/session scope
- minimal permissions
- no broad Desk access

## 7. AI security
- tenant isolation
- prompt policy control
- provider allowlist
- secret redaction
- PII handling
- source evidence
- human approval for sensitive actions
- model/action audit

## 8. Audit trail
Business audit events should record:
- actor
- timestamp
- event
- target doctype/name
- previous value summary
- new value summary
- IP/session metadata where permitted
- source (UI/API/AI/scheduler)
- correlation ID

## 9. Encryption
Use HTTPS/TLS for all network traffic. Protect secrets using site/app secret mechanisms and deployment secret management. Do not place credentials in source code or fixtures.

## 10. Retention and legal hold
Retention policies cannot purge documents under active legal hold. Legal hold release requires authorized role and is itself auditable.

## 11. Data export/deletion
Support controlled export and privacy requests where applicable, but never allow ordinary users to bypass legal hold, records retention, or system security controls.

## 12. Threat model priorities
- Unauthorized contract download
- Broken object-level authorization
- Token/session replay
- Webhook spoofing
- AI prompt injection through documents
- Data exfiltration via AI tools
- Duplicate signature requests
- Duplicate ERP synchronization
- Privilege escalation through workflow transitions
- Malicious macro/attachment files
- Leakage through logs

## 13. Prompt injection defense
Treat contract content as untrusted data. AI extraction/review must not allow text inside a contract to redefine system instructions, grant tools, or bypass policy.


---

## SOURCE FILE: 10_UI_UX_SPEC.md

# UI / UX Specification

## 1. Desk workspace
Workspace name: `Contract Management`

Sections:
- My Work
- Contracts
- Requests
- Reviews
- Negotiations
- Approvals
- Signatures
- Obligations
- Renewals
- Amendments
- Performance
- Disputes
- AI Intelligence
- Reports
- Administration

## 2. Dashboard
Cards:
- My pending approvals
- My reviews
- Expiring in 30/60/90 days
- Overdue obligations
- Signature pending
- High-risk contracts
- Renewal pipeline
- Contract value
- Leakage detected
- Open disputes

Charts:
- contract lifecycle funnel
- cycle time trend
- risk distribution
- renewal timeline
- obligation completion
- contract value by type/company

## 3. Contract form
Header:
- Contract number
- Title
- Status
- Risk
- Value
- Owner
- Counterparty
- Effective/Expiration
- Renewal/Notice

Tabs:
1. Overview
2. Parties
3. Terms
4. Clauses
5. Documents
6. Versions
7. Reviews
8. Negotiation
9. Approvals
10. Signature
11. Obligations
12. Renewals
13. Amendments
14. Performance
15. ERP/CRM Links
16. AI Insights
17. Timeline

## 4. AI Insights panel
Show:
- summary
- risk score
- critical findings
- extracted terms
- missing clauses
- deviations
- obligations
- suggested actions
- evidence links

Never display an AI score without a way to inspect underlying findings/evidence.

## 5. Contract workspace
Provide a split view:
```text
Left: document/version
Middle: contract metadata/issues
Right: AI insights / tasks / comments
```

## 6. Negotiation workspace
- version selector
- side-by-side diff
- redline view
- comment thread
- issue panel
- playbook comparison
- AI recommendation panel
- resolve/accept/reject controls

## 7. Renewal workspace
Display:
- expiration date
- notice deadline
- renewal decision
- current commercial terms
- previous terms
- performance summary
- open obligations
- disputes
- AI renewal brief
- next actions

## 8. Obligation workspace
List/group by:
- due today
- due this week
- overdue
- owner
- contract
- priority
- status

## 9. Executive portfolio
Use a clean summary interface with drill-down. No destructive actions from summary cards.

## 10. Counterparty portal
Pages:
- Welcome / verification
- Agreements
- Current review
- Documents
- Comments
- Signatures
- Tasks
- Support

The portal must not expose unrelated tenant data.

## 11. Mobile requirements
All critical read/action APIs must work from mobile clients even if the first delivery is Desk-first. Prioritize:
- approvals
- contract search
- obligations
- renewal deadlines
- signature status
- AI assistant

## 12. UX rules
- Every status-changing button must explain prerequisites if blocked.
- Never hide failed background jobs; show retry state.
- Every AI action must show whether it is suggestion-only or executable.
- Use consistent lifecycle color semantics, but do not rely on color alone for status.
- Preserve Frappe accessibility and keyboard interaction patterns.


---

## SOURCE FILE: 11_INTEGRATIONS.md

# Integration Specification

## 1. ERPNext native integration
Use native Link fields where practical.

### Customer
Contract parties can reference Customer.

### Supplier
Contract parties can reference Supplier.

### Contact / Address
Use native ERPNext records for party contact data.

### Opportunity / Quotation / Sales Order
Link commercial/customer agreements to sales transactions.

### Purchase Order
Link supplier contracts to procurement.

### Sales Invoice / Purchase Invoice
Use for performance/value/leakage analysis.

### Project / Task
Map SOW milestones and obligations.

## 2. CRM adapters
Provide generic integration interfaces with initial adapters for common CRMs.

Interface methods:
```text
find_party
get_opportunity
get_account
push_contract_status
push_contract_value
push_renewal
```

## 3. Microsoft 365
### Word
- open/edit contract
- generate document
- import revised document
- synchronize version metadata

### Outlook
- email-to-contract
- attach email evidence
- link message thread
- initiate intake from email

### Teams
- notifications
- approval cards
- contract links

## 4. Google Workspace
- Drive document import
- Gmail intake
- Calendar deadline synchronization (optional)

## 5. eSignature providers
Adapter interface:
```python
class SignatureProvider:
    def create_request(self, packet, signers): ...
    def send(self, request): ...
    def get_status(self, provider_request_id): ...
    def cancel(self, provider_request_id): ...
    def download_evidence(self, provider_request_id): ...
    def parse_webhook(self, payload): ...
```

## 6. External AI providers
Same adapter architecture as AI specification.

## 7. MCP gateway
Expose safe business tools:
- search contracts
- get contract
- list obligations
- list renewals
- compare versions
- ask contract
- create review task
- prepare renewal brief

Write actions should be separately permissioned and audited.

## 8. Email
Email templates:
- new request
- review assignment
- approval request
- rejection
- signature request
- signature reminder
- obligation due
- obligation overdue
- renewal warning
- notice deadline

## 9. SMS / WhatsApp
Use provider adapter. Never place sensitive full contract text into a notification message by default.

## 10. Webhooks
Provide configurable outbound webhooks for lifecycle events, respecting Frappe's webhook pattern. See https://docs.frappe.io/framework/user/en/guides/integration/webhooks

## 11. Integration mapping
DocType: `Contract Integration Mapping`
Fields:
- contract
- system
- external_object_type
- external_object_id
- sync_direction
- status
- last_synced_on
- last_error
- checksum

## 12. Retry policy
- exponential backoff
- max retry count
- dead-letter/error state
- manual replay
- idempotency
- provider response logging without secrets


---

## SOURCE FILE: 12_REPORTS.md

# Reports, Dashboards and Analytics

## 1. Operational reports
- Contract Register
- Contracts by Status
- Contracts by Type
- Contracts by Company
- Contracts by Owner
- Pending Reviews
- Pending Approvals
- Signature Status
- Negotiation Aging
- Negotiation Issues
- Obligations Due
- Overdue Obligations
- Upcoming Renewals
- Missed Notice Deadlines
- Expired Contracts
- Terminated Contracts
- Active Legal Holds

## 2. Risk reports
- Contract Risk Register
- Critical Risk Findings
- High-risk contracts
- Non-standard Clauses
- Playbook Deviations
- Liability Exposure
- Termination Exposure
- Data Privacy Exceptions
- Compliance Exceptions

## 3. Commercial reports
- Contract Value by Period
- Contract Value by Customer
- Contract Value by Supplier
- Contracted vs Actual Spend
- Contracted vs Actual Revenue
- Savings
- Discounts
- Rebates
- Penalties
- Credits
- Revenue Leakage
- Realized vs Contracted Value

## 4. Lifecycle reports
- Request-to-Draft Cycle Time
- Draft-to-Approval Cycle Time
- Negotiation Cycle Time
- Signature Cycle Time
- End-to-End Cycle Time
- Contracts Completed within SLA

## 5. AI reports
- AI Reviews Completed
- AI Review Confidence
- Human Corrections
- AI Risk Findings
- AI Action Acceptance Rate
- AI Cost by Company
- AI Provider Performance
- Agent Runs
- Agent Failures
- Agent Actions requiring approval

## 6. Executive dashboard
- total active contract value
- renewals next 90 days
- critical/high risk exposure
- overdue obligations
- contract cycle time trend
- realized value
- leakage recovered
- disputes

## 7. Saved filters
Every report should expose reusable filters by:
- Company
- Legal Entity
- Contract Type
- Counterparty
- Owner
- Status
- Risk
- Date range
- Currency
- Country

## 8. Export
Allow controlled CSV/XLSX/PDF export according to permissions. Exporting contract data should have a distinct permission where appropriate.


---

## SOURCE FILE: 13_TESTING_QA.md

# Testing & Quality Assurance

## 1. Unit tests
Cover:
- date/notice calculations
- status transitions
- approval rules
- obligation recurrence
- risk scoring
- clause matching
- idempotency
- permission checks
- data normalization

## 2. Integration tests
- ERPNext Customer/Supplier linking
- eSignature provider adapter
- AI provider adapter
- webhook processing
- email intake
- document upload
- REST API

## 3. E2E scenario
Create a complete MSA:
1. Request
2. AI classification
3. Draft from template
4. Legal review
5. Commercial approval
6. Counterparty negotiation
7. Redline analysis
8. Final approval
9. Signature
10. Execution
11. Obligations
12. Renewal scheduling
13. Performance data
14. Renewal brief
15. Amendment

## 4. Security tests
- unauthorized read
- unauthorized download
- unauthorized action permission
- tenant/company data leakage
- token replay
- expired portal token
- webhook signature failure
- prompt injection document
- malicious attachment
- IDOR/BOLA checks

## 5. Performance tests
Data volumes to test:
- 100k contracts
- 500k contract versions
- 1M obligations
- 5M audit/events
- 10M AI evidence/chunks where supported by deployment architecture

Test indexed list filters, search, dashboard queries, background jobs and bulk imports.

## 6. AI evaluation
Create a golden dataset of representative contracts in English and Arabic, including:
- standard contracts
- scanned PDFs
- bilingual clauses
- poor OCR
- complex tables
- nested schedules
- intentionally risky clauses
- prompt injection content

Measure:
- extraction precision
- extraction recall
- risk classification accuracy
- evidence grounding
- hallucination rate
- confidence calibration
- human correction rate

## 7. Definition of Done for a feature
- code complete
- DocTypes/fixtures updated
- permissions tested
- server validation tested
- UI state tested
- API tested
- background jobs tested if applicable
- migration tested
- documentation updated
- no lint/type errors where configured
- no raw secrets

## 9. ERPNext Integration Test Matrix

### Selling
- Contract -> Sales Order -> Delivery Note -> Sales Invoice -> Payment Entry.
- Contract pricing vs invoiced pricing.
- Partial delivery/billing.
- Dunning on overdue linked invoice.

### Buying
- Contract -> Purchase Order -> Purchase Receipt -> Purchase Invoice -> Payment Entry.
- Contract rate vs supplier invoice rate.
- Partial receipt and billing.

### Projects
- Contract -> Project -> Task -> Timesheet/Expense Claim.
- Contract cost and profitability metrics.

### Subscription
- Contract -> Subscription -> recurring invoice -> payment.

### Support
- Contract -> Issue/SLA -> Maintenance Visit/Warranty Claim.
- SLA breach creates contractual obligation/risk finding according to policy.

### HR
- Employment Contract -> Employee.
- Onboarding/Separation obligations link to native HR tasks/projects.

### Assets
- Asset-linked maintenance/warranty contract.

### Security
- Underlying ERPNext permissions enforced on all linked documents.
- Company/User Permission restrictions cannot be bypassed through contract APIs.

### Idempotency
- Duplicate ERP event does not create duplicate Contract ERP Reference.
- Duplicate Payment Entry webhook/event does not double-count paid value.
- Retry after timeout returns prior success.


---

## SOURCE FILE: 14_DEPLOYMENT.md

# Deployment & Operations

## 1. Supported deployment model
Primary target: self-hosted ERPNext v16 bench/site.

## 2. Installation
```bash
bench get-app <git-url>
bench --site <site> install-app nsd_contract_management
bench --site <site> migrate
bench build --app nsd_contract_management
```

Use the exact app repository URL supplied by the implementation team; do not invent it in code.

## 3. Production prerequisites
- ERPNext/Frappe v16-compatible environment
- Redis
- workers
- scheduler
- Node build toolchain appropriate to the selected Frappe v16 patch release
- persistent file storage
- outbound HTTPS for external integrations
- optional object storage

## 4. Configuration
Use Site Config / app configuration for:
- AI providers
- eSignature provider credentials
- portal configuration
- webhook secrets
- external CRM/ERP credentials
- storage configuration
- default timezone
- rate limits

Never store credentials in Git.

## 5. Fixtures
Ship standard:
- Roles
- Role Profiles where required
- Contract Type demo/reference records only if explicitly marked as fixtures
- Clause categories
- standard workflow configuration
- custom permission types
- reports/workspaces where appropriate

## 6. Migration strategy
All schema changes must be deployable with `bench migrate`.
Never require manual database edits.

## 7. Backup
Ensure database and file backup coverage. Executed contracts and evidence are business-critical and must be included in disaster recovery planning.

## 8. Observability
Monitor:
- worker health
- scheduler health
- queue depth
- failed jobs
- API latency/errors
- AI provider latency/errors/cost
- storage failures
- webhook backlog

## 9. CI/CD
Pipeline stages:
1. lint
2. unit tests
3. build assets
4. migration test
5. integration tests
6. security checks
7. package/version
8. deploy to staging
9. smoke tests
10. production approval

## 10. Upgrade policy
Every supported ERPNext/Frappe version must have a compatibility matrix. Do not assume forward compatibility without tests.


---

## SOURCE FILE: 15_BUILD_ROADMAP.md

# Build Roadmap

## Phase 0 — Foundation
### Deliverables
- app skeleton
- module structure
- workspace
- roles
- permissions
- fixtures
- test infrastructure
- CI

### DoD
Fresh install on ERPNext v16 succeeds without manual DB changes.

## Phase 1 — Core CLM
- Contract Type
- Contract
- Contract Version
- Parties
- Relationship
- Repository
- Contract Request
- Templates
- Clauses
- basic workflow
- comments/files
- audit

## Phase 2 — Review / Negotiation / Approval
- reviews
- negotiation rounds/issues
- redline import
- version comparison
- approval matrix
- dynamic routing
- delegations
- SLAs

## Phase 3 — Signature / Post-signature
- signature adapters
- signer management
- obligations
- renewals
- amendments
- termination
- legal hold
- calendar/reminders

## Phase 4 — AI Foundation
- document ingestion
- OCR adapter
- extraction
- evidence
- clause detection
- risk findings
- AI summary
- contract chat

## Phase 5 — ERPNext Transaction Integration
- Sales and CRM transaction chain
- Buying and procurement chain
- Accounts and payment chain
- Project / Task / Timesheet / Expense integration
- Subscription integration
- Support / SLA / Maintenance / Warranty integration
- HR / Employee integration
- Asset integration
- Stock / Manufacturing / Quality adapters
- contract allocation for multi-contract payments
- financial leakage engine
- end-to-end transaction tests

## Phase 6 — Intelligence & Performance
- ERP transaction links
- performance metrics
- actual vs contractual
- leakage rules
- relationship brief
- renewal brief
- advanced dashboards

## Phase 7 — Agents / MCP
- agent framework
- tool registry
- human approval
- agent audit
- Agent Studio
- MCP adapter

## Phase 8 — Enterprise hardening
- external integrations
- portals
- identity verification
- notarization adapter
- advanced security
- load/performance hardening
- disaster recovery testing

## Release gates
### Alpha
Core lifecycle works on sample contracts.

### Beta
Security + integrations + AI extraction work and are tested.

### Production
All P0/P1 requirements, migrations, backup/restore, permissions and E2E lifecycle are verified.


---

## SOURCE FILE: 16_ANTIGRAVITY_BUILD_PROMPT.md

# Google Antigravity Master Build Prompt

You are the lead software architect and senior Frappe/ERPNext v16 engineer. Build a production-grade ERPNext v16 custom application named `nsd_contract_management` using the attached project specification files.

## Primary objective
Implement the complete NSD Contract Management & Contract Intelligence application described by:
- `00_MASTER_README.md`
- `01_PRD.md`
- `02_FEATURE_MATRIX.md`
- `03_ARCHITECTURE.md`
- `04_DOCTYPES_ERD.md`
- `05_DOCTYPE_FIELD_SPEC.md`
- `06_WORKFLOWS_AND_AUTOMATIONS.md`
- `07_AI_SPEC.md`
- `08_API_SPEC.md`
- `09_PERMISSIONS_SECURITY.md`
- `10_UI_UX_SPEC.md`
- `11_INTEGRATIONS.md`
- `12_REPORTS.md`
- `13_TESTING_QA.md`
- `14_DEPLOYMENT.md`
- `15_BUILD_ROADMAP.md`

Treat these files as the source of truth. When a detail conflicts, prefer the more specific implementation document, then record the conflict in `docs/DECISIONS.md` rather than silently inventing behavior.

## Critical engineering constraints
1. Target ERPNext/Frappe v16 only unless compatibility is explicitly added.
2. Do not modify Frappe/ERPNext core files.
3. Use standard Frappe DocTypes, child tables, links, hooks, workflows, background jobs, REST APIs and permissions.
4. Use v16 Custom Permission Types for action-specific permissions.
5. Keep all business logic in app-owned service modules.
6. Do not create a second transactional database.
7. Do not place secrets in source code.
8. All external side effects must be idempotent.
9. AI results must have evidence, confidence and model/policy metadata.
10. AI document content is untrusted input; defend against prompt injection.
11. High-impact AI actions require human approval unless an explicit tenant policy allows otherwise.
12. Keep executed contract versions immutable.
13. Honor legal holds and retention policies.
14. Make all renewal/notice calculations timezone-aware.
15. Use background jobs for OCR, AI, imports, bulk analysis and slow integrations.

## Build sequence
### Step 1 — Inspect environment
- Verify Frappe/ERPNext version.
- Verify bench/site.
- Verify developer mode.
- Verify Python/Node toolchain.
- Verify app installation path.
Do not change system versions unless explicitly required by the existing environment.

### Step 2 — Scaffold app
Create:
```text
nsd_contract_management/
  hooks.py
  modules.txt
  README.md
  setup.py / pyproject equivalent appropriate to Frappe v16
  nsd_contract_management/
    config/
    contracts/
    intake/
    templates/
    clauses/
    negotiation/
    approvals/
    signatures/
    obligations/
    renewals/
    performance/
    disputes/
    repository/
    ai/
    integrations/
    security/
    analytics/
    tests/
```

### Step 3 — Create DocTypes
Create all P0 DocTypes from `04_DOCTYPES_ERD.md` and field specs in `05_DOCTYPE_FIELD_SPEC.md`.
Use consistent naming, modules, permissions, descriptions and links.

### Step 4 — Fixtures and roles
Create all roles, custom permission types, workflows, standard configuration and safe fixtures.

### Step 5 — Implement Contract lifecycle
Implement deterministic service methods and status transition validation.

### Step 6 — Implement templates/clauses
Implement versioned templates, clauses, playbooks and fallback rules.

### Step 7 — Implement reviews/negotiation/approvals
Build review assignments, issue tracking, versions, comparisons and dynamic approval routing.

### Step 8 — Implement signatures
Build provider interface + mock provider first. Do not hard-wire to one vendor.

### Step 9 — Implement obligations/renewals/amendments
Build scheduler jobs, escalation and timezone-aware deadline engine.

### Step 10 — Implement AI foundation
Build provider adapters and deterministic schema validators before advanced prompts.
AI outputs must be structured and stored in AI DocTypes.

### Step 11 — Implement performance/intelligence
Link contracts to ERPNext transactions and calculate contractual-vs-actual metrics.

### Step 12 — Implement deep ERPNext integration
The application MUST be transactionally integrated with all relevant ERPNext modules described in `17_ERPNext_INTEGRATION_MATRIX.md`.

Mandatory integration chains to implement and test:
```text
CRM
Lead -> Opportunity -> Contract -> Quotation -> Sales Order

Selling
Sales Order -> Delivery Note -> Sales Invoice -> Payment Request -> Payment Entry -> Dunning

Buying
Contract -> Material Request/RFQ -> Supplier Quotation -> Purchase Order -> Purchase Receipt -> Purchase Invoice -> Payment Entry

Projects
Contract -> Project -> Task -> Timesheet / Expense Claim

Recurring
Contract -> Subscription -> recurring Invoice -> Payment Entry

Support
Contract -> Issue / SLA -> Maintenance Schedule/Visit / Warranty Claim

HR
Employment Contract -> Employee -> Onboarding/Separation tasks

Assets
Asset Contract -> Asset -> Maintenance/Warranty records
```

Rules:
- Reuse native ERPNext DocTypes and masters; do not duplicate Customer, Supplier, Employee, Item, Project, Asset, Invoice or Payment data.
- Source accounting truth remains native ERPNext transactions and General Ledger.
- Never write GL Entry, Stock Ledger Entry or payment records directly.
- Use app-owned service adapters and native document APIs.
- Install required Custom Field fixtures on relevant ERPNext DocTypes for Contract links.
- Support multi-contract financial allocations for Payment Entry and Journal Entry where a single source document spans multiple contracts.
- Process ERPNext document events idempotently and queue expensive metric calculations.
- Enforce underlying ERPNext permissions on all contract-linked transaction reads/writes.
- Implement contractual-vs-actual leakage detection for sales, procurement and payments.
- Implement automated end-to-end tests for every mandatory chain.

### Step 13 — Implement Agents
Build tool registry, agent runs/actions, approval gates and audit trail.

### Step 14 — Implement external interfaces
REST/RPC, webhooks, portal endpoints, MCP adapter and integration adapters.

### Step 15 — Test
Create fixtures and automated tests for every P0/P1 feature and critical permission boundary.

## Required code quality
- PEP8-compatible Python.
- Type hints where practical.
- Clear docstrings for public service functions.
- Avoid giant controller files.
- Centralize constants and policy names.
- Avoid magic strings where a configuration/enum is appropriate.
- Validate inputs server-side.
- Add transaction-safe patterns around state changes.
- Log useful errors, never credentials.

## Frappe conventions
Use:
- DocType controllers
- `frappe.get_doc`, `frappe.new_doc`, `frappe.db` through ORM/query builder
- whitelisted methods for domain actions
- `frappe.enqueue` for background processing
- `scheduler_events` for standard recurring checks
- hooks.py for app integration
- fixtures for shipped configuration

Do not bypass the ORM with raw SQL unless there is a documented performance reason and the query is safe/portable.

## Required services
Implement at minimum:
```text
contract_service
contract_version_service
intake_service
template_service
clause_service
playbook_service
review_service
negotiation_service
approval_service
signature_service
obligation_service
renewal_service
amendment_service
termination_service
performance_service
risk_service
search_service
ai_service
agent_service
integration_service
retention_service
```

## Required reports
Implement at minimum the reports listed in `12_REPORTS.md`, using Script Reports where complex logic is needed.

## Required API
Implement the API actions listed in `08_API_SPEC.md` with permission checks and idempotency.

## Required tests
At minimum:
- contract lifecycle happy path
- lifecycle invalid transition
- dynamic approval routing
- company-level access restriction
- legal hold deletion prevention
- renewal notice calculation
- obligation escalation
- version immutability
- signature webhook idempotency
- AI evidence storage
- prompt injection defense
- external token expiry
- unauthorized contract download

## UI expectations
The final app should look and behave like a professional ERPNext module, not a generic CRUD demo. Build usable workspaces, dashboards, forms, timelines, status indicators, related-document links and action buttons. Add custom pages only where native Desk cannot provide the intended experience.

## Demo data
Create a safe demo dataset with:
- 3 companies/legal entities
- 10 customers
- 10 suppliers
- 20 contracts of multiple types
- 10 clauses and versions
- 15 obligations
- 5 renewals
- 5 risk findings
- 5 AI-reviewed contract samples
Do not ship demo data as production fixtures unless explicitly marked.

## Documentation to generate
Create:
- `README.md`
- `docs/INSTALL.md`
- `docs/CONFIGURATION.md`
- `docs/ADMIN_GUIDE.md`
- `docs/API.md`
- `docs/AI_GOVERNANCE.md`
- `docs/INTEGRATIONS.md`
- `docs/DECISIONS.md`
- `docs/CHANGELOG.md`

## Final validation
Before declaring completion:
1. Run migrations on a clean test site.
2. Run unit tests.
3. Run integration tests.
4. Run all permission/security tests.
5. Confirm no core Frappe/ERPNext files were modified.
6. Confirm all DocTypes are loadable.
7. Confirm workspaces and role permissions.
8. Confirm background scheduler jobs.
9. Confirm API endpoint permissions.
10. Confirm install/uninstall behavior.
11. Produce a concise implementation report listing completed, partial and blocked requirements.

## Implementation style
Do not build placeholders disguised as complete functionality. When a real external provider is unavailable, build a clean adapter interface plus a working mock provider and mark the provider-specific portion as pending configuration. Core CLM behavior must still work end-to-end.

Start by inspecting the existing ERPNext v16 environment and repository, then scaffold the app and implement the foundation in the build sequence above.


---

## SOURCE FILE: 17_ERPNext_INTEGRATION_MATRIX.md

# ERPNext v16 Deep Integration Specification
# NSD Contract Management

## 1. Objective

The Contract Management application MUST be a first-class ERPNext v16 application, not an isolated CLM repository.

The Contract record remains the source of truth for contractual terms, obligations, negotiation history, approvals, risk, and lifecycle state. ERPNext remains the source of truth for operational and accounting transactions.

The application MUST:

- link contracts to native ERPNext transactions through real Link fields or controlled reference tables;
- reuse native ERPNext masters instead of duplicating Customer, Supplier, Employee, Item, Company, Project, Asset, etc.;
- create downstream ERPNext transactions through supported document APIs/services, never by inserting raw accounting rows;
- read actual financial/operational results from submitted ERPNext transactions;
- never copy or recreate General Ledger / Stock Ledger logic inside the custom app;
- support one contract linked to many ERPNext transactions and one ERPNext transaction linked to a contract when business context permits;
- support many-to-many financial allocation when one transaction genuinely spans several contracts;
- preserve ERPNext accounting, stock, tax, payment, and workflow rules;
- provide auditability for every contract-to-ERP relationship.

---

## 2. Mandatory ERPNext integration domains

### Tier 1 — Mandatory for production

1. Company / Accounting Dimensions
2. Customer / Contact / Address
3. Supplier / Contact / Address
4. CRM: Lead, Opportunity, Communication, ToDo
5. Selling: Quotation, Sales Order, Delivery Note, Sales Invoice, Payment Request, Payment Entry, Dunning
6. Buying: Material Request, Request for Quotation, Supplier Quotation, Purchase Order, Purchase Receipt, Purchase Invoice, Payment Request, Payment Entry
7. Accounts: Payment Terms, Payment Entry, Journal Entry / General Ledger reporting, Cost Center, Tax Templates, Payment Gateway references
8. Projects: Project, Task, Timesheet, Expense Claim
9. Subscription: Subscription Plan, Subscription
10. Support: Issue, Maintenance Schedule, Maintenance Visit, Warranty Claim, SLA
11. HR/Frappe HR when installed: Employee, Employee Onboarding, Employee Separation, Employee Transfer
12. Assets: Asset, Asset Category / maintenance-related records as applicable
13. Files / Attachments / Email / Communication
14. ERPNext Web Portal / Customer and Supplier portal where enabled

### Tier 2 — Conditional but fully supported adapters

15. Stock: Item, Item Price, Price List, Warehouse, Pick List, Serial No, Batch No
16. Manufacturing: Work Order, Production Plan, subcontracting-related documents where enabled
17. Quality: Quality Inspection, Non Conformance, corrective/preventive action where enabled
18. Maintenance and service operations
19. Inter-company transactions
20. External CRM / ERP / procurement systems

The application MUST not pretend that all customers use all modules. Integrations must be feature-detected/configurable while the core contract application remains installable without optional modules.

---

## 3. Contract-to-ERP reference model

### 3.1 Primary fields on Contract

The Contract DocType should contain these high-value native links where meaningful:

- Company
- Legal Entity / Company
- Customer
- Supplier
- Primary Contact
- Primary Address
- Opportunity
- Quotation
- Sales Order
- Purchase Order
- Project
- Cost Center
- Subscription
- Employee
- Asset

These are optional and mutually validated according to Contract Type.

### 3.2 Contract ERP Reference child table

Create child table `Contract ERP Reference` with:

| Field | Type | Purpose |
|---|---|---|
| reference_doctype | Link/Select | ERPNext DocType |
| reference_name | Dynamic Link | Linked document name |
| reference_role | Select | Source / Fulfillment / Billing / Payment / Cost / Revenue / Project / Support / Asset / HR / Other |
| direction | Select | Contract -> ERP / ERP -> Contract / Bidirectional |
| is_primary | Check | Primary reference for this type |
| amount | Currency | Relevant monetary amount |
| currency | Link Currency | Currency of amount |
| status | Data/Select | Last known source status |
| last_synced_on | Datetime | Synchronization timestamp |
| sync_hash | Data | Idempotency/change detection |
| notes | Small Text | Context |

Do not use Dynamic Link alone for high-volume reporting. For critical transaction types also create indexed explicit Link fields or derived reporting tables.

---

## 4. Selling integration

ERPNext standard sales flow is Quotation -> Sales Order -> Delivery Note -> Sales Invoice -> Payment Entry, with some valid alternate paths. The contract application must preserve these native flows. (ERPNext Sales Order and Sales Invoice documentation)

### 4.1 Lead

Use native `Lead`.

Integration:
- Contract Request may originate from a Lead.
- Contract may be associated with a Lead before Customer creation.
- AI intake may identify the Lead by email/domain/company.
- On Customer qualification, the Contract party relationship may be migrated from Lead context to Customer context while retaining the source Lead.

### 4.2 Opportunity

Use native `Opportunity`.

Required integration:
- Link Contract Request / Contract to Opportunity.
- Show related contracts on Opportunity.
- Push contract status/value back to Opportunity timeline/summary.
- Support Opportunity -> Contract Request action.
- Support Contract -> Opportunity navigation.
- Do not duplicate opportunity value/probability logic.

### 4.3 Quotation

Use native `Quotation`.

Supported flow:
```text
Opportunity
  -> Contract Request
  -> Contract / Commercial Schedule
  -> Quotation
```

Or:
```text
Opportunity
  -> Quotation
  -> Contract
```

Requirements:
- Link Quotation to Contract.
- Allow contract commercial terms to prefill Quotation terms when explicitly approved.
- Support contracted price lists, payment terms, taxes, discounts and validity dates without bypassing ERPNext pricing/tax validation.
- Track Quotation revisions against contract negotiation/version when applicable.

### 4.4 Sales Order

Use native `Sales Order`.

Contract actions:
- Create Sales Order from Contract where contract type permits.
- Create Contract from submitted Sales Order.
- Link all related Sales Orders.
- Map contract line items, service periods, quantities, rates, currencies, delivery dates and payment terms.
- Support partial orders from a framework agreement.
- Track Ordered vs Contracted Quantity / Value.

A Sales Order is an operational commitment and should drive downstream fulfillment rather than duplicating fulfillment logic inside the Contract app. (ERPNext Sales Order documentation)

### 4.5 Delivery Note

Use native `Delivery Note`.

Requirements:
- Link Delivery Note to Contract when originating from a contract-linked Sales Order.
- Track delivered quantity/value against contractual commitments.
- Use Contract Performance Metrics for delivery performance.
- Do not post stock movements from the Contract DocType directly.

ERPNext Delivery Notes update inventory and normally originate from submitted Sales Orders. (ERPNext Delivery Note documentation)

### 4.6 Sales Invoice

Use native `Sales Invoice`.

Requirements:
- Link invoice to Contract.
- Support invoice generation from contract-linked Sales Order or approved milestone.
- Capture contractual billing period, milestone, schedule, discount, price escalation and tax references.
- Compare contract rate vs invoiced rate.
- Compare contracted quantity vs invoiced quantity.
- Calculate billed/unbilled contract value.
- Detect revenue leakage and incorrect pricing.
- Support credit notes/returns through native ERPNext flows.
- Never write GL entries directly.

ERPNext Sales Invoice posting creates receivable, income and tax accounting entries; the CLM app must consume those results, not reproduce them. (ERPNext Sales Invoice documentation)

### 4.7 Payment Request

Use native `Payment Request` for contract-linked collection requests.

Supported flows:
- Contract milestone -> Sales Invoice -> Payment Request -> customer payment
- Sales Order advance -> Payment Request
- Renewal invoice -> Payment Request

The Contract app must track payment-request status without treating the request itself as payment. ERPNext explicitly separates payment requests from actual payment settlement. (ERPNext Payment Request documentation)

### 4.8 Payment Entry

Use native `Payment Entry`.

Requirements:
- Detect contract context from referenced Sales Invoice / Sales Order / Purchase Invoice / Purchase Order.
- Support explicit contract allocation for payments covering multiple contracts.
- Provide Contract Payment Allocation child table where required.
- Update contractual paid amount from submitted Payment Entries.
- Support partial payments, advances, unallocated payments and later reconciliation.
- Never create duplicate payment records.

ERPNext Payment Entry supports receipts, supplier payments, advances, partial payments and references to Sales/Purchase documents. (ERPNext Payment Entry documentation)

### 4.9 Dunning

Use native `Dunning` for overdue contractual receivables where enabled.

Requirements:
- Identify overdue contract-linked invoices.
- Link Dunning to Contract.
- Display contractual collection clauses.
- Track payment overdue days and collection actions.
- Feed delinquency into Contract Risk / Performance.

ERPNext Dunning works from overdue Sales Invoices and can post applicable fees/interest through the native accounting workflow. (ERPNext Dunning documentation)

---

## 5. Buying / Procurement integration

ERPNext purchasing uses native documents and should remain the authoritative source for procurement and supplier accounting.

### 5.1 Material Request

Use for contract-driven procurement requirements where appropriate.

Examples:
- Contract obligation requires material purchase.
- SOW requires equipment/material fulfillment.
- Supplier contract creates recurring procurement demand.

Link Material Request to Contract and obligation.

### 5.2 Request for Quotation

Use `Request for Quotation` for supplier sourcing.

Requirements:
- Contract procurement request may generate RFQ.
- RFQ can link back to Contract / Obligation / Project.
- Preserve supplier competition and quotation records.

### 5.3 Supplier Quotation

Use `Supplier Quotation`.

Requirements:
- Link quotation to Contract.
- Compare quoted commercial terms with contract benchmarks.
- Support AI comparison of supplier quote against contract/playbook.

ERPNext Supplier Quotations can be created from RFQs and can lead to Purchase Orders. (ERPNext Supplier Quotation documentation)

### 5.4 Purchase Order

Use `Purchase Order`.

Requirements:
- Create PO from Contract or Procurement Obligation.
- Create Contract from submitted PO when appropriate.
- Link PO to Supplier Contract.
- Track ordered value, quantity and delivery dates.
- Compare PO terms/rates/payment terms against contract.
- Support partial POs against a framework agreement.

ERPNext Purchase Orders can lead to Purchase Receipts and Purchase Invoices and carry supplier terms such as payment terms and additional discounts. (ERPNext Purchase Order documentation)

### 5.5 Purchase Receipt

Use `Purchase Receipt`.

Requirements:
- Link receipts to Supplier Contract.
- Track received quantity/value against contractual commitments.
- Feed supplier performance and delivery metrics.

### 5.6 Purchase Invoice

Use native `Purchase Invoice`.

Requirements:
- Link invoice to Contract.
- Track contractual cost vs invoiced cost.
- Detect overbilling.
- Detect uncontracted purchases.
- Detect price drift.
- Track taxes, payment terms, expense account and Cost Center.
- Feed supplier spend analytics.
- Support credit/debit-note processes using ERPNext native documents.

ERPNext Purchase Invoice posts supplier payable, expense/asset values and taxes to the General Ledger and can originate from Purchase Order or Purchase Receipt. (ERPNext Purchase Invoice documentation)

### 5.7 Supplier Payment

Use native Payment Entry with `Pay` type.

Requirements:
- Contract-to-payment allocation.
- Track supplier paid amount.
- Detect advance payments.
- Compare payment timing with contractual terms.
- Surface early/late payment risk.

---

## 6. Accounting integration

### 6.1 Core masters

Use native ERPNext:
- Company
- Account
- Cost Center
- Accounting Dimensions
- Currency
- Exchange Rate
- Payment Terms Template
- Taxes and Charges Templates
- Item Tax Templates where applicable
- Price Lists
- Payment Gateway Account

Contract DocType may store references to commercial/accounting defaults, but must not replace them.

### 6.2 Journal Entry

Use native `Journal Entry` for manually posted accounting adjustments where contract finance policy requires them.

Do not automatically create JEs merely because a contract changes status.

Supported controlled use cases:
- approved contract penalty accrual;
- approved contract rebate accrual;
- approved provision/adjustment;
- inter-company contractual adjustment.

Each auto-created JE must:
- have explicit business reason;
- be permission-gated;
- be linked to Contract;
- use configured accounts/cost centers;
- be idempotent;
- preserve native accounting validation;
- have full audit trail.

### 6.3 General Ledger analytics

Contract Performance may read submitted GL entries through reports or controlled queries for analysis. It must never rewrite GL entries.

Use source transactions as the preferred audit source; use GL for consolidated accounting truth.

### 6.4 Contract financial dimensions

Contract should support:
- Company
- Cost Center
- Project
- Department where relevant
- custom Accounting Dimension references if configured

Do not hard-code every possible future accounting dimension. Build a configurable mapping layer.

---

## 7. Payment and cash integration

Contract payment intelligence must combine:

```text
Contract
  -> Sales Invoice / Purchase Invoice
  -> Payment Request (when used)
  -> Payment Entry
  -> Reconciliation
  -> Outstanding
  -> Dunning / Collection
```

Metrics:
- Contracted Value
- Invoiced Value
- Paid Value
- Outstanding Value
- Overdue Value
- Days Sales Outstanding related to contract
- Supplier payment days
- Advance received
- Advance paid
- Retention where applicable
- Credit Notes
- Debit Notes
- Interest / penalties
- Contractual payment term vs actual payment behavior

---

## 8. Project Management integration

Use native:
- Project
- Task
- Timesheet
- Expense Claim
- Activity Type / Activity Cost where available

### Contract -> Project

A contract may create or link to one or more Projects.

Typical flow:
```text
Signed Contract
   -> Project
   -> Tasks / Milestones
   -> Timesheets
   -> Expenses
   -> Billing / Revenue
```

### Obligations -> Task

Each operational obligation may:
- create a Task;
- assign to a User/Employee;
- have due date from the Contract Obligation;
- inherit Project and Contract;
- return completion status to Contract Obligation.

### Cost / profitability

Use native Timesheet and Expense Claim data for actual project/service cost. ERPNext project costing uses Timesheets to calculate project/task service cost, so Contract Performance should consume those figures. (ERPNext Project Costing documentation)

### Milestones

Contract Milestones can optionally map to Tasks and Project progress.

---

## 9. Subscription integration

For recurring contracts:

```text
Contract
  -> Subscription Plan(s)
  -> Subscription
  -> recurring Sales Invoices / Purchase Invoices
  -> Payment Entry
```

Requirements:
- Contract stores subscription relationship.
- Contract renewal state must not conflict with Subscription state.
- Subscription can be created from an approved Contract only when configured.
- Contract must display upcoming billing cycles.
- Compare expected contracted recurring value vs generated invoices.
- Support customer and supplier subscriptions where applicable.

ERPNext Subscriptions generate recurring Sales Invoices or Purchase Invoices from Subscription Plans. (ERPNext Subscription documentation)

---

## 10. CRM integration

### Communication

Use Frappe/ERPNext Communication for:
- email threads;
- internal/external messages;
- contract request intake;
- negotiation evidence;
- approval communication;
- signature communication.

Do not build a parallel email history database if native Communication is sufficient.

### ToDo / assignment

Contract reviews, obligations, approvals, and escalations may create native `ToDo` assignments when appropriate, while retaining the richer Contract task record.

### Lead / Opportunity

Maintain navigation and summary synchronization without copying the CRM lifecycle logic.

---

## 11. Support / SLA integration

Use native Support modules for post-signature support and service contracts:

- Issue
- Issue Type
- SLA
- Maintenance Schedule
- Maintenance Visit
- Warranty Claim

### Contract -> Support

A service contract can:
- link Customer and Asset/Serial No;
- define SLA obligations;
- link Issues to Contract;
- measure response/resolution SLA against contractual commitments;
- link Maintenance Visits to Contract;
- link Warranty Claims to Contract;
- create obligation breaches when contractual SLA is missed.

ERPNext Issues support SLA tracking, assignments and Customer/Project/Company references. (ERPNext Issue documentation)

Maintenance Sales Orders and Maintenance Visits already connect sales commitments to service activity; the Contract app must extend this with the Contract context rather than replace native maintenance documents. (ERPNext Maintenance Sales Order / Maintenance Visit documentation)

Warranty Claim can already track warranty/AMC status and relate it to Customer, Item and Serial Number. (ERPNext Warranty Claim documentation)

---

## 12. HR / Frappe HR integration

When Frappe HR is installed, contract types such as Employment, Consultancy, Contractor, Internship and Confidentiality must link to native HR records.

Use:
- Employee
- Employee Onboarding
- Employee Separation
- Employee Transfer
- Department
- Designation
- Employment-related masters where applicable

### Employment contract example

```text
Employee
  -> Employment Contract
  -> Contract Obligations
  -> Onboarding / Separation Tasks
  -> Asset handover obligations
```

The CLM app must not create a second Employee master or duplicate HR lifecycle state.

Frappe HR's employee onboarding and separation workflows already create/manage activities and Projects/Tasks, so contract obligations should integrate with those records rather than duplicate them. (Frappe HR Employee Lifecycle / Onboarding / Separation documentation)

---

## 13. Asset integration

Use native `Asset`.

Contract types:
- Asset Lease
- Asset Maintenance
- AMC
- Equipment Service Agreement
- Warranty
- Property/Equipment Use Agreement

Requirements:
- Link Contract to Asset.
- Track contract coverage start/end.
- Track warranty/AMC coverage.
- Link maintenance visits/issues.
- Surface asset contract expiry.
- Create renewal tasks before asset coverage expires.

ERPNext Asset contains operating history, acquisition value, location, depreciation, maintenance and disposal context; the contract app should enrich that lifecycle with contractual coverage. (ERPNext Asset documentation)

---

## 14. Stock and inventory integration

Where contract terms involve physical goods, support:
- Item
- Item Group
- Item Price
- Price List
- Warehouse
- Serial No
- Batch No
- Delivery Note
- Purchase Receipt
- Pick List where applicable

Use these to calculate:
- ordered quantity;
- delivered quantity;
- received quantity;
- remaining commitment;
- batch/serial contractual warranty;
- service coverage.

The Contract app does not maintain a parallel stock ledger.

---

## 15. Manufacturing integration

When a Sales Contract or SOW requires manufactured products, support linkage to:
- Sales Order
- Work Order
- Production Plan
- Stock/Material Request
- Delivery Note

For supplier/subcontracting contracts, support the relevant ERPNext subcontracting documents when the feature is installed.

Contract Performance should be able to compare contractual promised delivery dates with production and delivery outcomes.

---

## 16. Quality integration

For contracts with acceptance criteria, quality gates or supplier quality obligations, optionally integrate with:
- Quality Inspection
- Non Conformance
- corrective action records

Contract obligation examples:
- inspection required before invoice;
- quality threshold;
- acceptance certificate;
- non-conformance notification window.

---

## 17. Customer / Supplier portal integration

Use ERPNext portal capabilities where they satisfy the business need; extend with a custom secure Contract Portal for CLM-specific actions.

Customer-facing information may include:
- agreements;
- pending reviews;
- signatures;
- contract status;
- obligations requiring customer input;
- linked orders/invoices where permission allows;
- support issues;
- renewal actions.

Supplier-facing information may include:
- supplier agreements;
- RFQs;
- supplier quotations;
- POs;
- contract obligations;
- renewal actions.

Portal must not expose data outside the party's document-level permission scope.

ERPNext's customer portal already exposes orders/invoices/shipping and support Issues; the CLM portal should complement rather than duplicate these capabilities. (ERPNext Customer Portal documentation)

---

## 18. Integration events

### Inbound ERPNext events

Monitor configured document events for:

Selling:
- Lead
- Opportunity
- Quotation
- Sales Order
- Delivery Note
- Sales Invoice
- Payment Request
- Payment Entry
- Dunning

Buying:
- Material Request
- Request for Quotation
- Supplier Quotation
- Purchase Order
- Purchase Receipt
- Purchase Invoice
- Payment Entry

Projects/operations:
- Project
- Task
- Timesheet
- Expense Claim
- Issue
- Maintenance Visit
- Warranty Claim
- Asset
- Subscription

### Event processing rules

1. Ignore drafts unless configuration explicitly requires draft visibility.
2. Prefer submitted/confirmed records for financial truth.
3. Resolve contract context from direct link, source document chain, or integration mapping.
4. Recalculate only affected Contract Performance Metrics.
5. Queue expensive aggregation jobs.
6. Record sync result and errors.
7. Never duplicate references.
8. Never mutate the source document merely to make the contract app work unless a configured custom field/mapping explicitly allows it.

---

## 19. ERPNext custom fields / schema extensions

The application may ship Custom Field fixtures for relevant ERPNext DocTypes.

Minimum recommended fields:

### Commercial
- Contract link on Opportunity
- Contract link on Quotation
- Contract link on Sales Order
- Contract link on Delivery Note
- Contract link on Sales Invoice
- Contract link on Purchase Order
- Contract link on Purchase Receipt
- Contract link on Purchase Invoice
- Contract link on Project
- Contract link on Task
- Contract link on Timesheet
- Contract link on Expense Claim
- Contract link on Issue
- Contract link on Maintenance Visit
- Contract link on Warranty Claim
- Contract link on Asset
- Contract link on Subscription

### Allocation tables
For documents that can span multiple contracts:
- Payment Entry contract allocation child table
- Journal Entry contract allocation child table when enabled
- optional Invoice contract allocation only when a single header Link is insufficient

These must be installed as standard custom-field fixtures by the app, never by editing ERPNext source files.

---

## 20. Transaction creation matrix

| From Contract | ERPNext transaction | Allowed | Approval | Source of truth |
|---|---|---:|---|---|
| Contract | Sales Order | Yes | Configurable | ERPNext Sales Order |
| Contract | Purchase Order | Yes | Configurable | ERPNext Purchase Order |
| Contract | Project | Yes | Configurable | ERPNext Project |
| Contract | Subscription | Yes | Configurable | ERPNext Subscription |
| Contract | Sales Invoice | Only through approved billing flow | Required | ERPNext Sales Invoice |
| Contract | Purchase Invoice | Only through approved billing flow | Required | ERPNext Purchase Invoice |
| Contract | Payment Entry | No direct creation by default | Strict | ERPNext Payment Entry |
| Contract | Journal Entry | Optional controlled workflow | Strict Finance | ERPNext Journal Entry |
| Contract | Delivery Note | Usually from Sales Order | Native ERPNext | ERPNext Delivery Note |
| Contract | Purchase Receipt | Usually from Purchase Order | Native ERPNext | ERPNext Purchase Receipt |
| Contract | Payment Request | Yes when billing/collection flow supports | Configurable | ERPNext Payment Request |
| Contract | Dunning | Yes from overdue invoice | Finance policy | ERPNext Dunning |

The UI should expose only contextually valid Create actions.

---

## 21. Financial leakage engine

Implement deterministic rules before AI.

### Sales leakage examples
- Contract unit price < invoiced unit price => favorable / overcharge exception depending on policy.
- Contract discount > actual discount => potential revenue leakage.
- Contracted minimum commitment not invoiced.
- Delivered but not billed.
- Billed beyond contracted quantity.
- Expired contract used for billing.
- Renewal not executed before new billing period.

### Procurement leakage examples
- PO price > contract price.
- Invoice price > PO price.
- Invoice price > contract price.
- Purchase outside contract where maverick-buying policy prohibits.
- Supplier charged unsupported fees.
- Payment outside contractual terms.

Each finding must store:
- contract;
- source document;
- rule;
- expected value;
- actual value;
- variance;
- currency;
- financial impact;
- severity;
- evidence;
- owner;
- status.

---

## 22. Contract performance metrics sourced from ERPNext

### Sales
- Ordered value
- Delivered value
- Invoiced value
- Paid value
- Outstanding value
- Overdue value
- Order quantity
- Delivery quantity
- Invoice quantity
- Discount variance
- Price variance

### Procurement
- Ordered spend
- Received spend
- Invoiced spend
- Paid spend
- Outstanding spend
- Price variance
- Quantity variance
- Supplier delivery performance

### Project
- Budgeted cost
- Actual cost
- Timesheet cost
- Expense cost
- Revenue
- Gross margin where available
- Task completion

### Service
- Issues count
- SLA response compliance
- SLA resolution compliance
- Maintenance visits
- Warranty claims
- Service credits / penalties

---

## 23. Integration security

- Use Frappe permissions on linked documents.
- Respect Company restrictions.
- Respect User Permissions for Customer, Supplier, Company, Project and other masters.
- Never expose source transaction data through Contract APIs unless caller has permission on the underlying document or policy explicitly allows summarized metrics.
- Mask payment/account data where role does not allow detail.
- Do not expose bank account secrets or gateway credentials to Contract users.
- Log all cross-module reads that involve sensitive documents when configurable audit policy requires it.

---

## 24. Integration configuration

Single DocType: `Contract ERPNext Integration Settings`

Fields:
- enabled
- enable_selling
- enable_buying
- enable_accounts
- enable_projects
- enable_subscriptions
- enable_support
- enable_hr
- enable_assets
- enable_stock
- enable_manufacturing
- enable_quality
- enable_portal
- auto_link_source_transactions
- auto_create_project
- auto_create_subscription
- auto_create_sales_order
- auto_create_purchase_order
- allow_invoice_creation
- allow_journal_entry_creation
- enable_payment_allocation
- enable_leakage_detection
- sync_frequency
- error_notification_role
- default_cost_center
- default_project

The configuration should fail safely when an optional module/DocType is not installed.

---

## 25. ERPNext-first principles for Antigravity

The implementation MUST NOT create duplicate versions of:

- Customer
- Supplier
- Contact
- Address
- Employee
- Company
- Item
- Warehouse
- Account
- Cost Center
- Project
- Task
- Sales Order
- Purchase Order
- Sales Invoice
- Purchase Invoice
- Payment Entry
- Subscription
- Asset
- Issue

Create only the contract-specific records that ERPNext does not already provide.

For example:
- `Contract Obligation` is custom.
- `Contract Risk Finding` is custom.
- `Contract Version` is custom.
- `Contract Performance Metric` is custom.
- `Sales Invoice` is NOT custom and must remain native.

---

## 26. Required integration tests

At minimum implement automated tests for:

### Sales
1. Opportunity -> Contract Request -> Contract -> Quotation.
2. Contract -> Sales Order.
3. Sales Order -> Delivery Note -> Sales Invoice -> Payment Entry.
4. Payment Entry updates Contract paid value.
5. Contract price vs invoice price leakage is detected.
6. Contract cancellation prevents configured downstream creation.

### Buying
7. Contract -> Material Request/RFQ as configured.
8. Contract -> Purchase Order.
9. Purchase Order -> Purchase Receipt -> Purchase Invoice -> Payment Entry.
10. Purchase Invoice variance against Contract detected.
11. Supplier payment updates Contract financial performance.

### Projects
12. Contract -> Project.
13. Contract Obligation -> Task.
14. Timesheet/Expense Claim updates contract/project cost metrics.

### Subscription
15. Contract -> Subscription -> recurring invoice.
16. Subscription state and Contract renewal state remain consistent.

### Support
17. Issue references Contract and updates SLA performance.
18. Maintenance Visit references Contract.
19. Warranty Claim references Contract/Asset.

### HR
20. Employment Contract references Employee.
21. Contract obligations can link to Employee Onboarding/Separation tasks.

### Asset
22. Asset Maintenance Contract references Asset.
23. Contract expiry generates asset coverage warning.

### Security
24. User cannot view linked Sales Invoice without required ERPNext permission.
25. Cross-company Contract cannot expose unauthorized invoices.
26. Payment allocation is idempotent.
27. Duplicate event delivery does not duplicate performance records.

---

## 27. Acceptance criterion

The application is NOT considered ERPNext-integrated if it merely stores IDs of ERPNext documents.

Integration is complete only when the application can:

1. navigate between Contract and native ERPNext transactions;
2. create approved downstream transactions through native APIs/actions where configured;
3. consume submitted transaction states and amounts;
4. calculate contractual vs actual performance;
5. trace money from contract -> invoice -> payment;
6. trace procurement from contract -> PO -> receipt -> invoice -> payment;
7. trace service from contract -> issue/maintenance/warranty;
8. trace project work from contract -> project -> task -> time/expense;
9. trace recurring billing from contract -> subscription -> invoice -> payment;
10. enforce permissions across all linked modules;
11. remain upgrade-safe without editing ERPNext/Frappe core.

---

## 28. Official ERPNext/Frappe references

- DocTypes: https://docs.frappe.io/erpnext/doctype
- Quotation: https://docs.frappe.io/erpnext/quotation
- Sales Order: https://docs.frappe.io/erpnext/sales-order
- Delivery Note: https://docs.frappe.io/erpnext/delivery-note
- Sales Invoice: https://docs.frappe.io/erpnext/sales-invoice
- Payment Entry: https://docs.frappe.io/erpnext/payment-entry
- Payment Request: https://docs.frappe.io/erpnext/payment-request
- Dunning: https://docs.frappe.io/erpnext/dunning
- Purchase Order: https://docs.frappe.io/erpnext/purchase-order
- Supplier Quotation: https://docs.frappe.io/erpnext/supplier-quotation
- Purchase Invoice: https://docs.frappe.io/erpnext/purchase-invoice
- Project: https://docs.frappe.io/erpnext/project
- Project Costing: https://docs.frappe.io/erpnext/project-costing
- Subscription: https://docs.frappe.io/erpnext/subscription
- Subscription Plan: https://docs.frappe.io/erpnext/subscription-plan
- Issue: https://docs.frappe.io/erpnext/issue
- Maintenance Visit: https://docs.frappe.io/erpnext/maintenance-visit
- Warranty Claim: https://docs.frappe.io/erpnext/warranty-claim
- Asset: https://docs.frappe.io/erpnext/asset
- Customer Portal: https://docs.frappe.io/erpnext/customer-portal
- Frappe HR Employee Lifecycle: https://docs.frappe.io/hr/employee-lifecycle-management
- Frappe HR Employee Onboarding: https://docs.frappe.io/hr/employee-onboarding
- Frappe HR Employee Separation: https://docs.frappe.io/hr/employee-separation
