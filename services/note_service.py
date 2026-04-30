from storage.note_repository import NoteRepository
from domain.note import Note
from datetime import datetime
import uuid


class NoteService:

    def __init__(self):
        self.repo = NoteRepository()

    def add_note(self, text: str) -> Note:
        self.validate_text(text)
        note = Note(id=str(uuid.uuid4()), text=text, created_at=datetime.now())
        self.repo.add(note)
        return note

    def get_notes(self) -> list[Note]:
        return self.repo.get_all()

    def get_note(self, note_id: str) -> Note | None:
        return self.repo.find_by_id(note_id)

    def delete_note(self, note_id: str) -> bool:
        return self.repo.delete(note_id)

    def validate_text(self, text: str) -> None:
        if not text or not text.strip():
            raise ValueError("Note text cannot be empty")
