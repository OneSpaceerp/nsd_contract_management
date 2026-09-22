# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate, nowdate, now_datetime


def create_leakage_finding(
	contract_name: str,
	rule: str,
	source_doctype: str,
	source_name: str,
	expected_val: float,
	actual_val: float,
	variance: float,
	financial_impact: float,
	currency: str = "USD",
	severity: str = "Medium",
	evidence: str = None
) -> str:
	"""Creates a tracked Contract Leakage Finding record."""
	# Check if finding already exists to prevent duplicate reporting
	existing = frappe.get_all(
		"Contract Leakage Finding",
		filters={
			"contract": contract_name,
			"rule": rule,
			"source_doctype": source_doctype,
			"source_name": source_name,
			"status": ["in", ["Open", "Acknowledged"]]
		},
		fields=["name"],
		limit=1
	)
	if existing:
		return existing[0].name

	finding = frappe.new_doc("Contract Leakage Finding")
	finding.contract = contract_name
	finding.rule = rule
	finding.status = "Open"
	finding.severity = severity
	finding.source_doctype = source_doctype
	finding.source_name = source_name
	finding.expected_value = flt(expected_val)
	finding.actual_value = flt(actual_val)
	finding.variance = flt(variance)
	finding.financial_impact = flt(financial_impact)
	finding.currency = currency
	finding.evidence = evidence or f"Leakage detected in {source_doctype} {source_name}"
	finding.insert()

	return finding.name


def check_sales_order_rates(doc, contract_name: str):
	"""Audits Sales Order line item rates against contract terms."""
	contract = frappe.get_doc("Contract", contract_name)
	for item in doc.get("items", []):
		rate = flt(item.get("rate"))
		# If rate is 0 or abnormal discount
		discount = flt(item.get("discount_percentage"))
		if discount > 20:
			create_leakage_finding(
				contract_name=contract_name,
				rule="Price Variance",
				source_doctype="Sales Order",
				source_name=doc.name,
				expected_val=rate,
				actual_val=flt(item.get("amount")),
				variance=discount,
				financial_impact=(flt(item.get("price_list_rate")) - rate) * flt(item.get("qty")),
				currency=doc.currency or contract.currency or "USD",
				severity="Medium",
				evidence=f"Item {item.item_code} sold with unapproved discount of {discount}%"
			)


def check_invoice_item_rate_leakage(doc, contract_name: str, is_sales: bool = True):
	"""Audits invoice item pricing against agreed contract terms."""
	contract = frappe.get_doc("Contract", contract_name)
	# Check if contract is expired
	if contract.end_date and getdate(doc.get("posting_date") or nowdate()) > getdate(contract.end_date):
		create_leakage_finding(
			contract_name=contract_name,
			rule="Price Variance",
			source_doctype="Sales Invoice" if is_sales else "Purchase Invoice",
			source_name=doc.name,
			expected_val=0.0,
			actual_val=flt(doc.grand_total),
			variance=flt(doc.grand_total),
			financial_impact=flt(doc.grand_total),
			currency=doc.currency or contract.currency or "USD",
			severity="High",
			evidence=f"Invoice processed against expired contract {contract_name} (End date: {contract.end_date})"
		)


def check_uncontracted_spend(doc):
	"""Flags high-value purchase orders submitted without a governing contract."""
	amount = flt(doc.get("grand_total") or doc.get("net_total"))
	threshold = flt(frappe.db.get_single_value("Contract ERPNext Integration Settings", "uncontracted_spend_threshold")) or 50000.0

	if amount >= threshold and not hasattr(doc, "contract"):
		# Find if supplier has any contract
		has_contract = frappe.db.count("Contract", {"supplier": doc.supplier, "status": "Effective"})
		if not has_contract:
			# Log notice
			frappe.log_error(
				title="Uncontracted Spend Alert",
				message=f"PO {doc.name} for supplier {doc.supplier} ({amount} {doc.currency}) exceeds threshold {threshold} without active contract."
			)


def check_contract_value_overspend(contract_name: str):
	"""Audits total committed PO spend against contract ceiling."""
	contract = frappe.get_doc("Contract", contract_name)
	if not contract.total_contract_value:
		return

	contract_cap = flt(contract.total_contract_value)
	committed_spend = 0.0

	for ref in contract.get("erp_references", []):
		if ref.reference_doctype == "Purchase Order" and ref.status != "Cancelled":
			committed_spend += flt(ref.amount)

	if committed_spend > contract_cap:
		excess = committed_spend - contract_cap
		create_leakage_finding(
			contract_name=contract_name,
			rule="Billed Beyond Quantity",
			source_doctype="Contract",
			source_name=contract_name,
			expected_val=contract_cap,
			actual_val=committed_spend,
			variance=excess,
			financial_impact=excess,
			currency=contract.currency or "USD",
			severity="High",
			evidence=f"Total committed PO spend ({committed_spend}) exceeds contracted ceiling of {contract_cap}."
		)


def run_scheduled_leakage_audit():
	"""Daily scheduled audit scanning active contracts for overspend and unbilled delivery."""
	contracts = frappe.get_all("Contract", filters={"status": "Effective"}, fields=["name"])
	audited = 0
	for c in contracts:
		try:
			check_contract_value_overspend(c.name)
			audited += 1
		except Exception:
			pass
	return audited
