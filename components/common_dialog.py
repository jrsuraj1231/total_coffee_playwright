"""Generic modal dialog wrapper (used by the mini-cart 'Basket' drawer,
quick-view lightboxes, and any WooCommerce Blocks modal)."""
from playwright.sync_api import Page


class CommonDialog:
    def __init__(self, page: Page, container_selector: str):
        self.page = page
        self.container = page.locator(container_selector)

    def is_open(self) -> bool:
        return self.container.is_visible()

    def wait_until_open(self, timeout: int = 15000) -> None:
        self.container.wait_for(state="visible", timeout=timeout)

    def wait_until_closed(self, timeout: int = 15000) -> None:
        self.container.wait_for(state="hidden", timeout=timeout)

    def close(self, close_selector: str = "button[aria-label='Close']") -> None:
        self.container.locator(close_selector).first.click()
