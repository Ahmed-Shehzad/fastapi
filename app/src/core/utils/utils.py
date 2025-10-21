"""Utility functions."""

import uuid


def generate_uuid():
    """
    Generate a unique UUID for a task.

    This function creates a new UUID (Universally Unique Identifier) using the
    uuid4() method, which generates a random UUID. The UUID is converted to a
    string format for easy usage and storage.

    Returns:
        str: A string representation of a randomly generated UUID.

    Example:
        >>> uuid_string = generate_uuid()
        >>> print(uuid_string)
        'f47ac10b-58cc-4372-a567-0e02b2c3d479'
    """
    return str(uuid.uuid4())


def is_valid_uuid(val: str) -> bool:
    """
    Check if the provided value is a valid UUID version 4.

        This function validates whether a given string represents a valid UUID version 4
        by attempting to parse it and comparing the result with the original input to
        ensure proper formatting.

        Args:
            val (str): The string value to validate as a UUID.

        Returns:
            bool: True if the value is a valid UUID version 4, False otherwise.

        Example:
            >>> is_valid_uuid("550e8400-e29b-41d4-a716-446655440000")
            True
            >>> is_valid_uuid("invalid-uuid")
            False
            >>> is_valid_uuid("550e8400-e29b-41d4-a716-44665544000")  # Missing digit
            False
    """

    try:
        uuid_obj = uuid.UUID(val, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == val
