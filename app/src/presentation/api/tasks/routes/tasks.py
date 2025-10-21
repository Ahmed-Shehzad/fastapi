"""Task API routes."""

from app.src.application.tasks.commands import TaskCreateCommand
from app.src.presentation.dependencies import TaskMediatorDep
from fastapi import APIRouter, status

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.post("/", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_task(*, task: TaskCreateCommand, mediator: TaskMediatorDep) -> str:
    """Create a new task."""
    result = await mediator.send(task)
    return result
