# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from nsd_contract_management.services.negotiation_service import (
	create_negotiation_round, import_redline, resolve_issue, close_round
)


@frappe.whitelist()
def create_round(contract_name: str, counterparty_contact: str = None) -> dict:
	"""RPC: Creates new negotiation round."""
	round_name = create_negotiation_round(contract_name, counterparty_contact=counterparty_contact)
	return {"round_name": round_name}


@frappe.whitelist()
def import_redline_action(round_name: str, redline_text: str = None, redline_file: str = None) -> dict:
	"""RPC: Imports redline document and extracts issues against playbook."""
	issues = import_redline(round_name, redline_text=redline_text, redline_file=redline_file)
	return {"issues_created": len(issues), "issues": issues}


@frappe.whitelist()
def accept_change(issue_name: str, agreed_text: str = None) -> dict:
	"""RPC: Accepts counterparty change."""
	resolve_issue(issue_name, resolution="Accepted", agreed_text=agreed_text)
	return {"issue_name": issue_name, "status": "Accepted"}


@frappe.whitelist()
def reject_change(issue_name: str, explanation: str = None) -> dict:
	"""RPC: Rejects counterparty change."""
	resolve_issue(issue_name, resolution="Rejected", agreed_text=explanation)
	return {"issue_name": issue_name, "status": "Rejected"}


@frappe.whitelist()
def resolve_issue_action(issue_name: str, agreed_text: str = None) -> dict:
	"""RPC: Resolves negotiation issue with compromise text."""
	resolve_issue(issue_name, resolution="Resolved", agreed_text=agreed_text)
	return {"issue_name": issue_name, "status": "Resolved"}


@frappe.whitelist()
def finish_round(round_name: str) -> dict:
	"""RPC: Closes round and updates contract version."""
	new_ver = close_round(round_name)
	return {"round_name": round_name, "version": new_ver}
