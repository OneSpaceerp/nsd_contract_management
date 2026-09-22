# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, nowdate, date_diff


def execute(filters=None):
	columns = [
		{"label": _("Renewal"), "fieldname": "name", "fieldtype": "Link", "options": "Contract Renewal", "width": 140},
		{"label": _("Contract"), "fieldname": "contract", "fieldtype": "Link", "options": "Contract", "width": 140},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": _("Expiration Date"), "fieldname": "current_end_date", "fieldtype": "Date", "width": 110},
		{"label": _("Notice Deadline"), "fieldname": "notice_deadline", "fieldtype": "Date", "width": 110},
		{"label": _("Days to Notice"), "fieldname": "days_to_notice", "fieldtype": "Int", "width": 110},
		{"label": _("Auto Renewal"), "fieldname": "auto_renewal", "fieldtype": "Check", "width": 100},
		{"label": _("Assigned To"), "fieldname": "assigned_to", "fieldtype": "Data", "width": 140}
	]

	today = getdate(nowdate())
	conds = {"status": ["in", ["Upcoming", "Notice Pending", "Under Negotiation"]]}
	if filters and filters.get("status"):
		conds["status"] = filters.get("status")

	renewals = frappe.get_all(
		"Contract Renewal",
		filters=conds,
		fields=["name", "contract", "status", "current_end_date", "notice_deadline", "auto_renewal", "assigned_to"],
		order_by="notice_deadline asc"
	)

	data = []
	for r in renewals:
		if r.notice_deadline:
			r["days_to_notice"] = date_diff(getdate(r.notice_deadline), today)
		else:
			r["days_to_notice"] = 999
		data.append(r)

	return columns, data
