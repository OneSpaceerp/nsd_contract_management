// Copyright (c) 2026, NSD Core Architecture Team and contributors
// For license information, please see license.txt

frappe.query_reports["Upcoming Renewals"] = {
	filters: [
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "\nUpcoming\nNotice Pending\nUnder Negotiation"
		}
	]
};
