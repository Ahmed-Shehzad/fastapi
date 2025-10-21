"""Task Management API main module."""

from src.presentation.api.tasks import router as tasks_router

from app.src.core.config.config import IS_DEVELOPMENT
from fastapi import FastAPI

app = FastAPI(
    title="Task Management API",
    description="API for managing tasks with FastAPI, SQLModel, and Pydantic",
    version="0.1.0",
)

# Include routers
app.include_router(tasks_router)


@app.get("/")
async def root():
    """Health check endpoint for the API."""
    return {"message": "Welcome to the Task Management API"}


if __name__ == "__main__":
    import uvicorn

    if IS_DEVELOPMENT:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
