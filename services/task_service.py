import uuid

from domain.task import Task
from storage.task_repository import TaskRepository


class TaskService:

    def __init__(self, repo=None):
        self.repo = repo or TaskRepository()

    def add_task(self, title, priority) -> Task:
        self._validate_title(title)
        self._validate_priority(priority)

        task = Task(id=str(uuid.uuid4()), title=title, priority=priority, done=False)

        self.repo.add(task)
        return task
    
    def delete_task(self, task_id) -> bool:
        return self.repo.delete(task_id)

    def get_tasks(self) -> list[Task]:
        return self.repo.get_all()

    def get_task(self, task_id) -> Task | None:
        return self.repo.find_by_id(task_id)

    def complete_task(self, task_id) -> Task:
        task = self.repo.find_by_id(task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")

        task.done = True
        self.repo.update(task)

        return task

    def _validate_title(self, title) -> None:
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

    def _validate_priority(self, priority) -> None:
        if priority not in ["low", "medium", "high"]:
            raise ValueError("Priority must be one of: low, medium, high")
