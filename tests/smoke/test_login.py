"""Smoke tests for /my-account/ login.

Covers: page reachability, invalid-credential rejection, and data-driven
field-validation (empty username/password) sourced from testdata/excel/login.xlsx.
"""
import pytest

from config.config import CONFIG
from pages.login_page import LoginPage
from utilities.excel_reader import read_excel

LOGIN_CASES = read_excel("login.xlsx")


@pytest.mark.smoke
@pytest.mark.account
def test_login_page_loads_successfully(page):
    login_page = LoginPage(page).open()

    assert "my-account" in login_page.current_url()
    assert login_page.is_visible(login_page.username_input)
    assert login_page.is_visible(login_page.password_input)


@pytest.mark.smoke
@pytest.mark.account
@pytest.mark.parametrize("case", LOGIN_CASES, ids=[c["test_case"] for c in LOGIN_CASES])
def test_login_field_validation_data_driven(page, case):
    login_page = LoginPage(page).open()

    login_page.login(case["username"] or "", case["password"] or "")

    assert login_page.is_login_error_visible(), f"Expected a login error for case '{case['test_case']}'"
    error_text = login_page.login_error_text()
    assert case["expected_message_contains"].lower() in error_text.lower(), (
        f"Expected error to contain '{case['expected_message_contains']}', got '{error_text}'"
    )
    assert not login_page.is_logged_in()


@pytest.mark.smoke
@pytest.mark.account
@pytest.mark.skipif(
    not CONFIG.get("test_account", {}).get("username"),
    reason="No real test account configured (TEST_USERNAME/TEST_PASSWORD) - "
    "skipping the only test that needs a valid login on the live store.",
)
def test_login_with_valid_credentials_succeeds(page):
    login_page = LoginPage(page).open()
    account = CONFIG.test_account

    login_page.login(account["username"], account["password"])

    assert login_page.is_logged_in()
