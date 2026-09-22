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
