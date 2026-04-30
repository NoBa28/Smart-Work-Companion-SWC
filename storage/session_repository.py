from domain.session import Session
from storage.json_storage import JsonStorage


class SessionRepository:
    def __init__(self, file_path="data/sessions.json"):
        self.storage = JsonStorage(file_path)

    def get_all(self) -> list[Session]:
        raw = self.storage.load()
        return [Session.from_dict(s) for s in raw]

    def save_all(self, sessions: list[Session]) -> None:
        data = [s.to_dict() for s in sessions]
        self.storage.save(data)

    def add(self, session: Session) -> None:
        sessions = self.get_all()
        sessions.append(session)
        self.save_all(sessions)

    def update(self, session: Session) -> None:
        sessions = self.get_all()

        for i, s in enumerate(sessions):
            if s.id == session.id:
                sessions[i] = session
                self.save_all(sessions)
                return

        raise ValueError(f"Session with id {session.id} not found")

    def delete(self, session_id: str) -> bool:
        sessions = self.get_all()
        original_len = len(sessions)

        sessions = [s for s in sessions if s.id != session_id]

        if len(sessions) < original_len:
            self.save_all(sessions)
            return True
        return False

    def find_by_id(self, session_id: str) -> Session | None:
        return next((s for s in self.get_all() if s.id == session_id), None)
