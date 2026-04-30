from services.task_service import TaskService
from services.tracker_service import TrackerService
from services.note_service import NoteService


def test_task_service() -> None:
    service = TaskService()

    task = service.add_task("Test Task", "high")
    print("Created: ", task)

    tasks = service.get_tasks()
    print("All Tasks: ", tasks)


def test_tracker_service() -> None:

    service = TrackerService()

    session = service.start_session("Project A", "Task 1")
    print("Started Session: ", session)

    active = service.get_active_session()
    print("Active Session: ", active)

    stopped = service.stop_session(session.id)
    print("Stopped Session: ", stopped)

    all_sessions = service.get_sessions()
    print("All Sessions: ", all_sessions)

def test_note_service() -> None:
    service = NoteService()

    note = service.add_note("This is a test note")
    print("Created Note: ", note)

    notes = service.get_notes()
    print("All Notes: ", notes)


def main():
    # test_task_service()
    # test_tracker_service()
    test_note_service()


if __name__ == "__main__":
    main()
