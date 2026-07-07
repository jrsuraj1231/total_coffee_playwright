"""YAML test-data reader."""
from pathlib import Path
from typing import Any

import yaml


def read_yaml(relative_path: str) -> Any:
    """relative_path is relative to the testdata/yaml directory, e.g. 'config.yaml'."""
    base = Path(__file__).resolve().parent.parent / "testdata" / "yaml"
    path = base / relative_path
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
