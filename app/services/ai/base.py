"""
Abstract Base AI Inference Service.

Defines the contract for Natural Language Understanding (NLU) services.
Enables pluggable architecture for mock rule-based parsers, local ML models,
or remote LLM providers (e.g. OpenAI, Anthropic, Gemini).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseNLUService(ABC):
    """Abstract base class for all AI inference and NLP components."""

    @abstractmethod
    def parse(self, text: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Extract structured insights from unstructured natural language text.

        :param text: Unstructured raw text input.
        :param kwargs: Optional contextual parameters (e.g. reference timestamp, metadata).
        :return: Dictionary containing extracted domain entities and scores.
        """
        pass

