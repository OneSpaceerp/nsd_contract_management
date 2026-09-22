# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class AIProvider(ABC):
	"""Abstract base class interface for all AI / LLM providers in NSD Contract Management."""

	def __init__(self, provider_config: Optional[Dict[str, Any]] = None):
		self.config = provider_config or {}

	@abstractmethod
	def extract(self, document_text: str, schema: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		"""
		Extracts structured fields, entities, dates, financial terms, and clauses from document text.
		Returns a dictionary conforming to the specified schema with evidence spans and confidence scores.
		"""
		pass

	@abstractmethod
	def analyze(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		"""
		Runs analytical or risk reasoning prompts (e.g. playbook compliance, risk scoring, renewal brief).
		"""
		pass

	@abstractmethod
	def embed(self, texts: List[str]) -> List[List[float]]:
		"""
		Generates vector embeddings for a list of text passages.
		"""
		pass

	@abstractmethod
	def chat(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		"""
		Multi-turn conversational completion with optional tool/function calling support.
		"""
		pass
