# Permissions, Security and Compliance

## 1. Roles
### System/Platform
- Contract System Manager
- Contract System Administrator

### Business
- Contract Requester
- Contract Manager
- Contract Owner
- Legal Counsel
- Legal Manager
- Procurement User
- Procurement Manager
- Sales User
- Sales Manager
- Finance User
- Finance Manager
- Compliance User
- Compliance Manager
- Executive Viewer

### AI
- AI Administrator
- AI Reviewer
- AI Agent Operator

### External
- Counterparty Reviewer
- Counterparty Signer

## 2. Permission strategy
Use standard Frappe DocType permissions for base CRUD and v16 Custom Permission Types for action-level operations such as:
- approve_contract
- reject_contract
- send_for_signature
- execute_contract
- download_contract
- export_contract_data
- release_legal_hold
- run_ai_review
- run_ai_agent
- execute_ai_action
- manage_playbook
- manage_clause
- manage_workflow

Frappe v16 explicitly supports custom permission types beyond read/write/create/delete/submit. https://docs.frappe.io/framework/user/en/permission-types

## 3. Data scope
A user may be restricted by:
- Company
- Legal Entity
- Department
- Territory
- Contract Type
- Contract Owner
- Role
- User Permission records
- Document-specific sharing

## 4. Server-side enforcement
Never rely only on UI hiding. Every sensitive operation must re-check permissions server-side.

## 5. Document access
Attachments inherit document read permission in Frappe. Keep executed documents private unless a controlled portal/signature path explicitly creates a secure external access mechanism. https://docs.frappe.io/framework/user/en/desk/attachments

## 6. External review security
Counterparty sessions should use:
- random high-entropy token
- expiration
- one-time or scoped access
- optional password/OTP
- IP/device audit where allowed
- contract/session scope
- minimal permissions
- no broad Desk access

## 7. AI security
- tenant isolation
- prompt policy control
- provider allowlist
- secret redaction
- PII handling
- source evidence
- human approval for sensitive actions
- model/action audit

## 8. Audit trail
Business audit events should record:
- actor
- timestamp
- event
- target doctype/name
- previous value summary
- new value summary
- IP/session metadata where permitted
- source (UI/API/AI/scheduler)
- correlation ID

## 9. Encryption
Use HTTPS/TLS for all network traffic. Protect secrets using site/app secret mechanisms and deployment secret management. Do not place credentials in source code or fixtures.

## 10. Retention and legal hold
Retention policies cannot purge documents under active legal hold. Legal hold release requires authorized role and is itself auditable.

## 11. Data export/deletion
Support controlled export and privacy requests where applicable, but never allow ordinary users to bypass legal hold, records retention, or system security controls.

## 12. Threat model priorities
- Unauthorized contract download
- Broken object-level authorization
- Token/session replay
- Webhook spoofing
- AI prompt injection through documents
- Data exfiltration via AI tools
- Duplicate signature requests
- Duplicate ERP synchronization
- Privilege escalation through workflow transitions
- Malicious macro/attachment files
- Leakage through logs

## 13. Prompt injection defense
Treat contract content as untrusted data. AI extraction/review must not allow text inside a contract to redefine system instructions, grant tools, or bypass policy.
