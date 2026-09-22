# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from nsd_contract_management.services.review_service import (
	start_review, submit_review_feedback, complete_review
)
from nsd_contract_management.services.ai_service import extract_contract


@frappe.whitelist()
def start(contract_name: str, review_type: str = "Internal", reviewers: str = None) -> dict:
	"""RPC: Launches formal review session."""
	reviewer_list = [r.strip() for r in reviewers.split(",")] if reviewers else []
	review_name = start_review(contract_name, review_type=review_type, reviewers=reviewer_list)
	return {"review_name": review_name}


@frappe.whitelist()
def complete(review_name: str) -> dict:
	"""RPC: Marks review session complete."""
	complete_review(review_name)
	return {"review_name": review_name, "status": "Completed"}


@frappe.whitelist()
def request_changes(review_name: str, feedback: str) -> dict:
	"""RPC: Submits changes requested decision."""
	submit_review_feedback(review_name, reviewer=frappe.session.user, decision="Changes Requested", feedback_text=feedback)
	return {"review_name": review_name, "status": "Changes Requested"}


@frappe.whitelist()
def create_ai_review(contract_name: str) -> dict:
	"""RPC: Runs AI extraction and analysis review on contract."""
	ai_review_name = extract_contract(contract_name)
	return {"ai_review_name": ai_review_name}
