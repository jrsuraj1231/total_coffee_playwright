"""CSV test-data reader."""
import csv
from pathlib import Path
from typing import Any


def read_csv(relative_path: str) -> list[dict[str, Any]]:
    """relative_path is relative to the testdata/csv directory, e.g. 'users.csv'."""
    base = Path(__file__).resolve().parent.parent / "testdata" / "csv"
    path = base / relative_path
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))
