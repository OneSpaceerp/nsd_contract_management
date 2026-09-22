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
