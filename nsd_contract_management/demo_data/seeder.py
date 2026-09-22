# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate, add_days, add_months
from nsd_contract_management.services.clause_service import create_clause
from nsd_contract_management.services.contract_service import create_contract, transition_status
from nsd_contract_management.services.contract_version_service import create_version, seal_executed_version
from nsd_contract_management.services.obligation_service import complete_obligation
from nsd_contract_management.integrations.leakage_engine import create_leakage_finding


def seed_demo_data():
	"""
	Seeds complete, production-grade demo data for NSD Contract Management:
	- Clause Categories & Standard Clauses
	- Clause Playbooks with fallback and unacceptable rules
	- Contract Templates
	- Multi-tier Contracts across lifecycle states (Draft, In Review, Approved, Executed, Effective)
	- Tracked Obligations and Commercial Leakage Findings
	"""
	frappe.flags.ignore_permissions = True

	# 1. Clause Categories
	categories = ["Confidentiality", "Limitation of Liability", "Indemnification", "Governing Law", "Termination", "Intellectual Property"]
	for cat in categories:
		if not frappe.db.exists("Clause Category", cat):
			frappe.get_doc({
				"doctype": "Clause Category",
				"category_name": cat,
				"description": f"Standard {cat} clauses"
			}).insert()

	# 2. Standard Clauses
	standard_clauses = [
		{
			"title": "Standard Mutual Confidentiality",
			"category": "Confidentiality",
			"text": "Each party agrees to maintain the confidentiality of all proprietary information disclosed by the other party for a period of five (5) years from disclosure.",
			"risk": "Low"
		},
		{
			"title": "Mutual Limitation of Liability",
			"category": "Limitation of Liability",
			"text": "Except for willful misconduct or breach of confidentiality, neither party's aggregate liability shall exceed the total fees paid in the twelve (12) months preceding the claim.",
			"risk": "Medium"
		},
		{
			"title": "Standard IP Ownership",
			"category": "Intellectual Property",
			"text": "Customer retains all rights, title, and interest in Customer Data. Provider retains all rights in the underlying Cloud Platform.",
			"risk": "Low"
		},
		{
			"title": "Convenience Termination - 30 Days",
			"category": "Termination",
			"text": "Either party may terminate this agreement without cause upon thirty (30) days prior written notice to the other party.",
			"risk": "Low"
		}
	]

	created_clause_names = {}
	for c in standard_clauses:
		existing = frappe.get_all("Clause", filters={"clause_title": c["title"]}, fields=["name"], limit=1)
		if existing:
			created_clause_names[c["title"]] = existing[0].name
		else:
			cl_id = create_clause(
				title=c["title"],
				category=c["category"],
				standard_text=c["text"],
				risk_level=c["risk"]
			)
			created_clause_names[c["title"]] = cl_id

	# 3. Clause Playbook
	if not frappe.db.exists("Clause Playbook", "Global Commercial Playbook"):
		playbook = frappe.new_doc("Clause Playbook")
		playbook.playbook_name = "Global Commercial Playbook"
		playbook.is_active = 1
		playbook.description = "Corporate baseline negotiation playbook for commercial agreements."

		if "Mutual Limitation of Liability" in created_clause_names:
			playbook.append("rules", {
				"category": "Limitation of Liability",
				"standard_clause": created_clause_names["Mutual Limitation of Liability"],
				"unacceptable_terms": "unlimited liability\nno liability cap\nconsequential damages uncapped",
				"negotiation_guidance": "Do not accept unlimited liability without General Counsel written waiver.",
				"escalation_role": "General Counsel"
			})

		if "Standard Mutual Confidentiality" in created_clause_names:
			playbook.append("rules", {
				"category": "Confidentiality",
				"standard_clause": created_clause_names["Standard Mutual Confidentiality"],
				"unacceptable_terms": "perpetual confidentiality without trade secret qualification",
				"negotiation_guidance": "Standard term is 3-5 years.",
				"escalation_role": "Legal Reviewer"
			})

		playbook.insert()

	# 4. Contract Template
	if not frappe.db.exists("Contract Template", "Standard Master Services Agreement"):
		tmpl = frappe.new_doc("Contract Template")
		tmpl.template_name = "Standard Master Services Agreement"
		tmpl.contract_type = "Master Services Agreement"
		tmpl.is_active = 1
		tmpl.header_content = "# MASTER SERVICES AGREEMENT\n\nThis Master Services Agreement is entered into between {{ contract.company }} and {{ doc.customer or 'Client' }}."
		tmpl.footer_content = "\n\nIN WITNESS WHEREOF, the parties hereto have caused this Agreement to be executed."

		for title, c_name in created_clause_names.items():
			tmpl.append("clauses", {
				"clause": c_name,
				"custom_title": title,
				"is_mandatory": 1
			})
		tmpl.insert()

	# 5. Companies / Parties Setup Check
	default_company = frappe.db.get_single_value("Global Defaults", "default_company") or "Test Company"
	if not frappe.db.exists("Company", default_company):
		comp = frappe.new_doc("Company")
		comp.company_name = default_company
		comp.default_currency = "USD"
		comp.country = "United States"
		comp.insert()

	# 6. Demo Contracts
	# Contract 1: Effective Master Services Agreement with Obligations & ERP References
	if not frappe.db.exists("Contract", {"title": "Acme Global - Cloud Infrastructure MSA"}):
		c1 = frappe.new_doc("Contract")
		c1.title = "Acme Global - Cloud Infrastructure MSA"
		c1.company = default_company
		c1.contract_type = "Master Services Agreement"
		c1.status = "Draft"
		c1.total_contract_value = 1200000.00
		c1.currency = "USD"
		c1.effective_date = add_months(nowdate(), -6)
		c1.end_date = add_months(nowdate(), 6)
		c1.auto_renewal = 1
		c1.notice_period_days = 60
		c1.governing_law = "Delaware, USA"
		c1.risk_level = "Low"

		c1.append("parties", {
			"party_name": "Acme Global Enterprises",
			"party_type": "Customer",
			"is_primary": 1
		})

		c1.append("obligations", {
			"title": "Quarterly Service Level Review & SOC2 Audit Delivery",
			"obligation_type": "Reporting",
			"due_date": add_days(nowdate(), 15),
			"priority": "High",
			"evidence_required": 1
		})

		c1.append("obligations", {
			"title": "Deliver Bi-Monthly Architecture Reports",
			"obligation_type": "Deliverable",
			"due_date": add_days(nowdate(), -10),  # Overdue
			"priority": "Medium",
			"evidence_required": 1
		})

		c1.insert()

		# Progress to Effective
		transition_status(c1.name, "In Review")
		transition_status(c1.name, "Approval Pending")
		transition_status(c1.name, "Approved")
		transition_status(c1.name, "Signature Pending")
		seal_executed_version(c1.name, "/files/acme_msa_signed.pdf")
		transition_status(c1.name, "Executed")
		transition_status(c1.name, "Effective")

		# Add Leakage Finding
		create_leakage_finding(
			contract_name=c1.name,
			rule="Price Variance",
			source_doctype="Sales Invoice",
			source_name="SINV-2026-0001",
			expected_val=100000.0,
			actual_val=85000.0,
			variance=15000.0,
			financial_impact=15000.0,
			currency="USD",
			severity="Medium",
			evidence="Uncontracted 15% discount applied without approval on monthly cloud charges."
		)

	# Contract 2: Legal Hold Contract
	if not frappe.db.exists("Contract", {"title": "Apex Technologies - Software License"}):
		c2 = frappe.new_doc("Contract")
		c2.title = "Apex Technologies - Software License"
		c2.company = default_company
		c2.contract_type = "Software License"
		c2.status = "Draft"
		c2.total_contract_value = 450000.00
		c2.currency = "USD"
		c2.effective_date = add_months(nowdate(), -12)
		c2.end_date = add_months(nowdate(), 12)
		c2.governing_law = "New York, USA"
		c2.risk_level = "High"

		c2.append("parties", {
			"party_name": "Apex Technologies Inc",
			"party_type": "Customer",
			"is_primary": 1
		})
		c2.insert()

		transition_status(c2.name, "In Review")
		transition_status(c2.name, "Approval Pending")
		transition_status(c2.name, "Approved")
		transition_status(c2.name, "Signature Pending")
		seal_executed_version(c2.name, "/files/apex_signed.pdf")
		transition_status(c2.name, "Executed")
		transition_status(c2.name, "Effective")

		# Place under Legal Hold
		from nsd_contract_management.services.contract_service import apply_legal_hold
		apply_legal_hold(c2.name, reason="Pending IP copyright audit matter MAT-2026-042.")

	return {"success": True, "message": "Demo data successfully seeded."}
