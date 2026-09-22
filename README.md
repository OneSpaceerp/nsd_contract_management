# NSD Contract Management & Contract Intelligence

Production-grade Contract Lifecycle Management (CLM) and Contract Intelligence application for **ERPNext v16 / Frappe Framework v16**.

## Overview
`nsd_contract_management` is an enterprise-grade CLM app built to operate natively inside ERPNext v16 without modifying core files. It provides end-to-end management of agreements from intake, authoring, redlining, dynamic approval, and electronic signatures, to post-signature obligation monitoring, AI extraction, and deep transactional integration across sales, procurement, projects, subscriptions, support, assets, and accounting.

## Key Features
- **Contract Lifecycle Management**: Full state machine (Draft → Intake → In Review → Negotiation → Approval Pending → Signature Pending → Executed → Effective → Expired/Terminated/Archived).
- **Immutable Versioning**: SHA-256 integrity hashing and strict immutability locks on executed versions.
- **Dynamic Approval Engine**: Multi-factor routing matrices (values, risk levels, non-standard clauses, local jurisdictions) using v16 Custom Permission Types.
- **Provider-Agnostic eSignatures**: Clean adapter interface with working mock provider, DocuSign REST adapter, and internal native digital signatures.
- **Timezone-Aware Obligations & Renewals**: Background escalation engine tracking deadlines, notice periods, and recurring commitments.
- **Deep ERPNext Transactional Integration**: Real-time bidirectional linking across:
  - CRM: Lead → Opportunity → Contract → Quotation
  - Selling: Sales Order → Delivery Note → Sales Invoice → Payment Entry
  - Buying: RFQ → Supplier Quotation → Purchase Order → Purchase Receipt → Purchase Invoice
  - Projects: Project → Task (Contract Obligations) → Timesheets & Expenses
  - Subscriptions: Subscription Plan → Subscription → Recurring Invoices
  - Support & SLAs: Issue / SLA tracking → Maintenance Visits → Warranty Claims
  - HR: Employment Contracts → Employee Onboarding / Separation
  - Assets: Maintenance & Warranty Coverage
  - Accounting: Payment Entry multi-contract allocation & deterministic financial leakage detection.
- **AI Intelligence & Governance**: Structured extraction with bounding boxes, confidence scoring, evidence citations, prompt injection defense, and human-in-the-loop AI Agent Studio.

## Installation
Requires Python 3.14+ and Frappe/ERPNext v16.
```bash
bench get-app https://github.com/nsd/nsd_contract_management.git
bench --site [your-site] install-app nsd_contract_management
bench --site [your-site] migrate
```

## Documentation
- [Installation Guide](docs/INSTALL.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Administrator Guide](docs/ADMIN_GUIDE.md)
- [REST & RPC API Specification](docs/API.md)
- [AI Governance & Architecture](docs/AI_GOVERNANCE.md)
- [ERPNext Transaction Integration Matrix](docs/INTEGRATIONS.md)
- [Architectural Decisions Log](docs/DECISIONS.md)
- [Changelog](docs/CHANGELOG.md)

## License
GNU General Public License v3.0 or later.
