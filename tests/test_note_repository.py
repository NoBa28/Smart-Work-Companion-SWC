from datetime import datetime
import json
import pytest

from domain.note import Note
from storage.json_storage import JsonStorage
from storage.note_repository import NoteRepository


@pytest.fixture
def repo(tmp_path):
    storage = JsonStorage(str(tmp_path / "notes.json"))
    return NoteRepository(storage=storage)


def create_note(text="Test note") -> Note:
    return Note(id="1", text=text, created_at=datetime(2024, 1, 1, 12, 0, 0))


def test_add_note(repo):
    note = create_note()

    repo.add(note)

    notes = repo.get_all()

    assert len(notes) == 1
    assert notes[0].id == "1"
    assert notes[0].text == "Test note"


def test_get_all_empty(repo):
    assert repo.get_all() == []


def test_save_all_overwrites(repo):
    note1 = create_note("A")
    note2 = create_note("B")

    repo.save_all([note1])
    repo.save_all([note2])

    notes = repo.get_all()

    assert len(notes) == 1
    assert notes[0].text == "B"


def test_find_by_id_existing(repo):
    note = create_note()

    repo.add(note)

    found = repo.find_by_id("1")

    assert found is not None
    assert found.id == "1"


def test_find_by_id_non_existing(repo):
    result = repo.find_by_id("does-not-exist")

    assert result is None


def test_update_note(repo):
    note = create_note()
    repo.add(note)

    note.text = "Updated"
    repo.update(note)

    updated = repo.find_by_id("1")

    assert updated.text == "Updated"


def test_update_non_existing_raises(repo):
    note = create_note()

    try:
        repo.update(note)
        assert False, "Expected ValueError"
    except ValueError:
        assert True


def test_delete_note(repo):
    note = create_note()
    repo.add(note)

    result = repo.delete("1")

    assert result is True
    assert repo.get_all() == []


def test_delete_non_existing(repo):
    result = repo.delete("does-not-exist")

    assert result is False


def test_json_persistence_format(repo, tmp_path):
    note = create_note()

    repo.add(note)

    file_path = tmp_path / "notes.json"
    raw = json.loads(file_path.read_text())

    assert isinstance(raw, list)
    assert raw[0]["id"] == "1"
    assert raw[0]["text"] == "Test note"
