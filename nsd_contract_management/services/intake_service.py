# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, now_datetime
from nsd_contract_management.services.contract_version_service import create_version


def validate_request(request_name: str) -> dict:
	"""Validates that a Contract Request has all necessary metadata and parties before approval."""
	req = frappe.get_doc("Contract Request", request_name)
	issues = []

	if not req.title:
		issues.append(_("Title is mandatory."))
	if not req.company:
		issues.append(_("Company is mandatory."))
	if not req.counterparty_name:
		issues.append(_("Counterparty Name is mandatory."))

	risk_score = 0
	val = flt(req.estimated_value)
	if val >= 1000000:
		risk_score += 3
	elif val >= 250000:
		risk_score += 1

	if req.intake_answers:
		for row in req.intake_answers:
			ans = (row.answer or "").lower()
			if any(k in ans for k in ["personal data", "gdpr", "ip transfer", "exclusivity", "non-standard liability"]):
				risk_score += 2

	risk_level = "Low"
	if risk_score >= 5:
		risk_level = "Critical"
	elif risk_score >= 3:
		risk_level = "High"
	elif risk_score >= 1:
		risk_level = "Medium"

	return {
		"is_valid": len(issues) == 0,
		"issues": issues,
		"recommended_risk_level": risk_level,
		"risk_score": risk_score
	}


def check_duplicate_contracts(request_name: str) -> list:
	"""Identifies active or expiring contracts with the same counterparty to prevent accidental duplicates."""
	req = frappe.get_doc("Contract Request", request_name)
	filters = {
		"company": req.company,
		"status": ["in", ["Draft", "In Review", "Negotiation", "Approval Pending", "Approved", "Signature Pending", "Executed", "Effective"]]
	}

	if req.customer:
		filters["customer"] = req.customer
	elif req.supplier:
		filters["supplier"] = req.supplier
	else:
		filters["title"] = ["like", f"%{req.counterparty_name}%"]

	duplicates = frappe.get_all(
		"Contract",
		filters=filters,
		fields=["name", "title", "status", "contract_type", "effective_date", "end_date", "total_contract_value"]
	)
	return duplicates


def convert_request_to_contract(request_name: str, created_by: str = None) -> str:
	"""
	Converts an accepted Contract Request into a formal Contract draft document.
	Sets up initial parties, tags, and generates the initial v1.0 draft version.
	"""
	req = frappe.get_doc("Contract Request", request_name)
	if req.status not in ["Submitted", "Approved", "Classified"]:
		frappe.throw(
			_("Contract Request {0} must be Submitted, Classified, or Approved before converting to a Contract (Current: {1}).").format(
				request_name, req.status
			),
			frappe.ValidationError
		)

	# Create new contract
	contract = frappe.new_doc("Contract")
	contract.title = req.title
	contract.company = req.company
	contract.contract_type = req.contract_type
	contract.status = "Draft"
	contract.total_contract_value = req.estimated_value
	contract.currency = req.currency or frappe.db.get_value("Company", req.company, "default_currency") or "USD"
	contract.governing_law = req.governing_law
	contract.risk_level = req.risk_level or "Low"

	if req.counterparty_type == "Customer" and req.customer:
		contract.customer = req.customer
	elif req.counterparty_type == "Supplier" and req.supplier:
		contract.supplier = req.supplier

	if req.department:
		contract.department = req.department

	# Add party row for counterparty
	contract.append("parties", {
		"party_name": req.counterparty_name,
		"party_type": req.counterparty_type or "Third Party",
		"customer": req.customer,
		"supplier": req.supplier,
		"is_primary": 1
	})

	# Copy intake answers into contract notes / summary
	intake_notes = []
	for ans in req.get("intake_answers", []):
		intake_notes.append(f"**{ans.question}**: {ans.answer}")

	if intake_notes:
		contract.description = (req.description or "") + "\n\n### Intake Questionnaire Responses:\n" + "\n".join(intake_notes)
	else:
		contract.description = req.description

	contract.insert()

	# Generate v1.0 draft version
	initial_content = f"# {contract.title}\n\nCompany: {contract.company}\nCounterparty: {req.counterparty_name}\n\n{contract.description or ''}"
	ver_name = create_version(
		contract_name=contract.name,
		title=f"{contract.title} - Initial Draft",
		content=initial_content,
		change_summary=f"Generated from Contract Request {request_name}",
		creator=created_by or frappe.session.user
	)

	# Update request status and backlink
	req.db_set("contract", contract.name)
	req.db_set("status", "Accepted")

	frappe.get_doc({
		"doctype": "Comment",
		"comment_type": "Info",
		"reference_doctype": "Contract Request",
		"reference_name": request_name,
		"content": _("Created Contract {0} from Request.").format(contract.name)
	}).insert(ignore_permissions=True)

	return contract.name
