# AGENTS.md

Simple Python project using service/repository pattern over JSON storage.

## Running
- Web app: `uvicorn app:app --reload`
- Tests: `pytest`
- Manual service tests: `python main.py`

## Structure
- `app.py`: FastAPI entrypoint
- `services/`: business logic
- `storage/`: JSON repositories
- `domain/`: models
- `web/`: routes, templates, static
- `tests/`: pytest tests (use fixtures for repos)
