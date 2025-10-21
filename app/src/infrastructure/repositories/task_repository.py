"""Repository concrete implementations.

This module contains concrete implementations of repository interfaces
using SQLModel/SQLAlchemy for data persistence.
"""

from typing import List, Optional

from sqlmodel import Session, col, select

from app.src.domain.aggregates.entities.task import Task
from app.src.domain.repositories.abstractions import ITaskRepository


class SQLModelTaskRepository(ITaskRepository):
    """
    SQLModel-based implementation of the task repository.

    Implements the ITaskRepository interface using SQLModel/SQLAlchemy
    for database operations.
    """

    def __init__(self, session: Session):
        """Initialize the repository with a database session."""
        self._session = session

    async def create(self, task: Task) -> Task:
        """Create a new task."""
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Get a task by its ID."""
        statement = select(Task).where(Task.id == task_id)
        result = self._session.exec(statement)
        return result.first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks with pagination."""
        statement = select(Task).offset(skip).limit(limit)
        result = self._session.exec(statement)
        return list(result.all())

    async def update(self, task: Task) -> Task:
        """Update an existing task."""
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    async def delete(self, task_id: str) -> bool:
        """Delete a task by its ID."""
        task = await self.get_by_id(task_id)
        if task:
            self._session.delete(task)
            self._session.commit()
            return True
        return False

    async def get_by_title(self, title: str) -> List[Task]:
        """Get tasks by title (search functionality)."""
        statement = select(Task).where(
            col(Task.title).like(f"%{title}%")  # pylint: disable=no-member
        )
        result = self._session.exec(statement)
        return list(result.all())

    async def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks."""
        statement = select(Task).where(Task.completed is True)
        result = self._session.exec(statement)
        return list(result.all())

    async def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks."""
        statement = select(Task).where(Task.completed is False)
        result = self._session.exec(statement)
        return list(result.all())
