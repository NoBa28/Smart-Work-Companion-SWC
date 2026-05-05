from datetime import datetime
import pytest

from services.report_service import ReportService
from services.task_service import TaskService
from services.tracker_service import TrackerService
from services.note_service import NoteService

from storage.task_repository import TaskRepository
from storage.session_repository import SessionRepository
from storage.note_repository import NoteRepository

from storage.json_storage import JsonStorage

from domain.task import Task
from domain.session import Session
from domain.note import Note


@pytest.fixture
def service(tmp_path):
    task_storage = JsonStorage(str(tmp_path / "tasks.json"))
    task_repo = TaskRepository(storage=task_storage)
    task_service = TaskService(repo=task_repo)

    session_storage = JsonStorage(str(tmp_path / "sessions.json"))
    session_repo = SessionRepository(storage=session_storage)
    tracker_service = TrackerService(repo=session_repo)

    note_storage = JsonStorage(str(tmp_path / "notes.json"))
    note_repo = NoteRepository(storage=note_storage)
    note_service = NoteService(repo=note_repo)

    return ReportService(task_service, tracker_service, note_service)


def create_session(session_id="s1", task_id="t1", active=False):
    return Session(
        id=session_id,
        project="Project",
        task_id=task_id,
        start_time=datetime(2024, 1, 1, 10, 0, 0),
        end_time=None if active else datetime(2024, 1, 1, 11, 0, 0),
    )


def test_generate_report(service):
    service.task_service.add_task("Task 1", "medium")
    service.tracker_service.repo.add(create_session("s1"))
    service.note_service.add_note("Hello")

    report = service.generate_report()

    assert "generated_at" in report
    assert len(report["tasks"]) == 1
    assert len(report["sessions"]) == 1
    assert len(report["notes"]) == 1


def test_get_total_tracked_time(service):
    service.tracker_service.repo.add(create_session("s1"))
    service.tracker_service.repo.add(create_session("s2"))

    assert service.get_total_tracked_time() == 2 * 3600


def test_get_total_tracked_time_ignores_open_sessions(service):
    service.tracker_service.repo.add(create_session("s1", active=True))

    assert service.get_total_tracked_time() == 0


def test_get_active_session_report(service):
    task = service.task_service.add_task("Task A", "medium")

    session = create_session("s1", task_id=task.id, active=True)
    service.tracker_service.repo.add(session)

    service.note_service.add_note("note")

    result = service.get_active_session_report()

    assert result is not None
    assert result["session"]["id"] == "s1"
    assert result["task"]["id"] == result["task"]["id"]
    assert len(result["notes"]) == 1


def test_get_active_session_report_none(service):
    assert service.get_active_session_report() is None


def test_get_open_tasks_count(service):
    service.task_service.add_task("A", "medium")
    service.task_service.add_task("B", "medium")
    service.task_service.add_task("C", "medium")

    tasks = service.task_service.get_tasks()
    tasks[1].done = True
    service.task_service.repo.save_all(tasks)

    assert service.get_open_tasks_count() == 2
