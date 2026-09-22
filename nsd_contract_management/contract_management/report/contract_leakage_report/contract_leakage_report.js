// Copyright (c) 2026, NSD Core Architecture Team and contributors
// For license information, please see license.txt

frappe.query_reports["Contract Leakage Report"] = {
	filters: [
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "\nOpen\nAcknowledged\nResolved\nWaived"
		},
		{
			fieldname: "severity",
			label: __("Severity"),
			fieldtype: "Select",
			options: "\nLow\nMedium\nHigh\nCritical"
		}
	]
};
