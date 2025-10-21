from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional, Type


class ValidationException(Exception):
    """Exception raised for validation errors."""

    def __init__(self, errors: Dict[str, Any]) -> None:
        super().__init__("Validation failed")
        self.errors = errors


class BusinessRuleViolationException(Exception):
    """Exception raised for business rule violations."""

    def __init__(self, message: str):
        super().__init__(message)


class IExceptionHandler(ABC):
    """Interface for exception handlers."""

    @abstractmethod
    def handle(self, exception: Exception, request: Any) -> Any:
        """Handle an exception."""


class ExceptionHandlerRegistry:
    """Registry for exception handlers."""

    def __init__(self) -> None:
        """Initialize the registry."""
        self._handlers: dict[Type[Exception], IExceptionHandler] = {}

    def register(
        self, exception_type: Type[Exception], handler: IExceptionHandler
    ) -> None:
        """Register an exception handler."""
        self._handlers[exception_type] = handler

    def get_handler(self, exception: Exception) -> Optional[IExceptionHandler]:
        """Get handler for an exception."""
        return self._handlers.get(type(exception))


class ValidationExceptionHandler(IExceptionHandler):
    """Handler for validation exceptions."""

    def handle(self, exception: Exception, request: Any) -> Dict[str, Any]:
        if isinstance(exception, ValidationException):
            return {"type": "validation_error", "errors": exception.errors}
        return {"type": "unknown_error", "message": str(exception)}


class BusinessRuleExceptionHandler(IExceptionHandler):
    """Handler for business rule violation exceptions."""

    def handle(self, exception: Exception, request: Any) -> Dict[str, Any]:
        if isinstance(exception, BusinessRuleViolationException):
            return {"type": "business_rule_violation", "message": str(exception)}
        return {"type": "unknown_error", "message": str(exception)}
