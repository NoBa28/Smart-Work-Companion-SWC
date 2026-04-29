from datetime import datetime


class Session:

    def __init__(self, id: str, project: str, start_time: datetime, end_time: datetime):
        self.id = id
        self.project = project
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Session(**data)
