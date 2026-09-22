# Administrator Guide: NSD Contract Management

## 1. Legal Hold Enforcement
A Legal Hold suspends normal document lifecycles and retention schedules to preserve electronic evidence for pending litigation or regulatory audits.

### Applying a Legal Hold
- Only users with the `General Counsel` or `Legal Manager` role may apply or release a Legal Hold.
- Navigate to the Contract form and select **Legal Hold > Apply Legal Hold**.
- Enter the formal litigation or investigation matter reference and mandatory justification.
- The contract is instantly locked:
  - Deletion is strictly blocked at the database event level (`on_trash`).
  - Termination, Cancellation, and Archival transitions raise `PermissionError`.
  - Scheduled retention purges will skip the record.

### Releasing a Legal Hold
- Select **Legal Hold > Release Legal Hold**.
- The release reason and timestamp are appended to the immutable audit trail.

## 2. Retention Schedules & Archival
The application executes a nightly background job (`nightly_retention_and_legal_hold_check` at `02:00`):
- Contracts in `Terminated` or `Expired` status older than `retention_period_years` are reviewed.
- Any contract with `legal_hold == 1` is completely bypassed.
- Eligible records are cleanly moved to `Archived` status with an audit comment.

## 3. Managing Roles & Permissions
The application seeds 21 specialized roles including:
- `Contract Manager`: Full drafting, review, negotiation, and lifecycle management.
- `General Counsel`: Legal approval, playbook management, legal hold enforcement.
- `Contract Auditor`: Read-only access across all contracts, obligations, and leakage findings.
- `Finance Approver`: Financial approvals and invoice payment reconciliation.

In Frappe v16, custom permission types are registered:
- `approve_contract`, `reject_contract`, `send_for_signature`, `execute_contract`, `release_legal_hold`, `run_ai_review`, `manage_playbook`, `manage_clause`.
