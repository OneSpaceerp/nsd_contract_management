# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, nowdate, now_datetime, date_diff, add_days


def generate_obligations_from_clauses(contract_name: str) -> list:
	"""
	Scans contract terms and clauses to automatically generate tracking Contract Obligation records.
	"""
	contract = frappe.get_doc("Contract", contract_name)
	created_obligations = []

	# Check child obligations defined on contract
	for row in contract.get("obligations", []):
		ob = frappe.new_doc("Contract Obligation")
		ob.contract = contract_name
		ob.title = row.title
		ob.obligation_type = row.obligation_type or "Deliverable"
		ob.responsible_party = row.responsible_party or contract.company
		ob.due_date = row.due_date or contract.end_date
		ob.status = "Pending"
		ob.priority = row.priority or "Medium"
		ob.evidence_required = 1 if row.evidence_required else 0
		ob.insert()
		created_obligations.append(ob.name)

	# If contract has effective date and payment terms, add initial payment / milestone obligation
	if contract.total_contract_value and not created_obligations:
		ob = frappe.new_doc("Contract Obligation")
		ob.contract = contract_name
		ob.title = f"Fulfill Contract Payment Terms: {contract.title}"
		ob.obligation_type = "Payment"
		ob.responsible_party = contract.customer or contract.supplier or contract.company
		ob.due_date = contract.end_date or add_days(nowdate(), 30)
		ob.status = "Pending"
		ob.priority = "High"
		ob.insert()
		created_obligations.append(ob.name)

	return created_obligations


def evaluate_due_obligations() -> dict:
	"""
	Scheduled daily job:
	- Identifies obligations approaching deadline (90, 60, 30, 14, 7, 1 days).
	- Sends reminder notifications.
	- Marks past-due obligations as Overdue.
	- Creates linked ToDos for evidence collection when required.
	"""
	today = getdate(nowdate())
	open_obligations = frappe.get_all(
		"Contract Obligation",
		filters={"status": ["in", ["Pending", "In Progress"]]},
		fields=["name", "contract", "title", "due_date", "responsible_party", "evidence_required", "owner"]
	)

	overdue_count = 0
	approaching_count = 0

	for ob in open_obligations:
		if not ob.due_date:
			continue

		due_d = getdate(ob.due_date)
		days_left = date_diff(due_d, today)

		if days_left < 0:
			frappe.db.set_value("Contract Obligation", ob.name, "status", "Overdue")
			overdue_count += 1
		elif days_left in [90, 60, 30, 14, 7, 1]:
			approaching_count += 1
			# Notification or ToDo
			if ob.owner:
				frappe.get_doc({
					"doctype": "ToDo",
					"allocated_to": ob.owner,
					"reference_type": "Contract Obligation",
					"reference_name": ob.name,
					"description": f"Obligation due in {days_left} days: {ob.title} (Contract: {ob.contract})"
				}).insert(ignore_permissions=True)

	return {
		"processed_total": len(open_obligations),
		"marked_overdue": overdue_count,
		"approaching_reminders": approaching_count
	}


def complete_obligation(
	obligation_name: str,
	evidence_file: str = None,
	completed_by: str = None
) -> None:
	"""Marks an obligation as Fulfilled, verifying required evidence files."""
	ob = frappe.get_doc("Contract Obligation", obligation_name)
	if ob.status == "Fulfilled":
		return

	if ob.evidence_required and not evidence_file and not ob.evidence_file:
		frappe.throw(
			_("Obligation {0} requires evidence file upload before it can be fulfilled.").format(obligation_name),
			frappe.ValidationError
		)

	ob.status = "Fulfilled"
	ob.completion_date = now_datetime()
	if evidence_file:
		ob.evidence_file = evidence_file
	ob.save()

	frappe.get_doc({
		"doctype": "Comment",
		"comment_type": "Info",
		"reference_doctype": "Contract Obligation",
		"reference_name": obligation_name,
		"content": _("Obligation fulfilled by {0}.").format(completed_by or frappe.session.user)
	}).insert(ignore_permissions=True)


def waive_obligation(obligation_name: str, reason: str, waived_by: str = None) -> None:
	"""Waives an obligation with mandatory justification."""
	if not reason:
		frappe.throw(_("Reason is mandatory to waive an obligation."), frappe.MandatoryError)

	ob = frappe.get_doc("Contract Obligation", obligation_name)
	ob.status = "Waived"
	ob.notes = (ob.notes or "") + f"\n\nWaived on {now_datetime()} by {waived_by or frappe.session.user}: {reason}"
	ob.save()


def run_daily_obligation_scan():
	"""Scheduler alias for evaluate_due_obligations."""
	return evaluate_due_obligations()
