# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def get_playbook_for_contract(contract_type: str = None, company: str = None):
	"""Returns the most specific active Clause Playbook for the given contract context."""
	filters = {"is_active": 1}
	if contract_type:
		filters["contract_type"] = contract_type
	if company:
		filters["company"] = company

	playbooks = frappe.get_all("Clause Playbook", filters=filters, limit=1)
	if playbooks:
		return frappe.get_doc("Clause Playbook", playbooks[0].name)

	# Fallback to default active playbook
	default_playbooks = frappe.get_all("Clause Playbook", filters={"is_active": 1}, limit=1)
	if default_playbooks:
		return frappe.get_doc("Clause Playbook", default_playbooks[0].name)
	return None


def evaluate_clause_against_playbook(
	clause_category: str,
	proposed_text: str,
	playbook_name: str = None
) -> dict:
	"""
	Compares a proposed clause text against playbook rules to classify risk and recommend negotiation guidance.
	"""
	playbook = frappe.get_doc("Clause Playbook", playbook_name) if playbook_name else get_playbook_for_contract()
	if not playbook:
		return {
			"classification": "Non-Standard",
			"risk_level": "Medium",
			"guidance": "No active playbook found for this category.",
			"fallback_clause": None,
			"escalation_role": "Legal Reviewer"
		}

	matched_rule = None
	for rule in playbook.rules:
		if rule.category == clause_category or rule.clause == clause_category:
			matched_rule = rule
			break

	if not matched_rule:
		return {
			"classification": "Standard" if not proposed_text else "Non-Standard",
			"risk_level": "Low",
			"guidance": f"No specific playbook restriction defined for {clause_category}.",
			"fallback_clause": None,
			"escalation_role": None
		}

	prop_clean = (proposed_text or "").strip().lower()

	# Check standard clause
	std_clause_text = ""
	if matched_rule.standard_clause:
		from nsd_contract_management.services.clause_service import get_clause
		std_info = get_clause(matched_rule.standard_clause)
		std_clause_text = (std_info.get("clause_text") or "").strip().lower()

	if std_clause_text and prop_clean == std_clause_text:
		return {
			"classification": "Standard",
			"risk_level": "Low",
			"guidance": "Matches approved standard company clause exactly.",
			"fallback_clause": matched_rule.standard_clause,
			"escalation_role": None
		}

	# Check unacceptable terms / triggers
	unacceptable_terms = (matched_rule.unacceptable_terms or "").lower().split("\n")
	for term in unacceptable_terms:
		term = term.strip()
		if term and term in prop_clean:
			return {
				"classification": "Unacceptable",
				"risk_level": "Critical",
				"guidance": f"Violates company playbook: contains unacceptable term '{term}'. Escalation mandatory.",
				"fallback_clause": matched_rule.fallback_clause_1 or matched_rule.standard_clause,
				"escalation_role": matched_rule.escalation_role or "General Counsel"
			}

	# If fallback exists, recommend it
	if matched_rule.fallback_clause_1:
		return {
			"classification": "Acceptable Fallback",
			"risk_level": "Medium",
			"guidance": matched_rule.negotiation_guidance or "Non-standard wording detected. Recommend proposing standard Fallback 1.",
			"fallback_clause": matched_rule.fallback_clause_1,
			"escalation_role": matched_rule.escalation_role or "Legal Reviewer"
		}

	return {
		"classification": "Non-Standard",
		"risk_level": "High",
		"guidance": matched_rule.negotiation_guidance or "Custom clause requires legal counsel approval.",
		"fallback_clause": matched_rule.standard_clause,
		"escalation_role": matched_rule.escalation_role or "Legal Reviewer"
	}
