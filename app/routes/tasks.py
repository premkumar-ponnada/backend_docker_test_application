"""All /tasks endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.models.task import Task, TaskCreate
from app.services.task_service import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[Task], status_code=status.HTTP_200_OK)
def get_tasks() -> list[Task]:
    """Return every task currently held in memory."""
    return task_service.list_tasks()


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    """Create a task. FastAPI returns 422 automatically if the body is invalid."""
    return task_service.add_task(payload.title)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
    """Delete a task by id, or 404 if that id does not exist."""
    if not task_service.delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
