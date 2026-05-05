from datetime import datetime
import uuid

from domain.session import Session
from storage.session_repository import SessionRepository


class TrackerService:

    def __init__(self, repo=None):
        self.repo = repo or SessionRepository()

    def start_session(self, project: str, task_id: str) -> Session:
        if self.get_active_session():
            raise ValueError("A session is already active")

        session = Session(
            id=str(uuid.uuid4()),
            task_id=task_id,
            project=project,
            start_time=datetime.now(),
            end_time=None,
        )

        self.repo.add(session)
        return session

    def stop_session(self, session_id: str) -> Session:
        session = self.repo.find_by_id(session_id)
        if not session:
            raise ValueError(f"Session with id {session_id} not found")

        if session.end_time is not None:
            raise ValueError("Session is already stopped")

        session.end_time = datetime.now()
        self.repo.update(session)

        return session

    def get_active_session(self) -> Session | None:
        sessions = self.repo.get_all()

        for session in sessions:
            if session.end_time is None:
                return session
        return None

    def get_sessions(self) -> list[Session]:
        return self.repo.get_all()
