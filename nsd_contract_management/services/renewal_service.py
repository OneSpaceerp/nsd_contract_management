# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, nowdate, now_datetime, add_days, add_months, date_diff, flt


def calculate_notice_deadline(end_date: str, notice_period_days: int) -> str:
	"""Calculates the final date by which renewal or non-renewal notice must be served."""
	if not end_date:
		return None
	notice_days = int(notice_period_days or 30)
	return str(add_days(getdate(end_date), -notice_days))


def scan_upcoming_renewals(days_ahead: int = 90) -> dict:
	"""
	Daily scheduler job:
	- Identifies active contracts approaching notice deadline or expiration.
	- Generates Contract Renewal records where missing.
	- Sends alerts for contracts inside their critical notice window.
	"""
	today = getdate(nowdate())
	target_date = add_days(today, days_ahead)

	contracts = frappe.get_all(
		"Contract",
		filters={
			"status": ["in", ["Effective", "Expiring"]],
			"end_date": ["between", [str(today), str(target_date)]]
		},
		fields=["name", "title", "end_date", "notice_period_days", "auto_renewal", "owner", "status"]
	)

	created_renewals = 0
	for c in contracts:
		notice_deadline = calculate_notice_deadline(c.end_date, c.notice_period_days)
		existing = frappe.get_all("Contract Renewal", filters={"contract": c.name, "status": ["!=", "Cancelled"]}, limit=1)

		if not existing:
			ren = frappe.new_doc("Contract Renewal")
			ren.contract = c.name
			ren.status = "Upcoming"
			ren.current_end_date = c.end_date
			ren.notice_deadline = notice_deadline
			ren.auto_renewal = c.auto_renewal
			ren.assigned_to = c.owner
			ren.insert()
			created_renewals += 1

		# If notice deadline is within 14 days and not yet notified
		if notice_deadline and date_diff(getdate(notice_deadline), today) <= 14:
			frappe.db.set_value("Contract", c.name, "status", "Expiring")

	return {
		"contracts_scanned": len(contracts),
		"renewals_created": created_renewals
	}


def process_auto_renewals() -> int:
	"""
	Executes automated renewal extensions for contracts with auto-renewal enabled
	that have successfully cleared their notice deadline without termination.
	"""
	today = getdate(nowdate())
	renewals = frappe.get_all(
		"Contract Renewal",
		filters={
			"status": "Upcoming",
			"auto_renewal": 1
		},
		fields=["name", "contract", "current_end_date", "notice_deadline", "renewal_term_months"]
	)

	auto_renewed_count = 0
	for r in renewals:
		if not r.current_end_date:
			continue

		end_d = getdate(r.current_end_date)
		# If today is on or past the current end date
		if today >= end_d:
			months_to_add = int(r.renewal_term_months or 12)
			new_end_date = str(add_months(end_d, months_to_add))

			frappe.db.set_value("Contract", r.contract, {
				"end_date": new_end_date,
				"status": "Effective"
			})

			frappe.db.set_value("Contract Renewal", r.name, {
				"proposed_end_date": new_end_date,
				"status": "Auto Renewed"
			})

			frappe.get_doc({
				"doctype": "Comment",
				"comment_type": "Info",
				"reference_doctype": "Contract",
				"reference_name": r.contract,
				"content": _("Contract automatically renewed until {0} ({1} months extension).").format(new_end_date, months_to_add)
			}).insert(ignore_permissions=True)

			auto_renewed_count += 1

	return auto_renewed_count


def generate_renewal_brief(renewal_name: str) -> str:
	"""
	Produces an executive briefing summary evaluating contract performance,
	leakage, and financial history to support renegotiation or renewal decisions.
	"""
	ren = frappe.get_doc("Contract Renewal", renewal_name)
	contract = frappe.get_doc("Contract", ren.contract)

	total_obligations = frappe.db.count("Contract Obligation", {"contract": contract.name})
	fulfilled_obligations = frappe.db.count("Contract Obligation", {"contract": contract.name, "status": "Fulfilled"})
	overdue_obligations = frappe.db.count("Contract Obligation", {"contract": contract.name, "status": "Overdue"})

	leakage_count = frappe.db.count("Contract Leakage Finding", {"contract": contract.name})

	brief = f"""### Executive Renewal Brief
**Contract**: {contract.title} ({contract.name})
**Company**: {contract.company}
**Status**: {contract.status}
**Contract Value**: {contract.total_contract_value} {contract.currency}
**Current Expiration**: {contract.end_date}
**Notice Deadline**: {ren.notice_deadline or 'N/A'}

#### Obligation Fulfillment Health:
- Total Obligations Tracked: {total_obligations}
- Fulfilled: {fulfilled_obligations}
- Overdue / Breached: {overdue_obligations}

#### Financial & Leakage Findings:
- Leakage Incidents Recorded: {leakage_count}

#### Recommendation:
{"Auto-renewal eligible. No critical breaches detected." if overdue_obligations == 0 and leakage_count == 0 else "Review required prior to renewal: contract has open overdue obligations or unresolved financial leakage."}
"""

	ren.renewal_brief = brief
	ren.save()
	return brief


def run_daily_renewal_scan():
	"""Runs both renewal notice scanning and automatic extension processing."""
	res_scan = scan_upcoming_renewals(days_ahead=90)
	res_auto = process_auto_renewals()
	return {"scan": res_scan, "auto_renewals": res_auto}
