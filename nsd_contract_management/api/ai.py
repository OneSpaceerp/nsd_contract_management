# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from nsd_contract_management.services.ai_service import extract_contract, ask_contract, get_active_ai_provider
from nsd_contract_management.services.contract_version_service import compare_versions
from nsd_contract_management.services.agent_service import run_agent, approve_agent_action


@frappe.whitelist()
def extract(contract_name: str, document_text: str = None) -> dict:
	"""RPC: Triggers AI contract extraction pipeline."""
	review_name = extract_contract(contract_name, document_text=document_text)
	return {"review_name": review_name}


@frappe.whitelist()
def review(contract_name: str) -> dict:
	"""RPC: AI contract review alias."""
	return extract(contract_name)


@frappe.whitelist()
def compare(version_a: str, version_b: str) -> dict:
	"""RPC: Compares two versions returning diff and line metrics."""
	return compare_versions(version_a, version_b)


@frappe.whitelist()
def ask(contract_name: str, question: str) -> dict:
	"""RPC: Grounded question answering on specific contract."""
	answer = ask_contract(contract_name, question)
	return {"contract": contract_name, "answer": answer}


@frappe.whitelist()
def ask_portfolio(question: str) -> dict:
	"""RPC: Portfolio-wide intelligence query across active contracts."""
	active_count = frappe.db.count("Contract", {"status": "Effective"})
	provider = get_active_ai_provider()
	prompt = f"Portfolio contains {active_count} active contracts. Answer question: {question}"
	res = provider.analyze(prompt, {"scope": "portfolio"})
	return {"question": question, "answer": res.get("analysis")}


@frappe.whitelist()
def run_ai_agent(agent_name: str, contract_name: str = None) -> dict:
	"""RPC: Runs autonomous AI agent workflow."""
	run_name = run_agent(agent_name, contract_name=contract_name)
	return {"agent_run": run_name}


@frappe.whitelist()
def approve_action(action_name: str) -> dict:
	"""RPC: HITL approval of autonomous agent action."""
	return approve_agent_action(action_name, approver=frappe.session.user)
