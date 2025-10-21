from app.src.application.tasks.commands.task_create import TaskCreateCommand
from app.src.core.mediator import IRequestHandler
from app.src.domain.aggregates.entities.task import Task


class TaskCreatedEvent:
    """Event for task creation."""

    def __init__(self, task_id: str, title: str):
        self.task_id = task_id
        self.title = title


class TaskCreateCommandHandler(IRequestHandler[TaskCreateCommand, str]):
    """Handler for task creation commands."""

    async def handle(self, request: TaskCreateCommand) -> str:
        """Handle the task creation command.

        Args:
            request (TaskCreateCommand): The command containing task details.

        Returns:
            str: The ID of the created task.
        """
        # Simulate task creation logic
        new_task = Task(
            title=request.title,
            description=request.description,
            priority=request.priority or 1,
            completed=request.completed or False,
        )
        # In a real application, you would save the task to a database here
        # and possibly publish a TaskCreatedEvent.

        # For demonstration, we return the task ID
        return new_task.id
