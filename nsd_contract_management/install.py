# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def after_install():
	"""Runs once after application installation on site."""
	create_roles()
	create_custom_permission_types()
	seed_default_contract_types()
	seed_default_settings()


def after_migrate():
	"""Runs after bench migrate."""
	create_roles()
	create_custom_permission_types()
	seed_default_contract_types()
	seed_default_settings()


def create_roles():
	"""Create CLM domain roles if they do not exist."""
	roles = [
		("Contract System Administrator", "Desk User"),
		("Contract System Manager", "Desk User"),
		("Contract Requester", "Desk User"),
		("Contract Manager", "Desk User"),
		("Contract Owner", "Desk User"),
		("Legal Counsel", "Desk User"),
		("Legal Manager", "Desk User"),
		("Procurement User", "Desk User"),
		("Procurement Manager", "Desk User"),
		("Sales User", "Desk User"),
		("Sales Manager", "Desk User"),
		("Finance User", "Desk User"),
		("Finance Manager", "Desk User"),
		("Compliance User", "Desk User"),
		("Compliance Manager", "Desk User"),
		("Executive Viewer", "Desk User"),
		("AI Administrator", "Desk User"),
		("AI Reviewer", "Desk User"),
		("AI Agent Operator", "Desk User"),
		("Counterparty Reviewer", "Website User"),
		("Counterparty Signer", "Website User"),
	]

	for role_name, user_type in roles:
		if not frappe.db.exists("Role", role_name):
			doc = frappe.new_doc("Role")
			doc.role_name = role_name
			doc.desk_access = 1 if user_type == "Desk User" else 0
			doc.is_custom = 1
			doc.insert(ignore_permissions=True)


def create_custom_permission_types():
	"""Create Frappe v16 Custom Permission Types."""
	permission_types = [
		"approve_contract",
		"reject_contract",
		"send_for_signature",
		"execute_contract",
		"download_contract",
		"export_contract_data",
		"release_legal_hold",
		"run_ai_review",
		"run_ai_agent",
		"execute_ai_action",
		"manage_playbook",
		"manage_clause",
		"manage_workflow",
	]

	# Check if Custom Permission Type DocType exists in this Frappe instance
	if frappe.db.table_exists("Custom Permission Type"):
		for pt in permission_types:
			if not frappe.db.exists("Custom Permission Type", pt):
				doc = frappe.new_doc("Custom Permission Type")
				doc.custom_permission_type = pt
				doc.description = pt.replace("_", " ").title()
				doc.insert(ignore_permissions=True)


def seed_default_contract_types():
	"""Seed standard contract types if none exist."""
	contract_types = [
		{
			"contract_type_name": "Master Services Agreement",
			"code": "MSA",
			"active": 1,
			"description": "Standard framework agreement for client and vendor commercial engagements.",
			"default_contract_duration_days": 365,
			"default_notice_days": 60,
			"requires_legal_review": 1,
			"requires_finance_review": 1,
			"requires_compliance_review": 0,
		},
		{
			"contract_type_name": "Statement of Work",
			"code": "SOW",
			"active": 1,
			"description": "Project deliverables, milestone schedule, and service scope under a parent MSA.",
			"default_contract_duration_days": 180,
			"default_notice_days": 30,
			"requires_legal_review": 0,
			"requires_finance_review": 1,
			"requires_compliance_review": 0,
		},
		{
			"contract_type_name": "Non-Disclosure Agreement",
			"code": "NDA",
			"active": 1,
			"description": "Mutual or unilateral confidentiality and trade secret protection agreement.",
			"default_contract_duration_days": 730,
			"default_notice_days": 0,
			"requires_legal_review": 1,
			"requires_finance_review": 0,
			"requires_compliance_review": 1,
		},
		{
			"contract_type_name": "Procurement Agreement",
			"code": "PROC",
			"active": 1,
			"description": "Supplier purchasing agreement for raw materials, goods, or recurring supply.",
			"default_contract_duration_days": 365,
			"default_notice_days": 60,
			"requires_legal_review": 1,
			"requires_finance_review": 1,
			"requires_compliance_review": 1,
		},
		{
			"contract_type_name": "Equipment Lease & AMC",
			"code": "LEASE",
			"active": 1,
			"description": "Lease and annual maintenance contract covering enterprise assets and machinery.",
			"default_contract_duration_days": 365,
			"default_notice_days": 45,
			"requires_legal_review": 1,
			"requires_finance_review": 1,
			"requires_compliance_review": 0,
		},
		{
			"contract_type_name": "Employment Contract",
			"code": "EMP",
			"active": 1,
			"description": "Standard staff employment agreement, onboarding and non-compete.",
			"default_contract_duration_days": 365,
			"default_notice_days": 30,
			"requires_legal_review": 1,
			"requires_finance_review": 0,
			"requires_compliance_review": 1,
		},
	]

	if frappe.db.table_exists("Contract Type"):
		for ct in contract_types:
			if not frappe.db.exists("Contract Type", ct["contract_type_name"]):
				doc = frappe.new_doc("Contract Type")
				doc.update(ct)
				doc.insert(ignore_permissions=True)


def seed_default_settings():
	"""Initialize default configuration Single DocTypes."""
	if frappe.db.table_exists("Contract Management Settings"):
		settings = frappe.get_single("Contract Management Settings")
		if not settings.default_notice_period_days:
			settings.default_notice_period_days = 60
			settings.enable_auto_renewal_reminders = 1
			settings.enable_obligation_escalation = 1
			settings.save(ignore_permissions=True)

	if frappe.db.table_exists("Contract ERPNext Integration Settings"):
		erp_settings = frappe.get_single("Contract ERPNext Integration Settings")
		erp_settings.enabled = 1
		erp_settings.enable_selling = 1
		erp_settings.enable_buying = 1
		erp_settings.enable_accounts = 1
		erp_settings.enable_projects = 1
		erp_settings.enable_subscriptions = 1
		erp_settings.enable_support = 1
		erp_settings.enable_assets = 1
		erp_settings.enable_hr = 1
		erp_settings.enable_leakage_detection = 1
		erp_settings.save(ignore_permissions=True)
