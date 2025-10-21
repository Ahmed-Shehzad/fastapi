"""Infrastructure repositories package.

Contains concrete implementations of repository interfaces using
specific infrastructure technologies like SQLModel, MongoDB, etc.
"""

from .task_repository import SQLModelTaskRepository

__all__ = ["SQLModelTaskRepository"]
