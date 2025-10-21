"""Domain repositories package.

Contains repository interfaces following the Repository pattern from DDD.
These abstractions define contracts for data access operations without
depending on specific infrastructure implementations.
"""

from .abstractions import ITaskRepository

__all__ = ["ITaskRepository"]
