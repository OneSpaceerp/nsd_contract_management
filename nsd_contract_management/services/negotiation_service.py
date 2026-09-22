# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import now_datetime
from nsd_contract_management.services.contract_service import transition_status
from nsd_contract_management.services.playbook_service import evaluate_clause_against_playbook
from nsd_contract_management.services.contract_version_service import create_version, get_latest_version


def create_negotiation_round(
	contract_name: str,
	counterparty_contact: str = None,
	counterparty_entity: str = None,
	notes: str = None
) -> str:
	"""Starts a new negotiation round for the contract."""
	contract = frappe.get_doc("Contract", contract_name)
	if contract.status not in ["Negotiation", "In Review", "Draft"]:
		frappe.throw(
			_("Contract {0} cannot enter negotiation from status {1}.").format(contract_name, contract.status),
			frappe.ValidationError
		)

	if contract.status != "Negotiation":
		transition_status(contract_name, "Negotiation", reason="Negotiation round opened")

	existing_rounds = frappe.db.count("Negotiation Round", {"contract": contract_name})
	round_number = existing_rounds + 1

	round_doc = frappe.new_doc("Negotiation Round")
	round_doc.contract = contract_name
	round_doc.round_number = round_number
	round_doc.status = "Open"
	round_doc.counterparty_contact = counterparty_contact
	round_doc.counterparty_entity = counterparty_entity
	round_doc.summary = notes or f"Negotiation Round #{round_number}"
	round_doc.insert()

	return round_doc.name


def import_redline(
	round_name: str,
	redline_text: str = None,
	redline_file: str = None,
	summary: str = None
) -> list:
	"""
	Parses incoming counterparty redlines, evaluates clauses against company playbook,
	and creates tracked Negotiation Issue records for review.
	"""
	neg_round = frappe.get_doc("Negotiation Round", round_name)
	contract = frappe.get_doc("Contract", neg_round.contract)

	if redline_file:
		neg_round.received_file = redline_file
		neg_round.save()

	created_issues = []
	# For each clause in the contract, compare with redline if text is available
	current_ver = get_latest_version(contract.name)
	current_text = current_ver.content if current_ver else ""

	# Simple redline clause extraction or direct evaluation
	for c_row in contract.get("clauses", []):
		category = c_row.category or c_row.clause_title
		analysis = evaluate_clause_against_playbook(
			clause_category=category,
			proposed_text=c_row.clause_text or ""
		)

		if analysis.get("classification") in ["Acceptable Fallback", "Non-Standard", "Unacceptable"]:
			issue = frappe.new_doc("Negotiation Issue")
			issue.negotiation_round = round_name
			issue.contract = contract.name
			issue.clause = c_row.clause
			issue.clause_category = category
			issue.issue_title = f"{c_row.clause_title} - {analysis.get('classification')}"
			issue.original_text = c_row.clause_text
			issue.proposed_text = c_row.clause_text
			issue.status = "Open"
			issue.risk_level = analysis.get("risk_level", "Medium")
			issue.resolution_notes = f"Playbook Guidance: {analysis.get('guidance')}"
			issue.insert()
			created_issues.append(issue.name)

	return created_issues


def resolve_issue(
	issue_name: str,
	resolution: str,
	agreed_text: str = None,
	resolved_by: str = None
) -> None:
	"""Marks a negotiation issue as Resolved, Accepted, or Rejected."""
	issue = frappe.get_doc("Negotiation Issue", issue_name)
	if issue.status in ["Resolved", "Accepted", "Rejected", "Waived"]:
		frappe.throw(_("Issue {0} is already closed ({1}).").format(issue_name, issue.status))

	issue.status = resolution
	if agreed_text:
		issue.agreed_text = agreed_text
	issue.resolved_by = resolved_by or frappe.session.user
	issue.save()

	# Check if all issues in round are now resolved
	open_issues = frappe.db.count("Negotiation Issue", {
		"negotiation_round": issue.negotiation_round,
		"status": ["in", ["Open", "In Review", "Escalated"]]
	})

	if open_issues == 0:
		frappe.db.set_value("Negotiation Round", issue.negotiation_round, "status", "Resolved")


def close_round(round_name: str, create_new_version_doc: bool = True) -> str:
	"""
	Closes the negotiation round. Optionally compiles agreed terms into a new Contract Version.
	"""
	neg_round = frappe.get_doc("Negotiation Round", round_name)
	neg_round.status = "Closed"
	neg_round.save()

	new_version_name = None
	if create_new_version_doc:
		contract = frappe.get_doc("Contract", neg_round.contract)
		# Assemble updated content
		clauses_content = []
		for c in contract.get("clauses", []):
			clauses_content.append(f"## {c.clause_title}\n{c.clause_text or ''}\n")

		updated_body = f"# {contract.title}\n\n" + "\n".join(clauses_content)
		new_version_name = create_version(
			contract_name=contract.name,
			title=f"{contract.title} - Post-Round {neg_round.round_number}",
			content=updated_body,
			change_summary=f"Negotiation round #{neg_round.round_number} terms incorporated."
		)

	return new_version_name or round_name
