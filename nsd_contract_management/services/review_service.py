# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import now_datetime
from nsd_contract_management.services.contract_service import transition_status


def start_review(
	contract_name: str,
	review_type: str = "Internal",
	reviewers: list = None,
	due_date: str = None,
	notes: str = None
) -> str:
	"""Initiates a formal review cycle for a Contract and assigns reviewers."""
	contract = frappe.get_doc("Contract", contract_name)

	# Transition contract to In Review if not already
	if contract.status != "In Review":
		transition_status(contract_name, "In Review", reason="Review cycle started")

	review_doc = frappe.new_doc("Contract Review")
	review_doc.contract = contract_name
	review_doc.review_type = review_type
	review_doc.status = "In Progress"
	review_doc.due_date = due_date
	review_doc.notes = notes
	review_doc.version = contract.current_version
	review_doc.insert()

	if reviewers:
		for r in reviewers:
			frappe.get_doc({
				"doctype": "ToDo",
				"allocated_to": r,
				"reference_type": "Contract Review",
				"reference_name": review_doc.name,
				"description": f"Review requested for contract: {contract.title}"
			}).insert(ignore_permissions=True)

	return review_doc.name


def submit_review_feedback(
	review_name: str,
	reviewer: str,
	decision: str,
	feedback_text: str = None
) -> None:
	"""
	Records feedback and decision (Approved, Changes Requested, Rejected) from a reviewer.
	"""
	review = frappe.get_doc("Contract Review", review_name)
	if review.status in ["Completed", "Cancelled"]:
		frappe.throw(_("Contract Review {0} is already closed.").format(review_name))

	if decision not in ["Approved", "Changes Requested", "Rejected"]:
		frappe.throw(_("Invalid decision '{0}'. Must be Approved, Changes Requested, or Rejected.").format(decision))

	# Record comment
	frappe.get_doc({
		"doctype": "Comment",
		"comment_type": "Comment",
		"reference_doctype": "Contract Review",
		"reference_name": review_name,
		"content": f"**Decision: {decision}** by {reviewer}\n\n{feedback_text or ''}"
	}).insert(ignore_permissions=True)

	# Update review status
	if decision == "Rejected":
		review.db_set("status", "Rejected")
	elif decision == "Changes Requested":
		review.db_set("status", "Changes Requested")
	elif decision == "Approved":
		review.db_set("status", "Approved")


def complete_review(review_name: str) -> None:
	"""Finalizes the review cycle and updates status."""
	review = frappe.get_doc("Contract Review", review_name)
	review.db_set("status", "Completed")

	frappe.get_doc({
		"doctype": "Comment",
		"comment_type": "Info",
		"reference_doctype": "Contract",
		"reference_name": review.contract,
		"content": _("Review cycle {0} completed.").format(review_name)
	}).insert(ignore_permissions=True)
