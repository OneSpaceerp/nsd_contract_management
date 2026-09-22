# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, now_datetime
from nsd_contract_management.services.contract_service import transition_status


def evaluate_approval_requirements(contract_name: str) -> list:
	"""
	Evaluates active Approval Matrices and workflow conditions against the Contract's
	value, risk level, company, and clauses to determine the sequence of required approval steps.
	"""
	contract = frappe.get_doc("Contract", contract_name)
	val = flt(contract.total_contract_value)
	risk = contract.risk_level or "Low"

	steps = []
	step_num = 1

	# Standard Tier 1: Commercial / Line Manager
	steps.append({
		"step_number": step_num,
		"approver_role": "Contract Manager",
		"is_mandatory": 1,
		"status": "Pending"
	})
	step_num += 1

	# Check high value thresholds
	if val >= 5000000:
		steps.append({
			"step_number": step_num,
			"approver_role": "CEO",
			"is_mandatory": 1,
			"status": "Pending"
		})
		step_num += 1
		steps.append({
			"step_number": step_num,
			"approver_role": "CFO",
			"is_mandatory": 1,
			"status": "Pending"
		})
		step_num += 1
	elif val >= 1000000:
		steps.append({
			"step_number": step_num,
			"approver_role": "CFO",
			"is_mandatory": 1,
			"status": "Pending"
		})
		step_num += 1
	elif val >= 250000:
		steps.append({
			"step_number": step_num,
			"approver_role": "Finance Approver",
			"is_mandatory": 1,
			"status": "Pending"
		})
		step_num += 1

	# Check legal & risk thresholds
	has_non_standard = any(c.is_standard == 0 for c in contract.get("clauses", []))
	if risk in ["Critical", "High"] or has_non_standard:
		steps.append({
			"step_number": step_num,
			"approver_role": "General Counsel" if risk == "Critical" else "Legal Reviewer",
			"is_mandatory": 1,
			"status": "Pending"
		})
		step_num += 1

	return steps


def submit_for_approval(contract_name: str, submitted_by: str = None) -> str:
	"""Creates Contract Approval record and transitions Contract to Approval Pending."""
	contract = frappe.get_doc("Contract", contract_name)
	if contract.status not in ["Draft", "In Review", "Negotiation"]:
		frappe.throw(
			_("Contract {0} cannot be submitted for approval from status '{1}'.").format(contract_name, contract.status),
			frappe.ValidationError
		)

	# Verify active legal hold
	if contract.legal_hold:
		frappe.throw(_("Contract {0} is under Legal Hold and cannot enter approval.").format(contract_name))

	steps = evaluate_approval_requirements(contract_name)

	# Transition contract
	transition_status(contract_name, "Approval Pending", reason="Submitted for multi-tier approval")

	approval = frappe.new_doc("Contract Approval")
	approval.contract = contract_name
	approval.status = "Pending"
	approval.submitted_by = submitted_by or frappe.session.user
	approval.submission_date = now_datetime()
	approval.current_step = 1

	for s in steps:
		approval.append("approval_steps", s)

	approval.insert()

	# Create ToDo for first step
	first_step = approval.approval_steps[0] if approval.approval_steps else None
	if first_step:
		frappe.get_doc({
			"doctype": "ToDo",
			"role": first_step.approver_role,
			"reference_type": "Contract Approval",
			"reference_name": approval.name,
			"description": f"Approval required for contract {contract.title} (Value: {contract.total_contract_value} {contract.currency})"
		}).insert(ignore_permissions=True)

	return approval.name


def approve_step(
	approval_name: str,
	step_idx: int,
	approver: str,
	comments: str = None
) -> None:
	"""Approves an individual step in the approval chain. Advances to next step or executes final approval."""
	approval = frappe.get_doc("Contract Approval", approval_name)
	if approval.status != "Pending":
		frappe.throw(_("Contract Approval {0} is not pending (Current: {1}).").format(approval_name, approval.status))

	target_step = None
	for row in approval.approval_steps:
		if row.idx == step_idx or row.step_number == step_idx:
			target_step = row
			break

	if not target_step:
		frappe.throw(_("Approval step {0} not found.").format(step_idx))

	target_step.status = "Approved"
	target_step.approver_user = approver
	target_step.action_date = now_datetime()
	target_step.comments = comments or "Approved."

	# Check if all steps are now approved
	remaining = [s for s in approval.approval_steps if s.status == "Pending"]
	if not remaining:
		approval.status = "Approved"
		approval.completion_date = now_datetime()
		approval.save()

		# Transition contract to Approved
		transition_status(approval.contract, "Approved", reason="All approval steps successfully completed")
	else:
		approval.current_step = remaining[0].step_number
		approval.save()

		# Notify next role
		frappe.get_doc({
			"doctype": "ToDo",
			"role": remaining[0].approver_role,
			"reference_type": "Contract Approval",
			"reference_name": approval.name,
			"description": f"Approval required (Step {remaining[0].step_number}) for Contract {approval.contract}"
		}).insert(ignore_permissions=True)


def reject_step(
	approval_name: str,
	step_idx: int,
	approver: str,
	reason: str
) -> None:
	"""Rejects an approval step, marking the entire approval rejected and returning contract to Rejected."""
	approval = frappe.get_doc("Contract Approval", approval_name)
	if not reason:
		frappe.throw(_("Rejection reason is mandatory."), frappe.MandatoryError)

	target_step = None
	for row in approval.approval_steps:
		if row.idx == step_idx or row.step_number == step_idx:
			target_step = row
			break

	if target_step:
		target_step.status = "Rejected"
		target_step.approver_user = approver
		target_step.action_date = now_datetime()
		target_step.comments = reason

	approval.status = "Rejected"
	approval.completion_date = now_datetime()
	approval.save()

	transition_status(approval.contract, "Rejected", reason=f"Rejected by {approver}: {reason}")


def check_pending_approval_slas():
	"""Scans pending approvals for SLA compliance or overdue reminders."""
	pending = frappe.get_all("Contract Approval", filters={"status": "Pending"}, fields=["name", "contract", "current_step"])
	return len(pending)
