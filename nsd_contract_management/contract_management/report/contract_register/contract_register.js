// Copyright (c) 2026, NSD Core Architecture Team and contributors
// For license information, please see license.txt

frappe.query_reports["Contract Register"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company"
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "\nDraft\nIn Review\nNegotiation\nApproval Pending\nApproved\nSignature Pending\nExecuted\nEffective\nExpiring\nRenewal In Progress\nAmendment In Progress\nTerminated\nExpired\nArchived"
		},
		{
			fieldname: "contract_type",
			label: __("Contract Type"),
			fieldtype: "Link",
			options: "Contract Type"
		},
		{
			fieldname: "risk_level",
			label: __("Risk Level"),
			fieldtype: "Select",
			options: "\nLow\nMedium\nHigh\nCritical"
		}
	]
};
