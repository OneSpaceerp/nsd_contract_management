# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, now_datetime


def record_metric_value(
	contract_name: str,
	metric_code: str,
	actual_value: float,
	target_value: float = None,
	period: str = None,
	unit: str = "%"
) -> str:
	"""
	Logs a performance metric measurement for a contract and assesses SLA breach status.
	"""
	metric_records = frappe.get_all(
		"Contract Performance Metric",
		filters={"contract": contract_name, "metric_code": metric_code},
		fields=["name", "target_value"],
		limit=1
	)

	if metric_records:
		metric = frappe.get_doc("Contract Performance Metric", metric_records[0].name)
		target = flt(target_value or metric.target_value)
	else:
		metric = frappe.new_doc("Contract Performance Metric")
		metric.contract = contract_name
		metric.metric_name = metric_code.replace("_", " ").title()
		metric.metric_code = metric_code
		target = flt(target_value or 100.0)
		metric.target_value = target
		metric.unit = unit

	actual = flt(actual_value)
	metric.actual_value = actual
	variance = actual - target
	metric.variance = variance

	# Determine breach: if target > actual and higher is better, or vice versa
	is_breached = 1 if variance < 0 else 0
	metric.is_breached = is_breached

	if is_breached and metric.penalty_amount:
		# Log potential service credit / leakage finding
		frappe.get_doc({
			"doctype": "Comment",
			"comment_type": "Warning",
			"reference_doctype": "Contract",
			"reference_name": contract_name,
			"content": _("SLA metric {0} breached (Actual: {1}, Target: {2}). Potential penalty: {3}.").format(
				metric_code, actual, target, metric.penalty_amount
			)
		}).insert(ignore_permissions=True)

	metric.save()
	return metric.name


def aggregate_period_performance(contract_name: str, period_name: str) -> dict:
	"""
	Calculates the overall weighted score across all tracked metrics for a performance period.
	"""
	metrics = frappe.get_all(
		"Contract Performance Metric",
		filters={"contract": contract_name},
		fields=["metric_code", "target_value", "actual_value", "is_breached"]
	)

	if not metrics:
		return {"overall_score": 100.0, "breaches": 0}

	total_score = 0.0
	breaches = 0
	for m in metrics:
		target = flt(m.target_value) or 100.0
		actual = flt(m.actual_value)
		ratio = min(1.0, max(0.0, actual / target)) if target > 0 else 1.0
		total_score += (ratio * 100.0)
		if m.is_breached:
			breaches += 1

	overall = round(total_score / len(metrics), 2)
	return {
		"overall_score": overall,
		"total_metrics": len(metrics),
		"breaches": breaches
	}
