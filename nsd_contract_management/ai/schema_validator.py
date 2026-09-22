# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

from typing import Dict, Any, List


CANONICAL_CONTRACT_SCHEMA = {
	"type": "object",
	"properties": {
		"title": {"type": "string"},
		"agreement_number": {"type": "string"},
		"parties": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"party_name": {"type": "string"},
					"party_role": {"type": "string"},
					"country": {"type": "string"}
				},
				"required": ["party_name"]
			}
		},
		"effective_date": {"type": "string"},
		"end_date": {"type": "string"},
		"total_contract_value": {"type": "number"},
		"currency": {"type": "string"},
		"payment_terms": {"type": "string"},
		"auto_renewal": {"type": "boolean"},
		"notice_period_days": {"type": "integer"},
		"governing_law": {"type": "string"},
		"liability_cap": {"type": "string"},
		"extracted_clauses": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"category": {"type": "string"},
					"title": {"type": "string"},
					"text": {"type": "string"},
					"confidence": {"type": "number"},
					"page_number": {"type": "integer"}
				}
			}
		},
		"risk_findings": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"category": {"type": "string"},
					"risk_level": {"type": "string"},
					"description": {"type": "string"},
					"evidence": {"type": "string"}
				}
			}
		}
	}
}


def validate_extraction_result(data: Any) -> Dict[str, Any]:
	"""
	Validates and normalizes extracted contract data to conform to the canonical structure.
	Ensures safe defaults and correct types.
	"""
	if not isinstance(data, dict):
		return {}

	normalized = {
		"title": str(data.get("title") or "Untitled Extracted Contract"),
		"agreement_number": str(data.get("agreement_number") or ""),
		"parties": [],
		"effective_date": str(data.get("effective_date") or ""),
		"end_date": str(data.get("end_date") or ""),
		"total_contract_value": float(data.get("total_contract_value") or 0.0),
		"currency": str(data.get("currency") or "USD").upper(),
		"payment_terms": str(data.get("payment_terms") or ""),
		"auto_renewal": bool(data.get("auto_renewal")),
		"notice_period_days": int(data.get("notice_period_days") or 30),
		"governing_law": str(data.get("governing_law") or ""),
		"liability_cap": str(data.get("liability_cap") or ""),
		"extracted_clauses": [],
		"risk_findings": []
	}

	for p in data.get("parties", []):
		if isinstance(p, dict) and p.get("party_name"):
			normalized["parties"].append({
				"party_name": str(p.get("party_name")),
				"party_role": str(p.get("party_role") or "Third Party"),
				"country": str(p.get("country") or "")
			})

	for c in data.get("extracted_clauses", []):
		if isinstance(c, dict):
			normalized["extracted_clauses"].append({
				"category": str(c.get("category") or "General"),
				"title": str(c.get("title") or "Clause"),
				"text": str(c.get("text") or ""),
				"confidence": float(c.get("confidence") or 0.85),
				"page_number": int(c.get("page_number") or 1)
			})

	for r in data.get("risk_findings", []):
		if isinstance(r, dict):
			normalized["risk_findings"].append({
				"category": str(r.get("category") or "Operational"),
				"risk_level": str(r.get("risk_level") or "Medium"),
				"description": str(r.get("description") or ""),
				"evidence": str(r.get("evidence") or "")
			})

	return normalized
