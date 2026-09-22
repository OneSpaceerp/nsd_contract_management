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
