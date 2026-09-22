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
