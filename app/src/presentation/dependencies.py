"""Application dependency provider following DDD and SOLID principles.

This module provides a clean interface for dependency injection in the presentation layer,
organizing dependencies by bounded contexts and following the Dependency Inversion Principle.
"""

from typing import Annotated

from app.src.core.mediator.mediator import Mediator
from app.src.infrastructure.dependencies import ContainerDep, SessionDep
from fastapi import Depends


def get_task_mediator(
    container: ContainerDep,
    session: SessionDep,
) -> Mediator:
    """
    Get a mediator configured for task operations.

    This function follows the Factory pattern to create a mediator
    with all task-related dependencies properly injected.
    """
    return container.create_mediator(session)


# Type alias for dependency injection in task-related endpoints
TaskMediatorDep = Annotated[Mediator, Depends(get_task_mediator)]
