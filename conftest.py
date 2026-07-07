"""Root pytest configuration: CLI options, fixture wiring, failure screenshots."""
import os

import pytest

pytest_plugins = [
    "fixtures.browser_fixture",
    "fixtures.api_fixture",
]


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default=None, help="Target environment: dev|qa|stage|prod")
    parser.addoption("--browser-name", action="store", default=None, help="chromium|firefox|webkit")
    parser.addoption("--headed-mode", action="store_true", default=False, help="Run browser headed")


def pytest_configure(config):
    env = config.getoption("--env")
    if env:
        os.environ["ENV"] = env

    browser_name = config.getoption("--browser-name")
    if browser_name:
        os.environ["BROWSER"] = browser_name

    if config.getoption("--headed-mode"):
        os.environ["HEADLESS"] = "false"

    for marker in (
        "smoke", "regression", "api", "cart", "search", "product", "account", "checkout",
    ):
        config.addinivalue_line("markers", f"{marker}: see pytest.ini")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            from utilities.screenshot import capture_failure_screenshot

            capture_failure_screenshot(page, item.nodeid)
