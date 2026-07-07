"""JSON test-data reader."""
import json
from pathlib import Path
from typing import Any


def read_json(relative_path: str) -> Any:
    """relative_path is relative to the testdata/json directory, e.g. 'login.json'."""
    base = Path(__file__).resolve().parent.parent / "testdata" / "json"
    path = base / relative_path
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
