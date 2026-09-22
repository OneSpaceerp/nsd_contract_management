# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def get_clause(clause_name: str, version_number: str = None) -> dict:
	"""Fetches clause details along with the specified or latest active clause version text."""
	clause = frappe.get_doc("Clause", clause_name)
	clause_text = ""
	active_ver = None

	if version_number:
		ver_records = frappe.get_all(
			"Clause Version",
			filters={"clause": clause_name, "version_number": version_number},
			fields=["name", "version_number", "clause_text", "status"],
			limit=1
		)
		if ver_records:
			clause_text = ver_records[0].clause_text
			active_ver = ver_records[0].version_number
	else:
		# Check active version
		ver_records = frappe.get_all(
			"Clause Version",
			filters={"clause": clause_name, "status": "Active"},
			fields=["name", "version_number", "clause_text"],
			order_by="creation desc",
			limit=1
		)
		if ver_records:
			clause_text = ver_records[0].clause_text
			active_ver = ver_records[0].version_number

	return {
		"name": clause.name,
		"clause_title": clause.clause_title,
		"category": clause.category,
		"risk_level": clause.risk_level,
		"version_number": active_ver,
		"clause_text": clause_text or clause.description or ""
	}


def create_clause(
	title: str,
	category: str,
	standard_text: str,
	fallback_text: str = None,
	risk_level: str = "Low"
) -> str:
	"""Creates a new Clause and registers its initial v1.0 standard version."""
	doc = frappe.new_doc("Clause")
	doc.clause_title = title
	doc.category = category
	doc.risk_level = risk_level
	doc.is_standard = 1
	doc.status = "Active"
	doc.insert()

	# Create initial v1.0 version
	ver = frappe.new_doc("Clause Version")
	ver.clause = doc.name
	ver.version_number = "v1.0"
	ver.clause_text = standard_text
	ver.status = "Active"
	ver.change_summary = "Initial standard clause"
	ver.insert()

	return doc.name


def search_clauses(query: str = None, category: str = None, limit: int = 20) -> list:
	"""Searches available clauses filtered by query keyword and category."""
	filters = {"status": "Active"}
	if category:
		filters["category"] = category
	if query:
		filters["clause_title"] = ["like", f"%{query}%"]

	clauses = frappe.get_all(
		"Clause",
		filters=filters,
		fields=["name", "clause_title", "category", "risk_level", "is_standard"],
		limit=limit
	)
	return clauses
