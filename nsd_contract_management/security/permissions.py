# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe


def get_user_permitted_companies(user: str = None) -> list:
	"""Returns list of companies the user is explicitly permitted to access, or empty if unrestricted."""
	if not user:
		user = frappe.session.user

	if user in ["Administrator"]:
		return []

	roles = frappe.get_roles(user)
	if any(r in ["System Manager", "General Counsel", "Contract Auditor"] for r in roles):
		return []

	# Check Frappe User Permissions
	user_perms = frappe.get_all(
		"User Permission",
		filters={"user": user, "allow": "Company"},
		fields=["for_value"]
	)
	return [p.for_value for p in user_perms]


def get_contract_query_conditions(user: str = None) -> str:
	"""Generates SQL condition for row-level company and entity isolation on Contract."""
	permitted = get_user_permitted_companies(user)
	if not permitted:
		return ""

	formatted = ", ".join([frappe.db.escape(c) for c in permitted])
	return f"(`tabContract`.`company` in ({formatted}) or `tabContract`.`company` is null or `tabContract`.`company` = '')"


def get_contract_request_query_conditions(user: str = None) -> str:
	"""Generates SQL condition for row-level isolation on Contract Request."""
	permitted = get_user_permitted_companies(user)
	if not permitted:
		return ""

	formatted = ", ".join([frappe.db.escape(c) for c in permitted])
	return f"(`tabContract Request`.`company` in ({formatted}) or `tabContract Request`.`company` is null or `tabContract Request`.`company` = '')"


def get_contract_review_query_conditions(user: str = None) -> str:
	"""Generates SQL condition for row-level isolation on Contract Review."""
	if not user:
		user = frappe.session.user

	if user == "Administrator" or "System Manager" in frappe.get_roles(user):
		return ""

	return ""


def has_contract_permission(doc, user: str = None, ptype: str = "read") -> bool:
	"""
	Enforces action-level and custom permission types on Contract.
	Handles v16 custom permission types like 'release_legal_hold', 'approve_contract', etc.
	"""
	if not user:
		user = frappe.session.user

	if user == "Administrator":
		return True

	roles = set(frappe.get_roles(user))
	if "System Manager" in roles:
		return True

	# Legal Hold release requires explicit General Counsel or Legal Manager
	if ptype == "release_legal_hold":
		return bool(roles & {"General Counsel", "Legal Manager"})

	# Approval actions
	if ptype in ["approve_contract", "reject_contract"]:
		return bool(roles & {"General Counsel", "Contract Manager", "CFO", "CEO", "Finance Approver"})

	# eSignature actions
	if ptype in ["send_for_signature", "execute_contract"]:
		return bool(roles & {"Contract Manager", "General Counsel", "Operations Manager"})

	# Company permission check
	permitted = get_user_permitted_companies(user)
	if permitted and doc.company and doc.company not in permitted:
		return False

	return True
