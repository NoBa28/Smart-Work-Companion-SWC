from datetime import datetime


class Session:

    def __init__(
        self,
        id: str,
        project: str,
        start_time: datetime,
        end_time: datetime,
        task_id: str | None = None,
        notes: str = "",
    ):
        self.id = id
        self.project = project
        self.start_time = start_time
        self.end_time = end_time
        self.task_id = task_id
        self.notes = notes

    def to_dict(self):
        return {
            "id": self.id,
            "project": self.project,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "task_id": self.task_id,
            "notes": self.notes,
        }

    @staticmethod
    def from_dict(data):
        return Session(
            id=data["id"],
            project=data["project"],
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=(
                datetime.fromisoformat(data["end_time"]) if data["end_time"] else None
            ),
            task_id=data.get("task_id"),
            notes=data.get("notes", ""),
        )
