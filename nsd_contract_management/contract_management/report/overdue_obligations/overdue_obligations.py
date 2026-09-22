# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, nowdate, date_diff


def execute(filters=None):
	columns = [
		{"label": _("Obligation"), "fieldname": "name", "fieldtype": "Link", "options": "Contract Obligation", "width": 140},
		{"label": _("Contract"), "fieldname": "contract", "fieldtype": "Link", "options": "Contract", "width": 140},
		{"label": _("Title"), "fieldname": "title", "fieldtype": "Data", "width": 220},
		{"label": _("Type"), "fieldname": "obligation_type", "fieldtype": "Data", "width": 120},
		{"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 110},
		{"label": _("Days Overdue"), "fieldname": "days_overdue", "fieldtype": "Int", "width": 110},
		{"label": _("Responsible Party"), "fieldname": "responsible_party", "fieldtype": "Data", "width": 160},
		{"label": _("Priority"), "fieldname": "priority", "fieldtype": "Data", "width": 90},
		{"label": _("Evidence Required"), "fieldname": "evidence_required", "fieldtype": "Check", "width": 110}
	]

	today = getdate(nowdate())
	conds = {"status": ["in", ["Overdue", "Pending", "In Progress"]]}
	if filters and filters.get("contract"):
		conds["contract"] = filters.get("contract")

	obs = frappe.get_all(
		"Contract Obligation",
		filters=conds,
		fields=["name", "contract", "title", "obligation_type", "due_date", "responsible_party", "priority", "evidence_required"]
	)

	data = []
	for o in obs:
		if o.due_date and getdate(o.due_date) < today:
			days_over = date_diff(today, getdate(o.due_date))
			o["days_overdue"] = days_over
			data.append(o)

	data.sort(key=lambda x: x.get("days_overdue", 0), reverse=True)
	return columns, data
