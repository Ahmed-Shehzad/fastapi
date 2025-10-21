"""Application layer dependencies.

This module manages application service dependencies organized by bounded contexts.
It orchestrates the interaction between domain and infrastructure layers.
"""

from typing import Any, Dict, Type

from sqlmodel import Session

from app.src.application.tasks.command_handlers.task_create_command_handler import (
    TaskCreateCommandHandler,
)
from app.src.application.tasks.commands.task_create import TaskCreateCommand
from app.src.core.mediator.mediator import Mediator
from app.src.infrastructure.dependencies.domain import DomainDependencies
from app.src.infrastructure.dependencies.infrastructure import (
    InfrastructureDependencies,
)


class TaskApplicationServices:
    """
    Task bounded context application services.

    Contains all task-related application logic and command/query handlers.
    """

    def __init__(
        self,
        infrastructure_deps: InfrastructureDependencies,
        domain_deps: DomainDependencies,
    ):
        """Initialize task application services."""
        self._infrastructure_deps = infrastructure_deps
        self._domain_deps = domain_deps

    def create_command_handlers(self, session: Session) -> Dict[Type[Any], Any]:
        """Create command handlers with their dependencies."""
        # Create repository instances
        task_repository = self._infrastructure_deps.create_task_repository(session)

        # Create command handlers with their dependencies
        return {TaskCreateCommand: TaskCreateCommandHandler(task_repository)}

    def create_task_mediator(self, session: Session) -> Mediator:
        """Create a mediator configured with task handlers."""
        mediator = Mediator()

        # Register all task command handlers
        command_handlers = self.create_command_handlers(session)
        for command_type, handler in command_handlers.items():
            mediator.register_request_handler(command_type, handler)

        return mediator


class ApplicationDependencies:
    """
    Main application dependencies container.

    Orchestrates all application services across different bounded contexts.
    """

    def __init__(
        self,
        infrastructure_deps: InfrastructureDependencies,
        domain_deps: DomainDependencies,
    ):
        """Initialize application dependencies."""
        self._infrastructure_deps = infrastructure_deps
        self._domain_deps = domain_deps

        # Initialize bounded context services
        self._task_services = TaskApplicationServices(infrastructure_deps, domain_deps)

    @property
    def task_services(self) -> TaskApplicationServices:
        """Get task application services."""
        return self._task_services

    def create_mediator(self, session: Session) -> Mediator:
        """Create a fully configured mediator with all application services."""
        mediator = Mediator()

        # Register handlers from all bounded contexts
        task_handlers = self._task_services.create_command_handlers(session)
        for command_type, handler in task_handlers.items():
            mediator.register_request_handler(command_type, handler)

        # Future: Add other bounded contexts here
        # user_handlers = self._user_services.create_command_handlers(session)
        # project_handlers = self._project_services.create_command_handlers(session)

        return mediator
