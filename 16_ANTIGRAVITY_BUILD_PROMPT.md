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
