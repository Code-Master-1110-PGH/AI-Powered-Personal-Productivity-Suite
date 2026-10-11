"""
Domain Exceptions & Error Handling.

Custom domain-specific exceptions and error representation models.
"""

from typing import Any, Optional


class ProductivityAppException(Exception):
    """Base exception for all application domain errors."""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.details = details


class EntityNotFoundException(ProductivityAppException):
    """Raised when an entity is not found in the database."""
    pass


class AIInferenceException(ProductivityAppException):
    """Raised when an AI/NLU model fails parsing or extraction."""
    pass


class SchedulingConflictException(ProductivityAppException):
    """Raised when an operation results in an invalid scheduling conflict."""
    pass


class ValidationException(ProductivityAppException):
    """Raised when domain validation rules are violated."""
    pass

