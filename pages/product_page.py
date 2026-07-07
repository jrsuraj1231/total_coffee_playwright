"""Page Object for the product detail page (PDP)."""
from playwright.sync_api import Page

from locators.product_locator import ProductLocators
from pages.base_page import BasePage
from utilities.common_utils import extract_price_to_float


class ProductPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.locator(ProductLocators.TITLE)
        self.price = page.locator(ProductLocators.PRICE).first
        self.quantity_input = page.locator(ProductLocators.QUANTITY_INPUT)
        self.add_to_cart_button = page.locator(ProductLocators.ADD_TO_CART_BUTTON)
        self.breadcrumb = page.locator(ProductLocators.BREADCRUMB)
        self.stock_status = page.locator(ProductLocators.STOCK_STATUS)
        self.added_to_cart_message = page.locator(ProductLocators.ADDED_TO_CART_MESSAGE)

    def open(self, product_path: str) -> "ProductPage":
        self.goto(product_path)
        return self

    def get_title(self) -> str:
        return self.get_text(self.title)

    def get_price_value(self) -> float:
        return extract_price_to_float(self.get_text(self.price))

    def set_quantity(self, quantity: int) -> None:
        self.quantity_input.first.fill(str(quantity))

    def is_add_to_cart_visible(self) -> bool:
        return self.is_visible(self.add_to_cart_button)

    def add_to_cart(self) -> None:
        """Clicks Add to basket and waits for the AJAX round-trip to finish.

        The Savoy theme's add-to-cart button gives no visible on-page
        feedback (no message, no badge update) until the follow-up
        `?product_added_to_cart=<id>` request that populates the mini-cart
        drawer completes - navigating away before that request finishes
        aborts it and the item never actually lands in the session cart.
        """
        with self.page.expect_response(lambda r: "product_added_to_cart=" in r.url, timeout=15000):
            self.click(self.add_to_cart_button)

    def get_breadcrumb_text(self) -> str:
        return self.get_text(self.breadcrumb)

    def is_out_of_stock(self) -> bool:
        text = self.get_text(self.stock_status) if self.is_visible(self.stock_status) else ""
        return "out of stock" in text.lower()
