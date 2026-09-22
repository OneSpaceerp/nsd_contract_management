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
