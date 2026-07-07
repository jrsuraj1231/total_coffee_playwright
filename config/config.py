"""Environment-aware configuration loader.

Usage:
    from config.config import CONFIG
    CONFIG.base_url

Environment is selected via the ``ENV`` environment variable
(dev|qa|stage|prod), defaulting to ``qa``. Individual values can be
overridden without touching the YAML files via environment variables:
``BASE_URL``, ``HEADLESS``, ``BROWSER``.

Note: total.coffee is a single public production store, so all four
environment YAML files currently point at the same base_url. The
per-environment structure is kept so the framework demonstrates the
standard pattern and can be pointed at real dev/qa/stage hosts by
editing the relevant config_<env>.yaml file.
"""
import os
from pathlib import Path
from typing import Any, Dict

import yaml

CONFIG_DIR = Path(__file__).resolve().parent
VALID_ENVS = ("dev", "qa", "stage", "prod")


def _load_env_file(env: str) -> Dict[str, Any]:
    config_path = CONFIG_DIR / f"config_{env}.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"No config file found for environment '{env}' at {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _apply_env_overrides(data: Dict[str, Any]) -> Dict[str, Any]:
    overrides = {
        "base_url": os.getenv("BASE_URL"),
        "api_base_url": os.getenv("API_BASE_URL"),
        "browser": os.getenv("BROWSER"),
    }
    for key, value in overrides.items():
        if value:
            data[key] = value

    if os.getenv("HEADLESS") is not None:
        data["headless"] = os.getenv("HEADLESS").strip().lower() in ("1", "true", "yes")

    if os.getenv("TEST_USERNAME"):
        data.setdefault("test_account", {})["username"] = os.getenv("TEST_USERNAME")
    if os.getenv("TEST_PASSWORD"):
        data.setdefault("test_account", {})["password"] = os.getenv("TEST_PASSWORD")

    return data


class Config:
    """Thin attribute-style wrapper around the active environment's YAML config."""

    def __init__(self, env: str | None = None):
        self.env = (env or os.getenv("ENV", "qa")).strip().lower()
        if self.env not in VALID_ENVS:
            raise ValueError(f"Unknown ENV '{self.env}'. Expected one of {VALID_ENVS}")

        data = _load_env_file(self.env)
        data = _apply_env_overrides(data)
        self._data = data

    def __getattr__(self, item: str) -> Any:
        try:
            return self._data[item]
        except KeyError as exc:
            raise AttributeError(f"Config has no attribute '{item}'") from exc

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._data)

    def __repr__(self) -> str:
        return f"Config(env={self.env!r}, base_url={self._data.get('base_url')!r})"


CONFIG = Config()
