from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from web.templating import templates

from services.task_service import TaskService
from services.tracker_service import TrackerService
from services.note_service import NoteService

router = APIRouter()

task_service = TaskService()
tracker_service = TrackerService()
note_service = NoteService()


@router.get("/tasks")
def get_tasks(request: Request):
    tasks = task_service.get_tasks()
    return templates.TemplateResponse(request, "tasks.html", {"tasks": tasks})


@router.post("/tasks/add")
def add_task(
    title: str = Form(...),
    priority: str = Form(...),
    project: str = Form(default=""),
    note: str = Form(default=""),
):
    task = task_service.add_task(title, priority)

    if project.strip():
        tracker_service.start_session(project.strip(), task.id)

    if note.strip():
        note_service.add_note(note.strip())

    return RedirectResponse(url="/tasks", status_code=303)


@router.post("/tasks/complete/{task_id}")
def complete_task(task_id: str):
    task_service.complete_task(task_id)

    # Stop any active tracking session for this task
    active = tracker_service.get_active_session()
    if active and active.task_id == task_id:
        tracker_service.stop_session(active.id)

    return RedirectResponse(url="/tasks", status_code=303)


@router.post("/tasks/delete/{task_id}")
def delete_task(task_id: str):
    task_service.delete_task(task_id)
    return RedirectResponse(url="/tasks", status_code=303)
