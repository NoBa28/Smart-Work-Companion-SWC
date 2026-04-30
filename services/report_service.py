from datetime import datetime

from services.task_service import TaskService
from services.tracker_service import TrackerService
from services.note_service import NoteService


class ReportService:

    def __init__(
        self,
        task_service: TaskService,
        tracker_service: TrackerService,
        note_service: NoteService,
    ):
        self.task_service = task_service
        self.tracker_service = tracker_service
        self.note_service = note_service

    def generate_report(self) -> dict:
        tasks = self.task_service.get_tasks()
        sessions = self.tracker_service.get_sessions()
        notes = self.note_service.get_notes()

        report = {
            "generated_at": datetime.now().isoformat(),
            "tasks": [t.to_dict() for t in tasks],
            "sessions": [s.to_dict() for s in sessions],
            "notes": [n.to_dict() for n in notes],
        }

        return report

    def get_total_tracked_time(self) -> int:
        sessions = self.tracker_service.get_sessions()
        total_seconds = sum(
            (s.end_time - s.start_time).total_seconds()
            for s in sessions
            if s.end_time is not None
        )
        return int(total_seconds)

    def get_active_session_report(self) -> dict | None:
        active = self.tracker_service.get_active_session()

        if not active:
            return None

        task = self.task_service.get_task(active.task_id)
        notes = self.note_service.get_notes()

        return {
            "session": active.to_dict(),
            "task": task.to_dict() if task else None,
            "notes": [n.to_dict() for n in notes],
        }

    def get_open_tasks_count(self) -> int:
        tasks = self.task_service.get_tasks()
        return sum(1 for t in tasks if not t.done)
