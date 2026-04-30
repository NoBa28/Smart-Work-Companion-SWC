from domain.note import Note
from storage.json_storage import JsonStorage


class NoteRepository:

    def __init__(self, file_path="data/notes.json"):
        self.storage = JsonStorage(file_path)

    def get_all(self) -> list[Note]:
        raw = self.storage.load()
        return [Note.from_dict(n) for n in raw]

    def save_all(self, notes: list[Note]) -> None:
        data = [n.to_dict() for n in notes]
        self.storage.save(data)

    def add(self, note: Note) -> None:
        notes = self.get_all()
        notes.append(note)
        self.save_all(notes)

    def update(self, note: Note) -> None:
        notes = self.get_all()

        for i, n in enumerate(notes):
            if n.id == note.id:
                notes[i] = note
                self.save_all(notes)
                return
            
        raise ValueError(f"Note with id {note.id} not found")

    def delete(self, note_id: str) -> bool:
        notes = self.get_all()
        original_len = len(notes)

        notes = [n for n in notes if n.id != note_id]

        if len(notes) < original_len:
            self.save_all(notes)
            return True

        return False

    def find_by_id(self, note_id: str) -> Note | None:
        return next((n for n in self.get_all() if n.id == note_id), None)
