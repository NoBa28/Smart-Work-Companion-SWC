from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from web.templating import templates

from services.note_service import NoteService

router = APIRouter()

note_service = NoteService()


@router.get("/notes")
def get_notes(request: Request):
    notes = note_service.get_notes()
    return templates.TemplateResponse(request, "notes.html", {"notes": notes})


@router.post("/notes/delete/{note_id}")
def delete_note(note_id: str):
    note_service.delete_note(note_id)
    return RedirectResponse(url="/notes", status_code=303)
