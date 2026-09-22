// Copyright (c) 2026, NSD Core Architecture Team and contributors
// For license information, please see license.txt

frappe.query_reports["Overdue Obligations"] = {
	filters: [
		{
			fieldname: "contract",
			label: __("Contract"),
			fieldtype: "Link",
			options: "Contract"
		}
	]
};
