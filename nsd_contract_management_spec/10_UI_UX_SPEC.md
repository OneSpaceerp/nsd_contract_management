# UI / UX Specification

## 1. Desk workspace
Workspace name: `Contract Management`

Sections:
- My Work
- Contracts
- Requests
- Reviews
- Negotiations
- Approvals
- Signatures
- Obligations
- Renewals
- Amendments
- Performance
- Disputes
- AI Intelligence
- Reports
- Administration

## 2. Dashboard
Cards:
- My pending approvals
- My reviews
- Expiring in 30/60/90 days
- Overdue obligations
- Signature pending
- High-risk contracts
- Renewal pipeline
- Contract value
- Leakage detected
- Open disputes

Charts:
- contract lifecycle funnel
- cycle time trend
- risk distribution
- renewal timeline
- obligation completion
- contract value by type/company

## 3. Contract form
Header:
- Contract number
- Title
- Status
- Risk
- Value
- Owner
- Counterparty
- Effective/Expiration
- Renewal/Notice

Tabs:
1. Overview
2. Parties
3. Terms
4. Clauses
5. Documents
6. Versions
7. Reviews
8. Negotiation
9. Approvals
10. Signature
11. Obligations
12. Renewals
13. Amendments
14. Performance
15. ERP/CRM Links
16. AI Insights
17. Timeline

## 4. AI Insights panel
Show:
- summary
- risk score
- critical findings
- extracted terms
- missing clauses
- deviations
- obligations
- suggested actions
- evidence links

Never display an AI score without a way to inspect underlying findings/evidence.

## 5. Contract workspace
Provide a split view:
```text
Left: document/version
Middle: contract metadata/issues
Right: AI insights / tasks / comments
```

## 6. Negotiation workspace
- version selector
- side-by-side diff
- redline view
- comment thread
- issue panel
- playbook comparison
- AI recommendation panel
- resolve/accept/reject controls

## 7. Renewal workspace
Display:
- expiration date
- notice deadline
- renewal decision
- current commercial terms
- previous terms
- performance summary
- open obligations
- disputes
- AI renewal brief
- next actions

## 8. Obligation workspace
List/group by:
- due today
- due this week
- overdue
- owner
- contract
- priority
- status

## 9. Executive portfolio
Use a clean summary interface with drill-down. No destructive actions from summary cards.

## 10. Counterparty portal
Pages:
- Welcome / verification
- Agreements
- Current review
- Documents
- Comments
- Signatures
- Tasks
- Support

The portal must not expose unrelated tenant data.

## 11. Mobile requirements
All critical read/action APIs must work from mobile clients even if the first delivery is Desk-first. Prioritize:
- approvals
- contract search
- obligations
- renewal deadlines
- signature status
- AI assistant

## 12. UX rules
- Every status-changing button must explain prerequisites if blocked.
- Never hide failed background jobs; show retry state.
- Every AI action must show whether it is suggestion-only or executable.
- Use consistent lifecycle color semantics, but do not rely on color alone for status.
- Preserve Frappe accessibility and keyboard interaction patterns.
