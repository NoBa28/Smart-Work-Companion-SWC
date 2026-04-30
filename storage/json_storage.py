import json
from pathlib import Path


class JsonStorage:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.parent.exists() or not self.file_path.read_text().strip():
            self.file_path.write_text("[]")

    def load(self) -> list[dict]:
        try:
            content = self.file_path.read_text()
            return json.loads(content) if content else []
        except FileNotFoundError:
            return []

    def save(self, data) -> None:
        self.file_path.write_text(json.dumps(data, indent=2))
