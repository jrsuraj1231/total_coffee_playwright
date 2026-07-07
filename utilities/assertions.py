"""Assertion helpers that log before asserting, so failures are traceable in automation.log."""
from playwright.sync_api import Locator, expect

from utilities.logger import get_logger

logger = get_logger(__name__)


class SoftAssert:
    """Collects failures and raises once at the end, useful for multi-field checks."""

    def __init__(self):
        self._failures: list[str] = []

    def check(self, condition: bool, message: str) -> None:
        if not condition:
            logger.error("Soft assertion failed: %s", message)
            self._failures.append(message)
        else:
            logger.info("Soft assertion passed: %s", message)

    def assert_all(self) -> None:
        if self._failures:
            details = "\n".join(f"- {f}" for f in self._failures)
            raise AssertionError(f"{len(self._failures)} soft assertion(s) failed:\n{details}")


def assert_visible(locator: Locator, message: str = "") -> None:
    logger.info("Asserting visible: %s", message or locator)
    expect(locator).to_be_visible()


def assert_hidden(locator: Locator, message: str = "") -> None:
    logger.info("Asserting hidden: %s", message or locator)
    expect(locator).to_be_hidden()


def assert_text_contains(locator: Locator, text: str) -> None:
    logger.info("Asserting locator contains text '%s'", text)
    expect(locator).to_contain_text(text)


def assert_count(locator: Locator, count: int) -> None:
    logger.info("Asserting locator count == %d", count)
    expect(locator).to_have_count(count)


def assert_url_contains(page, fragment: str) -> None:
    logger.info("Asserting URL contains '%s' (current: %s)", fragment, page.url)
    expect(page).to_have_url(f"**/*{fragment}*")
