"""Smoke tests for /checkout/.

Safety: these tests never click #place_order to completion with valid
data - they only check page state and the client-side validation that
fires when required fields are missing. See pages/checkout_page.py.
"""
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.product_page import ProductPage

IN_STOCK_PRODUCT_PATH = "/shop/aeropress-flow-control-filter-cap/"
IN_STOCK_PRODUCT_NAME = "AEROPRESS FLOW CONTROL FILTER CAP"


def _empty_cart_if_needed(page):
    CartPage(page).empty_cart()


@pytest.mark.smoke
@pytest.mark.checkout
def test_checkout_shows_empty_cart_notice_when_cart_is_empty(page):
    _empty_cart_if_needed(page)

    checkout_page = CheckoutPage(page).open()

    assert checkout_page.is_empty_cart_notice_visible()
    assert not checkout_page.is_order_review_visible()


@pytest.mark.smoke
@pytest.mark.checkout
def test_checkout_shows_order_review_when_cart_has_items(page):
    ProductPage(page).open(IN_STOCK_PRODUCT_PATH).add_to_cart()

    checkout_page = CheckoutPage(page).open()

    assert checkout_page.is_order_review_visible()
    assert not checkout_page.is_empty_cart_notice_visible()


@pytest.mark.smoke
@pytest.mark.checkout
def test_checkout_shows_validation_errors_on_incomplete_submission(page):
    ProductPage(page).open(IN_STOCK_PRODUCT_PATH).add_to_cart()

    checkout_page = CheckoutPage(page).open()
    checkout_page.attempt_place_order_without_completing()

    assert checkout_page.has_validation_errors()
    # Never actually reached an order-confirmation page.
    assert "order-received" not in page.url
