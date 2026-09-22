# AI Governance & Contract Intelligence Architecture

## 1. Principles of AI Governance
NSD Contract Management treats AI as an advisory and acceleration layer, not an unmonitored decision-maker. All AI actions adhere to three core pillars:
1. **Explainability & Grounded Evidence**: Extracted fields and identified risks must reference source text snippets and page numbers.
2. **Defensive Processing**: Untrusted document inputs are inspected for prompt injection and wrapped in passive delimiter sandboxes.
3. **Human-In-The-Loop (HITL) Safety Gates**: High-risk actions (e.g. creating transactional documents, modifying contracts, releasing holds) require explicit human review.

## 2. Extraction Pipeline
```text
Document Upload / Version
        ↓
Prompt Injection Scan (nsd_contract_management.ai.prompt_defense)
        ↓
Passive XML Sandboxing (<CONTRACT_TEXT_DATA>)
        ↓
Provider Extraction (MockProvider or OpenAIProvider)
        ↓
Canonical Schema Normalization (nsd_contract_management.ai.schema_validator)
        ↓
Record Generation:
- AI Review (summary, overall confidence)
- AI Extracted Field (per-field confidence score)
- AI Risk Finding (severity, evidence snippet)
        ↓
Confidence Evaluation against AI Settings:
- Score >= Threshold (e.g. 0.85): Canonical Contract fields updated.
- Score < Threshold: Flagged as 'Pending Review' for manual confirmation.
```

## 3. Autonomous AI Agents
Autonomous agents (`AI Agent`, `AI Agent Run`, `AI Agent Action`) automate background workflows:
- **Commercial Leakage Investigator**: Audits order lines against contracted rates.
- **Obligation Auditor**: Flags missing fulfillment evidence.
- **Renewal Scout**: Prepares executive briefings before notice windows close.

Each action produced by an agent with `requires_approval = 1` remains in `Pending Approval` until authorized via `approve_agent_action`.
