"""Regression tests for product detail pages and account/order-adjacent flows
(registration validation, lost password, my-account dashboard).

Named test_orders.py per the framework layout; total.coffee has no public
order-history API/UI we can drive without a real customer account, so the
order-related coverage here is the parts of the order journey that are
safe and reachable: product correctness feeding into an order, and the
account dashboard where order history would appear once real credentials
are supplied.
"""
import pytest

from config.config import CONFIG
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage, LostPasswordPage
from pages.product_page import ProductPage
from utilities.excel_reader import read_excel
from utilities.json_reader import read_json

PRODUCTS = read_excel("products.xlsx")
INVALID_EMAILS = read_json("users.json")["invalid_registration_emails"]


@pytest.mark.regression
@pytest.mark.product
@pytest.mark.parametrize("row", PRODUCTS, ids=[r["product_slug"] for r in PRODUCTS])
def test_product_page_displays_correct_details(page, row):
    product_page = ProductPage(page).open(row["product_path"])

    assert row["expected_title_contains"].lower() in product_page.get_title().lower()
    assert product_page.is_add_to_cart_visible() == bool(row["expected_in_stock"])
    if row["expected_in_stock"]:
        assert product_page.get_price_value() > 0


@pytest.mark.regression
@pytest.mark.product
def test_out_of_stock_product_hides_add_to_cart_button(page):
    product_page = ProductPage(page).open("/shop/clever-dripper-filter-papers/")

    assert product_page.is_out_of_stock()
    assert not product_page.is_add_to_cart_visible()


@pytest.mark.regression
@pytest.mark.product
def test_breadcrumb_navigation_on_product_page(page):
    product_page = ProductPage(page).open("/shop/aeropress-flow-control-filter-cap/")

    breadcrumb_text = product_page.get_breadcrumb_text()
    assert "Home" in breadcrumb_text
    assert "AeroPress" in breadcrumb_text or "Equipment" in breadcrumb_text


@pytest.mark.regression
@pytest.mark.account
@pytest.mark.skipif(
    not CONFIG.get("test_account", {}).get("username"),
    reason="No real test account configured - skipping the dashboard test that needs a valid login.",
)
def test_my_account_dashboard_navigation_tabs(page):
    login_page = LoginPage(page).open()
    account = CONFIG.test_account
    login_page.login(account["username"], account["password"])
    assert login_page.is_logged_in()

    dashboard_page = DashboardPage(page).open()

    assert dashboard_page.is_nav_visible()
    dashboard_page.go_to_orders()
    assert "orders" in page.url


@pytest.mark.regression
@pytest.mark.account
@pytest.mark.parametrize("case", INVALID_EMAILS, ids=[c["email"] for c in INVALID_EMAILS])
def test_register_form_rejects_invalid_email_formats(page, case):
    """Confirms the browser blocks obviously malformed emails before the
    register form could ever be submitted - no registration is submitted."""
    login_page = LoginPage(page).open()

    login_page.register_email_input.fill(case["email"])
    is_valid = login_page.register_email_input.evaluate("el => el.checkValidity()")

    assert not is_valid, f"Expected '{case['email']}' to fail HTML5 email validation ({case['reason']})"


@pytest.mark.regression
@pytest.mark.account
def test_lost_password_flow_validates_and_rejects_unregistered_email(page):
    lost_password_page = LostPasswordPage(page).open()

    assert lost_password_page.is_visible(lost_password_page.user_login_input)
    assert lost_password_page.user_login_input.evaluate("el => el.required")

    lost_password_page.request_reset("nonexistent_user_9999@example.com")

    assert "invalid username or email" in lost_password_page.notice_text().lower()
