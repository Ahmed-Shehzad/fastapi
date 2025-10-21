"""Database configuration and setup."""

import os
from typing import Any, Dict, Generator

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, SQLModel, create_engine

# Database URL - PostgreSQL configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://taskuser:taskpassword@localhost:5432/taskdb"
)

# Connection pool settings for PostgreSQL
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "20"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "30"))
DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "3600"))

# Validate that we're using PostgreSQL
if not DATABASE_URL.startswith("postgresql"):
    raise ValueError(
        f"Expected PostgreSQL database URL, but got: {DATABASE_URL}. "
        "Please ensure DATABASE_URL starts with 'postgresql://'"
    )

# Create PostgreSQL engine with connection pooling
engine_kwargs: Dict[str, Any] = {
    "echo": True,
    "pool_size": DB_POOL_SIZE,
    "max_overflow": DB_MAX_OVERFLOW,
    "pool_timeout": DB_POOL_TIMEOUT,
    "pool_recycle": DB_POOL_RECYCLE,
    "pool_pre_ping": True,  # Validate connections before use
}

try:
    engine = create_engine(DATABASE_URL, **engine_kwargs)
    print(f"✅ Successfully configured PostgreSQL connection: {DATABASE_URL}")
except SQLAlchemyError as e:
    print(f"❌ Failed to create PostgreSQL engine: {e}")
    raise RuntimeError(
        f"Cannot connect to PostgreSQL database. "
        f"Please ensure PostgreSQL is running and accessible at: {DATABASE_URL}"
    ) from e


def create_db_and_tables():
    """Create database and tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session."""
    with Session(engine) as session:
        yield session
