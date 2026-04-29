from datetime import datetime


class Note:

    def __init__(self, id: str, text: str, created_at: datetime):
        self.id = id
        self.text = text
        self.created_at = created_at

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Note(**data)
