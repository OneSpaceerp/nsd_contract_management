# Core DocType Field Specification

This is the implementation-level field contract for the core DocTypes. Add `owner`, `creation`, `modified`, `modified_by`, `docstatus`, and other standard Frappe fields automatically rather than duplicating them as custom fields.

## 1. Contract Type
| Field | Type | Required | Notes |
|---|---|---:|---|
| contract_type_name | Data | Yes | Unique |
| code | Data | Yes | Unique short code |
| active | Check | Yes | Default 1 |
| description | Small Text | No | |
| default_template | Link: Contract Template | No | |
| default_playbook | Link: Clause Playbook | No | |
| default_workflow | Link: Workflow | No | Optional |
| default_contract_duration_days | Int | No | |
| default_notice_days | Int | No | |
| requires_legal_review | Check | Yes | |
| requires_finance_review | Check | Yes | |
| requires_compliance_review | Check | Yes | |
| allowed_companies | Table | No | Child company list |
| allowed_countries | Small Text | No | JSON-like list or child table |

## 2. Contract
| Field | Type | Required | Notes |
|---|---|---:|---|
| title | Data | Yes | Human title |
| contract_type | Link: Contract Type | Yes | |
| company | Link: Company | Yes | ERPNext |
| legal_entity | Link: Legal Entity | Yes | Executing entity |
| contract_number | Data | Yes | Usually autoname |
| external_reference | Data | No | Counterparty ref |
| status | Select | Yes | Lifecycle status |
| sub_status | Data | No | Configurable |
| source | Select | Yes | Internal/Imported/Email/API/Web Form/Counterparty |
| business_owner | Link: User | Yes | Primary owner |
| legal_owner | Link: User | No | Legal owner |
| procurement_owner | Link: User | No | |
| sales_owner | Link: User | No | |
| counterparty_primary | Dynamic Link/Link design | Yes | Use party row as source of truth |
| effective_date | Date | No | |
| expiration_date | Date | No | |
| renewal_date | Date | No | Calculated where possible |
| auto_renewal | Check | Yes | |
| notice_period_days | Int | No | |
| notice_deadline | Date | No | Calculated |
| governing_law | Data | No | |
| jurisdiction | Data | No | |
| contract_timezone | Link: Timezone / Data | Yes | Default company timezone |
| language | Select | Yes | English/Arabic/Bilingual/Other |
| currency | Link: Currency | No | |
| contract_value | Currency | No | |
| contract_value_type | Select | No | Fixed/Recurring/Usage/Unknown |
| payment_terms | Data | No | Canonical summarized field |
| confidentiality | Select | No | Standard/Enhanced/Strict |
| risk_level | Select | No | Low/Medium/High/Critical |
| risk_score | Float | No | AI/rule score |
| compliance_score | Float | No | |
| performance_score | Float | No | |
| renewal_score | Float | No | |
| current_version | Link: Contract Version | No | |
| parent_contract | Link: Contract | No | |
| executed | Check | Yes | |
| executed_on | Datetime | No | |
| signed_document | Attach | No | Final executed document |
| archive_date | Date | No | |
| legal_hold | Check | Yes | |
| description | Text Editor | No | Executive summary |
| ai_summary | Long Text | No | Cached AI summary; never source of truth |
| ai_last_reviewed_on | Datetime | No | |

### Contract child tables
- Contract Party Row
- Contract Clause Row
- Contract Term Row
- Contract ERP Reference Row
- Contract Tag Row

## 3. Contract Party Row
| Field | Type |
|---|---|
| party_type | Select: Customer/Supplier/Company/Contact/Employee/Other |
| party | Dynamic Link or Link according to implementation |
| role | Link: Party Role |
| legal_name | Data |
| display_name | Data |
| registration_no | Data |
| tax_id | Data |
| country | Link: Country |
| email | Data |
| phone | Data |
| address | Small Text |
| authorized_signer | Data |
| signer_email | Data |
| primary | Check |

## 4. Contract Version
| Field | Type |
|---|---|
| contract | Link: Contract |
| version_no | Int |
| version_label | Data |
| version_status | Select: Draft/Negotiation/Approved/Executed/Superseded |
| source_type | Select: Generated/Uploaded/Amended/Imported |
| document_file | Attach |
| source_document | Attach |
| change_summary | Text Editor |
| hash_sha256 | Data |
| created_from_version | Link: Contract Version |
| created_by_user | Link: User |
| generated_on | Datetime |
| approved_on | Datetime |
| executed_on | Datetime |
| immutable | Check |

## 5. Clause
| Field | Type |
|---|---|
| clause_name | Data |
| clause_code | Data |
| clause_category | Link: Clause Category |
| active | Check |
| preferred_version | Link: Clause Version |
| risk_level | Select |
| mandatory | Check |
| prohibited | Check |
| applicable_contract_types | Table MultiSelect or child table |
| applicable_jurisdictions | Table MultiSelect or child table |
| owner | Link: User |
| notes | Small Text |

## 6. Clause Version
| Field | Type |
|---|---|
| clause | Link: Clause |
| version_no | Int |
| effective_from | Date |
| effective_to | Date |
| language | Select |
| text | Text Editor |
| fallback_text | Text Editor |
| prohibited_text | Text Editor |
| risk_explanation | Text Editor |
| approved_by | Link: User |
| approval_date | Date |
| status | Select: Draft/Approved/Retired |

## 7. Contract Review
| Field | Type |
|---|---|
| contract | Link: Contract |
| review_type | Select: Legal/Commercial/Finance/Compliance/Security/AI |
| status | Select: Pending/In Progress/Completed/Rejected |
| assigned_to | Link: User |
| due_date | Date |
| started_on | Datetime |
| completed_on | Datetime |
| decision | Select |
| comments | Text Editor |
| risk_score | Float |
| source_version | Link: Contract Version |

## 8. Negotiation Round
| Field | Type |
|---|---|
| contract | Link: Contract |
| round_no | Int |
| participant_type | Select: Internal/Counterparty |
| participant | Link: User or Contact |
| submitted_by | Data |
| submitted_on | Datetime |
| version_in | Link: Contract Version |
| version_out | Link: Contract Version |
| change_count | Int |
| issue_count | Int |
| ai_summary | Long Text |
| status | Select: Open/Resolved/Cancelled |

## 9. Negotiation Issue
| Field | Type |
|---|---|
| negotiation_round | Link: Negotiation Round |
| clause | Link: Clause |
| issue_type | Select: Liability/Payment/Termination/IP/Privacy/SLA/Other |
| severity | Select: Low/Medium/High/Critical |
| counterparty_position | Text Editor |
| company_position | Text Editor |
| fallback_position | Text Editor |
| recommended_action | Text Editor |
| requires_approval | Check |
| status | Select: Open/Accepted/Rejected/Resolved |

## 10. Approval Matrix
| Field | Type |
|---|---|
| name | Data |
| active | Check |
| contract_type | Link: Contract Type |
| company | Link: Company |
| conditions | JSON / child rules |
| fallback_approver_role | Link: Role |

## 11. Contract Approval
| Field | Type |
|---|---|
| contract | Link: Contract |
| matrix | Link: Approval Matrix |
| approval_status | Select: Pending/Approved/Rejected/Cancelled |
| current_step | Int |
| requested_on | Datetime |
| completed_on | Datetime |
| final_decision | Select |
| comments | Text Editor |

## 12. Contract Approval Step
| Field | Type |
|---|---|
| contract_approval | Link: Contract Approval |
| step_no | Int |
| approver_type | Select: User/Role/Department/Rule |
| approver | Link: User |
| approver_role | Link: Role |
| status | Select: Pending/Approved/Rejected/Skipped |
| due_date | Date |
| acted_on | Datetime |
| comments | Text Editor |

## 13. Signature Request
| Field | Type |
|---|---|
| contract | Link: Contract |
| provider | Link: Signature Provider |
| provider_request_id | Data |
| status | Select: Draft/Sent/Viewed/Partially Signed/Completed/Declined/Expired/Cancelled |
| signing_url | Data |
| sent_on | Datetime |
| completed_on | Datetime |
| expires_on | Datetime |
| identity_verification_required | Check |
| notary_required | Check |
| idempotency_key | Data |
| raw_provider_response | Code/JSON |

## 14. Signature Request Signer
| Field | Type |
|---|---|
| signature_request | Link: Signature Request |
| order_no | Int |
| signer_type | Select: Internal/Counterparty/Witness/Notary |
| contact | Link: Contact |
| user | Link: User |
| email | Data |
| phone | Data |
| authentication_method | Select: Email/OTP/SMS/Identity Provider |
| required | Check |
| status | Select: Pending/Sent/Viewed/Signed/Declined |
| signed_on | Datetime |

## 15. Contract Obligation
| Field | Type |
|---|---|
| contract | Link: Contract |
| clause | Link: Clause |
| obligation_type | Select |
| title | Data |
| description | Text Editor |
| obligated_party | Data |
| beneficiary_party | Data |
| owner | Link: User |
| department | Link: Department |
| start_date | Date |
| due_date | Date |
| recurrence | Select/Duration |
| trigger_type | Select: Date/Delivery/Event/Payment/Manual |
| priority | Select |
| status | Select: Open/In Progress/Completed/Overdue/Cancelled/Waived |
| evidence_required | Check |
| evidence_file | Attach |
| penalty_value | Currency |
| currency | Link: Currency |
| escalation_days | Int |
| source_evidence | Link: AI Evidence Reference |

## 16. Contract Renewal
| Field | Type |
|---|---|
| contract | Link: Contract |
| renewal_type | Select: Auto/Manual/Extension |
| current_expiration_date | Date |
| notice_period_days | Int |
| notice_deadline | Date |
| renewal_start_date | Date |
| renewal_end_date | Date |
| status | Select: Not Started/In Progress/Renewed/Not Renewed/Expired |
| owner | Link: User |
| decision | Select: Renew/Negotiate/Terminate/Undecided |
| renewal_value | Currency |
| ai_brief | Long Text |

## 17. Contract Amendment
| Field | Type |
|---|---|
| parent_contract | Link: Contract |
| amendment_contract | Link: Contract |
| amendment_no | Data |
| reason | Text Editor |
| effective_date | Date |
| change_summary | Text Editor |
| financial_impact | Currency |
| status | Select: Draft/Review/Approved/Signed/Effective/Cancelled |

## 18. Contract Performance Metric
| Field | Type |
|---|---|
| contract | Link: Contract |
| metric_name | Data |
| metric_type | Select: SLA/KPI/Financial/Volume/Quality/Compliance |
| target | Float |
| unit | Data |
| direction | Select: Higher Better/Lower Better/Range |
| source_type | Select: Manual/ERPNext/API/AI |
| source_reference | Data |
| owner | Link: User |
| active | Check |

## 19. Contract Performance Period
| Field | Type |
|---|---|
| metric | Link: Contract Performance Metric |
| period_start | Date |
| period_end | Date |
| target_value | Float |
| actual_value | Float |
| score | Float |
| status | Select: On Track/At Risk/Breached |
| evidence | Attach |
| notes | Text Editor |

## 20. AI Review
| Field | Type |
|---|---|
| contract | Link: Contract |
| contract_version | Link: Contract Version |
| provider | Link: AI Model Provider |
| model | Data |
| prompt_policy | Link: AI Prompt Policy |
| status | Select: Queued/Running/Completed/Failed/Needs Review |
| started_on | Datetime |
| completed_on | Datetime |
| confidence | Float |
| token_input | Int |
| token_output | Int |
| estimated_cost | Currency |
| summary | Long Text |
| raw_result | Code/JSON |

## 21. AI Extracted Field
| Field | Type |
|---|---|
| ai_review | Link: AI Review |
| field_name | Data |
| value_text | Long Text |
| value_number | Float |
| value_date | Date |
| value_boolean | Check |
| confidence | Float |
| page_number | Int |
| evidence_text | Long Text |
| bounding_box | JSON |
| normalized_value | Long Text |
| accepted | Check |
| accepted_by | Link: User |

## 22. AI Risk Finding
| Field | Type |
|---|---|
| ai_review | Link: AI Review |
| risk_category | Select |
| severity | Select: Low/Medium/High/Critical |
| score | Float |
| clause_reference | Data |
| evidence | Long Text |
| rationale | Long Text |
| standard_position | Long Text |
| recommended_action | Long Text |
| required_approval | Check |
| status | Select: Open/Acknowledged/Resolved/Waived |
| owner | Link: User |

## 23. AI Agent / AI Agent Run / AI Agent Action
### AI Agent
- name
- code
- description
- active
- agent_type
- allowed_tools
- system_policy
- model_provider
- model
- requires_human_approval
- max_actions_per_run
- allowed_contract_types
- allowed_roles

### AI Agent Run
- agent
- initiated_by
- trigger_type
- input_reference
- status
- started_on
- completed_on
- summary
- trace_id
- cost

### AI Agent Action
- agent_run
- action_type
- target_doctype
- target_name
- proposed_change
- action_status
- approved_by
- approved_on
- executed_on
- result
- error

## 24. Legal Hold
| Field | Type |
|---|---|
| contract | Link: Contract |
| hold_reason | Text Editor |
| issued_by | Link: User |
| issued_on | Datetime |
| release_on | Datetime |
| status | Select: Active/Released |
| scope_description | Long Text |
