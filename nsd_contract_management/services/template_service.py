# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from nsd_contract_management.services.clause_service import get_clause


def render_template(template_name: str, context: dict) -> str:
	"""Renders a Contract Template into a cohesive text document using safe Jinja templating."""
	tmpl = frappe.get_doc("Contract Template", template_name)
	sections = []

	# Header / intro
	header_text = tmpl.header_content or f"# {tmpl.template_name}"
	try:
		sections.append(frappe.render_template(header_text, context))
	except Exception as e:
		sections.append(header_text)

	# Template clauses
	for row in tmpl.get("clauses", []):
		clause_title = row.custom_title or row.clause
		clause_content = ""

		if row.clause:
			clause_info = get_clause(row.clause)
			clause_content = clause_info.get("clause_text") or ""
		elif row.content:
			clause_content = row.content

		try:
			rendered_clause = frappe.render_template(clause_content, context)
		except Exception:
			rendered_clause = clause_content

		section_block = f"\n## {row.idx}. {clause_title}\n\n{rendered_clause}\n"
		sections.append(section_block)

	# Footer / Sign-off block
	if tmpl.footer_content:
		try:
			sections.append(frappe.render_template(tmpl.footer_content, context))
		except Exception:
			sections.append(tmpl.footer_content)

	return "\n".join(sections)


def populate_contract_clauses(contract_name: str, template_name: str, context: dict = None) -> None:
	"""Applies clauses from a Contract Template onto the Contract document."""
	contract = frappe.get_doc("Contract", contract_name)
	tmpl = frappe.get_doc("Contract Template", template_name)

	ctx = context or {
		"contract": contract.as_dict(),
		"doc": contract.as_dict()
	}

	contract.set("clauses", [])

	for row in tmpl.get("clauses", []):
		clause_title = row.custom_title or row.clause
		clause_text = ""
		if row.clause:
			c_info = get_clause(row.clause)
			clause_text = c_info.get("clause_text") or ""
		elif row.content:
			clause_text = row.content

		try:
			rendered_text = frappe.render_template(clause_text, ctx)
		except Exception:
			rendered_text = clause_text

		contract.append("clauses", {
			"clause": row.clause,
			"clause_title": clause_title,
			"clause_text": rendered_text,
			"category": row.category or (c_info.get("category") if row.clause else None),
			"is_mandatory": row.is_mandatory,
			"is_standard": 1
		})

	contract.template = template_name
	contract.save()
