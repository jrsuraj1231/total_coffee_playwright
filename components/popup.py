"""Generic marketing popup/newsletter overlay handling.

total.coffee occasionally shows a subscribe/newsletter overlay on first
visit. Tests should call dismiss_if_present() right after navigation so
it never blocks a subsequent click.
"""
from playwright.sync_api import Page


class Popup:
    CLOSE_SELECTORS = (
        ".mfp-close",
        "[class*='popup'] [class*='close']",
        "button[aria-label='Close']",
    )

    def __init__(self, page: Page):
        self.page = page

    def dismiss_if_present(self, timeout: int = 3000) -> bool:
        for selector in self.CLOSE_SELECTORS:
            locator = self.page.locator(selector).first
            try:
                if locator.is_visible(timeout=timeout):
                    locator.click()
                    return True
            except Exception:
                continue
        return False
