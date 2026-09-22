# ERPNext Deep Integration & MCP Adapter Guide

## 1. Non-Invasive Architectural Model
NSD Contract Management is built as a first-class citizen of ERPNext v16. It links contract governance to real operational and accounting transactions without ever duplicating or directly manipulating General Ledger (GL) or Stock Ledger (SL) tables.

## 2. Integrated ERPNext Chains

### CRM & Selling
- **Lead / Opportunity**: Source reference tracking.
- **Quotation**: Contract pricing and commercial term alignment.
- **Sales Order**: Fulfillment tracking and uncontracted rate checks.
- **Delivery Note**: Operational dispatch fulfillment.
- **Sales Invoice**: Billing synchronization and commercial price leakage detection.

### Buying & Procurement
- **Purchase Order**: Committed spend tracking against contract value ceiling.
- **Purchase Receipt**: Goods receipt verification.
- **Purchase Invoice**: Supplier pricing audit and price variance detection.

### Accounts
- **Payment Entry**: Syncs payments against single contracts or multi-contract allocation child rows.
- **Financial Aggregation**: Dynamic calculation of committed, billed, and paid amounts via `Contract ERP Reference` records.

### Projects & Operations
- **Project**: Links contract to overarching delivery project.
- **Task**: Automatic completion synchronization for milestone-based Contract Obligations.
- **Timesheet & Expense Claim**: Direct cost tracking against contracted caps.

### Support & SLAs
- **Issue**: Resolution time audited against contracted SLA hours.
- **Maintenance Visit & Warranty Claim**: Support fulfillment tracking.

### HR & Assets
- **Employee**: Employment agreement linking.
- **Asset**: Equipment lease and maintenance contract association.

## 3. Model Context Protocol (MCP) Adapter
The application includes `nsd_contract_management.integrations.mcp_adapter` exposing safe tool capabilities to external AI systems:
- `mcp_search_contracts(query, company, status)`
- `mcp_get_contract_details(contract_name)`
- `mcp_check_contract_risk(contract_name)`
- `mcp_get_contract_obligations(contract_name)`
- `mcp_create_contract_request(title, company, counterparty_name, estimated_value, currency, description)`
