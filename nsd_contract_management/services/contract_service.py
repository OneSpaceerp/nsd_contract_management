# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import now_datetime, getdate, nowdate


VALID_TRANSITIONS = {
	"Draft": ["Intake", "In Review", "Cancelled", "On Hold"],
	"Intake": ["In Review", "Draft", "Rejected", "Cancelled"],
	"In Review": ["Negotiation", "Approval Pending", "Draft", "Rejected", "Cancelled", "On Hold"],
	"Negotiation": ["In Review", "Approval Pending", "Rejected", "Cancelled", "On Hold"],
	"Approval Pending": ["Approved", "In Review", "Rejected", "Cancelled", "On Hold"],
	"Approved": ["Signature Pending", "In Review", "Cancelled", "On Hold"],
	"Signature Pending": ["Executed", "Approved", "Cancelled", "On Hold"],
	"Executed": ["Effective", "Terminated", "Archived", "On Hold"],
	"Effective": ["Expiring", "Renewal In Progress", "Amendment In Progress", "Terminated", "Expired", "Archived", "On Hold"],
	"Expiring": ["Renewal In Progress", "Expired", "Terminated", "Effective"],
	"Renewal In Progress": ["Effective", "Expired", "Terminated"],
	"Amendment In Progress": ["Effective", "Terminated"],
	"Terminated": ["Archived"],
	"Expired": ["Archived", "Renewal In Progress"],
	"Archived": [],
	"Rejected": ["Draft"],
	"Cancelled": ["Draft"],
	"On Hold": ["Draft", "In Review", "Negotiation", "Approval Pending", "Approved", "Signature Pending", "Executed", "Effective"],
}


def create_contract(data: dict) -> str:
	"""Creates a new Contract document with validated default values and parties."""
	doc = frappe.new_doc("Contract")
	doc.update(data)
	if not doc.contract_timezone:
		doc.contract_timezone = frappe.db.get_single_value("Contract Management Settings", "default_contract_timezone") or "UTC"
	doc.status = "Draft"
	doc.insert()
	return doc.name


def transition_status(contract_name: str, target_status: str, reason: str = None) -> None:
	"""Validates and applies a deterministic status transition to a Contract."""
	contract = frappe.get_doc("Contract", contract_name)
	current_status = contract.status

	if contract.legal_hold and target_status in ["Cancelled", "Terminated", "Archived"]:
		frappe.throw(
			_("Contract {0} is under an active Legal Hold and cannot be moved to {1}.").format(contract_name, target_status),
			frappe.PermissionError
		)

	allowed = VALID_TRANSITIONS.get(current_status, [])
	if target_status not in allowed:
		frappe.throw(
			_("Invalid lifecycle transition from '{0}' to '{1}' for Contract {2}.").format(
				current_status, target_status, contract_name
			),
			frappe.ValidationError
		)

	# Transition prerequisites
	if target_status == "Signature Pending":
		validate_approvals_completed(contract_name)
	elif target_status == "Executed":
		contract.executed = 1
		contract.executed_on = now_datetime()

	contract.status = target_status
	if reason:
		contract.sub_status = reason
	contract.save()

	# Post-transition side effects
	if target_status == "Executed":
		on_contract_executed(contract)


def validate_approvals_completed(contract_name: str) -> None:
	"""Ensures that all mandatory approval steps have been approved before signature."""
	pending_approvals = frappe.db.count(
		"Contract Approval",
		{"contract": contract_name, "approval_status": "Pending"}
	)
	if pending_approvals > 0:
		frappe.throw(
			_("Contract {0} has pending approval processes that must be completed before signature.").format(contract_name),
			frappe.ValidationError
		)


def on_contract_executed(contract) -> None:
	"""Triggers post-signature automations: obligation generation, renewals, ERPNext sync."""
	from nsd_contract_management.services.contract_version_service import seal_executed_version
	from nsd_contract_management.services.renewal_service import schedule_renewal_if_applicable
	from nsd_contract_management.services.obligation_service import activate_contract_obligations

	if contract.current_version:
		seal_executed_version(contract.current_version)

	schedule_renewal_if_applicable(contract.name)
	activate_contract_obligations(contract.name)


def submit_for_review(contract_name: str) -> None:
	transition_status(contract_name, "In Review")


def start_negotiation(contract_name: str) -> None:
	transition_status(contract_name, "Negotiation")


def mark_approved(contract_name: str) -> None:
	transition_status(contract_name, "Approved")


def send_for_signature(contract_name: str) -> None:
	transition_status(contract_name, "Signature Pending")


def mark_executed(contract_name: str, signed_document: str = None) -> None:
	if signed_document:
		frappe.db.set_value("Contract", contract_name, "signed_document", signed_document)
	transition_status(contract_name, "Executed")


def activate_contract(contract_name: str) -> None:
	transition_status(contract_name, "Effective")


def put_on_hold(contract_name: str, reason: str = None) -> None:
	transition_status(contract_name, "On Hold", reason=reason)


def resume_from_hold(contract_name: str, target_status: str) -> None:
	transition_status(contract_name, target_status)


def terminate_contract(contract_name: str, reason: str, termination_type: str = "For Convenience") -> None:
	term_doc = frappe.new_doc("Contract Termination")
	term_doc.contract = contract_name
	term_doc.termination_type = termination_type
	term_doc.effective_date = nowdate()
	term_doc.reason = reason
	term_doc.status = "Approved"
	term_doc.insert()

	transition_status(contract_name, "Terminated", reason=reason)
