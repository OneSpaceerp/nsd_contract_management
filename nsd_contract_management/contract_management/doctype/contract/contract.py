# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, add_days


class Contract(Document):
	def validate(self):
		self.validate_dates()
		self.calculate_notice_deadline()
		self.sync_primary_counterparty()
		self.validate_legal_hold_modifications()

	def validate_dates(self):
		if self.effective_date and self.expiration_date:
			if getdate(self.expiration_date) < getdate(self.effective_date):
				frappe.throw(_("Expiration Date cannot be before Effective Date"))

	def calculate_notice_deadline(self):
		if self.expiration_date and self.notice_period_days:
			self.notice_deadline = add_days(self.expiration_date, -int(self.notice_period_days))

	def sync_primary_counterparty(self):
		if not self.counterparty_primary and hasattr(self, "parties") and self.parties:
			for p in self.parties:
				if p.primary or p.party_type != "Company":
					self.counterparty_primary = p.legal_name or p.party
					break

	def validate_legal_hold_modifications(self):
		if self.get_doc_before_save() and self.get_doc_before_save().legal_hold:
			# Prevent changing status to Terminated, Expired, or Cancelled while on legal hold
			if self.status in ["Cancelled", "Terminated", "Archived"] and self.get_doc_before_save().status != self.status:
				frappe.throw(
					_("Cannot change status to {0} while Contract is under an active Legal Hold.").format(self.status),
					frappe.PermissionError
				)

	def on_trash(self):
		if self.legal_hold:
			frappe.throw(
				_("Contract {0} is under an active Legal Hold and cannot be deleted.").format(self.name),
				frappe.PermissionError
			)
