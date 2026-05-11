from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from web.templating import templates

from services.tracker_service import TrackerService
from services.task_service import TaskService
from services.note_service import NoteService

router = APIRouter()

tracker_service = TrackerService()
task_service = TaskService()
note_service = NoteService()


@router.get("/tracker")
def get_tracker(request: Request):
    active = tracker_service.get_active_session()
    recent = tracker_service.get_sessions()
    completed = [s for s in recent if s.end_time is not None]
    completed.sort(key=lambda s: s.end_time, reverse=True)
    return templates.TemplateResponse(
        request,
        "tracker.html",
        {"active": active, "recent_sessions": completed[:8]},
    )


@router.post("/tracker/start")
def start_session(project: str = Form(...), task_id: str = Form(...)):
    tracker_service.start_session(project, task_id)
    return RedirectResponse(url="/tracker", status_code=303)


@router.post("/tracker/start-new")
def start_new_work(
    title: str = Form(...),
    priority: str = Form(...),
    project: str = Form(...),
    note: str = Form(default=""),
):
    # 1. Create the task
    task = task_service.add_task(title, priority)

    # 2. Start time tracking on it
    tracker_service.start_session(project, task.id)

    # 3. Optionally add a first note
    if note.strip():
        note_service.add_note(note.strip())

    return RedirectResponse(url="/tracker", status_code=303)


@router.post("/tracker/stop")
def stop_session():
    active = tracker_service.get_active_session()
    if active:
        tracker_service.stop_session(active.id)
    return RedirectResponse(url="/tracker", status_code=303)


@router.post("/tracker/note")
def add_session_note(text: str = Form(...)):
    active = tracker_service.get_active_session()
    if active and text.strip():
        note_service.add_note(text.strip())
    return RedirectResponse(url="/tracker", status_code=303)
