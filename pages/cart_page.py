"""Page Object for the mini-cart ('Basket') drawer and the classic /cart/ page."""
from playwright.sync_api import Page

from pages.base_page import BasePage
from utilities.common_utils import extract_price_to_float


class CartPage(BasePage):
    PATH = "/cart/"

    FORM = "form.woocommerce-cart-form"
    EMPTY_CART_MESSAGE = ".wc-empty-cart-message"
    CART_ITEM_ROW = "tr.woocommerce-cart-form__cart-item"
    ITEM_QUANTITY_INPUT = "input.qty"
    ITEM_REMOVE_LINK = "a.remove_from_cart_button"
    ITEM_SUBTOTAL = ".product-subtotal .woocommerce-Price-amount"
    UPDATE_CART_BUTTON = "button[name='update_cart']"
    CONTINUE_SHOPPING_BUTTON = "#nm-cart-continue-button"
    CART_SUBTOTAL_ROW = "tr.cart-subtotal .woocommerce-Price-amount"
    ORDER_TOTAL_ROW = "tr.order-total .woocommerce-Price-amount"
    PROCEED_TO_CHECKOUT_BUTTON = "a.checkout-button"

    # Savoy theme's AJAX side-drawer, titled "Basket", opened on add-to-cart.
    MINI_CART_PANEL = ".cart-panel, #nm-cart-panel"

    def __init__(self, page: Page):
        super().__init__(page)
        self.form = page.locator(self.FORM)
        self.empty_cart_message = page.locator(self.EMPTY_CART_MESSAGE)
        self.item_rows = page.locator(self.CART_ITEM_ROW)
        self.update_cart_button = page.locator(self.UPDATE_CART_BUTTON)
        self.continue_shopping_button = page.locator(self.CONTINUE_SHOPPING_BUTTON)
        self.proceed_to_checkout_button = page.locator(self.PROCEED_TO_CHECKOUT_BUTTON)
        self.mini_cart_panel = page.locator(self.MINI_CART_PANEL)

    def open(self) -> "CartPage":
        self.goto(self.PATH)
        return self

    def is_empty(self) -> bool:
        return self.is_visible(self.empty_cart_message) or not self.is_visible(self.form)

    def has_items(self) -> bool:
        return self.item_rows.count() > 0

    def item_count(self) -> int:
        return self.item_rows.count()

    def _row_for(self, product_name: str):
        return self.item_rows.filter(has_text=product_name)

    def get_item_quantity(self, product_name: str) -> int:
        row = self._row_for(product_name)
        return int(row.locator(self.ITEM_QUANTITY_INPUT).input_value())

    def set_item_quantity(self, product_name: str, quantity: int) -> None:
        row = self._row_for(product_name)
        qty_input = row.locator(self.ITEM_QUANTITY_INPUT)
        qty_input.fill(str(quantity))
        self.update_cart_button.click()
        # WooCommerce updates the cart via AJAX (no full navigation) and
        # signals progress with a jquery.blockUI overlay on the form.
        overlay = self.page.locator(".blockUI.blockOverlay")
        try:
            overlay.first.wait_for(state="visible", timeout=3000)
        except Exception:
            pass
        overlay.first.wait_for(state="hidden", timeout=15000)

    def get_item_subtotal(self, product_name: str) -> float:
        row = self._row_for(product_name)
        return extract_price_to_float(row.locator(self.ITEM_SUBTOTAL).first.inner_text())

    def _wait_for_row_count_below(self, count_before: int, timeout_ms: int = 15000) -> None:
        """WooCommerce's remove link sometimes triggers a real page
        navigation instead of an AJAX-intercepted removal (observed live -
        not consistently one or the other). Waiting for a specific row
        locator to hide breaks if a navigation swaps in a whole new table,
        since "the same" positional locator then matches a different,
        still-present row. Polling the row count is agnostic to which
        mechanism actually fired."""
        deadline = self.page.evaluate("Date.now()") + timeout_ms
        while self.page.evaluate("Date.now()") < deadline:
            if self.item_rows.count() < count_before:
                return
            self.page.wait_for_timeout(300)
        raise TimeoutError(f"Cart row count never dropped below {count_before} within {timeout_ms}ms")

    def remove_item(self, product_name: str) -> None:
        count_before = self.item_count()
        row = self._row_for(product_name)
        row.locator(self.ITEM_REMOVE_LINK).click()
        self._wait_for_row_count_below(count_before)

    def empty_cart(self) -> None:
        """Removes every line item one at a time, tolerant of either the
        AJAX-only removal path or a full page navigation (see
        _wait_for_row_count_below)."""
        self.open()
        while self.has_items():
            count_before = self.item_count()
            self.item_rows.first.locator(self.ITEM_REMOVE_LINK).click()
            self._wait_for_row_count_below(count_before)

    def get_cart_subtotal(self) -> float:
        return extract_price_to_float(self.page.locator(self.CART_SUBTOTAL_ROW).first.inner_text())

    def get_order_total(self) -> float:
        return extract_price_to_float(self.page.locator(self.ORDER_TOTAL_ROW).first.inner_text())

    def proceed_to_checkout(self) -> None:
        self.proceed_to_checkout_button.click()

    def wait_for_mini_cart_panel(self) -> None:
        self.mini_cart_panel.first.wait_for(state="visible", timeout=15000)
