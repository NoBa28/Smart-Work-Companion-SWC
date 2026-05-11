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

    def get_total_tracked_time(self) -> float:
        sessions = self.tracker_service.get_sessions()
        total = sum(
            (s.end_time - s.start_time).total_seconds()
            for s in sessions
            if s.end_time is not None
        )
        return total

    @staticmethod
    def format_duration(seconds: float) -> str:
        if seconds < 0:
            seconds = 0
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60

        if hours > 0:
            return f"{hours}h {minutes}m {secs:.0f}s"
        elif minutes > 0:
            return f"{minutes}m {secs:.1f}s"
        else:
            return f"{secs:.3f}s"

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

    def get_time_by_project(self) -> dict[str, dict]:
        sessions = self.tracker_service.get_sessions()
        result: dict[str, float] = {}
        for s in sessions:
            if s.end_time is None:
                continue
            duration = (s.end_time - s.start_time).total_seconds()
            result[s.project] = result.get(s.project, 0) + duration

        formatted = {}
        for project, secs in result.items():
            formatted[project] = {
                "seconds": secs,
                "formatted": self.format_duration(secs),
            }
        return formatted

    def get_time_by_task(self) -> list[dict]:
        tasks = {t.id: t for t in self.task_service.get_tasks()}
        sessions = self.tracker_service.get_sessions()
        result: dict[str, float] = {}
        for s in sessions:
            if s.end_time is None or not s.task_id:
                continue
            duration = (s.end_time - s.start_time).total_seconds()
            result[s.task_id] = result.get(s.task_id, 0) + duration

        output = []
        for task_id, secs in result.items():
            task = tasks.get(task_id)
            output.append({
                "task_id": task_id,
                "title": task.title if task else "Unknown task",
                "seconds": secs,
                "formatted": self.format_duration(secs),
            })
        return sorted(output, key=lambda x: x["seconds"], reverse=True)

    def get_recent_sessions(self, limit: int = 8) -> list[dict]:
        sessions = [
            s for s in self.tracker_service.get_sessions()
            if s.end_time is not None
        ]
        sessions.sort(key=lambda s: s.end_time, reverse=True)
        tasks = {t.id: t for t in self.task_service.get_tasks()}

        result = []
        for s in sessions[:limit]:
            duration = (s.end_time - s.start_time).total_seconds() if s.end_time else 0
            task = tasks.get(s.task_id) if s.task_id else None
            d = s.to_dict()
            d["duration_seconds"] = duration
            d["duration_formatted"] = self.format_duration(duration)
            d["task_title"] = task.title if task else "—"
            result.append(d)
        return result

    def get_recent_notes(self, limit: int = 10) -> list[dict]:
        notes = self.note_service.get_notes()
        notes.sort(key=lambda n: n.created_at, reverse=True)
        return [n.to_dict() for n in notes[:limit]]
