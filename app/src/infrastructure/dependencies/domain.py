"""Domain layer dependencies.

This module manages domain-specific dependencies including domain services,
value objects, and domain rules that are independent of infrastructure concerns.
"""

from app.src.core.utils.utils import generate_uuid, is_valid_uuid


class DomainDependencies:
    """
    Domain dependencies container.

    Manages pure domain logic dependencies that are independent
    of infrastructure and application concerns.
    """

    def __init__(self):
        """Initialize domain dependencies."""
        self._uuid_generator = generate_uuid
        self._uuid_validator = is_valid_uuid

    def get_uuid_generator(self):
        """Get UUID generator function."""
        return self._uuid_generator

    def get_uuid_validator(self):
        """Get UUID validator function."""
        return self._uuid_validator

    # Domain services can be added here as the application grows
    # For example:
    # - Task priority calculation service
    # - Task validation rules
    # - Business rule validators
    # - Domain event handlers
