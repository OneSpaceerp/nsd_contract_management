# Integration Specification

## 1. ERPNext native integration
Use native Link fields where practical.

### Customer
Contract parties can reference Customer.

### Supplier
Contract parties can reference Supplier.

### Contact / Address
Use native ERPNext records for party contact data.

### Opportunity / Quotation / Sales Order
Link commercial/customer agreements to sales transactions.

### Purchase Order
Link supplier contracts to procurement.

### Sales Invoice / Purchase Invoice
Use for performance/value/leakage analysis.

### Project / Task
Map SOW milestones and obligations.

## 2. CRM adapters
Provide generic integration interfaces with initial adapters for common CRMs.

Interface methods:
```text
find_party
get_opportunity
get_account
push_contract_status
push_contract_value
push_renewal
```

## 3. Microsoft 365
### Word
- open/edit contract
- generate document
- import revised document
- synchronize version metadata

### Outlook
- email-to-contract
- attach email evidence
- link message thread
- initiate intake from email

### Teams
- notifications
- approval cards
- contract links

## 4. Google Workspace
- Drive document import
- Gmail intake
- Calendar deadline synchronization (optional)

## 5. eSignature providers
Adapter interface:
```python
class SignatureProvider:
    def create_request(self, packet, signers): ...
    def send(self, request): ...
    def get_status(self, provider_request_id): ...
    def cancel(self, provider_request_id): ...
    def download_evidence(self, provider_request_id): ...
    def parse_webhook(self, payload): ...
```

## 6. External AI providers
Same adapter architecture as AI specification.

## 7. MCP gateway
Expose safe business tools:
- search contracts
- get contract
- list obligations
- list renewals
- compare versions
- ask contract
- create review task
- prepare renewal brief

Write actions should be separately permissioned and audited.

## 8. Email
Email templates:
- new request
- review assignment
- approval request
- rejection
- signature request
- signature reminder
- obligation due
- obligation overdue
- renewal warning
- notice deadline

## 9. SMS / WhatsApp
Use provider adapter. Never place sensitive full contract text into a notification message by default.

## 10. Webhooks
Provide configurable outbound webhooks for lifecycle events, respecting Frappe's webhook pattern. See https://docs.frappe.io/framework/user/en/guides/integration/webhooks

## 11. Integration mapping
DocType: `Contract Integration Mapping`
Fields:
- contract
- system
- external_object_type
- external_object_id
- sync_direction
- status
- last_synced_on
- last_error
- checksum

## 12. Retry policy
- exponential backoff
- max retry count
- dead-letter/error state
- manual replay
- idempotency
- provider response logging without secrets
