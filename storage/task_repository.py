from domain.task import Task
from storage.json_storage import JsonStorage


class TaskRepository:

    def __init__(self, file_path="data/tasks.json"):
        self.storage = JsonStorage(file_path)

    def get_all(self) -> list[Task]:
        raw = self.storage.load()
        return [Task.from_dict(t) for t in raw]

    def save_all(self, tasks: list[Task]) -> None:
        data = [t.to_dict() for t in tasks]
        self.storage.save(data)

    def add(self, task: Task) -> None:
        tasks = self.get_all()
        tasks.append(task)
        self.save_all(tasks)

    def update(self, task: Task) -> None:
        tasks = self.get_all()
        for i, t in enumerate(tasks):
            if t.id == task.id:
                tasks[i] = task
                self.save_all(tasks)
                break
        raise ValueError(f"Task with id {task.id} not found")

    def delete(self, task_id: str) -> bool:
        tasks = self.get_all()
        original_len = len(tasks)

        tasks = [t for t in tasks if t.id != task_id]

        if len(tasks) < original_len:
            self.save_all(tasks)
            return True

        return False

    def find_by_id(self, task_id: str) -> Task | None:
        return next((t for t in self.get_all() if t.id == task_id), None)
