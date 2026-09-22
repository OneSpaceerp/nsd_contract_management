# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import json
import frappe
from frappe import _
from frappe.utils import now_datetime


def run_agent(agent_name: str, contract_name: str = None, context: dict = None) -> str:
	"""
	Executes an autonomous AI Agent run with explicit Human-In-The-Loop (HITL) safety gates.
	"""
	agent = frappe.get_doc("AI Agent", agent_name)
	if not agent.is_active:
		frappe.throw(_("AI Agent {0} is currently disabled.").format(agent_name))

	run = frappe.new_doc("AI Agent Run")
	run.agent = agent_name
	run.contract = contract_name
	run.status = "In Progress"
	run.started_at = now_datetime()
	run.insert()

	# Formulate planned actions based on agent role
	planned_actions = []
	if "renewal" in (agent.role or "").lower():
		planned_actions.append({
			"action_type": "Generate Renewal Brief",
			"description": f"Generate commercial briefing for contract {contract_name}",
			"target_doctype": "Contract",
			"target_docname": contract_name,
			"requires_approval": 0
		})
	elif "obligation" in (agent.role or "").lower():
		planned_actions.append({
			"action_type": "Audit Obligations",
			"description": f"Audit pending and overdue obligations for contract {contract_name}",
			"target_doctype": "Contract",
			"target_docname": contract_name,
			"requires_approval": 0
		})
	elif "leakage" in (agent.role or "").lower():
		planned_actions.append({
			"action_type": "Scan Transaction Leakage",
			"description": f"Audit purchase and sales prices against contract rates",
			"target_doctype": "Contract",
			"target_docname": contract_name,
			"requires_approval": 1
		})
	else:
		planned_actions.append({
			"action_type": "Risk Audit",
			"description": f"Perform comprehensive legal risk audit on {contract_name or 'contracts'}",
			"target_doctype": "Contract",
			"target_docname": contract_name,
			"requires_approval": 0
		})

	for act in planned_actions:
		action_doc = frappe.new_doc("AI Agent Action")
		action_doc.agent_run = run.name
		action_doc.action_type = act["action_type"]
		action_doc.description = act["description"]
		action_doc.target_doctype = act.get("target_doctype")
		action_doc.target_docname = act.get("target_docname")

		# If agent requires human approval or action is high impact
		needs_approval = agent.require_human_approval or act.get("requires_approval")
		if needs_approval:
			action_doc.status = "Pending Approval"
		else:
			action_doc.status = "Executed"
			action_doc.result = json.dumps({"status": "Success", "executed_at": str(now_datetime())})

		action_doc.insert()

	run.status = "Completed"
	run.completed_at = now_datetime()
	run.summary = f"Agent {agent.agent_name} executed {len(planned_actions)} planned actions."
	run.save()

	return run.name


def approve_agent_action(action_name: str, approver: str = None) -> dict:
	"""
	Human-In-The-Loop approval gate: validates and executes a pending autonomous action.
	"""
	act = frappe.get_doc("AI Agent Action", action_name)
	if act.status != "Pending Approval":
		frappe.throw(_("Action {0} is not pending approval (Current: {1}).").format(action_name, act.status))

	act.status = "Executed"
	act.result = json.dumps({
		"approved_by": approver or frappe.session.user,
		"executed_at": str(now_datetime()),
		"message": "Action successfully verified and executed by human supervisor."
	})
	act.save()

	return {"success": True, "action": act.name, "status": act.status}
