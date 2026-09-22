# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import nowdate, now_datetime
from nsd_contract_management.services.contract_service import transition_status


def initiate_termination(
	contract_name: str,
	termination_type: str = "Convenience",
	effective_date: str = None,
	reason: str = None,
	settlement_amount: float = None
) -> str:
	"""
	Initiates formal contract termination.
	Strictly enforces Legal Hold invariants: actively held contracts cannot be terminated.
	"""
	contract = frappe.get_doc("Contract", contract_name)
	if contract.legal_hold:
		frappe.throw(
			_("Contract {0} is under an active Legal Hold and cannot be terminated.").format(contract_name),
			frappe.PermissionError
		)

	if not reason:
		frappe.throw(_("Termination reason is mandatory."), frappe.MandatoryError)

	term_doc = frappe.new_doc("Contract Termination")
	term_doc.contract = contract_name
	term_doc.termination_type = termination_type
	term_doc.status = "Approved"
	term_doc.notice_date = nowdate()
	term_doc.effective_date = effective_date or nowdate()
	term_doc.reason = reason
	term_doc.severance_or_settlement_amount = settlement_amount or 0.0
	term_doc.closeout_checklist_completed = 1
	term_doc.insert()

	# Transition contract to Terminated
	transition_status(contract_name, "Terminated", reason=f"Terminated ({termination_type}): {reason}")

	# Cancel pending obligations
	frappe.db.sql("""
		UPDATE `tabContract Obligation`
		SET status = 'Cancelled', notes = CONCAT(IFNULL(notes, ''), '\nCancelled due to contract termination.')
		WHERE contract = %s AND status IN ('Pending', 'In Progress', 'Overdue')
	""", (contract_name,))

	frappe.get_doc({
		"doctype": "Comment",
		"comment_type": "Info",
		"reference_doctype": "Contract",
		"reference_name": contract_name,
		"content": _("Contract terminated on {0} (Type: {1}). Open obligations cancelled.").format(term_doc.effective_date, termination_type)
	}).insert(ignore_permissions=True)

	return term_doc.name
