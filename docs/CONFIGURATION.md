# Configuration Guide

## 1. Single Settings Overview

### Contract Management Settings
Navigate to **Desk > Contract Management Settings**:
- `default_contract_timezone`: Default timezone for notice calculation (e.g., `UTC`, `America/New_York`).
- `default_currency`: Base portfolio reporting currency.
- `auto_generate_obligations`: Automatically create obligation rows on contract execution (Default: Enabled).
- `retention_period_years`: Archive retention lifespan (Default: 7 years).
- `enable_ai_intake_screening`: Automated risk score calculation on new requests.

### AI Settings
Navigate to **Desk > AI Settings**:
- `default_provider`: Select between `Mock` (deterministic offline engine) or `OpenAI` (cloud API).
- `api_key`: Secret API key for OpenAI or compatible LLM provider.
- `model_name`: Target LLM model (e.g. `gpt-4o-mini`, `gpt-4o`).
- `confidence_threshold`: Minimum confidence score (0.0 to 1.0) required to update canonical contract fields automatically. Fields below this threshold will be flagged for human review.

### Contract ERPNext Integration Settings
Navigate to **Desk > Contract ERPNext Integration Settings**:
- `auto_sync_erp_transactions`: Automatically sync Orders and Invoices to Contract ERP References.
- `uncontracted_spend_threshold`: Transaction value threshold above which uncontracted purchase orders will trigger commercial alerts.
- `enable_price_variance_audits`: Enables automatic price-list vs invoice item rate comparison.

## 2. Setting Up Approval Matrices

Navigate to **Desk > Approval Matrix**:
Create approval matrices to define who approves contracts based on value and risk:
- Min / Max contract values (e.g. $250,000 -> Finance Approver, $1,000,000 -> CFO, $5,000,000 -> CEO).
- Critical risk triggers (e.g., contracts containing non-standard clauses route to General Counsel).

## 3. Playbooks and Negotiation Rules

Navigate to **Desk > Clause Playbook**:
Define acceptable fallback clauses, negotiation guidance, and unacceptable triggers (e.g. "unlimited liability") to automate redline issue detection.
