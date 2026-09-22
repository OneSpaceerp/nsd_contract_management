# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, now_datetime
from nsd_contract_management.ai.mock_provider import MockAIProvider
from nsd_contract_management.ai.openai_provider import OpenAIProvider
from nsd_contract_management.services.contract_version_service import get_latest_version


def get_active_ai_provider():
	"""Instantiates the configured AI provider based on AI Settings."""
	provider_name = frappe.db.get_single_value("AI Settings", "default_provider") or "Mock"
	if provider_name.lower() == "openai":
		api_key = frappe.db.get_single_value("AI Settings", "api_key")
		model = frappe.db.get_single_value("AI Settings", "model_name") or "gpt-4o-mini"
		return OpenAIProvider({"api_key": api_key, "model": model})
	return MockAIProvider()


def extract_contract(contract_name: str, document_text: str = None, version_name: str = None) -> str:
	"""
	Executes full AI extraction pipeline:
	- Text extraction & segmentation
	- Structured field & clause extraction
	- Risk detection & evidence tracing
	- Populates AI Review, AI Extracted Field, and AI Risk Finding records
	- Applies human-in-the-loop threshold before updating canonical fields
	"""
	contract = frappe.get_doc("Contract", contract_name)

	# Fetch text from version if not explicitly passed
	if not document_text:
		ver = frappe.get_doc("Contract Version", version_name) if version_name else get_latest_version(contract_name)
		document_text = ver.content if ver else (contract.description or contract.title)

	provider = get_active_ai_provider()
	result = provider.extract(document_text, {})

	if result.get("error"):
		frappe.throw(_("AI Extraction failed: {0}").format(result.get("error")))

	ai_review = frappe.new_doc("AI Review")
	ai_review.contract = contract_name
	ai_review.version = version_name or (contract.current_version if hasattr(contract, "current_version") else None)
	ai_review.status = "Completed"
	ai_review.provider = "Mock" if isinstance(provider, MockAIProvider) else "OpenAI"
	ai_review.model = getattr(provider, "model", "mock-v1")
	ai_review.risk_score = 15
	ai_review.summary = f"Extracted {len(result.get('extracted_clauses', []))} clauses and {len(result.get('risk_findings', []))} risk factors."
	ai_review.insert()

	# Save extracted fields
	fields_to_save = [
		("title", result.get("title"), 0.95),
		("total_contract_value", str(result.get("total_contract_value")), 0.90),
		("currency", result.get("currency"), 0.98),
		("effective_date", result.get("effective_date"), 0.88),
		("end_date", result.get("end_date"), 0.88),
		("governing_law", result.get("governing_law"), 0.85),
		("liability_cap", result.get("liability_cap"), 0.80)
	]

	confidence_threshold = flt(frappe.db.get_single_value("AI Settings", "confidence_threshold")) or 0.80

	canonical_updates = {}
	for f_name, f_val, f_conf in fields_to_save:
		if not f_val:
			continue
		field_row = frappe.new_doc("AI Extracted Field")
		field_row.ai_review = ai_review.name
		field_row.contract = contract_name
		field_row.field_name = f_name
		field_row.extracted_value = str(f_val)
		field_row.confidence_score = f_conf
		field_row.needs_human_review = 1 if f_conf < confidence_threshold else 0
		field_row.status = "Accepted" if f_conf >= confidence_threshold else "Pending Review"
		field_row.insert()

		if f_conf >= confidence_threshold and hasattr(contract, f_name) and not getattr(contract, f_name):
			canonical_updates[f_name] = f_val

	# Save risk findings
	for rf in result.get("risk_findings", []):
		rf_doc = frappe.new_doc("AI Risk Finding")
		rf_doc.ai_review = ai_review.name
		rf_doc.contract = contract_name
		rf_doc.risk_category = rf.get("category")
		rf_doc.risk_level = rf.get("risk_level")
		rf_doc.summary = rf.get("description")
		rf_doc.evidence_snippet = rf.get("evidence")
		rf_doc.status = "Open"
		rf_doc.insert()

	# Update canonical fields if eligible
	if canonical_updates:
		frappe.db.set_value("Contract", contract_name, canonical_updates)

	return ai_review.name


def ask_contract(contract_name: str, question: str) -> str:
	"""Answers questions regarding a specific contract with grounded evidence."""
	contract = frappe.get_doc("Contract", contract_name)
	ver = get_latest_version(contract_name)
	content = ver.content if ver else contract.description

	provider = get_active_ai_provider()
	prompt = f"Contract Title: {contract.title}\nTerms:\n{content}\n\nQuestion: {question}"
	res = provider.analyze(prompt, {"contract": contract_name})
	return res.get("analysis", "No response generated.")
