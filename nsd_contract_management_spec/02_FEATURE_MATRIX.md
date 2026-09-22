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
