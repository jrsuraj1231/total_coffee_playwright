"""Pytest fixtures providing a config-driven Playwright browser/context/page.

These are imported into the root conftest.py via pytest_plugins so every
test file gets `page` for free without its own import.
"""
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from resources.test_config import CONFIG


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance) -> Browser:
    browser_type = getattr(playwright_instance, CONFIG.browser)
    browser = browser_type.launch(headless=CONFIG.headless, slow_mo=CONFIG.get("slow_mo", 0))
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser) -> BrowserContext:
    context = browser.new_context(
        base_url=CONFIG.base_url,
        viewport=CONFIG.viewport,
    )
    context.set_default_timeout(CONFIG.default_timeout)
    context.set_default_navigation_timeout(CONFIG.navigation_timeout)
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page
    page.close()
