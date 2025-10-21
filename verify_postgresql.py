#!/usr/bin/env python3
"""
PostgreSQL Connection Verification Script

This script verifies the PostgreSQL connection and displays current task data.
"""

import sys
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

from sqlmodel import Session, select

from app.src.domain.aggregates.entities.task import Task
from app.src.infrastructure.database.config import engine


def verify_postgresql_connection():
    """Verify PostgreSQL connection and display task data."""
    print("🔍 Verifying PostgreSQL connection...")

    try:
        with Session(engine) as session:
            # Test the connection
            print("✅ PostgreSQL connection successful!")

            # Get all tasks
            statement = select(Task)
            tasks = session.exec(statement).all()

            print(f"\n📊 Current tasks in PostgreSQL database: {len(tasks)}")
            print("-" * 80)

            if tasks:
                for task in tasks:
                    print(f"🆔 ID: {task.id}")
                    print(f"📝 Title: {task.title}")
                    print(f"📄 Description: {task.description}")
                    print(f"⭐ Priority: {task.priority}")
                    print(f"✅ Completed: {task.completed}")
                    print(f"📅 Created: {task.created_at}")
                    print(f"🕒 Updated: {task.updated_at}")
                    print("-" * 80)
            else:
                print("📭 No tasks found in the database.")

            return True

    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False


if __name__ == "__main__":
    success = verify_postgresql_connection()
    sys.exit(0 if success else 1)
