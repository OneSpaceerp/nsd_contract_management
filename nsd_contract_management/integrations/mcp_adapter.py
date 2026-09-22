# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import json
from typing import Dict, Any, List
import frappe
from nsd_contract_management.services.search_service import search_contracts
from nsd_contract_management.services.risk_service import calculate_contract_risk


def mcp_search_contracts(query: str = "", company: str = None, status: str = None) -> List[Dict[str, Any]]:
	"""MCP Tool: Searches contract repository matching query and filters."""
	return search_contracts(query=query, company=company, status=status, limit=10)


def mcp_get_contract_details(contract_name: str) -> Dict[str, Any]:
	"""MCP Tool: Retrieves comprehensive contract terms, parties, and references."""
	contract = frappe.get_doc("Contract", contract_name)
	return {
		"name": contract.name,
		"title": contract.title,
		"company": contract.company,
		"status": contract.status,
		"risk_level": contract.risk_level,
		"total_contract_value": contract.total_contract_value,
		"currency": contract.currency,
		"effective_date": str(contract.effective_date),
		"end_date": str(contract.end_date),
		"legal_hold": contract.legal_hold,
		"parties": [p.as_dict() for p in contract.get("parties", [])],
		"obligations_count": len(contract.get("obligations", [])),
		"erp_references_count": len(contract.get("erp_references", []))
	}


def mcp_check_contract_risk(contract_name: str) -> Dict[str, Any]:
	"""MCP Tool: Computes multi-factor risk score and breakdown."""
	return calculate_contract_risk(contract_name)


def mcp_get_contract_obligations(contract_name: str) -> List[Dict[str, Any]]:
	"""MCP Tool: Returns active obligations and fulfillment status."""
	return frappe.get_all(
		"Contract Obligation",
		filters={"contract": contract_name},
		fields=["name", "title", "obligation_type", "due_date", "status", "responsible_party", "evidence_required"]
	)


def mcp_create_contract_request(
	title: str,
	company: str,
	counterparty_name: str,
	estimated_value: float = 0.0,
	currency: str = "USD",
	description: str = ""
) -> Dict[str, Any]:
	"""MCP Tool: Submits a new Contract Request into the intake queue."""
	req = frappe.new_doc("Contract Request")
	req.title = title
	req.company = company
	req.counterparty_name = counterparty_name
	req.estimated_value = estimated_value
	req.currency = currency
	req.description = description
	req.status = "Submitted"
	req.insert()
	return {"success": True, "request_name": req.name, "status": req.status}
