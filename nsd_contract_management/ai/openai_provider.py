# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import json
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional
import frappe
from nsd_contract_management.ai.base import AIProvider
from nsd_contract_management.ai.prompt_defense import detect_prompt_injection, wrap_user_content_sandbox
from nsd_contract_management.ai.schema_validator import validate_extraction_result, CANONICAL_CONTRACT_SCHEMA


class OpenAIProvider(AIProvider):
	"""
	Live OpenAI / OpenAI-compatible API client for production LLM extraction and reasoning.
	Uses urllib for zero external heavy dependencies.
	"""

	def __init__(self, provider_config: Optional[Dict[str, Any]] = None):
		super().__init__(provider_config)
		self.api_key = self.config.get("api_key") or frappe.conf.get("openai_api_key")
		self.endpoint = self.config.get("endpoint") or "https://api.openai.com/v1"
		self.model = self.config.get("model") or "gpt-4o-mini"

	def _call_chat_completion(self, messages: List[Dict[str, str]], response_format: Optional[Dict[str, Any]] = None) -> str:
		if not self.api_key:
			frappe.throw("OpenAI API key is not configured in AI Settings or site_config.")

		url = f"{self.endpoint.rstrip('/')}/chat/completions"
		headers = {
			"Content-Type": "application/json",
			"Authorization": f"Bearer {self.api_key}"
		}

		payload = {
			"model": self.model,
			"messages": messages,
			"temperature": 0.1
		}
		if response_format:
			payload["response_format"] = response_format

		req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
		try:
			with urllib.request.urlopen(req, timeout=60) as resp:
				res_data = json.loads(resp.read().decode("utf-8"))
				return res_data["choices"][0]["message"]["content"]
		except urllib.error.HTTPError as e:
			err_body = e.read().decode("utf-8")
			frappe.throw(f"OpenAI API Error ({e.code}): {err_body}")

	def extract(self, document_text: str, schema: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		is_suspicious, patterns = detect_prompt_injection(document_text)
		if is_suspicious:
			return {
				"error": "Adversarial prompt injection pattern detected",
				"detected_patterns": patterns,
				"confidence": 0.0
			}

		sandboxed = wrap_user_content_sandbox(document_text)
		messages = [
			{
				"role": "system",
				"content": "You are a legal document extraction engine. Extract metadata, parties, values, dates, clauses and risks. Return only valid JSON conforming to the requested schema."
			},
			{
				"role": "user",
				"content": f"Extract all terms from this contract according to canonical schema:\n\n{sandboxed}"
			}
		]

		raw_content = self._call_chat_completion(messages, response_format={"type": "json_object"})
		parsed = json.loads(raw_content)
		return validate_extraction_result(parsed)

	def analyze(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		is_suspicious, _ = detect_prompt_injection(prompt)
		if is_suspicious:
			return {"analysis": "Request aborted: prompt injection detected.", "risk_level": "Critical"}

		messages = [
			{"role": "system", "content": "You are a senior contract intelligence analyst. Provide concise, factual legal and commercial analysis."},
			{"role": "user", "content": prompt}
		]
		content = self._call_chat_completion(messages)
		return {"analysis": content, "risk_score": 10, "risk_level": "Low"}

	def embed(self, texts: List[str]) -> List[List[float]]:
		# Fallback to mock vector calculation if embedding endpoint not targeted
		from nsd_contract_management.ai.mock_provider import MockAIProvider
		return MockAIProvider().embed(texts)

	def chat(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		content = self._call_chat_completion(messages)
		return {"role": "assistant", "content": content}
