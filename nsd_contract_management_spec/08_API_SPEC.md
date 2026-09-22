# API Specification

Frappe automatically exposes CRUD APIs for DocTypes and supports custom whitelisted methods. Use REST v2 for new integration contracts where possible, with app-owned RPC methods for domain actions. Official docs: https://docs.frappe.io/framework/user/en/guides/integration/rest_api

## 1. Base URL
`https://{site}/api/v2`

Standard Frappe document resources:
```text
GET    /api/v2/document/Contract
GET    /api/v2/document/Contract/{name}
POST   /api/v2/document/Contract
PATCH  /api/v2/document/Contract/{name}
DELETE /api/v2/document/Contract/{name}
```

## 2. Domain RPC endpoints
Expose app-owned methods under:
`/api/method/nsd_contract_management.api.<module>.<method>`

### Contract actions
```text
contract.create_from_request
contract.submit_for_review
contract.start_negotiation
contract.create_version
contract.mark_approved
contract.send_for_signature
contract.mark_executed
contract.activate
contract.put_on_hold
contract.resume
contract.terminate
contract.archive
```

### Review
```text
review.start
review.complete
review.request_changes
review.create_ai_review
```

### Negotiation
```text
negotiation.create_round
negotiation.import_redline
negotiation.analyze_changes
negotiation.accept_change
negotiation.reject_change
negotiation.resolve_issue
```

### Obligations
```text
obligation.complete
obligation.waive
obligation.reopen
obligation.add_evidence
```

### Renewals
```text
renewal.create
renewal.start
renewal.approve
renewal.mark_not_renewed
renewal.generate_brief
```

### AI
```text
ai.extract_contract
ai.review_contract
ai.compare_versions
ai.ask_contract
ai.ask_portfolio
ai.run_agent
ai.approve_agent_action
```

## 3. Idempotency
Mutation endpoints that create an external or financial side effect must accept:
`Idempotency-Key: <uuid>`

Persist the key, target action, result and timestamp. Repeating a valid identical request should return the previous result rather than duplicate work.

## 4. Webhooks
### Outbound
Events:
- contract.created
- contract.updated
- contract.status_changed
- contract.approved
- contract.executed
- contract.expiring
- contract.renewal_due
- obligation.due
- obligation.overdue
- signature.sent
- signature.completed
- ai.review.completed
- ai.risk.created

### Inbound
Provider adapters should expose a single signed webhook endpoint, then route internally.

```text
POST /api/method/nsd_contract_management.api.webhooks.receive
```

## 5. Example create contract request
```json
{
  "title": "Enterprise Services Agreement",
  "contract_type": "MSA",
  "company": "My Company",
  "legal_entity": "My Company LLC",
  "currency": "USD",
  "contract_value": 250000,
  "effective_date": "2026-10-01",
  "expiration_date": "2027-09-30",
  "auto_renewal": true,
  "notice_period_days": 60,
  "language": "Bilingual",
  "parties": [
    {
      "party_type": "Customer",
      "party": "CUST-0001",
      "role": "Customer"
    }
  ]
}
```

## 6. AI answer response
```json
{
  "answer": "The agreement allows termination for convenience with 60 days notice.",
  "confidence": 0.96,
  "evidence": [
    {
      "contract": "CTR-2026-00001",
      "version": "CTV-2026-00004",
      "page": 18,
      "clause": "Termination",
      "quote": "..."
    }
  ]
}
```

## 7. Error model
Use Frappe exceptions plus structured API messages where appropriate:
```json
{
  "error": {
    "code": "CONTRACT_APPROVAL_REQUIRED",
    "message": "The contract cannot be sent for signature until the Legal approval is completed.",
    "details": {
      "contract": "CTR-2026-00001",
      "missing_step": "Legal Review"
    }
  }
}
```

## 8. Authentication
Use Frappe's standard auth/session/token mechanisms for internal APIs; use OAuth/service accounts or signed tokens for controlled machine-to-machine integrations. Never embed privileged API secrets in client JavaScript.

## 9. Pagination/filtering
Support standard Frappe filters and pagination. Domain endpoints must document filter fields and maximum page sizes.

## 10. API versioning
Internal domain endpoints should be published under `/api/v1/...` and `/api/v2/...` when a breaking contract is introduced. Preserve backward compatibility for at least one documented deprecation window.

## 11. ERPNext integration endpoints

Domain actions must exist for controlled transaction integration:

```text
erp.get_related_transactions
erp.resolve_contract_context
erp.create_sales_order
erp.create_purchase_order
erp.create_project
erp.create_subscription
erp.create_payment_request
erp.sync_transaction
erp.sync_payment
erp.allocate_payment
erp.recalculate_contract_financials
erp.detect_leakage
erp.get_contract_statement
erp.get_contract_profitability
```

Read endpoints must enforce the underlying ERPNext document permissions.

Transaction-creation endpoints must require explicit permission and configuration flags.

## 12. ERPNext integration webhook events

Support controlled hooks for:

```text
selling.opportunity.submitted
selling.quotation.submitted
selling.sales_order.submitted
selling.delivery_note.submitted
selling.sales_invoice.submitted
accounts.payment_request.submitted
accounts.payment_entry.submitted
accounts.dunning.submitted
buying.purchase_order.submitted
buying.purchase_receipt.submitted
buying.purchase_invoice.submitted
projects.task.updated
projects.timesheet.submitted
projects.expense_claim.submitted
subscription.updated
support.issue.updated
support.maintenance_visit.submitted
support.warranty_claim.updated
assets.asset.updated
hr.employee_updated
```

## 13. ERPNext integration payload requirement

Every synchronization record must store:
- source_doctype
- source_name
- source_company
- source_status
- source_docstatus
- source_modified_on
- contract
- sync_direction
- sync_idempotency_key
- sync_hash
- last_success_on
- last_error
