from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from web.routes.task_routes import router as task_router
from web.routes.note_routes import router as note_router
from web.routes.tracker_routes import router as tracker_router
from web.routes.report_routes import router as report_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="web/static"), name="static")

app.include_router(task_router)
app.include_router(note_router)
app.include_router(tracker_router)
app.include_router(report_router)


@app.get("/")
def root():
    return RedirectResponse(url="/tasks")
