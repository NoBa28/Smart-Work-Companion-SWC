from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from web.templating import templates

from services.report_service import ReportService
from services.task_service import TaskService
from services.tracker_service import TrackerService
from services.note_service import NoteService

router = APIRouter()

report_service = ReportService(TaskService(), TrackerService(), NoteService())


@router.get("/reports")
def get_reports(request: Request):
    total_time = report_service.get_total_tracked_time()
    open_tasks = report_service.get_open_tasks_count()
    active = report_service.get_active_session_report()
    time_by_project = report_service.get_time_by_project()
    time_by_task = report_service.get_time_by_task()
    recent_sessions = report_service.get_recent_sessions(12)
    recent_notes = report_service.get_recent_notes(10)

    total_sessions = len([s for s in report_service.tracker_service.get_sessions() if s.end_time])
    total_notes = len(report_service.note_service.get_notes())

    # Calculate bar widths for visual charts
    max_project_time = max((p["seconds"] for p in time_by_project.values()), default=0) or 1
    for p in time_by_project.values():
        p["width"] = round((p["seconds"] / max_project_time) * 100, 1)

    max_task_time = time_by_task[0]["seconds"] if time_by_task else 1
    for item in time_by_task:
        item["width"] = round((item["seconds"] / max_task_time) * 100, 1)

    return templates.TemplateResponse(
        request,
        "reports.html",
        {
            "total_time": total_time,
            "open_tasks": open_tasks,
            "active": active,
            "time_by_project": time_by_project,
            "time_by_task": time_by_task,
            "recent_sessions": recent_sessions,
            "recent_notes": recent_notes,
            "total_sessions": total_sessions,
            "total_notes": total_notes,
        },
    )


@router.post("/data/clear")
def clear_all_data():
    import os
    for fname in ["tasks.json", "notes.json", "sessions.json"]:
        path = os.path.join("data", fname)
        if os.path.exists(path):
            with open(path, "w") as f:
                f.write("[]")
    return RedirectResponse(url="/reports", status_code=303)
