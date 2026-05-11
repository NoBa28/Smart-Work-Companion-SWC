# Smart Work Companion

Minimal task management, time tracking, and note capture tool.

## Prerequisites

- Python 3.12 or newer
- Git (to clone the repo)

## Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd smart_work_companion
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install fastapi uvicorn jinja2
   ```

## Running the Project

- **Web app** (recommended):
  ```bash
  uvicorn app:app --reload
  ```
  Open http://127.0.0.1:8000 in your browser.

- **Tests**:
  ```bash
  pytest
  ```

- **CLI**:
  ```bash
  python main.py
  ```

Data (tasks, notes, sessions) is stored in the `data/` directory as JSON files and is created automatically on first run.