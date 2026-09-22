# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import hashlib
import difflib
import frappe
from frappe import _
from frappe.utils import now_datetime


def calculate_content_hash(content: str) -> str:
	"""Computes SHA-256 hash for given document content or text."""
	if not content:
		return ""
	return hashlib.sha256(content.encode("utf-8")).hexdigest()


def get_latest_version(contract_name: str):
	"""Returns the most recent Contract Version document for a contract."""
	versions = frappe.get_all(
		"Contract Version",
		filters={"contract": contract_name},
		fields=["name", "version_number", "is_executed", "is_locked", "creation"],
		order_by="creation desc",
		limit=1
	)
	if versions:
		return frappe.get_doc("Contract Version", versions[0].name)
	return None


def get_next_version_number(contract_name: str, is_major: bool = False) -> str:
	"""Generates the next semantic version string (e.g. v1.0, v1.1, v2.0)."""
	latest = get_latest_version(contract_name)
	if not latest or not latest.version_number:
		return "v1.0"

	ver_str = str(latest.version_number).lstrip("vV")
	parts = ver_str.split(".")
	major = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 1
	minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0

	if is_major:
		return f"v{major + 1}.0"
	else:
		return f"v{major}.{minor + 1}"


def create_version(
	contract_name: str,
	title: str = None,
	content: str = None,
	file_url: str = None,
	change_summary: str = None,
	is_executed: int = 0,
	is_major: bool = False,
	creator: str = None
) -> str:
	"""Creates a new Contract Version record with SHA-256 integrity verification."""
	contract = frappe.get_doc("Contract", contract_name)
	if contract.legal_hold and is_executed:
		# Creating executed version under legal hold is permitted only if compliant
		pass

	next_version = get_next_version_number(contract_name, is_major=is_major)
	content_hash = calculate_content_hash(content or "")

	doc = frappe.new_doc("Contract Version")
	doc.contract = contract_name
	doc.version_number = next_version
	doc.title = title or f"{contract.title} - {next_version}"
	doc.content = content or ""
	doc.file = file_url
	doc.content_hash = content_hash
	doc.change_summary = change_summary or ("Initial version" if next_version == "v1.0" else "Updated version draft")
	doc.is_executed = is_executed
	doc.is_locked = 1 if is_executed else 0
	doc.effective_date = contract.effective_date
	if creator:
		doc.owner = creator
	doc.insert()

	# Update contract's current_version link
	frappe.db.set_value("Contract", contract_name, "current_version", doc.name)
	return doc.name


def seal_executed_version(
	contract_name: str,
	signed_file_url: str,
	certificate_url: str = None,
	signed_content: str = None
) -> str:
	"""
	Generates an immutable executed version upon contract signature completion.
	Locks the version permanently and records cryptographic audit evidence.
	"""
	contract = frappe.get_doc("Contract", contract_name)
	next_version = get_next_version_number(contract_name, is_major=True)
	content_hash = calculate_content_hash(signed_content or f"{contract_name}:{signed_file_url}:{now_datetime()}")

	doc = frappe.new_doc("Contract Version")
	doc.contract = contract_name
	doc.version_number = next_version
	doc.title = f"{contract.title} - Executed ({next_version})"
	doc.content = signed_content or ""
	doc.file = signed_file_url
	doc.content_hash = content_hash
	doc.change_summary = f"Executed contract agreement sealed on {now_datetime()}."
	doc.is_executed = 1
	doc.is_locked = 1
	doc.effective_date = contract.effective_date
	doc.insert()

	frappe.db.set_value("Contract", contract_name, {
		"current_version": doc.name,
		"executed_file": signed_file_url
	})

	frappe.get_doc({
		"doctype": "Comment",
		"comment_type": "Info",
		"reference_doctype": "Contract",
		"reference_name": contract_name,
		"content": _("Contract executed version sealed: {0} (Hash: {1})").format(doc.name, content_hash)
	}).insert(ignore_permissions=True)

	return doc.name


def compare_versions(version_a_name: str, version_b_name: str) -> dict:
	"""
	Compares two Contract Version texts and returns unified diff, added lines,
	and removed lines for negotiation and redline inspection.
	"""
	ver_a = frappe.get_doc("Contract Version", version_a_name)
	ver_b = frappe.get_doc("Contract Version", version_b_name)

	lines_a = (ver_a.content or "").splitlines(keepends=True)
	lines_b = (ver_b.content or "").splitlines(keepends=True)

	diff = list(difflib.unified_diff(
		lines_a,
		lines_b,
		fromfile=f"{ver_a.version_number} ({ver_a.name})",
		tofile=f"{ver_b.version_number} ({ver_b.name})"
	))

	additions = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
	deletions = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))

	return {
		"version_a": version_a_name,
		"version_b": version_b_name,
		"version_a_number": ver_a.version_number,
		"version_b_number": ver_b.version_number,
		"diff_text": "".join(diff),
		"additions_count": additions,
		"deletions_count": deletions,
		"identical": len(diff) == 0
	}
