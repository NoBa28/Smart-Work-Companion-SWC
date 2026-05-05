from datetime import datetime
import pytest

from domain.session import Session
from services.tracker_service import TrackerService
from storage.session_repository import SessionRepository


@pytest.fixture
def repo(tmp_path):
    storage = None
    repo = SessionRepository(storage=storage, file_path=str(tmp_path / "sessions.json"))
    return repo


def create_session(
    session_id="1",
    project="P",
    task_id="T",
    active=True,
):
    return Session(
        id=session_id,
        project=project,
        task_id=task_id,
        start_time=datetime(2024, 1, 1, 12, 0, 0),
        end_time=None if active else datetime(2024, 1, 1, 13, 0, 0),
    )


def test_start_session(repo):
    service = TrackerService(repo)

    session = service.start_session("Project A", "task-1")

    assert session.project == "Project A"
    assert session.task_id == "task-1"
    assert session.end_time is None

    sessions = repo.get_all()
    assert len(sessions) == 1
    assert sessions[0].id == session.id


def test_start_session_when_active_exists(repo):
    repo.add(create_session("1", active=True))

    service = TrackerService(repo)

    try:
        service.start_session("P", "T")
        assert False
    except ValueError:
        assert True


def test_get_active_session(repo):
    repo.add(create_session("1", active=False))
    repo.add(create_session("2", active=True))

    service = TrackerService(repo)

    active = service.get_active_session()

    assert active is not None
    assert active.id == "2"


def test_stop_session(repo):
    session = create_session("1", active=True)
    repo.add(session)

    service = TrackerService(repo)

    updated = service.stop_session("1")

    assert updated.end_time is not None

    stored = repo.find_by_id("1")
    assert stored.end_time is not None


def test_stop_session_not_found(repo):
    service = TrackerService(repo)

    try:
        service.stop_session("missing")
        assert False
    except ValueError:
        assert True


def test_stop_session_already_stopped(repo):
    repo.add(create_session("1", active=False))

    service = TrackerService(repo)

    try:
        service.stop_session("1")
        assert False
    except ValueError:
        assert True


def test_get_sessions(repo):
    repo.add(create_session("1"))

    service = TrackerService(repo)

    sessions = service.get_sessions()

    assert len(sessions) == 1
