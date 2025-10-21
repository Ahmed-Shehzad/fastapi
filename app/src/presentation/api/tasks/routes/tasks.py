"""Task API routes."""

from src.application.tasks.commands import TaskCreateCommand
from src.core.mediator import Mediator
from fastapi import APIRouter, status

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.post("/", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_task(*, task: TaskCreateCommand, mediator: Mediator) -> str:
    """Create a new task."""
    result = await mediator.send(task)
    return result
