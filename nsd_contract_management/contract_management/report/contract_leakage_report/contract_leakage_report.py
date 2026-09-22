# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = [
		{"label": _("Finding"), "fieldname": "name", "fieldtype": "Link", "options": "Contract Leakage Finding", "width": 140},
		{"label": _("Contract"), "fieldname": "contract", "fieldtype": "Link", "options": "Contract", "width": 140},
		{"label": _("Rule"), "fieldname": "rule", "fieldtype": "Data", "width": 180},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 110},
		{"label": _("Severity"), "fieldname": "severity", "fieldtype": "Data", "width": 90},
		{"label": _("Source DocType"), "fieldname": "source_doctype", "fieldtype": "Data", "width": 130},
		{"label": _("Source Doc"), "fieldname": "source_name", "fieldtype": "Data", "width": 130},
		{"label": _("Impact"), "fieldname": "financial_impact", "fieldtype": "Currency", "options": "currency", "width": 120},
		{"label": _("Currency"), "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 80},
		{"label": _("Evidence"), "fieldname": "evidence", "fieldtype": "Data", "width": 250}
	]

	conds = {}
	if filters and filters.get("status"):
		conds["status"] = filters.get("status")
	if filters and filters.get("severity"):
		conds["severity"] = filters.get("severity")

	data = frappe.get_all(
		"Contract Leakage Finding",
		filters=conds,
		fields=["name", "contract", "rule", "status", "severity", "source_doctype", "source_name", "financial_impact", "currency", "evidence"],
		order_by="financial_impact desc"
	)

	return columns, data
