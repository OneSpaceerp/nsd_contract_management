# API Reference: NSD Contract Management

All endpoints conform to Frappe REST v2 and Domain RPC specifications.

## 1. REST v2 Document Resources
Standard CRUD access:
```http
GET    /api/v2/document/Contract
GET    /api/v2/document/Contract/{contract_name}
POST   /api/v2/document/Contract
PATCH  /api/v2/document/Contract/{contract_name}
DELETE /api/v2/document/Contract/{contract_name}
```

## 2. Domain RPC Methods

### Contract Lifecycle
- **Create From Request**:
  `POST /api/method/nsd_contract_management.api.contract.create_from_request`
  `{"request_name": "REQ-2026-0001"}`

- **Submit for Review**:
  `POST /api/method/nsd_contract_management.api.contract.submit_for_review`
  `{"contract_name": "CNT-2026-0001", "reviewers": "legal@example.com,cfo@example.com"}`

- **Start Negotiation**:
  `POST /api/method/nsd_contract_management.api.contract.start_negotiation`
  `{"contract_name": "CNT-2026-0001", "counterparty_contact": "counsel@counterparty.com"}`

- **Send for Signature**:
  `POST /api/method/nsd_contract_management.api.contract.send_for_signature`
  `{"contract_name": "CNT-2026-0001", "provider": "Native"}`

- **Legal Hold Management**:
  `POST /api/method/nsd_contract_management.api.contract.put_on_hold`
  `{"contract_name": "CNT-2026-0001", "reason": "Litigation matter MAT-101"}`

  `POST /api/method/nsd_contract_management.api.contract.resume`
  `{"contract_name": "CNT-2026-0001", "reason": "Hold resolved"}`

- **Terminate**:
  `POST /api/method/nsd_contract_management.api.contract.terminate`
  `{"contract_name": "CNT-2026-0001", "termination_type": "Convenience", "reason": "Project completed"}`

### AI Intelligence Endpoints
- **Extract Contract**:
  `POST /api/method/nsd_contract_management.api.ai.extract`
  `{"contract_name": "CNT-2026-0001"}`

- **Grounded Q&A**:
  `POST /api/method/nsd_contract_management.api.ai.ask`
  `{"contract_name": "CNT-2026-0001", "question": "What is the liability cap?"}`

- **Run AI Agent**:
  `POST /api/method/nsd_contract_management.api.ai.run_ai_agent`
  `{"agent_name": "Commercial Leakage Investigator", "contract_name": "CNT-2026-0001"}`

- **Approve Agent Action (HITL Gate)**:
  `POST /api/method/nsd_contract_management.api.ai.approve_action`
  `{"action_name": "ACT-2026-0001"}`

### ERP Financials
- **Get Real-Time Financial Summary**:
  `GET /api/method/nsd_contract_management.api.erp.get_financial_summary?contract_name=CNT-2026-0001`

  Response:
  ```json
  {
    "contract": "CNT-2026-0001",
    "contract_value": 1200000.0,
    "currency": "USD",
    "total_committed": 800000.0,
    "total_billed": 450000.0,
    "total_paid": 450000.0,
    "balance_remaining": 750000.0
  }
  ```

## 3. Idempotency Support
For mutation endpoints with financial or external side effects, pass:
`Idempotency-Key: <unique-uuid-or-hash>`
If an identical request has already been executed within 24 hours, the cached result is returned without duplicating database or webhook operations.
