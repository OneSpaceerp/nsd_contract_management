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
