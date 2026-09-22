# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt


def calculate_contract_risk(contract_name: str) -> dict:
	"""
	Computes a comprehensive risk score and classification based on financial exposure,
	non-standard clauses, overdue obligations, leakage findings, and legal holds.
	"""
	contract = frappe.get_doc("Contract", contract_name)
	score = 0
	breakdown = []

	# 1. Financial value exposure
	val = flt(contract.total_contract_value)
	if val >= 5000000:
		score += 30
		breakdown.append("Very high contract value (>= $5M): +30")
	elif val >= 1000000:
		score += 20
		breakdown.append("High contract value (>= $1M): +20")
	elif val >= 250000:
		score += 10
		breakdown.append("Medium contract value (>= $250k): +10")

	# 2. Non-standard or modified clauses
	non_std = sum(1 for c in contract.get("clauses", []) if not c.is_standard)
	if non_std > 0:
		pts = min(25, non_std * 5)
		score += pts
		breakdown.append(f"{non_std} non-standard clauses detected: +{pts}")

	# 3. Operational breach: Overdue obligations
	overdue_count = frappe.db.count("Contract Obligation", {"contract": contract_name, "status": "Overdue"})
	if overdue_count > 0:
		pts = min(25, overdue_count * 10)
		score += pts
		breakdown.append(f"{overdue_count} overdue obligations: +{pts}")

	# 4. Leakage findings
	leakage_count = frappe.db.count("Contract Leakage Finding", {"contract": contract_name, "status": ["!=", "Resolved"]})
	if leakage_count > 0:
		pts = min(20, leakage_count * 10)
		score += pts
		breakdown.append(f"{leakage_count} active leakage findings: +{pts}")

	# 5. Legal hold flag
	if contract.legal_hold:
		score += 20
		breakdown.append("Active legal hold applied: +20")

	# Classification
	if score >= 60:
		risk_level = "Critical"
	elif score >= 40:
		risk_level = "High"
	elif score >= 20:
		risk_level = "Medium"
	else:
		risk_level = "Low"

	# Update contract record
	if contract.risk_level != risk_level:
		contract.db_set("risk_level", risk_level)

	return {
		"contract": contract_name,
		"risk_score": score,
		"risk_level": risk_level,
		"breakdown": breakdown
	}
