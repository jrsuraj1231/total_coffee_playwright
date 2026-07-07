"""Explicit-wait helpers layered on top of Playwright's own auto-waiting.

Playwright locators already auto-wait for actionability, so most tests
should not need these. They exist for the handful of cases where we
need to wait on a condition that isn't a simple locator action (AJAX
mini-cart panel closing, a URL change, a network-driven attribute).
"""
from playwright.sync_api import Locator, Page

DEFAULT_TIMEOUT_MS = 15000


def wait_for_visible(locator: Locator, timeout: int = DEFAULT_TIMEOUT_MS) -> Locator:
    locator.first.wait_for(state="visible", timeout=timeout)
    return locator


def wait_for_hidden(locator: Locator, timeout: int = DEFAULT_TIMEOUT_MS) -> Locator:
    locator.first.wait_for(state="hidden", timeout=timeout)
    return locator


def wait_for_url_contains(page: Page, fragment: str, timeout: int = DEFAULT_TIMEOUT_MS) -> None:
    page.wait_for_url(f"**/*{fragment}*", timeout=timeout)


def wait_for_text_in_locator(locator: Locator, text: str, timeout: int = DEFAULT_TIMEOUT_MS) -> None:
    locator.filter(has_text=text).first.wait_for(state="visible", timeout=timeout)
