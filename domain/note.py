from datetime import datetime


class Note:

    def __init__(self, id: str, text: str, created_at: datetime):
        self.id = id
        self.text = text
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
        }

    @staticmethod
    def from_dict(data):
        return Note(
            id=data["id"],
            text=data["text"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )
