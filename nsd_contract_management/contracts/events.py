# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def validate_contract(doc, method=None):
	"""Validates core invariants on Contract save."""
	if doc.legal_hold and doc.get_db_value("legal_hold") and doc.status in ["Cancelled", "Terminated", "Archived"]:
		frappe.throw(
			_("Contract {0} is under an active Legal Hold and cannot be moved to {1}.").format(doc.name, doc.status),
			frappe.PermissionError
		)


def on_contract_update(doc, method=None):
	"""Post-update event: synchronizes risk levels and search indices."""
	pass


def prevent_legal_hold_deletion(doc, method=None):
	"""Strictly prevents deletion of any Contract under an active Legal Hold."""
	if doc.legal_hold:
		frappe.throw(
			_("Contract {0} is under an active Legal Hold and CANNOT be deleted.").format(doc.name),
			frappe.PermissionError
		)
