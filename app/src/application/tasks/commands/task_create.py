"""Task creation command."""

from typing import Optional

from pydantic import BaseModel

from app.src.core.mediator.abstractions import IRequest


class TaskCreateCommand(BaseModel, IRequest[str]):
    """Command for creating a task."""

    title: str
    description: Optional[str] = None
    priority: Optional[int] = 1
    completed: Optional[bool] = False
