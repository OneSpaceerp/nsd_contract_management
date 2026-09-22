# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": _("Contract"), "fieldname": "name", "fieldtype": "Link", "options": "Contract", "width": 140},
		{"label": _("Title"), "fieldname": "title", "fieldtype": "Data", "width": 200},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": _("Company"), "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 140},
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 130},
		{"label": _("Supplier"), "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 130},
		{"label": _("Contract Type"), "fieldname": "contract_type", "fieldtype": "Link", "options": "Contract Type", "width": 130},
		{"label": _("Value"), "fieldname": "total_contract_value", "fieldtype": "Currency", "options": "currency", "width": 120},
		{"label": _("Currency"), "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 80},
		{"label": _("Effective Date"), "fieldname": "effective_date", "fieldtype": "Date", "width": 110},
		{"label": _("End Date"), "fieldname": "end_date", "fieldtype": "Date", "width": 110},
		{"label": _("Risk Level"), "fieldname": "risk_level", "fieldtype": "Data", "width": 100},
		{"label": _("Legal Hold"), "fieldname": "legal_hold", "fieldtype": "Check", "width": 90}
	]


def get_data(filters):
	f = filters or {}
	conds = {}
	if f.get("company"):
		conds["company"] = f.get("company")
	if f.get("status"):
		conds["status"] = f.get("status")
	if f.get("contract_type"):
		conds["contract_type"] = f.get("contract_type")
	if f.get("risk_level"):
		conds["risk_level"] = f.get("risk_level")

	return frappe.get_all(
		"Contract",
		filters=conds,
		fields=[
			"name", "title", "status", "company", "customer", "supplier",
			"contract_type", "total_contract_value", "currency",
			"effective_date", "end_date", "risk_level", "legal_hold"
		],
		order_by="creation desc"
	)
