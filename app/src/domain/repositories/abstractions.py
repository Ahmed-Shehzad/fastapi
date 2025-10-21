"""Repository abstractions.

This module defines repository interfaces following the Repository pattern
and Dependency Inversion Principle from SOLID.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from app.src.domain.aggregates.entities.task import Task


class ITaskRepository(ABC):
    """
    Abstract task repository interface.

    Defines the contract for task data access operations,
    following the Repository pattern from DDD.
    """

    @abstractmethod
    async def create(self, task: Task) -> Task:
        """Create a new task."""
        pass

    @abstractmethod
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Get a task by its ID."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks with pagination."""
        pass

    @abstractmethod
    async def update(self, task: Task) -> Task:
        """Update an existing task."""
        pass

    @abstractmethod
    async def delete(self, task_id: str) -> bool:
        """Delete a task by its ID."""
        pass

    @abstractmethod
    async def get_by_title(self, title: str) -> List[Task]:
        """Get tasks by title (search functionality)."""
        pass

    @abstractmethod
    async def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks."""
        pass

    @abstractmethod
    async def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks."""
        pass
