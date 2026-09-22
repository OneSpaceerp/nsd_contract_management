# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

app_name = "nsd_contract_management"
app_title = "NSD Contract Management"
app_publisher = "NSD Core Architecture Team"
app_description = "Enterprise Contract Lifecycle Management & Contract Intelligence for ERPNext v16"
app_email = "architecture@nsd.local"
app_license = "GPL-3.0-or-later"

# Dependencies
required_apps = ["erpnext"]

# Includes in Desk
app_include_js = "/assets/nsd_contract_management/js/contract_management.bundle.js"
app_include_css = "/assets/nsd_contract_management/css/contract_management.bundle.css"

# Form script hooks
doctype_js = {
	"Contract": "public/js/contract_form.js",
}

# Installation lifecycle
after_install = "nsd_contract_management.install.after_install"
after_migrate = "nsd_contract_management.install.after_migrate"
before_uninstall = "nsd_contract_management.uninstall.before_uninstall"

# Scheduled background jobs
scheduler_events = {
	"hourly": [
		"nsd_contract_management.tasks.hourly_checks",
	],
	"daily": [
		"nsd_contract_management.tasks.daily_obligation_scan",
		"nsd_contract_management.tasks.daily_renewal_notice_scan",
		"nsd_contract_management.tasks.daily_leakage_detection_run",
	],
	"cron": {
		"0 2 * * *": [
			"nsd_contract_management.tasks.nightly_retention_and_legal_hold_check",
		],
		"*/15 * * * *": [
			"nsd_contract_management.tasks.process_signature_status_poll",
		],
	},
}

# ERPNext Document Event Triggers for Bidirectional Integration
doc_events = {
	"Contract": {
		"validate": "nsd_contract_management.contracts.events.validate_contract",
		"on_update": "nsd_contract_management.contracts.events.on_contract_update",
		"on_trash": "nsd_contract_management.contracts.events.prevent_legal_hold_deletion",
	},
	"Opportunity": {
		"on_submit": "nsd_contract_management.integrations.erp_selling.sync_opportunity",
	},
	"Quotation": {
		"on_submit": "nsd_contract_management.integrations.erp_selling.sync_quotation",
	},
	"Sales Order": {
		"on_submit": "nsd_contract_management.integrations.erp_selling.sync_sales_order",
		"on_cancel": "nsd_contract_management.integrations.erp_selling.sync_sales_order_cancel",
	},
	"Delivery Note": {
		"on_submit": "nsd_contract_management.integrations.erp_selling.sync_delivery_note",
	},
	"Sales Invoice": {
		"on_submit": "nsd_contract_management.integrations.erp_selling.sync_sales_invoice",
		"on_cancel": "nsd_contract_management.integrations.erp_selling.sync_sales_invoice_cancel",
	},
	"Payment Entry": {
		"on_submit": "nsd_contract_management.integrations.erp_accounts.sync_payment_entry",
		"on_cancel": "nsd_contract_management.integrations.erp_accounts.sync_payment_entry_cancel",
	},
	"Purchase Order": {
		"on_submit": "nsd_contract_management.integrations.erp_buying.sync_purchase_order",
		"on_cancel": "nsd_contract_management.integrations.erp_buying.sync_purchase_order_cancel",
	},
	"Purchase Receipt": {
		"on_submit": "nsd_contract_management.integrations.erp_buying.sync_purchase_receipt",
	},
	"Purchase Invoice": {
		"on_submit": "nsd_contract_management.integrations.erp_buying.sync_purchase_invoice",
		"on_cancel": "nsd_contract_management.integrations.erp_buying.sync_purchase_invoice_cancel",
	},
	"Task": {
		"on_update": "nsd_contract_management.integrations.erp_projects.sync_task_update",
	},
	"Timesheet": {
		"on_submit": "nsd_contract_management.integrations.erp_projects.sync_timesheet",
	},
	"Expense Claim": {
		"on_submit": "nsd_contract_management.integrations.erp_projects.sync_expense_claim",
	},
	"Issue": {
		"on_update": "nsd_contract_management.integrations.erp_support.sync_issue_update",
	},
	"Maintenance Visit": {
		"on_submit": "nsd_contract_management.integrations.erp_support.sync_maintenance_visit",
	},
	"Warranty Claim": {
		"on_update": "nsd_contract_management.integrations.erp_support.sync_warranty_claim",
	},
}

# Permission Query Conditions for Company / Multi-Entity Isolation
permission_query_conditions = {
	"Contract": "nsd_contract_management.security.permissions.get_contract_query_conditions",
	"Contract Request": "nsd_contract_management.security.permissions.get_contract_request_query_conditions",
	"Contract Review": "nsd_contract_management.security.permissions.get_contract_review_query_conditions",
}

has_permission = {
	"Contract": "nsd_contract_management.security.permissions.has_contract_permission",
}

# Frappe v16 Custom Permission Types
# These declare custom actions that can be configured in Role Permissions
custom_permission_types = [
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

# Fixtures export configuration
fixtures = [
	{"dt": "Custom Field", "filters": [["module", "=", "Contract Management"]]},
	{"dt": "Property Setter", "filters": [["module", "=", "Contract Management"]]},
	{"dt": "Role", "filters": [["name", "in", [
		"Contract System Administrator",
		"Contract System Manager",
		"Contract Requester",
		"Contract Manager",
		"Contract Owner",
		"Legal Counsel",
		"Legal Manager",
		"Procurement User",
		"Procurement Manager",
		"Sales User",
		"Sales Manager",
		"Finance User",
		"Finance Manager",
		"Compliance User",
		"Compliance Manager",
		"Executive Viewer",
		"AI Administrator",
		"AI Reviewer",
		"AI Agent Operator",
		"Counterparty Reviewer",
		"Counterparty Signer",
	]]]},
	{"dt": "Custom Permission Type", "filters": [["custom_permission_type", "in", custom_permission_types]]},
	{"dt": "Contract Type", "filters": [["active", "=", 1]]},
]
