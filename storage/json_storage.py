import json
from pathlib import Path

class JsonStorage:

    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        if not self.file_path.exists():
            return []
        return json.loads(self.file_path.read_text())
    
    def save(self, data):
        self.file_path.write_text(json.dumps(data, indent=2))