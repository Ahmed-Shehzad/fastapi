from typing import Any, Callable, Dict, List


class ValidationErrorDetail:
    """Represents a validation error detail."""

    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return {"field": self.field, "message": self.message}


class Rule:
    """Represents a validation rule."""

    def __init__(self, field: str):
        self.field = field
        self._predicate = None
        self._message = "Invalid"

    def must(self, predicate: Callable[[Any], bool]) -> "Rule":
        """Set validation predicate."""
        self._predicate = predicate
        return self

    def with_message(self, message: str) -> "Rule":
        """
        Set a custom validation message for this rule.

        Args:
            message (str): The custom validation message to display when this rule fails.

        Returns:
            Rule: Returns self to allow method chaining.

        Example:
            >>> rule = Rule().with_message("Custom error message")
            >>> # Chain with other methods
            >>> rule.with_message("Invalid input").some_other_method()
        """
        self._message = message
        return self

    def validate(self, instance: Any) -> List[ValidationErrorDetail]:
        """Validate instance against rule."""
        if self._predicate is None:
            return []
        value = getattr(instance, self.field, None)
        if not self._predicate(value):
            return [ValidationErrorDetail(self.field, self._message)]
        return []


class Validator:
    """Validates objects using defined rules."""

    def __init__(self):
        self._rules: list[Rule] = []

    def rule_for(self, field: str) -> Rule:
        """Create a rule for a field."""
        rule = Rule(field)
        self._rules.append(rule)
        return rule

    def validate(self, instance: Any) -> List[Dict[str, str]]:
        """Validate instance against all rules."""
        errors: List[ValidationErrorDetail] = []
        for rule in self._rules:
            errors.extend(rule.validate(instance))
        return [e.to_dict() for e in errors]


validator_registry: dict[type, Validator] = {}


def register_validator(request_type: type, validator: Validator) -> None:
    """Register a validator for a request type."""
    validator_registry[request_type] = validator
