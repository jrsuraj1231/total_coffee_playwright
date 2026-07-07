"""Page Object for /checkout/ - classic WooCommerce shortcode checkout.

Safety note: this framework deliberately never completes and submits the
#place_order button against total.coffee, since that would create a real
order/charge on a live production store. Checkout tests only verify
page/field state and client-side validation errors triggered by
submitting with required fields left blank.
"""
from playwright.sync_api import Page

from locators.checkout_locator import CheckoutLocators
from pages.base_page import BasePage
from resources.constants import PATH_CHECKOUT


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.form = page.locator(CheckoutLocators.FORM)
        self.empty_cart_notice = page.locator(CheckoutLocators.EMPTY_CART_NOTICE)
        self.order_review = page.locator(CheckoutLocators.ORDER_REVIEW)
        self.place_order_button = page.locator(CheckoutLocators.PLACE_ORDER_BUTTON)
        self.validation_notice = page.locator(CheckoutLocators.VALIDATION_ERROR_NOTICE)
        self.invalid_fields = page.locator(CheckoutLocators.INVALID_FIELD)

        self.first_name_input = page.locator(CheckoutLocators.BILLING_FIRST_NAME)
        self.last_name_input = page.locator(CheckoutLocators.BILLING_LAST_NAME)
        self.email_input = page.locator(CheckoutLocators.BILLING_EMAIL)
        self.phone_input = page.locator(CheckoutLocators.BILLING_PHONE)

    def open(self) -> "CheckoutPage":
        self.goto(PATH_CHECKOUT)
        return self

    def is_empty_cart_notice_visible(self) -> bool:
        return self.is_visible(self.empty_cart_notice) or not self.is_visible(self.form)

    def is_order_review_visible(self) -> bool:
        return self.is_visible(self.order_review)

    def fill_email(self, email: str) -> None:
        self.email_input.fill(email)

    def fill_first_name(self, first_name: str) -> None:
        self.first_name_input.fill(first_name)

    def fill_last_name(self, last_name: str) -> None:
        self.last_name_input.fill(last_name)

    def attempt_place_order_without_completing(self) -> None:
        """Clicks Place Order to trigger client-side validation only.

        Intended to be called with required fields intentionally left
        blank/invalid so the request never actually reaches the server as
        a valid, payable order. Waits for the order-review block to
        finish its AJAX render first, since checkout.js must be bound
        before clicking will trigger inline validation instead of a bare
        form submit.
        """
        self.order_review.wait_for(state="visible", timeout=15000)
        self.page.wait_for_timeout(1500)
        self.place_order_button.click()

    def has_validation_errors(self) -> bool:
        for _ in range(10):
            if self.is_visible(self.validation_notice, timeout=1000) or self.invalid_fields.count() > 0:
                return True
            self.page.wait_for_timeout(500)
        return False
