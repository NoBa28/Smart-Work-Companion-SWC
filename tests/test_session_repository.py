from datetime import datetime
import json
import pytest

from domain.session import Session
from storage.json_storage import JsonStorage
from storage.session_repository import SessionRepository


@pytest.fixture
def repo(tmp_path):
    storage = JsonStorage(str(tmp_path / "sessions.json"))
    return SessionRepository(storage=storage)


def create_session(session_id="1"):
    return Session(
        id=session_id,
        project="Test Project",
        start_time=datetime(2024, 1, 1, 12, 0, 0),
        end_time=datetime(2024, 1, 1, 13, 0, 0),
        task_id=None,
    )


def test_add_session(repo):
    session = create_session()

    repo.add(session)

    sessions = repo.get_all()

    assert len(sessions) == 1
    assert sessions[0].id == "1"


def test_get_all_empty(repo):
    assert repo.get_all() == []


def test_save_all_overwrites(repo):
    s1 = create_session("1")
    s2 = create_session("2")

    repo.save_all([s1])
    repo.save_all([s2])

    sessions = repo.get_all()

    assert len(sessions) == 1
    assert sessions[0].id == "2"


def test_find_by_id_existing(repo):
    session = create_session()

    repo.add(session)

    found = repo.find_by_id("1")

    assert found is not None
    assert found.id == "1"


def test_find_by_id_non_existing(repo):
    assert repo.find_by_id("missing") is None


def test_update_session(repo):
    session = create_session()

    repo.add(session)

    session.project = "Updated"
    repo.update(session)

    updated = repo.find_by_id("1")

    assert updated.project == "Updated"


def test_update_non_existing_raises(repo):
    session = create_session("x")

    with pytest.raises(ValueError):
        repo.update(session)


def test_delete_session(repo):
    session = create_session()

    repo.add(session)

    result = repo.delete("1")

    assert result is True
    assert repo.get_all() == []


def test_delete_non_existing(repo):
    assert repo.delete("missing") is False


def test_json_persistence_format(repo, tmp_path):
    session = create_session()

    repo.add(session)

    file_path = tmp_path / "sessions.json"
    raw = json.loads(file_path.read_text())

    assert isinstance(raw, list)
    assert raw[0]["id"] == "1"
    assert raw[0]["project"] == "Test Project"
