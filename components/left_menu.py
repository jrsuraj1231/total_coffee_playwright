"""Mobile side/left navigation menu (Savoy theme 'mobile-menu-layout-side')."""
from playwright.sync_api import Page


class LeftMenu:
    def __init__(self, page: Page):
        self.page = page
        self.toggle_button = page.locator(".nm-mobile-menu-toggle, .mobile-menu-icon-bold button").first
        self.panel = page.locator("#nm-mobile-menu, .mobile-menu-panel").first

    def open(self) -> None:
        self.toggle_button.click()
        self.panel.wait_for(state="visible")

    def close(self) -> None:
        self.page.keyboard.press("Escape")

    def select_link(self, link_text: str) -> None:
        self.panel.get_by_role("link", name=link_text).first.click()
