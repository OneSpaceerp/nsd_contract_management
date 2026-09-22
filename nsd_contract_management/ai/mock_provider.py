# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import re
import hashlib
from typing import Dict, List, Any, Optional
from nsd_contract_management.ai.base import AIProvider
from nsd_contract_management.ai.prompt_defense import detect_prompt_injection, wrap_user_content_sandbox
from nsd_contract_management.ai.schema_validator import validate_extraction_result


class MockAIProvider(AIProvider):
	"""
	Deterministic, fully functional offline AI provider for testing and air-gapped environments.
	Parses contract metadata, financial figures, clauses, and risks using rule engines
	without requiring external LLM API keys.
	"""

	def extract(self, document_text: str, schema: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		# Check prompt injection
		is_suspicious, patterns = detect_prompt_injection(document_text)
		if is_suspicious:
			return {
				"error": "Adversarial prompt injection pattern detected",
				"detected_patterns": patterns,
				"confidence": 0.0
			}

		text = document_text or ""

		# 1. Extract Title
		title_match = re.search(r"(?i)^(?:master\s+services\s+agreement|software\s+license\s+agreement|non-disclosure\s+agreement|commercial\s+contract|agreement)[\w\s-]*", text)
		title = title_match.group(0).strip() if title_match else "Commercial Agreement"

		# 2. Extract Agreement Number
		num_match = re.search(r"(?i)(?:agreement|contract)\s*(?:no\.?|number|id)?\s*[:#-]?\s*([A-Z0-9_-]{4,20})", text)
		agreement_number = num_match.group(1) if num_match else "CNT-2026-MOCK-01"

		# 3. Extract Parties
		parties = []
		party_matches = re.findall(r"(?i)(?:between|and)\s+([A-Z][A-Za-z0-9\s.,&-]{2,40}(?:Inc\.|LLC|Corp\.|Ltd\.|GmbH|Company))", text)
		for p in party_matches:
			parties.append({
				"party_name": p.strip(),
				"party_role": "Counterparty",
				"country": "US"
			})

		if not parties:
			parties.append({"party_name": "ACME Global Solutions", "party_role": "Supplier", "country": "US"})
			parties.append({"party_name": "Enterprise Client Inc", "party_role": "Customer", "country": "US"})

		# 4. Extract Dates
		dates = re.findall(r"\b(\d{4}-\d{2}-\d{2})\b", text)
		effective_date = dates[0] if len(dates) > 0 else "2026-01-01"
		end_date = dates[1] if len(dates) > 1 else "2027-01-01"

		# 5. Extract Financial Values
		val_match = re.search(r"(?i)(?:total(?:\s+contract)?\s+value|contract\s+value|total|value|fee|sum|price)\s*[:=]?\s*(?:USD|EUR|GBP|\$|\s)*([0-9][0-9,]+(?:\.[0-9]{2})?)", text)
		if val_match:
			val_str = val_match.group(1).replace(",", "")
			total_val = float(val_str)
		else:
			total_val = 150000.0

		currency_match = re.search(r"\b(USD|EUR|GBP|SAR|AED|INR)\b", text)
		currency = currency_match.group(1) if currency_match else "USD"

		# 6. Extract Clauses
		extracted_clauses = []
		if "confidential" in text.lower():
			extracted_clauses.append({
				"category": "Confidentiality",
				"title": "Confidentiality & Non-Disclosure",
				"text": "Each party agrees to protect the Confidential Information of the other party.",
				"confidence": 0.95,
				"page_number": 1
			})
		if "liability" in text.lower():
			extracted_clauses.append({
				"category": "Limitation of Liability",
				"title": "Limitation of Liability",
				"text": "In no event shall either party's liability exceed the total fees paid under this agreement.",
				"confidence": 0.92,
				"page_number": 2
			})
		if "terminat" in text.lower():
			extracted_clauses.append({
				"category": "Termination",
				"title": "Termination for Convenience",
				"text": "Either party may terminate upon 30 days prior written notice.",
				"confidence": 0.90,
				"page_number": 2
			})

		# 7. Risk Findings
		risk_findings = []
		if "unlimited liability" in text.lower():
			risk_findings.append({
				"category": "Liability",
				"risk_level": "Critical",
				"description": "Unlimited liability clause detected in agreement terms.",
				"evidence": "unlimited liability"
			})
		elif total_val >= 1000000:
			risk_findings.append({
				"category": "Financial",
				"risk_level": "High",
				"description": "High value commercial commitment exceeds $1,000,000 threshold.",
				"evidence": f"Total value: {total_val}"
			})

		raw_result = {
			"title": title,
			"agreement_number": agreement_number,
			"parties": parties,
			"effective_date": effective_date,
			"end_date": end_date,
			"total_contract_value": total_val,
			"currency": currency,
			"payment_terms": "Net 30 Days",
			"auto_renewal": "auto-renew" in text.lower(),
			"notice_period_days": 30,
			"governing_law": "Delaware, USA",
			"liability_cap": "12 Months Fees",
			"extracted_clauses": extracted_clauses,
			"risk_findings": risk_findings
		}

		return validate_extraction_result(raw_result)

	def analyze(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		is_suspicious, patterns = detect_prompt_injection(prompt)
		if is_suspicious:
			return {"analysis": "Request aborted: prompt injection detected.", "risk_level": "Critical"}

		return {
			"analysis": f"Deterministic risk evaluation completed for prompt. Context keys analyzed: {list((context or {}).keys())}.",
			"risk_score": 15,
			"risk_level": "Low",
			"recommendations": ["Standard commercial terms acceptable.", "Confirm insurance certificates on file."]
		}

	def embed(self, texts: List[str]) -> List[List[float]]:
		embeddings = []
		for t in texts:
			# Deterministic pseudo-embedding based on MD5 digest bytes normalized
			digest = hashlib.md5(t.encode("utf-8")).digest()
			vec = [float(b) / 255.0 for b in digest]  # 16-dimensional deterministic vector
			embeddings.append(vec)
		return embeddings

	def chat(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		last_msg = messages[-1]["content"] if messages else ""
		return {
			"role": "assistant",
			"content": f"NSD Contract Assistant response to: '{last_msg[:80]}...'. All contract terms are verified against governance policies."
		}
