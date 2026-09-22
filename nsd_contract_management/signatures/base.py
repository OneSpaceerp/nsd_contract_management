# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class SignatureProvider(ABC):
	"""Abstract base interface for electronic signature providers."""

	def __init__(self, provider_config: Optional[Dict[str, Any]] = None):
		self.config = provider_config or {}

	@abstractmethod
	def create_envelope(self, title: str, file_url: str, signers: List[Dict[str, Any]], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		"""
		Creates a signature envelope with the provider.
		Returns envelope identifier, status, and signer details.
		"""
		pass

	@abstractmethod
	def get_signing_url(self, envelope_id: str, signer_email: str) -> str:
		"""
		Generates an embedded or direct signing session URL for a signer.
		"""
		pass

	@abstractmethod
	def get_envelope_status(self, envelope_id: str) -> Dict[str, Any]:
		"""
		Checks current completion status of the envelope and signers.
		"""
		pass

	@abstractmethod
	def download_signed_document(self, envelope_id: str) -> bytes:
		"""
		Retrieves completed document and certificate of completion.
		"""
		pass
