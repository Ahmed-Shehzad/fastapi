"""Infrastructure layer dependencies.

This module manages all infrastructure-related dependencies including
database connections, external services, and cross-cutting concerns.
"""

from typing import Generator

from sqlmodel import Session

from app.src.domain.repositories.abstractions import ITaskRepository
from app.src.infrastructure.database.config import engine, get_session
from app.src.infrastructure.repositories.task_repository import SQLModelTaskRepository


class InfrastructureDependencies:
    """
    Infrastructure dependencies container.

    Manages infrastructure concerns like database connections,
    message brokers, external APIs, etc.
    """

    def __init__(self):
        """Initialize infrastructure dependencies."""
        self._engine = engine

    def get_database_session(self) -> Generator[Session, None, None]:
        """Get database session generator."""
        return get_session()

    def create_task_repository(self, session: Session) -> ITaskRepository:
        """Create a task repository instance."""
        return SQLModelTaskRepository(session)

    @property
    def database_engine(self):
        """Get the database engine."""
        return self._engine

    def health_check(self) -> dict[str, str]:
        """Perform infrastructure health checks."""
        try:
            # Test database connection by getting a session
            with next(self.get_database_session()):
                pass  # Just test the connection
            return {"database": "healthy"}
        except Exception as e:
            return {"database": f"unhealthy: {str(e)}"}
