from datetime import datetime

import pytest

from domain.note import Note
from services.note_service import NoteService
from storage.json_storage import JsonStorage
from storage.note_repository import NoteRepository


@pytest.fixture
def service(tmp_path):
    storage = JsonStorage(str(tmp_path / "notes.json"))
    repo = NoteRepository(storage=storage)
    return NoteService(repo=repo)


def test_add_note(service):
    note = service.add_note("Hello world")

    assert note.id is not None
    assert note.text == "Hello world"

    assert len(service.get_notes()) == 1


def test_get_notes(service):
    service.add_note("A")
    service.add_note("B")

    notes = service.get_notes()

    assert len(notes) == 2


def test_find_note_by_id(service):
    note = service.add_note("Test")

    found = service.get_note(note.id)

    assert found is not None
    assert found.text == "Test"


def test_find_note_by_id_returns_none(service):
    result = service.get_note("does-not-exist")

    assert result is None


def test_update_note(service):
    note = service.add_note("Old")

    note.text = "New"
    service.update_note(note)

    updated = service.get_note(note.id)

    assert updated.text == "New"


def test_update_non_existing_raises(service):
    note = Note(id="x", text="Ghost", created_at=datetime(2024, 1, 1, 12, 0, 0))

    with pytest.raises(ValueError):
        service.update_note(note)


def test_delete_note(service):
    note = service.add_note("To delete")

    result = service.delete_note(note.id)

    assert result is True
    assert len(service.get_notes()) == 0


def test_delete_non_existing(service):
    result = service.delete_note("missing")

    assert result is False
