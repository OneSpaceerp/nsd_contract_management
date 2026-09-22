// Copyright (c) 2026, NSD Core Architecture Team and contributors
// For license information, please see license.txt

frappe.ui.form.on("Contract", {
	refresh: function(frm) {
		if (frm.doc.legal_hold) {
			frm.dashboard.set_headline_alert(
				__("LEGAL HOLD ACTIVE: This agreement is subject to an active legal hold. Modifications and termination are strictly restricted."),
				"red"
			);
		}

		// Action buttons based on status
		if (!frm.is_new()) {
			// AI Audit button
			frm.add_custom_button(__("AI Extract & Review"), function() {
				frappe.call({
					method: "nsd_contract_management.api.ai.extract",
					args: { contract_name: frm.doc.name },
					freeze: true,
					freeze_message: __("Analyzing contract terms with AI..."),
					callback: function(r) {
						if (!r.exc) {
							frappe.show_alert({ message: __("AI Review Completed: {0}", [r.message.review_name]), indicator: "green" });
							frm.reload_doc();
						}
					}
				});
			}, __("Actions"));

			if (frm.doc.status === "Draft") {
				frm.add_custom_button(__("Submit for Review"), function() {
					frappe.call({
						method: "nsd_contract_management.api.contract.submit_for_review",
						args: { contract_name: frm.doc.name },
						callback: function(r) {
							if (!r.exc) {
								frappe.msgprint(__("Contract moved to In Review."));
								frm.reload_doc();
							}
						}
					});
				}, __("Workflow"));
			} else if (frm.doc.status === "In Review") {
				frm.add_custom_button(__("Submit for Approval"), function() {
					frappe.call({
						method: "nsd_contract_management.services.approval_service.submit_for_approval",
						args: { contract_name: frm.doc.name },
						callback: function(r) {
							if (!r.exc) {
								frappe.msgprint(__("Submitted for multi-tier approval."));
								frm.reload_doc();
							}
						}
					});
				}, __("Workflow"));

				frm.add_custom_button(__("Start Negotiation"), function() {
					frappe.call({
						method: "nsd_contract_management.api.contract.start_negotiation",
						args: { contract_name: frm.doc.name },
						callback: function(r) {
							if (!r.exc) {
								frappe.msgprint(__("Negotiation round opened."));
								frm.reload_doc();
							}
						}
					});
				}, __("Workflow"));
			} else if (frm.doc.status === "Approved") {
				frm.add_custom_button(__("Send for Signature"), function() {
					frappe.call({
						method: "nsd_contract_management.api.contract.send_for_signature",
						args: { contract_name: frm.doc.name, provider: "Mock" },
						callback: function(r) {
							if (!r.exc) {
								frappe.msgprint(__("Signature envelope dispatched."));
								frm.reload_doc();
							}
						}
					});
				}, __("Workflow"));
			} else if (frm.doc.status === "Signature Pending") {
				frm.add_custom_button(__("Simulate Counterparty Signature"), function() {
					frappe.call({
						method: "nsd_contract_management.api.webhooks.mock_sign",
						args: {
							req: frm.doc.name,
							signer: (frm.doc.parties && frm.doc.parties.length) ? frm.doc.parties[0].party_name : "signer@example.com"
						},
						callback: function(r) {
							if (!r.exc) {
								frappe.show_alert({ message: __("Signature simulated."), indicator: "green" });
								frm.reload_doc();
							}
						}
					});
				}, __("Workflow"));
			} else if (["Executed", "Effective"].includes(frm.doc.status)) {
				frm.add_custom_button(__("Create Renewal"), function() {
					frappe.call({
						method: "nsd_contract_management.api.renewals.create",
						args: { contract_name: frm.doc.name },
						callback: function(r) {
							if (!r.exc) {
								frappe.msgprint(__("Renewal record created: {0}", [r.message.renewal_name]));
							}
						}
					});
				}, __("Lifecycle"));
			}

			// Legal Hold toggles
			if (!frm.doc.legal_hold) {
				frm.add_custom_button(__("Apply Legal Hold"), function() {
					frappe.prompt([
						{ fieldname: "reason", fieldtype: "Small Text", label: __("Hold Reason / Legal Matter"), reqd: 1 }
					], function(values) {
						frappe.call({
							method: "nsd_contract_management.api.contract.put_on_hold",
							args: { contract_name: frm.doc.name, reason: values.reason },
							callback: function(r) {
								if (!r.exc) {
									frappe.show_alert({ message: __("Contract placed under Legal Hold."), indicator: "orange" });
									frm.reload_doc();
								}
							}
						});
					}, __("Apply Legal Hold"), __("Confirm"));
				}, __("Legal Hold"));
			} else {
				frm.add_custom_button(__("Release Legal Hold"), function() {
					frappe.confirm(__("Are you sure you want to release the active legal hold on this contract?"), function() {
						frappe.call({
							method: "nsd_contract_management.api.contract.resume",
							args: { contract_name: frm.doc.name, reason: "Legal hold release requested" },
							callback: function(r) {
								if (!r.exc) {
									frappe.show_alert({ message: __("Legal Hold released."), indicator: "green" });
									frm.reload_doc();
								}
							}
						});
					});
				}, __("Legal Hold"));
			}
		}
	}
});
