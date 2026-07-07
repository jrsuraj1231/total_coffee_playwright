"""Screenshot capture helper, used on test failure by conftest.py."""
import re
from datetime import datetime
from pathlib import Path

from playwright.sync_api import Page

from utilities.logger import get_logger

logger = get_logger(__name__)

SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "screenshots" / "failures"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def _safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", name)


def capture_failure_screenshot(page: Page, test_name: str) -> str:
    """Take a full-page screenshot and return the saved file path.

    Never raises: a screenshot failure shouldn't hide the real test failure.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{_safe_name(test_name)}_{timestamp}.png"
    path = SCREENSHOT_DIR / filename
    try:
        page.screenshot(path=str(path), full_page=True)
        logger.info("Saved failure screenshot to %s", path)
    except Exception as exc:  # pragma: no cover - best effort
        logger.warning("Could not capture screenshot for %s: %s", test_name, exc)
        return ""
    return str(path)
