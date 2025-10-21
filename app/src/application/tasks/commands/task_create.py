"""Task creation command."""

from typing import Optional

from app.src.core.mediator.abstractions import IRequest


class TaskCreateCommand(IRequest[str]):
    """Command for creating a task."""

    title: str
    description: Optional[str] = None
    priority: Optional[int] = 1
    completed: Optional[bool] = False
