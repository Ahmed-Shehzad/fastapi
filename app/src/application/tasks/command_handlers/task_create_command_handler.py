from app.src.application.tasks.commands.task_create import TaskCreateCommand
from app.src.core.mediator import IRequestHandler
from app.src.domain.aggregates.entities.task import Task
from app.src.domain.repositories.abstractions import ITaskRepository


class TaskCreatedEvent:
    """Event for task creation."""

    def __init__(self, task_id: str, title: str):
        self.task_id = task_id
        self.title = title


class TaskCreateCommandHandler(IRequestHandler[TaskCreateCommand, str]):
    """Handler for task creation commands."""

    def __init__(self, task_repository: ITaskRepository):
        """Initialize handler with repository dependency."""
        self._task_repository = task_repository

    async def handle(self, request: TaskCreateCommand) -> str:
        """Handle the task creation command.

        Args:
            request (TaskCreateCommand): The command containing task details.

        Returns:
            str: The ID of the created task.
        """
        # Create new task entity
        new_task = Task(
            title=request.title,
            description=request.description,
            priority=request.priority or 1,
            completed=request.completed or False,
        )

        # Save using repository pattern
        saved_task = await self._task_repository.create(new_task)

        # In a real application, you would also publish a TaskCreatedEvent here
        # domain_events.publish(TaskCreatedEvent(saved_task.id, saved_task.title))

        return saved_task.id
