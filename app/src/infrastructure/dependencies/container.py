"""Infrastructure dependency injection container.

This module contains the main DI container following the Dependency Inversion Principle.
It orchestrates all dependencies across different layers and bounded contexts.
"""

from typing import Annotated

from sqlmodel import Session

from app.src.core.mediator.mediator import Mediator
from app.src.infrastructure.database.config import get_session
from app.src.infrastructure.dependencies.application import ApplicationDependencies
from app.src.infrastructure.dependencies.domain import DomainDependencies
from app.src.infrastructure.dependencies.infrastructure import (
    InfrastructureDependencies,
)
from fastapi import Depends


class DIContainer:
    """
    Main Dependency Injection Container.

    Follows the Composition Root pattern, centrally managing all dependencies
    and their composition according to DDD and SOLID principles.
    """

    def __init__(self):
        """Initialize the DI container with all dependency modules."""
        self._infrastructure = InfrastructureDependencies()
        self._domain = DomainDependencies()
        self._application = ApplicationDependencies(
            infrastructure_deps=self._infrastructure,
            domain_deps=self._domain,
        )

    @property
    def infrastructure(self) -> InfrastructureDependencies:
        """Get infrastructure dependencies."""
        return self._infrastructure

    @property
    def domain(self) -> DomainDependencies:
        """Get domain dependencies."""
        return self._domain

    @property
    def application(self) -> ApplicationDependencies:
        """Get application dependencies."""
        return self._application

    def create_mediator(self, session: Session) -> Mediator:
        """Create a configured mediator with all dependencies."""
        return self._application.create_mediator(session)


# Module-level DI container instance (Singleton pattern)
_container: DIContainer | None = None


def get_container() -> DIContainer:
    """Get the DI container instance."""
    global _container
    if _container is None:
        _container = DIContainer()
    return _container


# FastAPI dependency for database session
SessionDep = Annotated[Session, Depends(get_session)]

# FastAPI dependency for DI container
ContainerDep = Annotated[DIContainer, Depends(get_container)]
