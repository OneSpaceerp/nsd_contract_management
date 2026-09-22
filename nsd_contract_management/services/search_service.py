# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def search_contracts(
	query: str = None,
	company: str = None,
	status: str = None,
	counterparty: str = None,
	contract_type: str = None,
	limit: int = 25
) -> list:
	"""
	Performs cross-field searching across Contracts, parties, titles, and clauses.
	"""
	filters = {}
	if company:
		filters["company"] = company
	if status:
		filters["status"] = status
	if contract_type:
		filters["contract_type"] = contract_type

	or_filters = []
	if query:
		or_filters.append(["title", "like", f"%{query}%"])
		or_filters.append(["description", "like", f"%{query}%"])
		or_filters.append(["customer", "like", f"%{query}%"])
		or_filters.append(["supplier", "like", f"%{query}%"])

	contracts = frappe.get_all(
		"Contract",
		filters=filters,
		or_filters=or_filters if or_filters else None,
		fields=[
			"name", "title", "company", "contract_type", "status",
			"customer", "supplier", "total_contract_value", "currency",
			"effective_date", "end_date", "risk_level"
		],
		limit=limit,
		order_by="modified desc"
	)

	return contracts
