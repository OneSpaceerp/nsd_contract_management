# Workflows, Rules and Automations

## 1. Contract Request workflow
```text
Draft
 → Submitted
 → Intake Validation
 → Classified
 → Accepted / Rejected
 → Contract Created
```

Rules:
- Missing mandatory business data blocks submission.
- Duplicate/related contract check runs before contract creation.
- High-value/high-risk intake automatically routes to Legal/Finance.

## 2. Contract workflow
```text
Draft
 → Internal Review
 → Legal Review
 → Commercial Review (conditional)
 → Negotiation (optional)
 → Approval Pending
 → Approved
 → Signature Pending
 → Executed
 → Effective
```

Alternative outcomes: `Rejected`, `Cancelled`, `On Hold`.

## 3. Dynamic approval examples
```text
IF contract_value >= 1000000 → CFO
IF contract_value >= 5000000 → CEO / delegated executive role
IF risk_level = Critical → General Counsel
IF data_processing = Yes → Privacy/Compliance
IF governing_law requires local review → Local Legal Role
IF non_standard_clause_count > 0 → Legal approval
IF payment_terms > company_policy_days → Finance approval
IF liability_cap below standard → General Counsel
```

Implement conditions as data, not hard-coded if a rule can reasonably be configured.

## 4. Negotiation workflow
1. Send secure review session.
2. Counterparty uploads or edits version.
3. Create Negotiation Round.
4. Parse changes.
5. Compare clauses against playbook.
6. Create Negotiation Issues.
7. AI proposes response/fallback.
8. Human accepts/edits/rejects AI suggestions.
9. Create next version.
10. Close round when all issues are resolved or escalated.

## 5. Signature workflow
```text
Approved
 → Build Signature Packet
 → Send
 → Viewed
 → Signed / Declined
 → Completed
 → Store certificate/evidence
 → Mark Contract Executed
```

External provider events must be idempotent.

## 6. Obligation automation
Daily job:
- identify due in 90/60/30/14/7/1 days;
- notify owner;
- escalate according to policy;
- mark overdue;
- update contract health where configured;
- create tasks where evidence is required.

## 7. Renewal automation
Daily job:
- recalculate notice deadline;
- identify contracts approaching notice window;
- generate Renewal records if not present;
- generate renewal task;
- produce AI renewal brief asynchronously;
- escalate missed deadlines.

## 8. AI review automation
On Contract Version upload/import:
- create AI Review job if policy enabled;
- extract metadata;
- extract clauses;
- extract dates/financial terms;
- identify risk;
- create obligations;
- update Contract canonical fields only where confidence/policy allows;
- otherwise create review tasks.

## 9. Post-signature automation
On executed:
- set executed flag/date;
- create or update effective lifecycle;
- create obligations;
- schedule renewal/notice;
- synchronize CRM/ERP references;
- notify owner and finance;
- generate immutable executed version;
- index document for search.

## 10. Retention automation
Scheduled task:
- identify records past retention date;
- skip legal hold;
- require retention-release permission;
- archive or purge only according to tenant policy;
- record audit evidence.

## 11. Webhook processing
Inbound external event pattern:
1. Authenticate signature.
2. Save raw event metadata.
3. Check idempotency/event ID.
4. Process.
5. Mark processed.
6. Retry failures safely.

## 12. Workflow transition tasks
Frappe v16 supports workflow transition tasks including app-defined actions, server scripts and webhooks. Use them for small transition-side effects, while keeping important domain logic inside the app service layer. https://docs.frappe.io/erpnext/workflow-transition-tasks
