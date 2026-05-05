import json
import pytest

from domain.task import Task
from storage.json_storage import JsonStorage
from storage.task_repository import TaskRepository


@pytest.fixture
def repo(tmp_path):
    storage = JsonStorage(str(tmp_path / "tasks.json"))
    return TaskRepository(storage=storage)


def create_task(text="Test task") -> Task:
    return Task(id="1", title=text, priority="medium", done=False)


def test_add_task(repo):
    task = create_task()

    repo.add(task)

    tasks = repo.get_all()

    assert len(tasks) == 1
    assert tasks[0].id == "1"
    assert tasks[0].title == "Test task"
    assert tasks[0].priority == "medium"
    assert tasks[0].done == False


def test_get_all_empty(repo):
    assert repo.get_all() == []


def test_save_all_overwrites(repo):
    task1 = create_task("A")
    task2 = create_task("B")

    repo.save_all([task1])
    repo.save_all([task2])

    tasks = repo.get_all()

    assert len(tasks) == 1
    assert tasks[0].title == "B"


def test_find_by_id_existing(repo):
    task = create_task()

    repo.add(task)

    found = repo.find_by_id("1")

    assert found is not None
    assert found.id == "1"


def test_find_by_id_non_existing(repo):
    result = repo.find_by_id("does-not-exist")

    assert result is None


def test_update_task(repo):
    task = create_task()
    repo.add(task)

    task.title = "Updated"
    repo.update(task)

    updated = repo.find_by_id("1")

    assert updated.title == "Updated"


def test_update_non_existing_raises(repo):
    task = create_task()

    try:
        repo.update(task)
        assert False, "Expected ValueError"
    except ValueError:
        assert True


def test_delete_task(repo):
    task = create_task()
    repo.add(task)

    result = repo.delete("1")

    assert result is True
    assert repo.get_all() == []


def test_delete_non_existing(repo):
    result = repo.delete("does-not-exist")

    assert result is False


def test_json_persistence_format(repo, tmp_path):
    task = create_task()

    repo.add(task)

    file_path = tmp_path / "tasks.json"
    raw = json.loads(file_path.read_text())

    assert isinstance(raw, list)
    assert raw[0]["id"] == "1"
    assert raw[0]["title"] == "Test task"
