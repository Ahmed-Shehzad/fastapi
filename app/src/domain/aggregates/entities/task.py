"""Task entity models."""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel  # type: ignore[misc]

from app.src.core.utils import generate_uuid


class TaskBase(SQLModel):
    """Base model for task data."""

    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    priority: int = Field(default=1, ge=1, le=5)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """Database model for tasks."""

    id: str = Field(default_factory=generate_uuid, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
