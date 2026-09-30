"""In-memory task storage.

No database on purpose. The list below lives in the Python process, so the
data disappears when the server (or the container) restarts. That is exactly
the lesson we want later: containers are disposable, their memory is not
persistent storage.
"""

from app.models.task import Task


class TaskService:
    def __init__(self) -> None:
        self.tasks: list[Task] = []
        self._next_id: int = 1

    def list_tasks(self) -> list[Task]:
        return self.tasks

    def add_task(self, title: str) -> Task:
        task = Task(id=self._next_id, title=title)
        self._next_id += 1
        self.tasks.append(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        """Return True if a task was removed, False if the id did not exist."""
        for index, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(index)
                return True
        return False


# One shared instance for the whole app.
task_service = TaskService()
