"""Regression tests for the /cart/ page (classic WooCommerce cart)."""
import pytest

from pages.cart_page import CartPage
from pages.product_page import ProductPage
from utilities.csv_reader import read_csv

CART_PRODUCTS = read_csv("users.csv")  # product_slug,product_path,initial_qty,updated_qty


@pytest.fixture(autouse=True)
def empty_cart_before_and_after(page):
    CartPage(page).empty_cart()
    yield
    CartPage(page).empty_cart()


@pytest.mark.regression
@pytest.mark.cart
def test_add_single_product_to_cart(page):
    product_page = ProductPage(page).open("/shop/aeropress-flow-control-filter-cap/")
    product_name = product_page.get_title()

    product_page.add_to_cart()

    cart_page = CartPage(page).open()
    assert cart_page.has_items()
    assert cart_page.get_item_quantity(product_name) == 1


@pytest.mark.regression
@pytest.mark.cart
def test_add_multiple_products_and_verify_cart_count(page):
    for row in CART_PRODUCTS:
        ProductPage(page).open(row["product_path"]).add_to_cart()

    cart_page = CartPage(page).open()
    assert cart_page.item_count() == len(CART_PRODUCTS)


@pytest.mark.regression
@pytest.mark.cart
@pytest.mark.parametrize("row", CART_PRODUCTS, ids=[r["product_slug"] for r in CART_PRODUCTS])
def test_update_quantity_in_cart(page, row):
    product_page = ProductPage(page).open(row["product_path"])
    product_name = product_page.get_title()
    product_page.add_to_cart()

    cart_page = CartPage(page).open()
    updated_qty = int(row["updated_qty"])
    cart_page.set_item_quantity(product_name, updated_qty)

    assert cart_page.get_item_quantity(product_name) == updated_qty


@pytest.mark.regression
@pytest.mark.cart
def test_remove_item_from_cart(page):
    product_page = ProductPage(page).open("/shop/cafflano-kompact/")
    product_name = product_page.get_title()
    product_page.add_to_cart()

    cart_page = CartPage(page).open()
    assert cart_page.has_items()

    cart_page.remove_item(product_name)

    assert cart_page.is_empty()


@pytest.mark.regression
@pytest.mark.cart
def test_empty_cart_displays_correct_message(page):
    cart_page = CartPage(page).open()

    assert cart_page.is_empty()
    assert cart_page.is_visible(cart_page.empty_cart_message)
