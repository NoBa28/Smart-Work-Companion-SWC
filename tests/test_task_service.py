import pytest

from services.task_service import TaskService
from storage.json_storage import JsonStorage
from storage.task_repository import TaskRepository


@pytest.fixture
def service(tmp_path):
    storage = JsonStorage(str(tmp_path / "tasks.json"))
    repo = TaskRepository(storage=storage)
    return TaskService(repo=repo)


def test_add_task_success(service):
    task = service.add_task("Learn Python", "high")

    assert task.title == "Learn Python"
    assert task.priority == "high"
    assert task.done is False
    assert task.id is not None


def test_add_task_empty_title_raises_error(service):
    with pytest.raises(ValueError):
        service.add_task("", "high")


def test_add_task_whitespace_title_raises_error(service):
    with pytest.raises(ValueError):
        service.add_task("   ", "high")


def test_add_task_invalid_priority_raises_error(service):
    with pytest.raises(ValueError):
        service.add_task("Learn Python", "invalid")


def test_get_tasks_returns_list(service):
    tasks = service.get_tasks()

    assert isinstance(tasks, list)


def test_get_tasks_contains_added_task(service):
    created = service.add_task("Test Task", "medium")
    tasks = service.get_tasks()

    assert any(task.id == created.id for task in tasks)


def test_get_task_by_existing_id(service):
    created = service.add_task("Task A", "low")

    task = service.get_task(created.id)

    assert task is not None
    assert task.id == created.id


def test_get_task_by_invalid_id_returns_none(service):
    task = service.get_task("does-not-exist")

    assert task is None


def test_delete_existing_task(service):
    created = service.add_task("Delete Me", "high")

    deleted = service.delete_task(created.id)

    assert deleted is True
    assert service.get_task(created.id) is None


def test_delete_non_existing_task_returns_false(service):
    deleted = service.delete_task("invalid-id")

    assert deleted is False


def test_complete_task(service):
    created = service.add_task("Finish me", "high")

    updated = service.complete_task(created.id)

    assert updated.done is True


def test_complete_task_invalid_id_raises_error(service):
    with pytest.raises(ValueError):
        service.complete_task("invalid-id")
